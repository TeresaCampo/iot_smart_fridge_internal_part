#include <Wire.h>
#include <Adafruit_BME280.h>
#include "HT_SSD1306Wire.h"
#include <BluetoothSerial.h>

// Primo bus I2C per il display OLED
#define OLED_SDA 4
#define OLED_SCL 15
#define OLED_RST 16

// Secondo bus I2C per il sensore BME280
#define BME_SDA 21
#define BME_SCL 22

Adafruit_BME280 bme;
SSD1306Wire oledDisplay(0x3C, 500000, OLED_SDA, OLED_SCL, GEOMETRY_128_64, OLED_RST);
TwoWire BME280_I2C = TwoWire(1); // Istanza per il secondo bus I2C
BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  // Inizializza la comunicazione seriale Bluetooth
  if (!SerialBT.begin("Sensore Smart Fridge sensor")) {
    Serial.println("An error occurred initializing Bluetooth");
    return;
  }
  Serial.println("Bluetooth Initialized.");
  
  // Inizializza il bus I2C per il BME280
  BME280_I2C.begin(BME_SDA, BME_SCL);
  if (!bme.begin(0x76, &BME280_I2C)) {
    Serial.println("BME280: connection error.");
    while (1);
  }
  Serial.println("Sensor initialized.");
  
  // Inizializza il bus I2C per il display OLED
  Wire.begin(OLED_SDA, OLED_SCL);
  
  // Inizializza il display OLED
  oledDisplay.init();
  oledDisplay.clear();
  oledDisplay.setFont(ArialMT_Plain_16);
  Serial.println("Display initialized.");
}

void loop() {
  String message = retrieveParameters();
  
  showMessageOnDisplay(message);

  SerialBT.println(message);

  delay(5000);    // Aspetta 2 secondi
}

String retrieveParameters(){
  String temp_message= "Temp: "+ String(bme.readTemperature())+ " *C";
  String hum_message= "Humidity:"+ String(bme.readHumidity()) + " %";
  String full_message= temp_message + "\n" + hum_message;
  return full_message;
}

void showMessageOnDisplay(String message){
  oledDisplay.clear();               // Pulisce lo schermo
  oledDisplay.drawString(0, 0, message);
  oledDisplay.display();             // Mostra i dati sul display
}
