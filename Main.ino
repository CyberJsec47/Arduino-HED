#include <DHT.h>
#include <WiFi.h>
#include <PubSubClient.h>

// Wi-Fi credentials
const char* ssid = //"My WIfi SSID";
const char* password = //"My WIFi Password";

// MQTT broker settings
const char* mqtt_server = //"Raspberry Pi IP;

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_INTERVAL 2000

// DHT11 settings
#define DHT11_PIN  2  
DHT dht11(DHT11_PIN, DHT11);

void setup_wifi() {
  Serial.println("Attempting to connect to Wi-Fi...");
  delay(10);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected to Wi-Fi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ArduinoNanoESP32Client")) {
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
  Serial.begin(9600);
  while (!Serial) {
  }
  Serial.println("Serial connected! Starting setup...");

  dht11.begin(); 
  setup_wifi();
  Serial.println("Wi-Fi setup completed.");
  
  client.setServer(mqtt_server, 1883);
  Serial.println("MQTT server set.");
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > MSG_INTERVAL) {
    lastMsg = now;

    float temperature_C = dht11.readTemperature();
    float humidity = dht11.readHumidity();

    if (isnan(temperature_C) || isnan(humidity)) {
      Serial.println("Failed to read from DHT11 sensor!");
    } else {
      char tempStr[50];
      char humiStr[50];

      // Format and publish temperature
      sprintf(tempStr, "Temperature is %.2f degrees C", temperature_C);
      client.publish("sensor/temperature", tempStr);
      Serial.println(tempStr);

      // Format and publish humidity
      sprintf(humiStr, "Humidity is %.2f%%", humidity);
      client.publish("sensor/humidity", humiStr);
      Serial.println(humiStr);
    }
  }
}
