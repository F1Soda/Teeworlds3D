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

MAX_COUNT = 4


class Server:
    def __init__(self, level_path):
        self.config = {"level": level_path,
                       "max_count": MAX_COUNT,
                       "count_players": 0,
                       "mode": "Deathmatch",
                       "name": "room_0"
                       }
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_state = {}
        # В clients actions хранится действия, которые должен сделать клиент для синхронизации игры
        # Пример: если client_actions не пусто, то в моменте принятия нового состояния от клиента, ему в ответ придёт
        # текущее состояние игры и затем запрос на исполнение его client_actions. Например какой то клиент заспавнился и
        # в этот момент он рассылает всем уведомления о том, что другие клиенты должны отобразить его спавн.
        # Для этого он в client_actions записывает каждому другому клиенту это действие.
        # Когда другой клиент это выполнит, он отправит запрос на то, что это действие было выполнено и сервер
        # уберёт именно это действие из его список акшинов.
        self.client_actions = {}
        self.run_server()

    def add_client(self, guid, pos):
        self.game_state[guid] = {"pos": pos}
        self.config["count_players"] += 1
        self.client_actions[guid] = {}

    def run_server(self):
        host, port = "localhost", 9000

        print(f"Server listening on {host}:{port}")

        try:
            self.server_socket.bind((host, port))
        except socket.error as e:
            str(e)

        self.server_socket.listen(MAX_COUNT)

        count_threads = 0

        while True:
            conn, addr = self.server_socket.accept()
            print("Connected to:", addr)

            guid_client = str(self.get_new_id_for_observer())

            response = Network.parse_data(conn.recv(2048))

            if response.get("action") == "handshake":
                reply = {"actions": {}}
                reply = self.get_handshake_config(reply)
                reply["observer_id"] = guid_client
                conn.send(str(reply).encode())

                print(reply)

                self.add_client(guid_client, (0, 0, 0))
                count_threads += 1
                start_new_thread(self.threaded_client, (conn, guid_client, count_threads,))

    def threaded_client(self, conn, guid, count_thread):
        successfully_disconnect = False

        while True:
            try:
                raw_response, _ = conn.recvfrom(1024)
                # Server.log(f"{count_thread}: Received data: {raw_response}", level=1)
                response = eval(raw_response, {"UUID": UUID})

                # print("Received: ", response)

                reply = {}
                reply = self.make_response(response, reply)

                if reply.get("disconnect"):
                    successfully_disconnect = True
                    break

                player_data = response.get("player_data")
                if player_data:
                    self.game_state[guid] = player_data

                with client_lock:
                    for client_action_id in self.client_actions[guid].keys():
                        action = self.client_actions[guid][client_action_id]["action"]
                        action_data = self.client_actions[guid][client_action_id]["action_data"]
                        reply["actions"][action] = action_data

                reply["game_state"] = self.game_state
                reply["source"] = str(response["source"])

                conn.sendall(str(reply).encode())
            except SyntaxError as e:
                print(e)
                break
            except Exception as e:
                raise

        if not successfully_disconnect:
            with client_lock:
                self.disconnect_client(guid)
            print(f"Lost connection with {guid}")
        conn.close()

    def make_response(self, data, reply):
        source = data["source"]

        reply["actions"] = {}

        for action in data["actions"].keys():
            match action:
                case "handshake":
                    reply = self.get_handshake_config(reply)
                case "spawn":
                    reply = self.get_spawn_pos_response(reply)
                    self.game_state[source]["pos"] = reply["actions"]["spawn"]["spawn_pos"]
                    self.game_state[source]["rot"] = (0, 0, 0)

                    key = "spawn_client"
                    key_value = {
                        "spawn_pos": self.game_state[source]["pos"],
                        "source": source,
                        "id_action": str(uuid.uuid1())
                    }

                    with client_lock:
                        self.notify_clients_with_action(source, key, key_value)
                case "synced":
                    with client_lock:
                        for synced_id in data["actions"][action]:
                            del self.client_actions[source][synced_id]
                case "echo":
                    reply["action"] = "echo"
                case "disconnect":
                    with client_lock:
                        self.disconnect_client(source)
                    reply = {"disconnect": True}

        return reply

    def notify_clients_with_action(self, source, action, action_data):
        for client_guid in self.client_actions.keys():
            if client_guid != source:
                self.client_actions[client_guid][action_data["id_action"]] = {
                    "action": action,
                    "action_data": action_data
                }

    def get_handshake_config(self, reply):
        reply["actions"]["handshake"] = self.config
        return reply

    def disconnect_client(self, guid):
        for client_guid in self.client_actions.keys():
            if client_guid != guid:
                actions_to_drop = []
                for action_id, action in self.client_actions[client_guid].items():
                    if action["action_data"]["source"] == guid:
                        actions_to_drop.append(action_id)

                for action_id in actions_to_drop:
                    del self.client_actions[client_guid][action_id]

                key = "disconnect_client"
                key_value = {
                    "source": guid,
                    "id_action": str(uuid.uuid1())
                }

                self.client_actions[client_guid][key_value["id_action"]] = {
                    "action": key,
                    "action_data": key_value
                }
        self.config["count_players"] -= 1
        del self.client_actions[guid]
        del self.game_state[guid]

    def get_spawn_pos_response(self, reply):
        reply["actions"]["spawn"] = {
            "spawn_pos": (5, 10, 0),
            "rot": (0, 0, 0)
        }
        return reply

    def get_game_state_response(self):
        return self.game_state

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
