import asyncio
import websockets

from autopilot.pattern_kafka_autopilot import PatternKafkaAutopilot
from autopilot.kafka_autopilot import ShipPositionKafkaAutopilot


async def websocket_handler(autopilot_class, *args, verbose=False):
    uri = "ws://127.0.0.1:3012"
    async with websockets.connect(uri, ping_timeout=None) as websocket:
        print("Connecté au serveur WebSocket")

        if autopilot_class in (ShipPositionKafkaAutopilot, PatternKafkaAutopilot):
            autopilot = autopilot_class(websocket, verbose=verbose, kafka_bootstrap_servers=args[0])
        else:
            autopilot = autopilot_class(websocket, *args, verbose)

        await autopilot.run()
