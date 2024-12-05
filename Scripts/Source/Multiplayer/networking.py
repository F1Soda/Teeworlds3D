import ast, asyncio
from uuid import UUID

class Observer:
    def __init__(self, sender=None, port=9000, host="localhost") -> None:
        # if observer_id is None:
        #     observer_id = uuid.uuid1()
        self._id = -1
        if sender is None:
            sender = TCPSender(port, host)
        self._sender = sender

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
    def __init__(self, port=9000, host="localhost") -> None:
        self.host = host
        self.port = port

    def set_port(self, port):
        self.port = port

    async def send_data(self, data: dict):
        print("TCPSender:")
        reader, writer = await asyncio.open_connection(self.host, self.port)

        print("Sending data!")
        writer.write(str(data).encode())
        await writer.drain()

        received = await reader.read(255)
        received = received.decode()
        print(f'Received: {received}')

        print('Close the connection')
        writer.close()
        await writer.wait_closed()
        if received is not None and received != '':
            return eval(received, {"UUID": UUID})
