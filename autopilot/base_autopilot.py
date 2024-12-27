class AutopilotBase:
    def __init__(self, websocket, verbose=0):
        self.websocket = websocket
        self.verbose = verbose

    async def run(self):
        """Méthode principale pour exécuter l'autopilote."""
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def log(self, message):
        if self.verbose:
            print(message)