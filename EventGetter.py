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
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
        )
            
        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())
    
    try:
        sharedVars.ASSIGNEMTNAMES.clear()
        sharedVars.COURSECODE.clear()
        sharedVars.DEADLINE.clear()
        sharedVars.EVENTID.clear()

        service = build("calendar", "v3", credentials=creds)

        now = dt.datetime.now().isoformat() + "Z"

        event_results = service.events().list(calendarId="jsohl8n7avebbk541d3r4811h2eoq6fe@import.calendar.google.com", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime").execute()
        events = event_results.get("items", [])

        if not events:
            print("No upcoming events")
            return
        
        for event in events:
            # Get information from each event
            assignmentName = event["summary"]
            courseCode = event["location"]
            dueDate = event["start"].get("dateTime", event["start"].get("date"))
            eventID = event["id"]
            #print(event)

            # Dubugging print statements
            # print(assignmentName)
            # print(courseCode[1:])
            # print(dueDate)
            # print(eventID)

            # print(type(assignmentName))
            # print(type(courseCode[1:]))
            # print(type(dueDate))
            # print(type(eventID))

            # Append to lists
            sharedVars.ASSIGNEMTNAMES.append(assignmentName)
            sharedVars.COURSECODE.append(courseCode[1:])
            sharedVars.DEADLINE.append(dueDate[:-1])
            sharedVars.EVENTID.append(eventID)

        # print(sharedVars.EVENTID)
            
        sharedVars.formatEvents()
        
    except HttpError as error:
        print("Error Occured: ", error)

getEvents()