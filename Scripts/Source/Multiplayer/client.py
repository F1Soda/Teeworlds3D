import Scripts.Source.Multiplayer.networking as networking_m
import asyncio


class Client:
    def __init__(self, gsm):
        self.listen_port = 0
        self.server_writer = None
        self.gsm = gsm
        self.observer = networking_m.Observer()

    async def connect(self) -> bool:
        print("trying connect to localhost:9000")
        try:
            message = {"action": "handshake"}
            sender = networking_m.TCPSender()
            message = self.observer.prepare_data(message)
            print("\t Waiting response from server")
            response = await sender.send_data(message)
            self.listen_port = int(response["port"])
            self.observer.set_id(response["observer_id"])
            print("\t Run game!")
            self.gsm.set_state("Game", response["level"])

            await self.set_spawn_position()

            asyncio.create_task(self.check_msg(self.listen_port))

            #asyncio.run(self.check_msg(self.listen_port), debug=True)

            return True
        except Exception as e:
            print("Some error while connecting!")
            print(e)
            self.gsm.state.exit()
        return False

    async def set_spawn_position(self):
        message = self.observer.prepare_data({
            "action": "spawn",
        })
        response = await self.observer.send_to_server(message)
        print(f"Spawn player response: {response}")
        spawn_point = response["pos"]

        self.gsm.state.spawn_player(spawn_point)

    async def check_msg(self, port):
        """Listen for updates from the server."""
        print(f"Listening for updates on port {port}...")
        server = await asyncio.start_server(self.handle_data_from_server, "localhost", port)

        async with server:
            await server.serve_forever()

    async def handle_data_from_server(self, reader, writer):
        """Handle incoming data from the server."""
        print("Receiving data from server...")
        data = (await reader.read(255)).decode()
        print(f"Data received: {data}")

        # Example: Update game state based on server data
        update = eval(data)  # Use literal_eval if safety is a concern
        action = data["action"]
        match action:
            case "spawn":
                self.gsm.spawn_client(pos=data["pos"], id=data["source"])
            case "move":
                self.gsm.state.move_client(pos=data["pos"], id=data["source"])
        # self.gsm.state.update_game_state(update)  # Apply the update to the game state

        writer.close()
        await writer.wait_closed()

    async def send_action(self, action_data):
        """Send an action to the server (e.g., movement or shooting)."""
        print(f"Notifying server of action: {action_data}")
        await self.observer.update(action_data)
