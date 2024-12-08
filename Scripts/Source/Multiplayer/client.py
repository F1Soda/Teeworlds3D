import Scripts.Source.Multiplayer.networking as networking_m
import asyncio
from uuid import UUID


class Client:
    def __init__(self, gsm):
        self.listen_port = 0
        self.gsm = gsm
        self.sender = networking_m.TCPSender()
        self.observer = networking_m.Observer(sender=self.sender)
        self.check_msg_task = None

    async def connect(self) -> bool:
        """Connect to the server."""
        if self.sender.writer:
            raise Exception("Attempt connect to server, but connection already exist")
        try:
            # print("Trying to connect to localhost:9000")
            # await self.sender.connect()

            message = {"action": "handshake"}
            message = self.observer.prepare_data(message)

            print("\tWaiting for response from server")
            response = await self.sender.send_data(message)

            self.listen_port = int(response["port"])
            self.observer.set_id(response["observer_id"])

            print("\tConnected! Running game...")

            self.gsm.set_state("Game", response["level"])
            await self.set_spawn_position()

            self.check_msg_task = asyncio.create_task(self.check_msg(self.listen_port))
            return True
        except Exception as e:
            print("Error while connecting!")
            print(e)
            await self.sender.close_connection()  # Clean up connection on failure
            self.gsm.state.exit()
        return False

    async def set_spawn_position(self):
        message = self.observer.prepare_data({
            "action": "spawn",
        })
        response = await self.observer.send_to_server(message)
        # print(f"Spawn player response: {response}")
        spawn_point = response["pos"]

        self.gsm.state.spawn_player(spawn_point)

    async def check_msg(self, port):
        """Listen for updates from the server."""
        print(f"Listening for updates on port {port}...")
        try:
            # loop = asyncio.get_event_loop()
            # server = await loop.create_server(self.handle_data_from_server, "localhost", port)

            server = await asyncio.start_server(self.handle_data_from_server, "localhost", port)

            async with server:
                await server.serve_forever()
            pass
        except asyncio.CancelledError:
            print("Check message task cancelled.")
        except Exception as e:
            print(f"Error in check_msg: {e}")

    async def handle_data_from_server(self, reader, writer):
        """Handle incoming data from the server."""
        try:
            print("Receiving data from server...")
            data = (await reader.read(255)).decode()
            print(f"Data received: {data}")

            # Example: Update game state based on server data
            update = eval(data, {"UUID": UUID})
            action = update["action"]
            match action:
                case "spawn":
                    self.gsm.spawn_client(pos=data["pos"], id=data["source"])
                case "move":
                    self.gsm.state.move_client(pos=data["pos"], id=data["source"])
            # self.gsm.state.update_game_state(update)  # Apply the update to the game state
        except Exception as e:
            print("OOOps, occurred some error in handling server data:", e)

    async def send_action(self, action_data):
        """Send an action to the server (e.g., movement or shooting)."""
        print(f"Notifying server of action: {action_data}")
        await self.observer.update(action_data)

    async def disconnect(self):
        """Gracefully disconnect from the server and stop the background tasks."""
        if self.check_msg_task:
            print("Disconnecting...")

            disconnect_message = {"action": "disconnect", "source": self.observer.get_id(),
                                  "reason": "Client requested disconnect"}
            await self.observer.send_to_server(disconnect_message)

            # Cancel the background check_msg task
            self.check_msg_task.cancel()
            try:
                # Await the task to ensure cancellation is complete
                await self.check_msg_task
            except asyncio.CancelledError:
                pass  # Task was cancelled, no need to handle the exception

        print("Disconnected.")
