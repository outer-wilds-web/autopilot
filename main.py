import asyncio

from autopilot.pattern_kafka_autopilot import PatternKafkaAutopilot
from websocket_client import websocket_handler
from autopilot.random_autopilot import RandomAutopilot
from autopilot.planet_autopilot import PlanetAutopilot
from autopilot.kafka_autopilot import ShipPositionKafkaAutopilot

if __name__ == "__main__":
    print("Choisissez un autopilote:")
    print("1. Autopilote aléatoire")
    print("2. Autopilote vers une planète")
    print("3. Autopilote avec Kafka")
    print("4. Autopilote avec Kafka (motif prédéfini)")

    choice = input("Votre choix: ")
    verbose = input("Mode verbose (0=non, 1=oui): ").strip() == "1"

    if choice == "1":
        asyncio.run(websocket_handler(RandomAutopilot, verbose=verbose))
    elif choice == "2":
        target_planet = input("Entrez le nom de la planète cible: ")
        asyncio.run(websocket_handler(PlanetAutopilot, target_planet, verbose=verbose))
    elif choice == "3":
        kafka_server = input("Entrez l'adresse du serveur Kafka (défaut: localhost:9092): ").strip()
        if not kafka_server:
            kafka_server = "localhost:9092"
        asyncio.run(websocket_handler(ShipPositionKafkaAutopilot, kafka_server, verbose=verbose))
    elif choice == "4":
        kafka_server = input("Entrez l'adresse du serveur Kafka (défaut: localhost:9092): ").strip()
        if not kafka_server:
            kafka_server = "localhost:9092"
        asyncio.run(websocket_handler(PatternKafkaAutopilot, kafka_server, verbose=verbose))
    else:
        print("Choix invalide")


# if __name__ == "__main__":
#     asyncio.run(websocket_handler(PatternKafkaAutopilot, "localhost:9092", verbose=0))