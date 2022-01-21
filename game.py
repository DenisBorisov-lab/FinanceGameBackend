class Game:
    identifier: str
    players: list

    def __init__(self, identifier):
        self.identifier = identifier
        self.players = []

    def convert(self):
        return {
            "identifier": self.identifier,
            "players": [player.convert() for player in self.players]
        }
