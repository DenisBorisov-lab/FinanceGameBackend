import random


class Application:
    name: str
    month: str

    def __init__(self, name, month):
        self.name = name
        self.month = month


class BuyRawApplication(Application):
    materials: int
    material_price: int

    def __init__(self, name, month, materials, material_price):
        super().__init__(name, month)
        self.materials = materials
        self.material_price = material_price


class ProduceApplication(Application):
    planes: int

    def __init__(self, name, month, planes):
        super().__init__(name, month)
        self.planes = planes


class SellPlanesApplication(Application):
    planes: int
    money: int

    def __init__(self, name, month, planes, money):
        super().__init__(name, month)
        self.planes = planes
        self.money = money


class Game:
    identifier: str
    players: list
    month: int
    level: int
    materials: int
    material_price: int
    planes: int
    plane_price: int
    buy_raw_applications: list
    produce_applications: list
    sell_planes_applications: list
    finished_players: list
    create_factory_applications: list
    logs: str
    ready_players: set

    def __init__(self, identifier):
        self.identifier = identifier
        self.players = []
        self.month = 1
        self.level = 3
        self.materials = 0
        self.plane_price = 0
        self.planes = 0
        self.material_price = 0
        self.buy_raw_applications = []
        self.produce_applications = []
        self.finished_players = []
        self.create_factory_applications = []
        self.sell_planes_applications = []
        self.logs = ""
        self.ready_players = set()

    def convert(self):
        return {
            "identifier": self.identifier,
            "players": [player.convert() for player in self.players],
            "month": self.month,
            "level": self.level,
            "materials": self.materials,
            "material_price": self.material_price,
            "planes": self.planes,
            "plane_price": self.plane_price,
            "logs": self.logs
        }

    def leveling_market(self):
        if self.level == 1:
            self.level = random.choices([1, 2, 3, 4, 5], weights=[1 / 3, 1 / 4, 1 / 12, 1 / 12, 1 / 12])[0]
        elif self.level == 2:
            self.level = random.choices([1, 2, 3, 4, 5], weights=[1 / 3, 1 / 3, 1 / 4, 1 / 12, 1 / 12])[0]
        elif self.level == 3:
            self.level = random.choices([1, 2, 3, 4, 5], weights=[1 / 6, 1 / 4, 1 / 3, 1 / 4, 1 / 6])[0]
        elif self.level == 4:
            self.level = random.choices([1, 2, 3, 4, 5], weights=[1 / 12, 1 / 12, 1 / 4, 1 / 3, 1 / 3])[0]
        else:
            self.level = random.choices([1, 2, 3, 4, 5], weights=[1 / 12, 1 / 12, 1 / 12, 1 / 4, 1 / 3])[0]

    def calculate_market(self):
        if self.level == 1:
            self.materials = len(self.players)
            self.material_price = 800
            self.planes = 3 * len(self.players)
            self.plane_price = 6500

        elif self.level == 2:
            self.materials = 1.5 * len(self.players)
            self.material_price = 650
            self.planes = 2.5 * len(self.players)
            self.plane_price = 6000

        elif self.level == 3:
            self.materials = 2 * len(self.players)
            self.material_price = 500
            self.planes = 2 * len(self.players)
            self.plane_price = 5500

        elif self.level == 4:
            self.materials = 2.5 * len(self.players)
            self.material_price = 400
            self.planes = 1.5 * len(self.players)
            self.plane_price = 5000

        else:
            self.materials = 3 * len(self.players)
            self.material_price = 300
            self.planes = 1 * len(self.players)
            self.plane_price = 4500

    def submit_buy_raw_application(self, application):
        access = True
        for app in self.buy_raw_applications:
            if app.name == application.name or application.materials * application.material_price == 0:
                access = False
                break

        if access:
            self.buy_raw_applications.append(application)
            self.logs += application.name + " оставил заявку на покупку сырья\n"
            return True
        else:
            return False

    def submit_sell_planes_application(self, application: SellPlanesApplication):
        access = True
        for app in self.sell_planes_applications:
            if app.name == application.name or application.planes * application.money == 0:
                access = False
                break

        if access:
            self.sell_planes_applications.append(application)
            self.logs += application.name + " оставил заявку на продажу истребителей\n"
            return True
        else:
            return False

    def submit_produce_application(self, application: ProduceApplication):
        access = True
        for app in self.produce_applications:
            if app.name == application.name:
                access = False
                break
        if access:
            self.produce_applications.append(application)
            self.logs += application.name + " оставил заявку на производство истребителей\n"
            return True
        else:
            return False

    def submit_create_factory_application(self, application: Application):
        access = True
        for app in self.create_factory_applications:
            if app.name == application.name and app.month == application.month:
                access = False
                break
        if access:
            self.create_factory_applications.append(application)
            self.logs += application.name + " оставил заявку на строительство завода\n"
            return True
        else:
            return False

    def count_create_factory_applications_by_name(self, name) -> int:
        count = 0
        for app in self.create_factory_applications:
            if app.name == name:
                count += 1
        return count

    def finish_buy_raw_applications(self):
        app_list = sorted(self.buy_raw_applications, key=lambda x: x.materials * x.material_price)
        app_list.reverse()
        available_materials = self.materials
        for app in app_list:
            if available_materials >= app.materials:
                for player in self.players:
                    if player.nickname == app.name:
                        player.money -= app.materials * app.material_price
                        player.materials += app.materials
                        available_materials -= app.materials
                        self.buy_raw_applications.remove(app)

    def finish_create_factory_applications(self):
        for app in self.create_factory_applications:
            for player in self.players:
                if player.nickname == app.name:
                    player.factories += 1
                    player.money -= 2500
                    self.create_factory_applications.remove(app)

    def finish_produce_application(self):
        for app in self.produce_applications:
            for player in self.players:
                if player.nickname == app.name:
                    player.planes += app.planes
                    self.produce_applications.remove(app)

    def finish_auction(self):
        app_list = sorted(self.sell_planes_applications, key=lambda x: x.planes * x.money)
        app_list.reverse()
        available_planes = self.planes
        for app in app_list:
            if app.planes <= available_planes:
                for player in self.players:
                    if player.nickname == app.name:
                        player.money += app.planes * app.money
                        player.planes -= app.planes
                        available_planes -= app.planes
                        self.sell_planes_applications.remove(app)


def get_application(applications: list, name):
    for app in applications:
        if app.name == name:
            return app
