import socket


class MySocket:
    class Server:
        def __init__(self,host="0.0.0.0",port=8080):
            self.host = host
            self.port = port
            self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    class Client:
        pass