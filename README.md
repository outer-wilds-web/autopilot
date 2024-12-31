# **Autopilot**

## **Lancement de l'application**

1. **Démarrage avec Docker Compose**  
   Lancez l'application avec la commande suivante pour construire et démarrer les conteneurs :  
   ```bash
   docker-compose up --build
   ```

2. **Initialisation du backend**  
   Assurez-vous que le backend est opérationnel avant de procéder à la création d'un vaisseau (juste pour l'initalisation).

---

## **Création d'un vaisseau**

- **Authentification requise**  
  La création d'un vaisseau nécessite une authentification préalable.

- **Contraintes d'unicité**  
  - **Email** : Chaque email doit être unique.  
  - **Nom d'utilisateur** : Chaque nom d'utilisateur doit être unique.  
  - **Nom du vaisseau** : Chaque nom de vaisseau doit être unique.

---

## **Enregistrement des données**

- Une fois les informations de création validées, elles sont transmises via **Kafka** pour être enregistrées dans la base de données.

---

## **Configuration par défaut**

- **Utilisateurs initiaux** :  
  Deux utilisateurs sont créés par défaut lors de l'initialisation.  

⚠️ **Note importante** : Vérifiez les contraintes d'unicité (email, nom d'utilisateur et nom de vaisseau) pour éviter tout conflit.
