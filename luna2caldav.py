from luna_extract_orders import luna_extract_calendar

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import uuid
import os

_LUNA_ONLY_ORDERED = eval(os.getenv('LUNA_ONLY_ORDERED', 'True'))
_SCHOOL_LUNCH_TIMEZONE = os.getenv('SCHOOL_LUNCH_TIMEZONE', 'Europe/Berlin')
_SCHOOL_LUNCH_START_TIME = os.getenv('SCHOOL_LUNCH_START_TIME', '114000')
_SCHOOL_LUNCH_END_TIME = os.getenv('SCHOOL_LUNCH_END_TIME', '122000')

_CALDAV_CALENDAR_NAME = os.getenv('CALDAV_CALENDAR_NAME','calendar')
_CALDAV_URL = 'https://' + os.getenv('CALDAV_DOMAIN','nextcloud') + '/' +  os.getenv('CALDAV_PATH','calendars') + '/' + os.getenv('CALDAV_USERNAME','user') + '/' +  _CALDAV_CALENDAR_NAME
_CALDAV_USERNAME = os.getenv('CALDAV_USERNAME','user')
_CALDAV_PASSWORD = os.getenv('CALDAV_PASSWORD', 'password')

def extractEntryDate(entry):
  date = entry.get('date').replace('-', '')
  return date

def extractEntryId(entry):
  date = extractEntryDate(entry)
  # evt_id = str(uuid.uuid4())
  title = entry.get('title')
  hash_value = hash(title)
  evt_id = 'luna-' + date + _CALDAV_CALENDAR_NAME + '-' + str(hash_value)
  return evt_id


def delete_event_from_calendar(entry):
  evt_id = extractEntryId(entry)
  title = entry.get('title')

  delete_entry_url = _CALDAV_URL + '/' + evt_id + '.ics'

  # Löscht das Ereignis
  response = requests.delete(delete_entry_url,
    headers={'Content-Type': 'text/calendar'},
    auth=HTTPBasicAuth(_CALDAV_USERNAME, _CALDAV_PASSWORD)
  )

  # Überprüfen, ob die Anfrage erfolgreich war
  if response.status_code == 204:
    print("Kalendereintrag '" + title + "' erfolgreich gelöscht.")
  elif response.status_code == 404:
    print("Kalendereintrag '" + title + "' übersprungen")
  else:
    print(f"Fehler beim Löschen des Kalendereintrags: {response.status_code} - {response.text}")

def add_event_to_calendar(entry):
  title = entry.get('title')

  if _LUNA_ONLY_ORDERED and not entry.get('ordered'):
    print("Kalendereintrag '" + title + "' übersprungen.")
    return

  date = extractEntryDate(entry)
  evt_id = extractEntryId(entry)

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
DTSTART;{_SCHOOL_LUNCH_TIMEZONE}:{date}T{_SCHOOL_LUNCH_START_TIME}
DTEND;{_SCHOOL_LUNCH_TIMEZONE}:{date}T{_SCHOOL_LUNCH_END_TIME}
END:VEVENT
END:VCALENDAR"""

  add_entry_url = _CALDAV_URL + '/' + evt_id + '.ics'

  # Füge das Ereignis hinzu
  response = requests.put(add_entry_url,
    data=ical_data,
    headers={'Content-Type': 'text/calendar'},
    auth=HTTPBasicAuth(_CALDAV_USERNAME, _CALDAV_PASSWORD)
  )

  if response.status_code not in (200, 201, 204):
    print('Kalendereintrag konnte nicht hinzugefügt werden: ' + ical_data, response.status_code, response.text)
  else:
    print("Kalendereintrag '" + title + "' hinzugefügt.")


calendar_entrys = luna_extract_calendar()
for entry in calendar_entrys:
  delete_event_from_calendar(entry)
  add_event_to_calendar(entry)
