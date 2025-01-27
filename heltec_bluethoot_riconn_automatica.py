import bluetooth
import time

address = "78:21:84:A0:BA:F2"
port = 1

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
        except bluetooth.BluetoothError as e:
            print(f"Errore durante la ricezione dei dati: {e}. Tentativo di riconnessione...")
            sock.close()
            sock = connect_to_device()
except KeyboardInterrupt:
    print("Interruzione manuale del programma.")
finally:
    sock.close()
    print("Connessione chiusa.")
