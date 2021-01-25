#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  time, json,sys,os
import paho.mqtt.client as paho
import ssl
# from dotenv import load_dotenv
# sys.path.append('/home/mbdj/agente')

# load_dotenv(os.path.join("/home/mbdj/.env"), override=True)
# awshost = str(os.environ.get('awshost')).strip()
# awsport = int(os.environ.get('awsport'))
# clientId = str(os.environ.get('clientId')).strip()
# thingName = str(os.environ.get('thingName')).strip()
# caPath = str(os.environ.get('caPath')).strip()
# certPath = str(os.environ.get('certPath')).strip()
# keyPath  = str(os.environ.get('keyPath')).strip()
awshost = "a22msdc6rv0ukb-ats.iot.us-east-1.amazonaws.com"  #!endPoint-api con la que podemos intereactuar con la sombra
awsport = 8883                                              #!Numero de puerto para amazon   
clientId = "my-agent-one"                                #!Nombre de la cosa
thingName = "my-agent-one"                               #!Nombre de la cosa
caPath = "./AmazonRootCA1.pem"                              #!Llave rain de amazon
certPath = "./certificate.pem.crt"                          #!Ubicacion del certificado de la cosa
keyPath = "./my-agent-one-private.pem.key"                  #!Llave privada de la cosa

connflag = False

def on_connect(client, userdata, flags, rc):
    client.subscribe("Mi-segundo-topic", 1)
    global connflag
    if rc==0:
        print("connected OK Returned code=",rc)
        connflag = True
    else:
        print("Bad connection Returned code=",rc)

#*0: Connection successful
#*1: Connection refused – incorrect protocol version
#*2: Connection refused – invalid client identifier
#*3: Connection refused – server unavailable
#*4: Connection refused – bad username or password
#*5: Connection refused – not authorised
#*6-255: Currently unused.

#    mqttc.subscribe('#', 1)
    # mqttc.subscribe(SHADOW_UPDATE_REJECTED_TOPIC, 1)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic=="Mi-segundo-topic":
        os.system("clear")
        paylodmsg = {
            'mac_id':"id_agente",
            'temperatura-agente': '65°',
            'data': "mi mamá me miam"
        }
        paylodmsg = json.dumps(paylodmsg)    #!JSON stringfy
        mqttc.publish("miprimertopic", paylodmsg , qos=1) #!topic al cual se enviaran los datos
        


def on_disconnect(client, userdata, rc):
    if rc != 0:
        connflag = False
        print ("Hemos perdido la conexion")

#! ASIGNAR EL MISMO ID-CLIENTE
#! PONER EL PARAMETRO CLEAN_SESSION EN FALSO
#! SUSCRIBIRSE A UNA QOS  MAYOR QUE CERO "1"
#* Estas opciones ayudarán a asegurar que cualquier mensaje publicado mientras esté desconectado será entregado una vez que se restablezca la conexión. 

mqttc = paho.Client(client_id=clientId, clean_session=False)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
# mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None) 
mqttc.connect(awshost, awsport, keepalive=60)            	
mqttc.loop_start()


counter = 0
while True:
    time.sleep(5)
    counter += 1
    #mqttc.publish("miprimertopic", f"{counter}" , qos=1)
    if connflag == True:
        paylodmsg = {
            'mac_id':"id_agente",
            'model_type': 'model_type',
            'data': json.dumps({"mac_id":"ramdom string","name":"Nelson",'ts':counter})
        }
        paylodmsg = json.dumps(paylodmsg)    #!JSON stringfy
        mqttc.publish("miprimertopic", paylodmsg , qos=1) #!topic al cual se enviaran los datos
        print("msg sent: miprimertopic",paylodmsg ) #!Print de mensaje enviado al topic
    else: 
        print("Connection lost")

#*loop_start()
#*loop_forever() and
#*loop().


# def run():
#     try:
#         contador = 0
        
#         while 1==1:
#             sleep(3)
#             mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  
#             mqttc.connect(awshost, awsport, keepalive=60)           
#             mqttc.loop_start()        

#             contador +=1
#             paylodmsg = {'id':"id_agente", 'model_type': 'model_type', 'data': json.dumps({"id":"mi mamame me mima","name":"Nelson",'contador':contador})}
#             paylodmsg = json.dumps(paylodmsg)    #!JSON stringfy
#             mqttc.publish("miprimertopic", paylodmsg , qos=1) #!topic al cual se enviaran los datos
#             print("msg sent: miprimertopic",paylodmsg ) #!Print de mensaje enviado al topic

#         else:
#             print ("Error enviar: No hay datos para enviar")
#     except ValueError as e:
#         print ("Error enviar data: " + str(e))
#     except gaierror as f:
#         print("Hemos perdido la conexion")
#         run()


# if __name__ == '__main__':
#     run()




