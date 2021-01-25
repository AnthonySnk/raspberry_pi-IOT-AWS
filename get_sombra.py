
import requests, datetime, sys,json
from aws_sig_ver_4 import get_HTTP_Request_Header


ACCESS_KEY = "acces-key" 
SECRET_KEY = "secret-key"
IOT_ENDPOINT = "endpo.amazonaws.com" 
AWS_REGION = "us-east-1"
HTTPS_ENDPOINT_URL = "https://endpo.amazonaws.com" 
IoT_THING_NAME = "my-agent-one"
# HTTPS_METHOD ="GET"
SHADOW_URI = "/things/" + IoT_THING_NAME + "/shadow" 
Request_Url = HTTPS_ENDPOINT_URL + SHADOW_URI
http_request_payload = ""

def handler_shadow(HTTPS_METHOD):
    Request_Headers = get_HTTP_Request_Header(HTTPS_METHOD, IOT_ENDPOINT, AWS_REGION, SHADOW_URI, ACCESS_KEY, SECRET_KEY, http_request_payload)
    HTTP_RESPONSE = requests.request(HTTPS_METHOD, Request_Url, data=http_request_payload ,headers=Request_Headers)
    print ("\nHTTP Response Code:" + str(HTTP_RESPONSE.status_code))
    # print ("Response:" , HTTP_RESPONSE.text)
    
    status  = json.loads(HTTP_RESPONSE.text)
    print("El estado es:" , status["state"]["desired"]["LED"])
    return  status["state"]["desired"]["LED"]

