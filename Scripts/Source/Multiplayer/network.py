from uuid import UUID
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.sessions = []
        self.port = 9000
        self.addr = (self.server, self.port)
        self.id = -1

    def connect(self):
        try:
            self.client.connect(self.addr)

            message = {"action": "handshake"}
            response = self.send(message)
            print(f"Server response: {response}")
            self.sessions = [response["actions"]["handshake"]]
            observer_id = response["observer_id"]
            print("\tConnected!")
            self.id = observer_id
        except:
            pass

    def disconnect(self):
        message = {"actions": {"disconnect": {"reason": "Player leave the game"}}}
        try:
            response = self.prepare_data(message)
            self.client.send(response)
        except socket.error as e:
            pass
        self.client.close()
        self.id = -1
        self.sessions = []

    def send(self, data):
        try:
            response = self.prepare_data(data)
            self.client.send(response)
            return self.parse_data(self.client.recv(2048))
        except socket.error as e:
            print(e)
            raise

    def prepare_data(self, data):
        data["source"] = str(self.id)
        return str(data).encode()

    @staticmethod
    def parse_data(data):
        return eval(data.decode(), {"UUID": UUID})
