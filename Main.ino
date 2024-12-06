#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <SparkFunBME280.h>
#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi details
const char* ssid = "MYSSID";
const char* password = "MYPASS";

// MQTT broker settings
const char* mqtt_server = "RasPi server";

WiFiClient espClient;
PubSubClient client(espClient);

//init pins for on the microcontroller
int windDirectionPin = 35;
int windSpeedPin = 14;
int rainfallPin = 27;

//delcaring the sensors
BME280 tempSensor;
SFEWeatherMeterKit weatherMeterKit(windDirectionPin, windSpeedPin, rainfallPin);

// Time intervals
#define ACTIVE_TIME 60000  
#define SLEEP_TIME 60000000 
#define MSG_INTERVAL 10000  
#define PRESSURE_INTERVAL 10000 

// set intervals between messages
unsigned long lastMsg = 0;
unsigned long lastPressureMsg = 0;
unsigned long activeStartTime = 0; 

void setup_wifi() {
  Serial.println("Attempting to connect to Wi-Fi...");
  WiFi.begin(ssid, password);
  unsigned long startAttemptTime = millis();
  unsigned long timeout = 60000;  // Timeout period (60 seconds)

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < timeout) {
    delay(500);
    Serial.print(".");
  }
  // if wifi doesnt connecting within timeframe (60 seconds) the esp proccessor restarts
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to Wi-Fi");
    Serial.println(WiFi.localIP()); 
  } else {
    Serial.println("\nFailed to connect to Wi-Fi within the timeout period.");
    Serial.println("Resetting the board...");
    ESP.restart();  // Reset the board if Wi-Fi connection fails after the timeout
  }
}

// connects to the MQTT server
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Serial connected! Starting setup...");

  setup_wifi();
  client.setServer(mqtt_server, 1883);

  Wire.begin();
  weatherMeterKit.begin();

  if (tempSensor.begin() == false) {
    Serial.println("BME280 did not respond.");
    while (1);
  }

  activeStartTime = millis();
}

// reads the sensors data
void readAndPrintSensorData() {
  float temperature_C = tempSensor.readTempC();
  float humidity = tempSensor.readFloatHumidity();
  float pressure = tempSensor.readFloatPressure();
  float wind_dir = weatherMeterKit.getWindDirection();
  float wind_speed = weatherMeterKit.getWindSpeed();
  float rain = weatherMeterKit.getTotalRainfall();

  // Print data to Serial Monitor for debugging purposes
  Serial.printf("Temperature: %.2f C\n", temperature_C);
  Serial.printf("Humidity: %.2f\n", humidity);
  Serial.printf("Pressure: %.2f Pa\n", pressure);
  Serial.printf("Wind Direction (Degrees): %.2f\n", wind_dir);
  Serial.printf("Wind Speed (Kph): %.2f\n", wind_speed);
  Serial.printf("Rainfall (mm): %.2f\n", rain);
  Serial.println("-------------------------------");

  // Publish data over MQTT
  if (client.connected()) {
    client.publish("sensor/temperature", String(temperature_C).c_str());
    client.publish("sensor/humidity", String(humidity).c_str());
    client.publish("sensor/pressure", String(pressure).c_str());
    client.publish("sensor/wind_direction", String(wind_dir).c_str());
    client.publish("sensor/wind_speed", String(wind_speed).c_str());
    client.publish("sensor/rainfall", String(rain).c_str());
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED && !client.connected()) {
    reconnect();
  }

  client.loop();

  unsigned long now = millis();

  if (now - lastMsg > MSG_INTERVAL) {
    lastMsg = now;
    readAndPrintSensorData();
  }

  // Check if the active period is over
  if (now - activeStartTime >= ACTIVE_TIME) {
    Serial.println("Entering light sleep for 60 seconds...");
    delay(1000);
    client.disconnect(); 
    esp_sleep_enable_timer_wakeup(SLEEP_TIME); 
    esp_light_sleep_start();
    Serial.println("Woke up from light sleep");

    setup_wifi();
    reconnect();

    activeStartTime = millis();
  }
}
