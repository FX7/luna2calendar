from luna_login import luna_login
from luna_extract_orders import luna_extract_calendar

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import uuid
import os

# Funktion zum Hinzufügen von Kalendereinträgen
def nextcloud_add_event_to_calendar(entry):
  if os.getenv('LUNA_ONLY_ORDERED') and not entry.get('ordered'):
    return

  date = entry.get('date').replace('-', '')
  timezone = os.getenv('SCHOOL_LUNCH_TIMEZONE')
  evt_id = str(uuid.uuid4())
  title = entry.get('title')

  if not os.getenv('LUNA_ONLY_ORDERED'):
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
DTSTART;{timezone}:{date}T{os.getenv('SCHOOL_LUNCH_START_TIME')}
DTEND;{timezone}:{date}T{os.getenv('SCHOOL_LUNCH_END_TIME')}
END:VEVENT
END:VCALENDAR"""

  nc_cal_url = 'https://' + os.getenv('NEXTCLOUD_DOMAIN') + '/remote.php/dav/calendars/' + os.getenv('NEXTCLOUD_USERNAME') + '/' +  os.getenv('NEXTCLOUD_CALENDAR_NAME') + '/' + evt_id + '.ics'

  # Füge das Ereignis hinzu
  response = requests.put(nc_cal_url,
    data=ical_data,
    headers={'Content-Type': 'text/calendar'},
    auth=HTTPBasicAuth(os.getenv('NEXTCLOUD_USERNAME'), os.getenv('NEXTCLOUD_PASSWORD'))
  )

  if response.status_code not in (200, 201, 204):
    print('Fehler beim Hinzufügen des Ereignisses ' + ical_data, response.status_code, response.text)


calendar_entrys = luna_extract_calendar()
for entry in calendar_entrys:
  nextcloud_add_event_to_calendar(entry)
