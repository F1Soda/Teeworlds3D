import Scripts.Source.Multiplayer.networking as networking_m
import asyncio
from uuid import UUID


class Client:
    def __init__(self, gsm):
        self.gsm = gsm
        self.observer = networking_m.Observer()
        self.listen_task = None

    async def connect(self) -> bool:
        """Establish a connection and start listening for server updates."""
        try:
            # Establish connection
            print("Trying to connect to localhost:9000")
            await self.observer.connect()

            # Send handshake message
            message = {"action": "handshake"}
            await self.observer.send_to_server(message)

            # Receive response
            response = await self.observer.get_response()

            observer_id = response["observer_id"]
            print("\tConnected! Running game...")
            self.gsm.set_state("Game", response["level"])
            self.observer.set_id(observer_id)

            await self.set_spawn_position()

            # Start listening for server updates
            self.listen_task = asyncio.create_task(self.listen_for_updates())

            return True
        except Exception as e:
            print("Error while connecting!")
            print(e)
            await self.disconnect()  # Clean up connection on failure
            self.gsm.state.exit()
        return False

    async def listen_for_updates(self):
        """Continuously listen for updates from the server."""

        print("Listening for updates...")
        while True:
            try:
                await self.observer.send_to_server({"action": "echo"})
                message = await self.observer.get_response()
                print(message)
                if not message:
                    print("!Empty message from server!")
                    break
                # await self.handle_data_from_server(message)
            except asyncio.CancelledError:
                print(f"Listening task cancelled. but FUCK IT")
            except Exception as e:
                print(f"Error in listen_for_updates: {e}")
        await self.disconnect()

    async def handle_data_from_server(self, data):
        """Handle incoming data from the server."""
        try:
            print(f"Data received: {data}")
            # Example: Update game state based on server data
            action = data["action"]
            match action:
                case "spawn":
                    self.gsm.spawn_client(pos=data["pos"], id=data["source"])
                case "move":
                    self.gsm.state.move_client(pos=data["pos"], id=data["source"])
        except Exception as e:
            print("OOOps, occurred some error in handling server data:", e)

    async def send_action(self, action_data):
        """Send an action to the server (e.g., movement or shooting)."""
        print(f"Notifying server of action: {action_data}")
        await self.observer.update(action_data)

    async def set_spawn_position(self):
        message = {
            "action": "spawn",
        }
        await self.observer.send_to_server(message)
        response = await self.observer.get_response()
        spawn_point = response["pos"]

        self.gsm.state.spawn_player(spawn_point)

    async def disconnect(self):
        """Gracefully disconnect from the server and stop the background tasks."""
        if self.observer.is_connected:
            print("Disconnecting...")

            disconnect_message = {"action": "disconnect", "source": self.observer.get_id(),
                                  "reason": "Client requested disconnect"}
            await self.observer.send_to_server(disconnect_message)

            # Cancel the background check_msg task
            self.listen_task.cancel()
            try:
                # Await the task to ensure cancellation is complete
                await self.listen_task
            except asyncio.CancelledError:
                pass  # Task was cancelled, no need to handle the exception

        print("Disconnected.")
