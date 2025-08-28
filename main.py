import NotionAPI
import EventGetter
import sharedVars

def EventsToNotion():
    try:
        EventGetter.getEvents()
        
        # Collect existing EventIDs from Notion
        sharedVars.ExistingEventID = [
            assignment["properties"]["EventID"]["rich_text"][0]["text"]["content"]
            for assignment in NotionAPI.getAssignments(NotionAPI.dbID)
        ]

        # Loop over a copy of EVENTS
        for event in sharedVars.EVENTS[:]:
            event_id = event.get("EventID")

            if event_id in sharedVars.ExistingEventID:
                print(f"{event_id} already exists.")
                # remove from EVENTS 
                sharedVars.EVENTS.remove(event)
            else:
                # Create the assignment in Notion
                NotionAPI.createAssignment(
                    NotionAPI.dbID,
                    event.get("Assignment Name"),
                    event.get("Course Code"),
                    event.get("Deadline"),
                    event_id
                )
                print("Creating new assignment with name:", event.get("Assignment Name"))

                # Add to ExistingEventID so no dupes
                sharedVars.ExistingEventID.append(event_id)

                # Remove from EVENTS once created
                sharedVars.EVENTS.remove(event)

    except Exception as error:
        print("Error caught: " + str(error))

EventsToNotion()