import logging
import paho.mqtt.client as mqtt
from blinker import signal
import json

MQTT_HOST = 'raspberrypi'
MQTT_PORT = 1883
MQTT_CLIENT = 'game_client'

class MQTTClient():
    '''
        MQTTClient constructor takes a topic list to subscribe
    '''
    def __init__(self, topics):
        self.topics = topics

    '''
        Send a MQTT Message
    '''
    def send_message(self, msg):
        topic = msg['topic']
        body = msg['body']
        status = self.client.publish(topic, json.dumps(body))
        statuscode = ['OK', 'ERROR']
        logging.info(f'Message {topic} published: {statuscode[status[0]]}')

    '''
        Connect MQTT
    '''
    def setup(self):
        self.client = mqtt.Client(MQTT_CLIENT)
        logging.debug('Connecting to MQTT')
        self.client.connect(MQTT_HOST, MQTT_PORT)

        def on_connect(client, userdata, flags, rc):
            logging.debug('Connection established')
        
        def on_message(client, userdata, msg):
            body = json.loads(msg.payload)
            logging.info(f'Topic {msg.topic}: message {body}')
            sig = signal(msg.topic)
            sig.send(body)
        
        for topic in self.topics:
            self.client.subscribe(topic)
        
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        # Signal to send messages
        sig = signal('message')
        sig.connect(self.send_message)
    
    def run(self):
        logging.debug('Running MQTT loop')
        self.client.loop_start()
    
    def stop(self):
        logging.debug('Stopping MQTT loop')
        self.client.loop_stop()
        self.client.disconnect()