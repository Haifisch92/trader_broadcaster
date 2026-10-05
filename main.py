import asyncio
import websockets

connected_clients = set()

async def handler(websocket):
    # Register client
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")
    try:
        await websocket.send("ping")
        async for message in websocket:
            print(f"Received message: {message}")
            await broadcast(message)
    except websockets.ConnectionClosed as e:
        print(e)
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def broadcast(message):
    if connected_clients:  # Check if there are any connected clients
        tasks = [asyncio.create_task(client.send(message)) for client in connected_clients]
        await asyncio.gather(*tasks)
        print(f"Broadcasted message: {message}")

async def main():
    address = "0.0.0.0"
    port = 7681

    async with websockets.serve(handler, address, port, ping_interval=None, ping_timeout=5):
        print(f"WebSocket server started on ws://{address}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
