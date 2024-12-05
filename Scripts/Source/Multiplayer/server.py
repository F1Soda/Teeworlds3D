import Scripts.Source.Multiplayer.observer_controller as observer_controller_m
import asyncio, ast, networking
import uuid


class Server:
    def __init__(self, level_path):
        self.next_client_port = 9001
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
        print("Server running...")
        async with game_server:
            await game_server.serve_forever()

    async def handle_client(self, reader, writer):
        """Handle an incoming client connection."""
        try:
            data = (await reader.read(255)).decode()
            print(f"Attempting to decode data: {data}")
            data = ast.literal_eval(data)
            action = data["action"]
            print(f"Action received: {action}")
            source = data["source"]
            print(f"Source: {source}")

            response = {"status": "good"}
            match action:
                case "handshake":
                    address = "localhost"
                    print(f"Address for client: {address}")
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
            print(f"Sending back response: {response}")
            writer.write(str(response).encode())
            await writer.drain()
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print("Client connection closed.")

    async def notify_shutdown(self):
        """Notify all observers (clients) about the server shutdown."""
        shutdown_message = {"action": "disconnect", "reason": "Server shutting down"}
        await self.observer_controller.notify_observers(shutdown_message, source=None)
        print("All clients notified about shutdown.")

    def add_client(self, observer_id, address):
        observer = self.observer_controller.add_observer(
            networking.Observer(port=self.get_next_client_port(), host=address)
        )
        observer.set_id(observer_id)
        print(f"Client added: {observer_id}")

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
        return {"pos": (5, 1, 5)}

    def get_move_response(self, data):
        return {"pos": data["pos"]}

    @staticmethod
    def get_new_id_for_observer():
        return uuid.uuid1()


if __name__ == '__main__':
    server = Server("Levels/Player/TestCollision.json")
