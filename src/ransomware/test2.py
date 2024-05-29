from mysocket import MySocket
import json

client = MySocket.Client()

data = {
    "UID":"sadn kljpojxcv",
    "fileNumber":99999999,
    "privateKey":"sdasaposdsa13245sad",
    "lockTime":"2024-05-30",
    "padding":True
}

client.sendTCPMeg(data,8080)