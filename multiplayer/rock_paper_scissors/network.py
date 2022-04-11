import socket
import pickle  # serialization / deserialization module


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initialize socket client
        self.ip = "127.0.0.1"
        self.port = 5555
        self.addr = (self.ip, self.port)
        self.dataObj = self.connect()

    def getDataObj(self):
        return self.dataObj

    def connect(self):
        """
          establishes socket connection to the defined address
          and receives encoded string, which is then decoded and returned

          """
        try:
            self.client.connect(self.addr)
            received_text = self.client.recv(2048).decode()
            return received_text
        except:
            pass

    def send(self, data):
        """
          sends string and returns the received data object for other player
          """
        try:
            self.client.send(str.encode(data))
            received_update = pickle.loads((self.client.recv(2048)))
            return received_update
        except socket.error as e:
            print(e)
