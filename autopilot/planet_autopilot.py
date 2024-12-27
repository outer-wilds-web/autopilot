import json
import asyncio
import math
from autopilot.base_autopilot import AutopilotBase


class PlanetAutopilot(AutopilotBase):
    def __init__(self, websocket, target_planet, verbose=0):
        super().__init__(websocket, verbose)
        self.target_planet = target_planet

    async def run(self):
        while True:
            try:
                # Recevoir les données du serveur
                message = await self.websocket.recv()
                data = json.loads(message)
                
                if self.verbose:
                    self.log(f"Received data: {json.dumps(data, indent=4)}")

                # Récupérer la position du vaisseau et de la planète cible
                ship_position = data["ship"]["position"]

                # Préparer un dictionnaire des planètes avec ajustement pour les coordonnées en 3D
                # car pour le moment le websocket renvoie les planètres dans un plan 2D et le vaisseau dans un plan 3D
                planets = {
                    planet[0]: planet[1] + [0] if len(planet[1]) == 2 else planet[1]
                    for planet in data["planets"]
                }

                if self.target_planet not in planets:
                    self.log(f"Planète {self.target_planet} non trouvée!")
                    break

                target_position = planets[self.target_planet]

                # Calculer la direction vers la planète
                direction = [
                    target_position[i] - ship_position[i]
                    for i in range(2)
                ]
                magnitude = math.sqrt(sum(d ** 2 for d in direction))
                normalized_direction = [d / magnitude for d in direction]

                # Envoi des commandes au moteur pour se diriger
                engine_commands = {
                    "data": {
                        "engines": {
                            "front": normalized_direction[0] > 0,
                            "back": normalized_direction[0] < 0,
                            "left": normalized_direction[1] < 0,
                            "right": normalized_direction[1] > 0,
                            "up": False,
                            "down": False,
                        }
                    }
                }
                if self.verbose:
                    self.log(f"Sending engine commands: {json.dumps(engine_commands, indent=4)}")
                await self.websocket.send(json.dumps(engine_commands))
                await asyncio.sleep(0.1)
            except json.JSONDecodeError:
                self.log("Erreur de décodage JSON")
                break
