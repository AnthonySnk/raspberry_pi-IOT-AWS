# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl

def on_connect(client, userdata, flags, rc):                #!Funcion para realizar la conexion
    print("Connection returned result: " + str(rc) )
    #!Suscribirse a on_connect()  significa que si perdemos la conexion
    #!al reconectarse la subscription sera renovada
    client.subscribe("#" , 1 )                              #!suscrito a todos los topics

def on_message(client, userdata, msg):                      #!Funcion mensaje
    print("payload: "+str(msg.payload))

#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()                                       #!El objeto mqttc
mqttc.on_connect = on_connect                               #!Asigandole las funcion de coneccion
mqttc.on_message = on_message                               #!Asigandole la funcion on_message

awshost = "a22msdc6rv0ukb-ats.iot.us-east-1.amazonaws.com"  #!endPoint-api con la que podemos intereactuar con la sombra
awsport = 8883                                              #!Numero de puerto para amazon   
clientId = "my-agent-one"                                #!Nombre de la cosa
thingName = "my-agent-one"                               #!Nombre de la cosa
caPath = "./AmazonRootCA1.pem"                              #!Llave rain de amazon
certPath = "./certificate.pem.crt"                          #!Ubicacion del certificado de la cosa
keyPath = "./my-agent-one-private.pem.key"                  #!Llave privada de la cosay

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      

mqttc.connect(awshost, awsport, keepalive=60)               #!Conexion hacia el servidor con 1 minuto de socket

mqttc.loop_forever()                                        #!Iniciamos un loop de la conexion