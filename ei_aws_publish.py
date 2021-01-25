
import paho.mqtt.client as paho
import os
import socket
import ssl
import random
import string
import json
from time import sleep
from random import uniform

#!declarondo una bandera del estado de la conexion
connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag        
    print ("Conectado a  AWS")
    connflag = True
    print("La conexion respondio con: " + str(rc) )
    mqttc.subscribe(SHADOW_UPDATE_ACCEPTED_TOPIC, 1)
    # mqttc.subscribe(SHADOW_UPDATE_REJECTED_TOPIC, 1)

def on_message(client, userdata, msg):   
    print(msg.topic+" "+str(msg.payload))
    
def get_random_string(length):
    #!Para generar una ramdom string para el almacenamiento de los evento
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Ramdom String del tamaño", length, "es:", result_str)
    return result_str
    
def getMAC(interface='eth0'):
    #!Retornaremos el mac addres de la interfase a la cual estemos conectado
    try:
        str = open('/sys/class/net/%s/address' %interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

def getEthName():
    #!Obtenmos el nombre de la interfase conectada
    try:
        for root,dirs,files in os.walk('/sys/class/net'):
            for dir in dirs:
                if dir[:3]=='enx' or dir[:3]=='eth':
                    interface=dir
    except:
        interface="Ninguna interafase conectada"
        return interface

mqttc = paho.Client()                                       #!El objeto mqttc
mqttc.on_connect = on_connect                               #!Asigandole las funcion de coneccion
mqttc.on_message = on_message                               #!Asigandole la funcion on_message

awshost = "a22msdc6rv0ukb-ats.iot.us-east-1.amazonaws.com"  #!endPoint-api con la que podemos intereactuar con la sombra
awsport = 8883                                              #!Numero de puerto para amazon   
clientId = "my-agent-one"                                #!Nombre de la cosa
thingName = "my-agent-one"                               #!Nombre de la cosa
caPath = "./AmazonRootCA1.pem"                              #!Llave rain de amazon
certPath = "./certificate.pem.crt"                          #!Ubicacion del certificado de la cosa
keyPath = "./my-agent-one-private.pem.key"                  #!Llave privada de la cosa

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None) #!Enviamos los parametros de las llaves

mqttc.connect(awshost, awsport, keepalive=60)               #!Conexion hacia el servidor con 1 minuto de socket
mqttc.loop_start()                                          #!Iniciamos un loop de la conexion

SHADOW_UPDATE_TOPIC = "$aws/things/" + thingName + "/shadow/update"
SHADOW_UPDATE_ACCEPTED_TOPIC = "$aws/things/" + thingName + "/shadow/update/accepted"
SHADOW_UPDATE_REJECTED_TOPIC = "$aws/things/" + thingName + "/shadow/update/rejected"
SHADOW_STATE_DOC_LED_ON = """{"state" : {"desired" : {"LED" : "ON"}}}"""
SHADOW_STATE_DOC_LED_OFF = """{"state" : {"desired" : {"LED" : "OFF"}}}"""
SHADOW_GET_STATE ="ShadowTopicPrefix/get"

while 1==1:
    sleep(5)
    contador = 0
    if connflag == True:
        contador +=1
        # ethName=getEthName()
        # ethMAC=getMAC(ethName)
        ethName='MAC-NAME'
        ethMAC='eth0'
        macIdStr = ethMAC
        # randomNumber = uniform(20.0,25.0)
        randomNumber=contador
        random_string= get_random_string(8)
        paylodmsg = {
            "mac_Id":ethMAC,
            "random_number":randomNumber,
            "random_string":random_string,
            "body":"Aqui podriamos enviar todo lo que necesites enviar"
        }
        paylodmsg = json.dumps(paylodmsg)    #!JSON stringfy
        mqttc.publish("miprimertopic", paylodmsg , qos=1) #!topic al cual se enviaran los datos
        print("msg sent: miprimertopic" ) #!Print de mensaje enviado al topic
        print(paylodmsg)
    if connflag== True:
        mqttc.publish(SHADOW_UPDATE_TOPIC,SHADOW_STATE_DOC_LED_ON,qos=1)
    else:
        print("Esperando una conexion...") 