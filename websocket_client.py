import asyncio
import websockets

from autopilot.kafka_autopilot import ShipPositionKafkaAutopilot


async def websocket_handler(autopilot_class, *args, verbose=False, name):
    uri = "ws://127.0.0.1:3012"
    async with websockets.connect(uri, ping_timeout=None) as websocket:
        print("Connecté au serveur WebSocket")

        if autopilot_class is ShipPositionKafkaAutopilot:
            autopilot = autopilot_class(
                websocket, verbose=verbose, kafka_bootstrap_servers=args[0], name=name)
        else:
            autopilot = autopilot_class(websocket, *args, verbose, name=name)

        await autopilot.run()
