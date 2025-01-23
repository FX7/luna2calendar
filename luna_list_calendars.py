from luna_login import luna_login
from bs4 import BeautifulSoup
import os

session = luna_login()

def luna_extract_calendars():
  # Kalenderseite abrufen
  response = session.get(os.getenv('LUNA_CALENDAR_URL'))

  # BeautifulSoup verwenden, um die Seite zu parsen
  soup = BeautifulSoup(response.text, 'html.parser')

  # Optionen extrahieren
  dropdown = soup.find('select', {'id': 'currentContract'})

  # Überprüfen, ob das Dropdown gefunden wurde
  if dropdown is None:
    print("Kalender dropdown nicht gefunden")
    exit()

  # Optionen extrahieren
  calendar_options = []
  for option in dropdown.find_all('option'):
    value = option['value']
    text = option.text.strip()
        
    # Optionen mit dem Text "-----" ignorieren
    if text == "-----":
      continue
        
    # Nur den Text nach dem letzten Komma extrahieren
    if ',' in text:
      text = text.rsplit(',', 1)[-1].strip()  # Alles nach dem letzten Komma
      calendar_options.append({'value':value, 'owner':text})

  return calendar_options

calendars = luna_extract_calendars()
print(calendars)
