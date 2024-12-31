class AutopilotBase:
    def __init__(self, websocket, verbose=0, name="default"):
        self.websocket = websocket
        self.verbose = verbose
        self.name = name

    async def run(self):
        """Méthode principale pour exécuter l'autopilote."""
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def log(self, message):
        if self.verbose:
            print(message)