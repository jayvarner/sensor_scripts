import logging
import board
import adafruit_ahtx0
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

clientname = 'home'
hostname = '192.168.1.150'
port = 1883
timeout = 60

config_file = open('config.json')

config = json.load(config_file)

# callback for CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# callback for received messages
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(clientname)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(config['mqttUser'], config['mqttPassword'])

now = datetime.now().strftime('%Y-%m-%d %H:%M')

try:
    client.connect(hostname, port, timeout)
    client.loop_start()
    client.publish(f"{config['location']}_temp", round(sensor.temperature * 9 / 5 + 32, 1))
    client.publish(f"{config['location']}_humidity", round(sensor.relative_humidity, 1))
    logging.info(f'Updated {now}')
except Exception as e:
    logging.error(f'Fuck, shit failed at {now}')
    logging.error(e)