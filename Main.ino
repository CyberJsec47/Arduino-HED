#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <SparkFunBME280.h>
#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi details
 const char* ssid = "//MyWIFI";
 const char* password = "//MyPassword";

// MQTT broker settings
 const char* mqtt_server = "//IP address";

WiFiClient espClient;
PubSubClient client(espClient);

int windDirectionPin = 35;
int windSpeedPin = 14;
int rainfallPin = 27;

BME280 tempSensor;
SFEWeatherMeterKit weatherMeterKit(windDirectionPin, windSpeedPin, rainfallPin);

// Time intervals
#define ACTIVE_TIME 60000  
#define SLEEP_TIME 60000000 
#define MSG_INTERVAL 10000  
#define PRESSURE_INTERVAL 10000 
#define WATCHDOG_TIMEOUT 60  // Watchdog timeout in seconds

unsigned long lastMsg = 0;
unsigned long lastPressureMsg = 0;
unsigned long activeStartTime = 0; 

void setup_wifi() {
  Serial.println("Attempting to connect to Wi-Fi...");
  WiFi.begin(ssid);
  unsigned long startAttemptTime = millis();
  unsigned long timeout = 10000;

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < timeout) {
    delay(500);
    Serial.print(".");
    esp_task_wdt_reset();
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to Wi-Fi");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to Wi-Fi within the timeout period.");
  }
}

void reconnect() {
  esp_task_wdt_reset();

  unsigned long startReconnectTime = millis();
  while (!client.connected()) {
    if (millis() - startReconnectTime > WATCHDOG_TIMEOUT * 1000) {
      Serial.println("Reconnect attempt exceeded 60 seconds, resetting...");
      ESP.restart(); 
    }

    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
      esp_task_wdt_reset(); 
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Serial connected! Starting setup...");

  esp_task_wdt_config_t config = {
    .timeout_ms = WATCHDOG_TIMEOUT * 1000 
  };
  esp_task_wdt_init(&config); 
  esp_task_wdt_add(NULL);  

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

void readAndPrintSensorData() {
  float temperature_C = tempSensor.readTempC();
  float humidity = tempSensor.readFloatHumidity();
  float pressure = tempSensor.readFloatPressure();
  float wind_dir = weatherMeterKit.getWindDirection();
  float wind_speed = weatherMeterKit.getWindSpeed();
  float rain = weatherMeterKit.getTotalRainfall();

  Serial.printf("Temperature: %.2f C\n", temperature_C);
  Serial.printf("Humidity: %.2f\n", humidity);
  Serial.printf("Pressure: %.2f Pa\n", pressure);
  Serial.printf("Wind Direction (Degrees): %.2f\n", wind_dir);
  Serial.printf("Wind Speed (Kph): %.2f\n", wind_speed);
  Serial.printf("Rainfall (mm): %.2f\n", rain);
  Serial.println("-------------------------------");

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

  esp_task_wdt_reset();
}
