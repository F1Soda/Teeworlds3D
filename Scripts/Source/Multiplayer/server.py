import sys, os
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import Scripts.Source.Multiplayer.network as network_m
import uuid, ast
import datetime
import socket
from _thread import *
from uuid import UUID

Network = network_m.Network

client_lock = threading.Lock()


class Server:
    def __init__(self, level_path):
        self.config = {"level": level_path}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.run_server()

    def add_client(self, guid, pos):
        self.clients[guid] = {"pos": pos, "actions": []}

    def run_server(self):
        host, port = "localhost", 9000

        print(f"Server listening on {host}:{port}")

        try:
            self.server_socket.bind((host, port))
        except socket.error as e:
            str(e)

        self.server_socket.listen(4)

        while True:
            conn, addr = self.server_socket.accept()
            print("Connected to:", addr)

            guid_client = str(self.get_new_id_for_observer())

            response = Network.parse_data(conn.recv(2048))
            print(response)
            if response.get("action") == "handshake":
                reply = {"status": "good"}
                reply = self.get_handshake_config(reply)
                reply["observer_id"] = guid_client
                conn.send(str(reply).encode())

                self.add_client(guid_client, (0, 0, 0))

                start_new_thread(self.threaded_client, (conn, guid_client,))

    def threaded_client(self, conn, guid):
        while True:
            try:
                raw_response, _ = conn.recvfrom(1024)
                response = eval(raw_response, {"UUID": UUID})

                # print("Received: ", response)

                reply = {"status": "good"}

                if response.get("action"):
                    reply = self.make_response(response, reply)

                state = {}
                with client_lock:
                    for client, client_data in self.clients.items():
                        state[client] = client_data["pos"]
                    reply["actions"] = self.clients[guid]["actions"]

                reply["state"] = state
                reply["source"] = str(response["source"])

                # print("send back:", reply)

                conn.sendall(str(reply).encode())

            except Exception as e:
                print(e)
                raise

        print("Lost connection")
        del self.clients[guid]
        conn.close()

    def notify_clients_with_action(self, source, action):
        for client_guid in self.clients.keys():
            if client_guid != source:
                self.clients[client_guid]["actions"].append(action)

    def make_response(self, data, reply):
        action = data["action"]
        source = data["source"]
        Server.log(f"Received data: {data}", level=1)

        match action:
            case "handshake":
                reply = self.get_handshake_config(reply)
            case "spawn":
                reply = self.get_spawn_pos_response(reply)
                self.clients[source]["pos"] = reply["spawn_pos"]
                with client_lock:
                    self.notify_clients_with_action(source, reply)
            case "update":
                reply["action"] = "update"
                self.clients[source]["pos"] = data["pos"]
            case "echo":
                reply["action"] = "echo"

        return reply

    def get_handshake_config(self, reply):
        reply["action"] = "handshake"
        reply["level"] = self.config["level"]
        return reply
        # reply["action"] = self.get_new_id_for_observer()

    def get_spawn_pos_response(self, reply):
        reply["action"] = "spawn"
        reply["spawn_pos"] = (5, 10, 0)
        return reply

    # def get_move_response(self, data):
    #     return {"action": "move", "pos": data["pos"]}

    def get_game_state_response(self):
        return self.clients

    @staticmethod
    def get_new_id_for_observer():
        return uuid.uuid1()

    @staticmethod
    def log(message, level=0):
        # Get the current time in the format HH:MM:SS
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        # Print the log message with the current time
        print(f"[{current_time}]{"\t" * level} {message}")


if __name__ == '__main__':
    server = Server("Levels/Player/TestCollision.json")
