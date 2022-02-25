class Profile:

    nickname: str
    status: bool
    factories: int
    materials: int
    planes: int
    money: int
    is_bankrupt: bool

    def __init__(self, nickname):
        self.nickname = nickname
        self.status = False
        self.factories = 2
        self.materials = 4
        self.planes = 2
        self.money = 10_000
        self.is_bankrupt = False

    def convert(self):
        return {
            "nickname": self.nickname,
            "status": self.status,
            "factories": self.factories,
            "materials": self.materials,
            "planes": self.planes,
            "money": self.money,
            "bankrupt": self.is_bankrupt
        }
