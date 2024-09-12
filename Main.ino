#include <LiquidCrystal.h>
#include <DHT.h>
#include <DHT_U.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define TRIGPIN 3
#define ECHOPIN 4
#define MAX_DISTANCE 25


#define BACKLIGHT_PIN 6
#define BACKLIGHT_BRIGHTNESS 128 
#define BACKLIGHT_OFF 0          

void setup() {
  lcd.begin(16, 2);
  dht.begin();
  
  pinMode(TRIGPIN, OUTPUT);
  pinMode(ECHOPIN, INPUT);

  pinMode(BACKLIGHT_PIN, OUTPUT);

  digitalWrite(BACKLIGHT_PIN, BACKLIGHT_OFF);
  lcd.noDisplay();
  
  Serial.begin(9600);
}

void loop() {
  long distance = measureDistance();
  
  if (distance < MAX_DISTANCE && distance > 0) {
    lcd.display();
    analogWrite(BACKLIGHT_PIN, BACKLIGHT_BRIGHTNESS);

    delay(2000); // Delay for sensor readings

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(F("Temp: "));
    lcd.print(t);
    lcd.print(F(" C"));

    lcd.setCursor(0, 1);
    lcd.print(F("Humidity: "));
    lcd.print(h);
    lcd.print(F("%"));
    
  } else {
    lcd.noDisplay(); 
    digitalWrite(BACKLIGHT_PIN, BACKLIGHT_OFF); 
  }

  delay(50); 
}

long measureDistance() {
  digitalWrite(TRIGPIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);

  long duration = pulseIn(ECHOPIN, HIGH);
  long distance = duration * 0.034 / 2;
  
  return distance;
}
