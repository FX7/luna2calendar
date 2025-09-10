from luna_extract_orders import luna_extract_calendar

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import uuid
import os

_LUNA_ONLY_ORDERED = eval(os.getenv('LUNA_ONLY_ORDERED', 'True'))

# Funktion zum Hinzufügen von Kalendereinträgen
def nextcloud_add_event_to_calendar(entry):
  if _LUNA_ONLY_ORDERED and not entry.get('ordered'):
    return

  date = entry.get('date').replace('-', '')
  timezone = os.getenv('SCHOOL_LUNCH_TIMEZONE', 'Europe/Berlin')
  evt_id = str(uuid.uuid4())
  title = entry.get('title')

  if not _LUNA_ONLY_ORDERED:
    if entry.get('ordered'):
      title = '✅ ' + title
    else:
      title = '❌ ' + title

  ical_data = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Luna//Luna Calendar//DE
BEGIN:VEVENT
SUMMARY:{title}
UID:{evt_id}
DTSTART;{timezone}:{date}T{os.getenv('SCHOOL_LUNCH_START_TIME', '114000')}
DTEND;{timezone}:{date}T{os.getenv('SCHOOL_LUNCH_END_TIME', '122000')}
END:VEVENT
END:VCALENDAR"""

  nc_cal_url = 'https://' + os.getenv('CALDAV_DOMAIN','nextcloud') + '/' +  os.getenv('CALDAV_PATH','calendars') + '/' + os.getenv('CALDAV_USERNAME','user') + '/' +  os.getenv('CALDAV_CALENDAR_NAME','calendar') + '/' + evt_id + '.ics'

  # Füge das Ereignis hinzu
  response = requests.put(nc_cal_url,
    data=ical_data,
    headers={'Content-Type': 'text/calendar'},
    auth=HTTPBasicAuth(os.getenv('CALDAV_USERNAME','user'), os.getenv('CALDAV_PASSWORD', 'password'))
  )

  if response.status_code not in (200, 201, 204):
    print('Fehler beim Hinzufügen des Ereignisses ' + ical_data, response.status_code, response.text)


calendar_entrys = luna_extract_calendar()
for entry in calendar_entrys:
  nextcloud_add_event_to_calendar(entry)
