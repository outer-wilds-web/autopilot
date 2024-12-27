import asyncio
import websockets
from autopilot.random_autopilot import RandomAutopilot
from autopilot.planet_autopilot import PlanetAutopilot

async def websocket_handler(autopilot_class, *args, verbose=0):
    uri = "ws://127.0.0.1:3012"
    async with websockets.connect(uri) as websocket:
        print("Connecté au serveur WebSocket")
        autopilot = autopilot_class(websocket, *args, verbose)
        await autopilot.run()