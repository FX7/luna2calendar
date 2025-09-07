import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

_LUNA_LOGIN_URL = os.getenv('LUNA_LOGIN_URL', 'https://bestellen.luna.de/login')

load_dotenv()

def luna_extract_csrf(session):
  # Schritt 1: Login-Seite abrufen, um den CSRF-Token zu erhalten
  response = session.get(_LUNA_LOGIN_URL)

  # Überprüfen, ob der Abruf der Login-Seite erfolgreich war
  if not response.ok:
    print("Fehler beim Abrufen der Login-Seite!")
    exit()

  # BeautifulSoup verwenden, um die Seite zu parsen
  soup = BeautifulSoup(response.text, 'html.parser')

  # CSRF-Token extrahieren
  csrf_token = soup.find('input', {'name': '_csrf_token'})['value']
  if csrf_token is None:
    print("CSRF-Token nicht gefunden!")
    exit()
  return csrf_token

def luna_login():
  # Session erstellen
  session = requests.Session()

  # Anmeldedaten
  payload = {
    'email': os.getenv('LUNA_USERNAME'),
    'password': os.getenv('LUNA_PASSWORD'),
    '_csrf_token': luna_extract_csrf(session)
  }

  # Anmelden
  response = session.post(_LUNA_LOGIN_URL, data=payload)

  # Überprüfen, ob der Login erfolgreich war
  if not response.ok:
    print("Login fehlgeschlagen!")
    print(response.status_code)
    exit()  # Beende das Skript, wenn der Abruf fehlschlägt

  return session
