import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def addEvent(row):
  
    name = row[1]
    create_time = row[2]
    current_time = row[3]
    event = row[4]
   # Auth
    creds = None

    if os.path.exists('token.json'):
        print('token exists')
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        print('cred invalid 1')
        if creds and creds.expired and creds.refresh_token:
            print('cred refresh request')
            creds.refresh(Request())
        else:
            print('flow')
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print('written')
  
    try:
        service = build("calendar", "v3", credentials=creds)

        event  = {
            "summary": name,
            "location" : "online",
            "description" : "Some deets",
            "colorId" : 6,
            "start": {
                "dateTime" : create_time + '+05:30',
                "timeZone" : "Asia/Kolkata"

            },
            "end": {
                "dateTime" : current_time + '+05:30',
                "timeZone" : "Asia/Kolkata"

            }  
        }

        event = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Event created {event.get('htmlLink')}")

    except HttpError as error:
        print("An error occured: ", error)






        
##########################


# now = dt.datetime.now().isoformat() + "Z"

# event_result = service.events().list(calendarId='primary', timeMin=now, maxResults=3, singleEvents=True, orderBy="startTime").execute()
# events = event_result.get("items", [])

# if not events:
#     print("No upcoming events found!")
#     return

# for event in events:
#     start = event["start"].get("dateTime", event["start"].get("date"))
#     print(start, event["summary"])
