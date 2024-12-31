import asyncio
import json
from aiokafka import AIOKafkaProducer
from datetime import datetime
from .base_autopilot import AutopilotBase


class PatternKafkaAutopilot(AutopilotBase):
    def __init__(self, websocket, verbose=False, kafka_bootstrap_servers='localhost:9092', name="default"):
        super().__init__(websocket, verbose)
        self.producer = None
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic_name = 'ship-positions'
        self.movement_index = 0
        self.movement_duration = 5
        self.name = name

        # self.movement_patterns = [
        #     {
        #         "engines": {"front": True, "back": False, "left": False, "right": False, "up": False, "down": False},
        #         "rotation": {"left": False, "right": False, "up": False, "down": False}
        #     },
        #     {
        #         "engines": {"front": False, "back": False, "left": False, "right": False, "up": False, "down": False},
        #         "rotation": {"left": False, "right": False, "up": False, "down": False}
        #     },
        #     {
        #         "engines": {"front": False, "back": False, "left": False, "right": True, "up": False, "down": False},
        #         "rotation": {"left": False, "right": False, "up": False, "down": False}
        #     },
        #     {
        #         "engines": {"front": False, "back": False, "left": False, "right": False, "up": False, "down": False},
        #         "rotation": {"left": False, "right": False, "up": False, "down": False}
        #     },
        #     {
        #         "engines": {"front": False, "back": False, "left": True, "right": False, "up": False, "down": False},
        #         "rotation": {"left": False, "right": False, "up": False, "down": False}
        #     },
        #     {
        #         "engines": {"front": False, "back": False, "left": False, "right": False, "up": False, "down": False},
        #         "rotation": {"left": False, "right": False, "up": False, "down": False}
        #     },
        #     {
        #         "engines": {"front": False, "back": True, "left": False, "right": False, "up": False, "down": False},
        #         "rotation": {"left": False, "right": False, "up": False, "down": False}
        #     }
        # ]

        self.movement_patterns = [
            {
                "engines": {"front": False, "back": True, "left": False, "right": False, "up": False, "down": False},
                "rotation": {"left": False, "right": False, "up": False, "down": False}
            }
        ]

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

    def get_current_movement(self):
        pattern = self.movement_patterns[self.movement_index]
        return {
            "data": {
                "engines": pattern["engines"],
                "rotation": pattern["rotation"]
            }
        }

    async def run(self):
        try:
            await self.initialize_producer()
            movement_timer = 0

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
                    "name": self.name,
                    "x": ship_position[0],
                    "y": ship_position[1],
                    "z": ship_position[2]
                }

                await self.send_to_kafka(position_message)

                engine_commands = self.get_current_movement()

                if self.verbose:
                    self.log(f"Sending engine commands: {json.dumps(engine_commands, indent=4)}")
                    self.log(f"Current movement phase: {self.movement_index}")

                await self.websocket.send(json.dumps(engine_commands))

                movement_timer += 1
                if movement_timer >= self.movement_duration:
                    movement_timer = 0
                    self.movement_index = (self.movement_index + 1) % len(self.movement_patterns)

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