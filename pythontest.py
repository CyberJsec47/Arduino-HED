import paho.mqtt.client as mqtt

# Callback when the client receives a connection response from the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        # Subscribe to a topic after connecting
        client.subscribe("your/topic")
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
broker_address = "broker.hivemq.com"  # Change to your broker address
port = 1883  # Default MQTT port

client.connect(broker_address, port, 60)

# Blocking loop to process network traffic and dispatch callbacks
client.loop_forever()
