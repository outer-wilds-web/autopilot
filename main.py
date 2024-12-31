import asyncio

import requests
import time

from config.config import config
from api_link import connection, ship_launch


from websocket_client import websocket_handler
from autopilot.kafka_autopilot import ShipPositionKafkaAutopilot


def wait_for_api(api_url, timeout):
    """Attendre que l'API soit disponible."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                print("API prête!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("Échec de la connexion à l'API.")
    return False


def ship_register():
    # Charger la configuration depuis le fichier YAML
    api_host = config["api"]["host"]
    api_port = config["api"]["port"]
    api_timeout = config["api"]["timeout"]
    # Construire l'URL complète de l'API
    api_url = f"http://{api_host}:{api_port}"

    api_ping = f"{api_url}/ping"
    # Vérifier si l'API est disponible
    if wait_for_api(api_ping, api_timeout):
        try:
            username = config["login"]["username"]
            email = config["login"]["email"]
            password = config["login"]["password"]
            connection_response = connection(
                api_url, email, password, username)

            if "error" in connection_response:
                print(f"Erreur lors de la connexion: {
                      connection_response['error']}")
                return

            # Récupérer le token
            token = connection_response["token"]["access_token"]
            token_type = connection_response["token"]["token_type"]
            id_owner = connection_response["user"]["id"]
            name = config["ship"]["name"]

            ship = ship_launch(api_url, id_owner, name, token_type, token)
            return ship["name"]
        except Exception as e:
            print(f"Erreur dans le processus: {e}")
            return None


def main():

    name = ship_register()
    choice = config["ship_driving"]["choice"]
    verbose = config["logger"]["verbose"]
    kafka_server = f"{config['kafka']['host']}:{config['kafka']['port']}"
    if choice == "autopilot":
        asyncio.run(websocket_handler(
            ShipPositionKafkaAutopilot, kafka_server, verbose=verbose, name=name))
    else:
        print("Choix invalide")


if __name__ == "__main__":
    main()
