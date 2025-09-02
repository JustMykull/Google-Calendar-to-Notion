import NotionAPI
import EventGetter
import sharedVars
import traceback
import re

from datetime import datetime
import pytz 

# PLEASE WORK PLEASE WORK PLEASE WORK PLEASE NO DUPES

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()

def make_key(event_id, name, deadline):
    """Composite uniqueness key (EventID + Assignment Name + Deadline)."""
    return (normalize(event_id), normalize(name), normalize(deadline))

def to_eastern(utc_str: str) -> str:
    """Convert UTC ISO string with Z to Eastern time ISO string."""
    if not utc_str:
        return ""
    try:
        # Parse UTC string
        dt_utc = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        # Convert to Eastern
        eastern = pytz.timezone("America/New_York")
        dt_eastern = dt_utc.astimezone(eastern)
        return dt_eastern.isoformat()
    except Exception:
        return utc_str  # fallback if parsing fails

def EventsToNotion():
    try:
        #Gets events from Google Calendar
        EventGetter.getEvents()

        # Build a set of existing keys from Notion
        existing_keys = set()
        for assignment in NotionAPI.getAssignments(NotionAPI.dbID):
            event_id = ""
            if assignment["properties"]["EventID"]["rich_text"]:
                event_id = assignment["properties"]["EventID"]["rich_text"][0]["text"]["content"]

            name = ""
            if assignment["properties"]["Assignment Name"]["title"]:
                name = assignment["properties"]["Assignment Name"]["title"][0]["text"]["content"]

            deadline = ""
            if assignment["properties"]["Deadline"]["date"]:
                deadline = assignment["properties"]["Deadline"]["date"]["start"]
                deadline = to_eastern(deadline)

            existing_keys.add(event_id)

        # Loop through events from Google Calendar
        for event in sharedVars.EVENTS[:]:
            event_id = event.get("EventID", "")
            name = event.get("Assignment Name", "")
            course_code = event.get("Course Code", "")
            deadline = event.get("Deadline", "")

            key = "".join(make_key(normalize(event_id), normalize(name), normalize(deadline)))
            print("Key: ")
            print(key)

            if key in existing_keys:
                print(f"Skipping duplicate: {name} ({key}, {deadline}) \n")
                sharedVars.EVENTS.remove(event)
                continue
            
            deadline_eastern = to_eastern(deadline)

            # Create assignment in Notion
            NotionAPI.createAssignment(
                NotionAPI.dbID,
                name,
                course_code,
                deadline_eastern,
                normalize("".join(key))
            )

            print(f"Created new assignment: {name} ({key}, {deadline}) \n")

            # Update keys set so no dupes within same run
            existing_keys.add(key)
            sharedVars.EVENTS.remove(event)

    except Exception as error:
        print("Error caught:", str(error))
        traceback.print_exc()

EventsToNotion()
