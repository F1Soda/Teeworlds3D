import Scripts.Source.Multiplayer.networking as networking_m
import socket
from uuid import UUID


class Client:
    def __init__(self, gsm):
        self.gsm = gsm
        self.observer = networking_m.Observer()
        self.listen_task = None
        self.sessions = []
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connected = False

    def udp_client(self):
        try:
            while True:
                # Send the message to the server
                # self.client_socket.sendto(self.message.encode(), ("localhost", 9000))

                # Receive a response from the server
                raw_response, _ = self.client_socket.recvfrom(1024)
                print(f"Server response: {raw_response.decode()}")
                response = eval(raw_response.decode(), {"UUID": UUID})
                action = response["action"]
                match action:
                    case "spawn":
                        self.gsm.spawn_client(pos=response["pos"], id=response["source"])
                    case "move":
                        self.gsm.state.move_client(pos=response["pos"], id=response["source"])

        finally:
            # Close the socket
            self.client_socket.close()

    def connect(self) -> bool:
        message = {"action": "handshake"}
        self.client_socket.sendto(self.observer.prepare_data(message), ("localhost", 9000))
        raw_response, _ = self.client_socket.recvfrom(1024)
        print(f"Server response: {raw_response.decode()}")
        response = eval(raw_response.decode(), {"UUID": UUID})

        observer_id = response["observer_id"]
        print("\tConnected!")
        self.sessions.append(response["level"])
        self.observer.set_id(observer_id)


        self.connected = True
        return True

    def ask_server_spawn(self):
        message = {
                "action": "spawn",
            }
        self.client_socket.sendto(self.observer.prepare_data(message), ("localhost", 9000))

        # raw_response, _ = self.client_socket.recvfrom(1024)
        # print(f"Server response: {raw_response.decode()}")
        # response = eval(raw_response.decode(), {"UUID": UUID})
        #
        # return response["pos"]

    # async def connect(self) -> bool:
    #     """Establish a connection and start listening for server updates."""
    #     try:
    #         # Establish connection
    #         print("Trying to connect to localhost:9000")
    #         await self.observer.connect()
    #
    #         # Send handshake message
    #         message = {"action": "handshake"}
    #         await self.observer.send_to_server(message)
    #
    #         # Receive response
    #         response = await self.observer.get_response()
    #
    #         observer_id = response["observer_id"]
    #         print("\tConnected!")
    #         self.sessions.append(response["level"])
    #         self.observer.set_id(observer_id)
    #
    #     except Exception as e:
    #         print("Error while connecting!")
    #         print(e)
    #     return False
    #
    # async def handle_data_from_server(self):
    #     """Handle incoming data from the server."""
    #     try:
    #         message = await self.observer.get_response()
    #         print(f"Data received: {message}")
    #         # Example: Update game state based on server data
    #         action = message["action"]
    #         # match action:
    #         #     case "spawn":
    #         #         self.gsm.spawn_client(pos=data["pos"], id=data["source"])
    #         #     case "move":
    #         #         self.gsm.state.move_client(pos=data["pos"], id=data["source"])
    #     except Exception as e:
    #         print("OOOps, occurred some error in handling server data:", e)
    #
    # async def send_action(self, action_data):
    #     """Send an action to the server (e.g., movement or shooting)."""
    #     print(f"Notifying server of action: {action_data}")
    #     await self.observer.update(action_data)
    #
    # async def set_spawn_position(self):
    #     message = {
    #         "action": "spawn",
    #     }
    #     await self.observer.send_to_server(message)
    #     response = await self.observer.get_response()
    #     spawn_point = response["pos"]
    #
    #     self.gsm.state.spawn_player(spawn_point)
    #
    # async def disconnect(self):
    #     """Gracefully disconnect from the server and stop the background tasks."""
    #     if self.observer.is_connected:
    #         print("Disconnecting...")
    #
    #         disconnect_message = {"action": "disconnect", "source": self.observer.get_id(),
    #                               "reason": "Client requested disconnect"}
    #         await self.observer.send_to_server(disconnect_message)
    #
    #         # Cancel the background check_msg task
    #         self.listen_task.cancel()
    #         try:
    #             # Await the task to ensure cancellation is complete
    #             await self.listen_task
    #         except asyncio.CancelledError:
    #             pass  # Task was cancelled, no need to handle the exception
    #
    #     print("Disconnected.")
