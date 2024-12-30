import asyncio
import websockets
from autopilot.random_autopilot import RandomAutopilot
from autopilot.planet_autopilot import PlanetAutopilot
from autopilot.kafka_autopilot import ShipPositionKafkaAutopilot  # Nouveau import


async def websocket_handler(autopilot_class, *args, verbose=False):
    uri = "ws://127.0.0.1:3012"
    async with websockets.connect(uri, ping_timeout=None) as websocket:
        print("Connecté au serveur WebSocket")

        if autopilot_class == ShipPositionKafkaAutopilot:
            autopilot = autopilot_class(websocket, verbose=verbose, kafka_bootstrap_servers=args[0])
        else:
            autopilot = autopilot_class(websocket, *args, verbose)

        await autopilot.run()
