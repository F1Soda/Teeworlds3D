import asyncio
from uuid import UUID


class Observer:
    def __init__(self, sender=None, port=9000, host="localhost") -> None:
        self._id = -1
        if sender is None:
            sender = TCPSender(port, host)
        self._sender = sender

    def get_id(self):
        return self._id

    def set_id(self, observer_id):
        self._id = observer_id

    def set_sender(self, sender):
        self._sender = sender

    async def send_to_server(self, state):
        state["source"] = self._id
        return await self._sender.send_data(self.prepare_data(state))

    async def update(self, state, source=None):
        if source == str(self._id):
            return
        await self.send_to_server(state)

    def prepare_data(self, data):
        data["source"] = str(self._id)
        return data


class TCPSender:
    def __init__(self, port=9000, host="localhost"):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        """Establish the connection if not already connected."""
        if self.writer is None:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def send_data(self, data: dict):
        """Send data to the server."""
        await self.connect()  # Ensure connection is established
        self.writer.write(str(data).encode())
        await self.writer.drain()

        received = await self.reader.read(255)
        return eval(received.decode(), {"UUID": UUID})

    async def close_connection(self):
        """Close the connection gracefully."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.reader = None
            self.writer = None
