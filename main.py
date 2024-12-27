import asyncio
from websocket_client import websocket_handler
from autopilot.random_autopilot import RandomAutopilot
from autopilot.planet_autopilot import PlanetAutopilot


if __name__ == "__main__":
    print("Choisissez un autopilote:")
    print("1. Autopilote aléatoire")
    print("2. Autopilote vers une planète")
    choice = input("Votre choix: ")

    verbose = input("Mode verbose (0=non, 1=oui): ").strip() == "1"

    if choice == "1":
        asyncio.run(websocket_handler(RandomAutopilot, verbose=verbose))
    elif choice == "2":
        target_planet = input("Entrez le nom de la planète cible: ")
        asyncio.run(websocket_handler(PlanetAutopilot, target_planet, verbose=verbose))
    else:
        print("Choix invalide")