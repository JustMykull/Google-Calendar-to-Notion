from notion_client import Client

client = Client(auth="SECRET")
dbID = "database id"

file_path = "pages.json"

def jsonDump(pages):
    try:
        with open(file_path, "w") as json_file:
            json.dump(pages, json_file, indent=4)
    except Exception as error:
        print(error)

def getAssignments(databaseID):
    try:
        pages = []
        # first request
        query = client.databases.query(database_id=databaseID)
        pages.extend(query["results"])

        # keep going until all assignments are accounted for because FUCK DUPES AND I FORGOT THIS IN THE FIST VERSION
        while query.get("has_more", False):
            query = client.databases.query(
                database_id=databaseID,
                start_cursor=query["next_cursor"]
            )
            pages.extend(query["results"])

        jsonDump(pages)
        return pages            

    except Exception as error:
        print(error)

def createAssignment(databaseID, assignmentName, courseCode, Deadline, EventID):
    try: 
        new_page = client.pages.create(
            parent={"database_id": databaseID},
            properties={
                "Assignment Name": {
                    "title": [{"text": {"content": assignmentName}}]
                },
                "Course Code": {
                    "type": "select",
                    "select": {"name": courseCode}
                },
                "Deadline": {
                    "type": "date",
                    "date": {
                        "start": Deadline,
                        "end": None,
                        "time_zone": None
                    }
                },
                "EventID": {
                    "type": "rich_text",
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": EventID if EventID else "MISSING_ID"}
                    }]
                }
            }
        )
        return new_page

    except Exception as error:
        print(error, "NotionAPI Page")
