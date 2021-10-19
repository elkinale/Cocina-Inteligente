import  paho.mqtt.client as mqtt
import object_detection

MQTT_HOST = '192.168.1.70'
TOPIC_1 = 'object/detect'
TOPIC_2 = 'object/label'

def on_connect(client, userdata, flag, rc):
    if rc == 0:
        client.subscribe(TOPIC_1)
        
    
def on_message(client, userdata, msg):
    m_decode = msg.payload.decode('utf-8')
    classes = object_detection.detect(m_decode)
    labels = ''
    for item in classes:
        labels += item
    client.publish(TOPIC_2, labels)
    
    
client = mqtt.Client('python_2')
client.connect(MQTT_HOST)

client.on_connect = on_connect
client.on_message = on_message

while True:
    client.loop_start()