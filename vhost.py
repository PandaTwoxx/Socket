import asyncio


class vhost:
    def __init__(self, port=8485):
        self.port = port
        self.data = ""
        self.server = None  # Store the server object for cleanup

    async def host(self):
        server = await asyncio.start_server(self.handle_client, "0.0.0.0", self.port)
        self.server = server
        print(f"Listening on port {self.port}")
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        while True:
            data = await reader.read(1024)  # Read data in chunks
            if not data:
                break
            writer.write(self.data.encode())  # Send current data
            await writer.drain()  # Ensure data is sent

    def update(self, new_data):
        self.data = new_data

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None
            print("Server stopped")

    