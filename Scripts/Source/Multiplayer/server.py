import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import Scripts.Source.Multiplayer.observer_controller as observer_controller_m
import networking
import uuid, ast
import datetime
import socket


class Server:
    def __init__(self, level_path):
        self.config = {"level": level_path}
        self.observer_controller = observer_controller_m.ObserverController()
        self.run_server()

    def run_server(self):
        HOST, PORT = "localhost", 9000
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            try:
                # Receive data from a client (maximum 1024 bytes)
                data, client_address = server_socket.recvfrom(1024)
                print(f"Received from {client_address}: {data.decode()}")

                data = ast.literal_eval(data.decode())
                action = data["action"]
                source = data["source"]
                Server.log(f"Received data: {data}", level=1)

                # Send a response back to the client
                response = {"status": "good"}
                match action:
                    case "handshake":
                        response = self.get_handshake_config()
                        # self.add_client(response["observer_id"], reader, writer)
                    case "spawn":
                        response = self.get_spawn_pos_response()
                        # self.observer_controller.notify_observers(response, data["source"])
                    case "move":
                        response = self.get_move_response(data)
                        # self.observer_controller.notify_observers(response, data["source"])
                    case "echo":
                        response["action"] = "echo"
                server_socket.sendto(str(response).encode(), client_address)
                print(f"Sent to {client_address}: {response}")

            except KeyboardInterrupt:
                print("Server shutting down.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

        # Close the socket
        server_socket.close()

    # def handle_client(self, reader, writer):
    #     """Handle an incoming client connection."""
    #     try:
    #         while not reader.at_eof():
    #             data = (reader.read(255)).decode()
    #             data = ast.literal_eval(data)
    #             action = data["action"]
    #             source = data["source"]
    #             Server.log(f"Received data: {data}", level=1)
    #
    #             response = {"status": "good"}
    #             match action:
    #                 case "handshake":
    #                     response = self.get_handshake_config()
    #                     self.add_client(response["observer_id"], reader, writer)
    #                 case "spawn":
    #                     response = self.get_spawn_pos_response()
    #                     self.observer_controller.notify_observers(response, data["source"])
    #                 case "move":
    #                     response = self.get_move_response(data)
    #                     awa self.observer_controller.notify_observers(response, data["source"])
    #                 case "echo":
    #                     response["action"] = "echo"
    #                     response["time"] = datetime.datetime.now()
    #                 case "disconnect":
    #                     observer_id = data["source"]
    #                     self.remove_client(observer_id)
    #                     disconnect_message = {"action": "disconnect", "observer_id": observer_id,
    #                                           "reason": "Client disconnected"}
    #                     await self.observer_controller.notify_observers(disconnect_message, source=observer_id)
    #                     break
    #
    #             Server.log(f"Sending response: {response}", level=1)
    #             writer.write(str(response).encode())
    #             await writer.drain()
    #     except Exception as e:
    #         Server.log(f"Error handling client: {e}")

    # def notify_shutdown(self):
    #     """Notify all observers (clients) about the server shutdown."""
    #     shutdown_message = {"action": "disconnect", "reason": "Server shutting down"}
    #     awai self.observer_controller.notify_observers(shutdown_message, source=None)
    #     print("All clients notified about shutdown.")
    #
    # def remove_client(self, observer_id):
    #     """Remove a client (observer) from the list of connected clients."""
    #     # This method should remove the observer from the observer_controller
    #     self.observer_controller.remove_observer(observer_id)
    #     Server.log(f"Client {observer_id} removed.", level=1)

    # def add_client(self, observer_id, reader, writer):
    #     observer = networking.Observer()
    #
    #     observer.set_reader(reader)
    #     observer.set_writer(writer)
    #     observer.set_id(observer_id)
    #
    #     self.observer_controller.add_observer(observer_id, observer)
    #
    #     Server.log(f"Client added: {observer_id}", level=1)
    #
    def get_handshake_config(self):
        config = {"action": "handshake",
                  "level": self.config["level"],
                  "observer_id": self.get_new_id_for_observer()}
        return config

    def get_spawn_pos_response(self):
        return {"action": "spawn", "pos": (0, 5, 0)}

    def get_move_response(self, data):
        return {"action": "move", "pos": data["pos"]}

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
