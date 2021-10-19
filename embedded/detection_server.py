import  paho.mqtt.client as mqtt

MQTT_HOST = '192.168.1.70'
TOPIC_1 = 'object/detect'
TOPIC_2 = 'object/label'

data=''
img=''

def on_connect(client, userdata, flag, rc):
    if rc == 0:
        client.subscribe(TOPIC_2)
        
def on_message(client, userdata, msg):
    global data
    m_decode = str(msg.payload.decode('utf-8'))
    labels = list(m_decode)
    data = labels
    client.loop_stop()
    
client = mqtt.Client('python_3')
client.connect(MQTT_HOST)
client.publish(TOPIC_1, img)

client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()

