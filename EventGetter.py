import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sharedVars

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def getEvents():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        # Clear existing events list
        sharedVars.EVENTS.clear()

        service = build("calendar", "v3", credentials=creds)

        now = dt.datetime.now().isoformat() + "Z"

        event_results = service.events().list(
            calendarId="jsohl8n7avebbk541d3r4811h2eoq6fe@import.calendar.google.com",
            timeMin=now,
            maxResults=250,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = event_results.get("items", [])

        if not events:
            print("No upcoming events")
            return
        
        for event in events:
            assignmentName = event.get("summary", "")
            courseCode = event.get("location", "") or ""
            if courseCode.startswith("-"):
                courseCode = courseCode[1:]

            dueDate = event["start"].get("dateTime", event["start"].get("date", ""))

            eventID = event.get("id", "")

            # Store as dict instead of separate lists
            sharedVars.EVENTS.append({
                "Assignment Name": assignmentName,
                "Course Code": courseCode,
                "Deadline": dueDate,
                "EventID": eventID
            })

        sharedVars.formatEvents()

    except HttpError as error:
        print("Error Occurred: ", error)
