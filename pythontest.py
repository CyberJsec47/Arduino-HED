import paho.mqtt.client as mqtt
import time

# List of topics to subscribe to
TOPICS = [
    "sensor/temperature",
    "sensor/humidity",
    "sensor/pressure",
    "sensor/altitude",
    "sensor/wind_dir",
    "sensor/wind_speed",
    "sensor/rainfall"
]

# Callback when the client receives a connection response from the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        # Subscribe to each topic in the list
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print(f"Connection failed with code {rc}")

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client()

# Attach callback functions to the client
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
broker_address = "localhost"  # Adjust to your broker's address if needed
port = 1883  # Default MQTT port

client.connect(broker_address, port, 60)

# Run a loop to process messages (similar to the "while true" loop in your bash script)
try:
    client.loop_start()  # Starts a separate thread to handle network traffic
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    print("Exiting")
    client.loop_stop()  # Stop the loop when exiting

