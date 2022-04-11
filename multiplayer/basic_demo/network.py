import socket
import pickle  # serialization / deserialization module

"""
The client connection bridge
connects the client to the server
sends and receives data from and to the client, similar to OkHTTP or retrofit in android app
"""


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = "127.0.0.1"  # ip of server
        self.port = 5555  # port number
        self.addr = (self.ip, self.port)
        self.dataObj = self.connect()

    def getDataObj(self):
        return self.dataObj

    def connect(self):
        try:
            self.client.connect(self.addr)  # establish socket connection to server
            return pickle.loads(self.client.recv(2048))  # receive and deserialize a data object from server
            # representing player

            # if you are receiving simple text (encoded) you can use:
            # self.client.recv(2048).decode()
        except:
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))  # encode and send a data object to server

            # if you are sending simple text you can use:
            # self.client.send(str.encode(data))

            return pickle.loads((self.client.recv(2048)))  # receive and deserialize a data object from server response
        except socket.error as e:
            print(e)
