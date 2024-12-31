import asyncio
import websockets

from autopilot.kafka_autopilot import ShipPositionKafkaAutopilot


async def websocket_handler(autopilot_class, kafka_server, websocket_url, verbose=False, name="default"):
    print(f"Connecting to WebSocket at {websocket_url}...")

    try:
        async with websockets.connect(websocket_url) as websocket:
            print("WebSocket connection established.")
            autopilot = autopilot_class(
                websocket, verbose=verbose, kafka_bootstrap_servers=kafka_server, name=name)
            await autopilot.run()
    except Exception as e:
        print(f"WebSocket connection failed: {e}")
