import paho.mqtt.client as mqtt
from main import Measure, db
from datetime import datetime
import json

MQTT_HOST = '192.168.1.70'
TOPIC = 'home/kitchen'
  
  
def on_connect(client, userdata, flag, rc):
    if rc == 0:
        # with open('/var/www/embedded/logs.log', 'w') as f:
        #     f.write("Conected OK\n")
        client.subscribe(TOPIC)
        
# def on_disconnect(client, userdata, flag, rc):
#     with open('/var/www/embedded/logs.log', 'a') as f:
#         f.write('Disconnected result code', rc)
    
def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode('utf-8'))
    data_in = json.loads(m_decode)
    # with open('/var/www/embedded/logs.log', 'a') as f:
    #     f.write(f'Temperature: {data_in["temp"]} \nHumidity:{data_in["hum"]} \nDevice:{data_in["device"]}')
    value = Measure(temperature=data_in['temp'], 
                    humidity=data_in['hum'], 
                    device=data_in['device'],
                    postDate= datetime.now())
    db.session.add(value)
    db.session.commit()
        

client = mqtt.Client('python_1')
client.connect(MQTT_HOST)

# client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message

while True:
    client.loop_start()
    
