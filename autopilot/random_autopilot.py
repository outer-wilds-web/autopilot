import random
import asyncio
import json
from autopilot.base_autopilot import AutopilotBase

class RandomAutopilot(AutopilotBase):
    async def run(self):
        while True:
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
