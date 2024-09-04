from machine import Pin, I2C
import utime as time
from time import sleep
import dht
import secrets
import uarray
import json
import ubinascii
from umqtt.robust import MQTTClient

# Pin configs
sensor = dht.DHT11(Pin(3))
led_green = Pin(15, Pin.OUT)
led_blue = Pin(14, Pin.OUT)
led_red = Pin(13, Pin.OUT)
# MQTT configs
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_SERVER = secrets.MQTT_BROKER
MQTT_PORT = 0
MQTT_USER = secrets.MQTT_USERNAME
MQTT_PASSWORD = secrets.MQTT_PASSWORD
MQTT_TOPIC_PUB = b"pico/sensors/data"
MQTT_TOPIC_SUB = b"pico/led/control"
MQTT_KEEPALIVE = 7200
MQTT_SSL = True   # set to False if using local Mosquitto MQTT broker
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

# Callback function that runs when you receive a message on subscribed topic
def my_callback(topic, msg):
    # Perform desired actions based on the subscribed topic and response
    print(f"Message for topic - {topic}")
    print(f"Received message - {msg}")
    msg = msg.decode('utf-8')
    json_acceptable_string = msg.replace("'", "\"")
    msg = json.loads(json_acceptable_string)
    if msg['led'] == 'red':
        if msg['state'] == 'on':
            led_red.on()
        else:
            led_red.off()
    elif msg['led'] == 'green':
        if msg['state'] == 'on':
            led_green.on()
        else:
            led_green.off()
    elif msg['led'] == 'blue':
        if msg['state'] == 'on':
            led_blue.on()
        else:
            led_blue.off()

# Publish sensor data
def read_sensor_data(client, topic):
    sensor.measure()
    temp  = sensor.temperature()
    humd = sensor.humidity()
    msg = b'{"temperature": %d, "humidity": %d}' % (temp, humd)
    return msg
        
def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params=MQTT_SSL_PARAMS)
        client.set_callback(my_callback)
        client.connect()
        print(f"Connected to MQTT broker - {MQTT_SERVER}")
        client.subscribe(MQTT_TOPIC_SUB)
        print(f"Subscribed to topic - {MQTT_TOPIC_SUB}")
        return client
    except Exception as e:
        print(f"Error connecting to MQTT: {e}")
        raise  # Re-raise the exception to see the full traceback


def run():
    client = connect_mqtt()
    # Continuously checking for messages
    while True: 
        client.check_msg()
        payload = read_sensor_data(client, MQTT_TOPIC_PUB)
        client.publish(MQTT_TOPIC_PUB, payload)
        print(f"Published: {payload}")        
        print(f"Pico device UP - {MQTT_CLIENT_ID}")
        time.sleep(5)

# Entry point
if __name__ == "__main__":
    run()
