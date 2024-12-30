import yaml


def load_config(file_path):
    """Charge la configuration depuis un fichier YAML."""
    with open(file_path, "r") as config_file:
        return yaml.safe_load(config_file)


config = load_config("config/config.yaml")
