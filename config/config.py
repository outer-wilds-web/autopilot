import os

config = {
    "api": {
        "host": os.getenv("API_HOST", "localhost"),
        "port": int(os.getenv("API_PORT", 8000)),
        "timeout": int(os.getenv("API_TIMEOUT", 30)),
    },
    "kafka": {
        "host": os.getenv("KAFKA_BROKERS", "localhost:9092").split(":")[0],
        "port": int(os.getenv("KAFKA_BROKERS", "localhost:9092").split(":")[1]),
    },
    "login": {
        "username": os.getenv("LOGIN_USERNAME", "default_user"),
        "email": os.getenv("LOGIN_EMAIL", "user@example.com"),
        "password": os.getenv("LOGIN_PASSWORD", "default_password"),
    },
    "ship": {
        "name": os.getenv("SHIP_NAME", "default_ship"),
    },
    "ship_driving": {
        "choice": os.getenv("CHOICE", "autopilot"),
    },
    "logger": {
        "verbose": os.getenv("LOGGER_VERBOSE", "false").lower() == "true",
    },
    "websocket": {
        "url": os.getenv("WEBSOCKET_URL", "ws://localhost:3012"),
    }
}
