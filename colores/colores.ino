#include <Wire.h>
#include <LiquidCrystal.h>

// LCD: RS, EN, D4, D5, D6, D7
LiquidCrystal lcd(6, 8, 9, 10, 11, 12);

String inputString = "";
bool stringComplete = false;

int r = 0, g = 0, b = 0;
String colorName = "";

// Dirección del esclavo I2C (PIC)
#define PIC_ADDRESS 0x11

void setup() {
  Serial.begin(9600);
  Wire.begin();  // Inicializa I2C como maestro

  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Esperando color");

  inputString.reserve(50);
}

void loop() {
  if (stringComplete) {
    Serial.print("Color recibido: ");
    Serial.println(inputString);

    // Separar el mensaje (formato: "Rojo,255,0,0")
    parseColorData(inputString);

    // Mostrar en LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Color detectado:");
    lcd.setCursor(0, 1);
    lcd.print(colorName);

    // Enviar valores RGB al PIC por I2C
    Wire.beginTransmission(PIC_ADDRESS);
    Wire.write((uint8_t)b);
    Wire.write((uint8_t)g);
    Wire.write((uint8_t)r);
    Wire.endTransmission();

    // Reset
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

void parseColorData(String data) {
  int idx1 = data.indexOf(',');
  int idx2 = data.indexOf(',', idx1 + 1);
  int idx3 = data.indexOf(',', idx2 + 1);

  if (idx1 > 0 && idx2 > idx1 && idx3 > idx2) {
    colorName = data.substring(0, idx1);
    r = data.substring(idx1 + 1, idx2).toInt();
    g = data.substring(idx2 + 1, idx3).toInt();
    b = data.substring(idx3 + 1).toInt();
  } else {
    colorName = "Desconocido";
    r = g = b = 0;
  }
}
