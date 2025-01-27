Istruzioni:

1. bluetoothctl scan on
	e cercare 78:21:84:A0:BA:F2
2. bluetoothctl pair 78:21:84:A0:BA:F2
3. bluetoothctl connect 78:21:84:A0:BA:F2
4. sudo rfcomm bind 0 78:21:84:A0:BA:F2
	con il comando rfcomm-> crea una connessione seriale bluethoot usando il protocollo SPP(serial port profile), ovvero un protocollo per la comunicazione seriale su bliethoot
	con bind-> crea la comunicazione seriale tra heltec(mac address) e il dispositivo seriale virtuale 0 (rfcomm0)
5. sudo cat /dev/rfcomm0
	per visualizzare messaggi in arrivo su quel dispositivo virtuale rfcomm
6. sudo rfcomm release 0
	per fermare la comunicazione seriale bluethoot su quel dispositivo virtuale

 
SENSORE BME/BMP280(sensore di temperatura, umidità e pressione)
Scaricare la libreria Adafruit BMP280
SCHERMO OLED
Scaricare la libreria Adafruit_SSD1306


