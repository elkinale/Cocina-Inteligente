import paho.mqtt.client as mqtt
import time

broker_adress = '192.168.1.70'
  
    
def on_connect(client, userdata, flag, rc):
    if rc == 0:
        with open('logs.log', 'w') as f:
            f.write("Conected OK\n")
        client.subscribe('home/kitchen')
    else:
        print("Bad connection Return code=", rc)
        
def on_disconnect(client, userdata, flag, rc):
    with open('logs.log', 'a') as f:
        f.write('Disconnected result code', rc)
    
def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode('utf-8'))
    with open('logs.log', 'a') as f:
        f.write(f'Topic: {topic} \nmessage : {m_decode}')
    
        

client = mqtt.Client('python_1')
client.connect(broker_adress)

client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message


while True:
    client.loop_start()
    
