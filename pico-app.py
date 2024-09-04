import machine
import time
import dht
import ubinascii
from umqtt.simple import MQTTClient
# Initialize sensor and LED pins
sensor = dht.DHT11(machine.Pin(4))  # Example sensor on GPIO 4
led_red = machine.Pin(15, machine.Pin.OUT)
led_green = machine.Pin(12, machine.Pin.OUT)
led_blue = machine.Pin(13, machine.Pin.OUT)
# MQTT configuration
MQTT_BROKER = "7a5ac4b86d0a408292b06e2abd774619.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "iot-test"
MQTT_PASSWORD = "Welcome1@"
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC_PUB = b"pico/sensors/data"
MQTT_TOPIC_SUB = b"pico/led/control"

def sub_cb(topic, msg):
    print(f"Received message: {msg} on topic: {topic}")
    if msg == b'red_on':
        led_red.on()
    elif msg == b'red_off':
        led_red.off()
    elif msg == b'green_on':
        led_green.on()
    elif msg == b'green_off':
        led_green.off()
    elif msg == b'blue_on':
        led_blue.on()
    elif msg == b'blue_off':
        led_blue.off()
# Connect to MQTT broker
def mqtt_connect():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(MQTT_TOPIC_SUB)
    print("Connected to MQTT broker and subscribed to topic")
    return client
# Publish sensor data
def publish_sensor_data(client):
    while True:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        msg = b'{"temperature": %d, "humidity": %d}' % (temp, hum)
        client.publish(MQTT_TOPIC_PUB, msg)
        print(f"Published: {msg}")
        time.sleep(10)
def run():
    client = mqtt_connect()
    try:
        while True:
            client.check_msg()  # Check for incoming messages
            publish_sensor_data(client)
    except KeyboardInterrupt:
        print("Disconnecting from MQTT broker")
        client.disconnect()
# Entry point
if __name__ == "__main__":
    run()