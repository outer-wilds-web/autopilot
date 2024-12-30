import random
import asyncio
import json
from aiokafka import AIOKafkaProducer
from datetime import datetime
from .base_autopilot import AutopilotBase


class ShipPositionKafkaAutopilot(AutopilotBase):
    def __init__(self, websocket, verbose=False, kafka_bootstrap_servers='localhost:9092'):
        super().__init__(websocket, verbose)
        self.producer = None
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic_name = 'ship-positions'

    async def initialize_producer(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
        if self.verbose:
            self.log("Producer Kafka initialisé")

    async def send_to_kafka(self, position_data):
        try:
            await self.producer.send_and_wait(self.topic_name, position_data)
            if self.verbose:
                self.log(f"Position envoyée à Kafka: {position_data}")
        except Exception as e:
            self.log(f"Erreur lors de l'envoi à Kafka: {str(e)}")

    async def run(self):
        try:
            await self.initialize_producer()

            while True:
                message = await self.websocket.recv()
                data = json.loads(message)

                if self.verbose:
                    self.log(f"Received data: {json.dumps(data, indent=4)}")

                ship_position = data["ship"]["position"]

                print(ship_position)

                position_message = {
                    "timestamp": int(datetime.now().timestamp() * 1000),
                    "type_object": "ship",
                    "name": data["ship"].get("id", "unknown"),
                    "x": ship_position[0],
                    "y": ship_position[1],
                    "z": ship_position[2]
                }


                await self.send_to_kafka(position_message)

                engine_commands = {
                    "data": {
                        "engines": {
                            "front": random.choice([True, False]),
                            "back": random.choice([True, False]),
                            "left": random.choice([True, False]),
                            "right": random.choice([True, False]),
                            "up": random.choice([True, False]),
                            "down": random.choice([True, False]),
                        },
                        "rotation": {
                            "left": random.choice([True, False]),
                            "right": random.choice([True, False]),
                            "up": random.choice([True, False]),
                            "down": random.choice([True, False]),
                        }
                    }
                }

                if self.verbose:
                    self.log(f"Sending engine commands: {json.dumps(engine_commands, indent=4)}")

                await self.websocket.send(json.dumps(engine_commands))
                await asyncio.sleep(1)

        except Exception as e:
            self.log(f"Erreur dans la boucle principale: {str(e)}")
            if self.producer:
                await self.producer.stop()
            raise

        finally:
            if self.producer:
                await self.producer.stop()

    async def cleanup(self):
        if self.producer:
            await self.producer.stop()