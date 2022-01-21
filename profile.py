class Profile:

    nickname: str

    def __init__(self, nickname):
        self.nickname = nickname

    def convert(self):
        return {
            "nickname": self.nickname
        }
