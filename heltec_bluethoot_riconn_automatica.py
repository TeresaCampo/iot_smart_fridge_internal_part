import bluetooth
import time
from datetime import datetime
import requests
import re

address = "78:21:84:A0:BA:F2"
port = 1
def current_time():
    return datetime.now().strftime('%Y-%m-%dT%H:%M')

def send_to_server(temperature, humidity):
    url = "http://127.0.0.1:8000/api/fridges/11/parameters"
    data = {
        "fridge": 11,
        "humidity": humidity,
        "temperature": temperature,
        "sampling_date": current_time()
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': '6S1eiOl9Kvu3MIIezl9EDYznqvILwaCRU9hNYkBVtu8Z0sH6NMTBkHp3ZAfrnqdS',
        'Authorization': 'Token 62aa1bd2271eedd587232a3259f262fa5b578d88'
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        print(response.status_code)
        if response.status_code == 201:
            print("Dati inviati con successo!")
        else:
            print(f"Errore durante l'invio:\n{response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print("Errore di connessione:", e)

def get_floats_parameters(message):
    temp_match = re.search(r"(\d+\.\d+)", message.split("\n")[0])
    if temp_match:
        temp = float(temp_match.group(1))
    
    humidity_match = re.search(r"(\d+\.\d+)", message.split("\n")[1])
    if humidity_match:
        humidity = float(humidity_match.group(1))
    
    return (temp,humidity)

def connect_to_device():
    while True:
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((address, port))
            print(f"Connesso a {address} su RFCOMM {port}")
            return sock
        except bluetooth.BluetoothError as e:
            print(f"Errore di connessione: {e}. Riprovo tra 5 secondi...")
            time.sleep(5)

# Connessione iniziale
sock = connect_to_device()

try:
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print(f"Dati ricevuti:\n{data.decode('utf-8')}")
                temp,hum=get_floats_parameters(data.decode('utf-8'))
                send_to_server(temp,hum)

                print("...in attesa per 10 minuti...")
                time.sleep(10 * 60)

        except bluetooth.BluetoothError as e:
            print(f"Errore durante la ricezione dei dati: {e}. Tentativo di riconnessione...")
            sock.close()
            sock = connect_to_device()
except KeyboardInterrupt:
    print("Interruzione manuale del programma.")
finally:
    sock.close()
    print("Connessione chiusa.")
