import requests
from uuid import UUID


def connection(api_url: str, email: str, password: str, username: str):
    """
    Tente d'enregistrer un utilisateur via /auth/register, puis de le connecter via /auth/login.

    Args:
        api_url (str): L'URL de base de l'API.
        email (str): L'email de l'utilisateur.
        password (str): Le mot de passe de l'utilisateur.
        username (str): Le nom d'utilisateur.

    Returns:
        dict: Résultat de la connexion ou message d'erreur.
    """
    # Endpoint d'enregistrement
    register_endpoint = f"{api_url}/auth/register"
    register_payload = {
        "email": email,
        "password": password,
        "username": username
    }

    # Tenter l'enregistrement
    register_response = requests.post(register_endpoint, json=register_payload)
    if register_response.status_code == 200:  # Succès
        print("Utilisateur enregistré avec succès.")
        return register_response.json()

    elif register_response.status_code == 401 and "User already exists" in register_response.text:
        print("Utilisateur déjà existant. Passage à la connexion.")
    else:  # Autre erreur
        return {
            "error": "Erreur lors de l'enregistrement",
            "details": register_response.json()
        }

    # Endpoint de connexion
    login_endpoint = f"{api_url}/auth/login"
    login_payload = {
        "email": email,
        "password": password
    }

    # Tenter la connexion
    login_response = requests.post(login_endpoint, json=login_payload)
    if login_response.status_code == 200:  # Succès
        print("Connection a l'utilisateur")
        return login_response.json()
    else:
        return {
            "error": "Erreur lors de la connexion",
            "details": login_response.json()
        }


def ship_launch(api_url: str, id_owner: UUID, name: str, token_type: str, token: str):
    """
    Tente de créer un vaisseau via /ships et le recupere s'il existe déjà via /ships/{ship_name}.

    Args:
        api_url (str): L'URL de base de l'API.
        id_owner (UUID): L'identifiant du propriétaire du vaisseau.
        name (str): Le nom du vaisseau.
        token (str): Le token d'accès pour l'autorisation.

    Returns:
        dict: un vaisseau ou un message d'erreur.
    """
    # Construire les headers pour les appels suivants
    headers = {
        "Authorization": f"{token_type} {token}"
    }
    print(headers)
    # Vérifier si le vaisseau existe déjà
    get_ship_endpoint = f"{api_url}/ships/name/{name}"
    get_ship_response = requests.get(get_ship_endpoint, headers=headers)
    if get_ship_response.status_code == 200:  # Vaisseau existant
        print("Le vaisseau existe déjà.")
        return get_ship_response.json()
    elif get_ship_response.status_code == 404 and "Ship not found" in get_ship_response.text:  # Autre erreur
        print("Le vaisseau n'existe pas. Passage à la création.")
    else:  # autre erreur
        return {
            "error": "Erreur lors de la vérification de l'existence du vaisseau",
            "details": get_ship_response.json()
        }

    create_endpoint = f"{api_url}/ships"
    payload = {
        "owner": str(id_owner),
        "name": name
    }
    create_response = requests.post(
        create_endpoint, json=payload, headers=headers)
    if create_response.status_code == 200:  # Succès
        print("vaisseau crée avec succès.")
        return create_response.json()
    else:  # Autre erreur
        return {
            "error": "Erreur lors de la creation",
            "details": create_response.json()
        }
