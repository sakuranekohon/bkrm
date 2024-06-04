from mysocket import MySocket
import json

client = MySocket.Client()

data = {
    "getPrivate":False,
    "UID":"A123456",
    "fileNumber":99999999,
    "privateKey":"sdasaposdsa13245sad",
    "lockTime":"2024-05-30",
    "padd":False
}

client.sendTCPMeg(data,8080)