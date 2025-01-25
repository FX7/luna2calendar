from luna_login import luna_login

import requests
from bs4 import BeautifulSoup
import os

session = luna_login()

def luna_load_calendar_page():
  # POST-Anfrage an die Action-URL des Formulars senden
  post_payload = {
      'customerContracts': os.getenv('LUNA_CALENDAR_ID')  # Der Wert des ausgewählten Kalenders
  }

  response = session.post(os.getenv('LUNA_SELECT_CONTRACT_URL'), data=post_payload)

  # Überprüfen, ob die Anfrage erfolgreich war
  if not response.ok:
    print(f"Fehler beim Abrufen der Daten für Kalender '{calendar}'!")
    exit()

def luna_extract_calendar():
  post_payload = {
      'month': os.getenv('LUNA_MONTH')  # Monat im Format "YYYY-MM-DD"
  }

  response = session.post(os.getenv('LUNA_LOAD_DATA_URL'), data=post_payload)

  # Überprüfen, ob die Anfrage erfolgreich war
  if not response.ok:
    print(f"Fehler beim Abrufen der Kalenderdaten für den Monat '{os.getenv('LUNA_MONTH')}'!")
    print(response.status_code)
    print(response.text)
    exit()

  # Die Antwort parsen (angenommen, es handelt sich um JSON)
  response_data = response.json()  # Hier wird angenommen, dass die Antwort im JSON-Format vorliegt
  calendar_data = response_data.get('data', [])

  # Umwandeln der Daten in das gewünschte Format
  formatted_data = []
  for entry in calendar_data:
    date = entry.get('start').split(' ')[0]  # Nur das Datum extrahieren
    title = entry.get('title')  # HTML-Text
    title_stripped = BeautifulSoup(title, 'html.parser').get_text(separator=' ', strip=True)  # HTML bereinigen und durch Leerzeichen trennen
    is_ordered = entry.get('extendedProps', {}).get('isOrdered', 0)  # Standardwert 0, falls nicht vorhanden

    entry = {
        'date': date,
        'title': title_stripped,
        'ordered': bool(is_ordered)  # Umwandeln in Boolean (True/False)
    }
    formatted_data.append(entry)
  return formatted_data

luna_load_calendar_page()
