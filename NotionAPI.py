from notion_client import Client

client = Client(auth="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")
dbID = "25a33e98aa5881d7a875f3813844bb2e"

def getAssignments(databaseID):
    try:
        pages = client.databases.query(database_id=databaseID)["results"]

        return pages

        # CourseCode = page.get("properties").get("Course Code").get("rich_text")[0].get("text").get("content")
        # print(page.get("properties"))

    except Exception as error:
        print(error)

def createAssignment(databaseID, assignmentName, courseCode, Deadline, EventID):
    try: 
        new_page = client.pages.create(
            parent = {"database_id" : databaseID},
            properties = {
                "Assignment Name" : {
                    "title" : [
                        {"text" : {"content" : assignmentName}}
                    ]
                },
                "Course Code" : {
                    "type" : "select",
                    "select" : {
                        "name" : courseCode
                    }
                },
                "Deadline" : {
                    "type" : "date",
                    "date" : {
                        "start" : Deadline,
                        "end" : None,
                        "time_zone" : None
                    }
                },
                "EventID" : {
                    "type" : "rich_text",
                    "rich_text" : [{
                        "type" : "text",
                        "text" : {
                            "content" : EventID
                        }
                }]
                }
            }
        )

    except Exception as error:
        print(error)

