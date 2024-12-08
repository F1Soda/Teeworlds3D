from uuid import UUID
import socket


class Observer:
    def __init__(self) -> None:
        self._id = -1
        self._writer = None
        self._reader = None

    def set_writer(self, writer):
        self._writer = writer

    def set_reader(self, reader):
        self._reader = reader

    # def connect(self, ip="localhost", port=9000):
    #     self._reader, self._writer = asyncio.open_connection(ip, port)
    #     return self._reader, self._writer

    @property
    def is_connected(self):
        return not (self._writer is None or self._reader is None)

    async def get_response(self):
        raw_response = await self._reader.read(255)
        return eval(raw_response.decode(), {"UUID": UUID})

    def get_id(self):
        return self._id

    def set_id(self, observer_id):
        self._id = observer_id

    async def send_to_server(self, state):
        if not self.is_connected:
            raise Exception("Trying to send message without connection to server!")
        state["source"] = self._id
        self._writer.write(self.prepare_data(state))
        await self._writer.drain()

    async def update(self, state, source=None):
        if not self.is_connected:
            raise Exception("Trying to send message without connection to server!")
        if source == str(self._id):
            return
        await self.send_to_server(state)

    def prepare_data(self, data):
        data["source"] = str(self._id)
        return str(data).encode()
