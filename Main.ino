#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <SparkFunBME280.h>
#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi details
 const char* ssid = "//MyWIFI";
 const char* password = "//MyPassword";

// MQTT broker settings
 const char* mqtt_server = "//PI address";

 WiFiClient espClient;
 PubSubClient client(espClient);

int windDirectionPin = 35;
int windSpeedPin = 14;
int rainfallPin = 27;

BME280 tempSensor;
SFEWeatherMeterKit weatherMeterKit(windDirectionPin, windSpeedPin, rainfallPin);

unsigned long lastMsg = 0;
#define MSG_INTERVAL 10000

void setup_wifi() {
  Serial.println("Attempting to connect to Wi-Fi...");
  
  WiFi.begin(ssid, password);
  unsigned long startAttemptTime = millis(); 
  unsigned long timeout = 10000; 

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < timeout) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to Wi-Fi");
    Serial.println(WiFi.localIP()); // Print the local IP
  } else {
    Serial.println("\nFailed to connect to Wi-Fi within the timeout period.");
  }
}


void reconnect() {
 while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
 }

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Serial connected! Starting setup...");
  
  setup_wifi(); // connect to Wi-Fi
  Serial.println("Wi-Fi setup completed.");
  
   client.setServer(mqtt_server, 1883); // Set MQTT server and port
   Serial.println("MQTT server set.");

  Wire.begin();
  weatherMeterKit.begin();
  
  if (tempSensor.begin() == false) {
    Serial.println("BME280 did not respond.");
    while(1);
  }
}

void readAndPrintSensorData() {
  float temperature_C = tempSensor.readTempC();
  float humidity = tempSensor.readFloatHumidity();
  float pressure = tempSensor.readFloatPressure();
  float altitude = tempSensor.readFloatAltitudeFeet();
  float wind_dir = weatherMeterKit.getWindDirection();
  float wind_speed = weatherMeterKit.getWindSpeed();
  float rain = weatherMeterKit.getTotalRainfall();

  // Print data to Serial Monitor
  Serial.printf("Temperature: %.2f C\n", temperature_C);
  Serial.printf("Humidity: %.2f\n", humidity);
  Serial.printf("Pressure: %.2f Pa\n", pressure);
  Serial.printf("Altitude: %.2f feet\n", altitude);
  Serial.printf("Wind Direction (Degrees): %.2f\n", wind_dir);
  Serial.printf("Wind Speed (Kph): %.2f\n", wind_speed);
  Serial.printf("Rainfall (mm): %.2f\n", rain);
  Serial.printf("-------------------------------\n");
 
  
  // Prepare strings for MQTT messages
  char tempStr[50], humiStr[50], pressStr[50], altStr[50], dirStr[50], speedStr[50], rainStr[50];
  
  sprintf(tempStr, "Temperature is %.2f .C", temperature_C);
  sprintf(humiStr, "Humidity is %.2f", humidity);
  sprintf(pressStr, "Pressure is %.2f", pressure);
  sprintf(altStr, "Altitude is %.2f", altitude);
  sprintf(dirStr, "Wind direction is %.2f degrees", wind_dir);
  sprintf(speedStr, "Wind speed is %.2f Kph", wind_speed);
  sprintf(rainStr, "There is %.2f mm of rainfall", rain);

  // Publish only if connected to MQTT
  if (client.connected()) {
    client.publish("sensor/temperature", tempStr);
    client.publish("sensor/humidity", humiStr);
    client.publish("sensor/pressure", pressStr);
    client.publish("sensor/altitude", altStr);
    client.publish("sensor/direction", dirStr);
    client.publish("sensor/speed", speedStr);
    client.publish("sensor/rain", rainStr);
  }
}

void loop() {
   // Try to reconnect to MQTT if disconnected
  if (WiFi.status() == WL_CONNECTED && !client.connected()) {
    reconnect();
  }

  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > MSG_INTERVAL) {
    lastMsg = now;
    readAndPrintSensorData();
  }
}
