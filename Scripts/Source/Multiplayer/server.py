import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import Scripts.Source.Multiplayer.observer_controller as observer_controller_m
import asyncio, ast, networking
import uuid
import datetime


class Server:
    def __init__(self, level_path):
        self.next_client_port = 9000
        self.config = {"level": level_path}
        self.observer_controller = observer_controller_m.ObserverController()
        self.shutdown_event = asyncio.Event()

        try:
            asyncio.run(self.run_server(), debug=True)
        except KeyboardInterrupt:
            print("Shutting down server...")
            asyncio.run(self.notify_shutdown(), debug=True)

    async def run_server(self):
        HOST, PORT = "localhost", 9000
        game_server = await asyncio.start_server(self.handle_client, HOST, PORT)
        Server.log(f"Server running on : {HOST}:{PORT}")
        async with game_server:
            await game_server.serve_forever()

    async def handle_client(self, reader, writer):
        """Handle an incoming client connection."""
        try:
            while not reader.at_eof():
                data = (await reader.read(255)).decode()
                if data == "":
                    continue
                data = ast.literal_eval(data)
                action = data["action"]
                source = data["source"]
                Server.log(f"Received data: {data}", level=1)

                response = {"status": "good"}
                match action:
                    case "handshake":
                        address = "localhost"
                        response = self.get_handshake_config()
                        self.add_client(response["observer_id"], address)
                    case "spawn":
                        response = self.get_spawn_pos_response()
                        await self.observer_controller.notify_observers(response, data["source"])
                    case "move":
                        response = self.get_move_response(data)
                        await self.observer_controller.notify_observers(response, data["source"])
                    case "echo":
                        response["data"] = data
                    case "disconnect":
                        observer_id = data["source"]
                        self.remove_client(observer_id)
                        disconnect_message = {"action": "disconnect", "observer_id": observer_id,
                                              "reason": "Client disconnected"}
                        await self.observer_controller.notify_observers(disconnect_message, source=observer_id)
                        break

                Server.log(f"Sending response: {response}", level=1)
                writer.write(str(response).encode())
                await writer.drain()
        except Exception as e:
            Server.log(f"Error handling client: {e}")

    async def notify_shutdown(self):
        """Notify all observers (clients) about the server shutdown."""
        shutdown_message = {"action": "disconnect", "reason": "Server shutting down"}
        await self.observer_controller.notify_observers(shutdown_message, source=None)
        print("All clients notified about shutdown.")

    def remove_client(self, observer_id):
        """Remove a client (observer) from the list of connected clients."""
        # This method should remove the observer from the observer_controller
        self.observer_controller.remove_observer(observer_id)
        Server.log(f"Client {observer_id} removed.", level=1)

    def add_client(self, observer_id, address):
        observer = networking.Observer(port=self.get_next_client_port(), host=address)
        observer.set_id(observer_id)
        self.observer_controller.add_observer(observer_id, observer)

        Server.log(f"Client added: {observer_id}", level=1)

    def get_next_client_port(self):
        self.next_client_port += 1
        return self.next_client_port

    def get_handshake_config(self):
        config = {"action": "handshake",
                  "port": self.next_client_port,
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
