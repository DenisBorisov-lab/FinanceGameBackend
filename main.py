import uuid

from flask import Flask, request, jsonify

from game import *
from profile import *
from sessions import *

app = Flask(__name__)
session = Session()


@app.post('/connect')
def connect():
    access = False
    data = request.form
    name = data.get("name")
    identifier = data.get("identifier")

    lobby = None
    if identifier == "host":
        identifier = uuid.uuid4()
        lobby = Game(str(identifier)[9:13])
        lobby.players.append(Profile(name))
        session.sessions.append(lobby)
        access = True
    else:
        for game in session.sessions:
            if game.identifier == identifier and not name in game.players:
                lobby = game
                game.players.append(Profile(name))
                access = True

    dictionary = {"access": access,
                  "identifier": lobby.identifier if access else None,
                  "players": [player.convert() for player in lobby.players] if access else None}
    return jsonify(dictionary)


@app.post('/disconnect')
def disconnect():
    data = request.form
    name = data.get("name")
    game_id = data.get("identifier")
    success = False

    for game in session.sessions:
        if game.identifier == game_id:
            for profile in game.players:
                if profile.nickname == name:
                    game.players.remove(profile)
                    success = True
                    if len(game.players) == 0:
                        session.sessions.remove(game)
                    break
    dictionary = {"access": success}
    return jsonify(dictionary)


@app.get('/get_lobby')
def get_lobby():
    id = request.args.get("id")
    profiles = []
    for game in session.sessions:
        if game.identifier == id:
            profiles = game.players
    return jsonify({"profiles": [profile.convert() for profile in profiles]})


@app.post('/ready')
def ready():
    data = request.form
    name = data.get("name")
    id = data.get("id")
    status = False

    for game in session.sessions:
        if game.identifier == id:
            for profile in game.players:
                if profile.nickname == name:
                    profile.status = True if not profile.status else False
                    status = profile.status
                    break
    return jsonify({"status": status})


@app.post("/is_all_ready")
def is_all_ready():
    data = request.form
    id = data.get("id")
    ready = 0
    all = 0
    res = False
    for game in session.sessions:
        if game.identifier == id:
            for profile in game.players:
                all += 1
                if profile.status:
                    ready += 1

    res = True if ready == all else False
    return jsonify({"status": res})


@app.get("/get_info")
def get_info():
    id = request.args.get("id")
    for s in session.sessions:
        if s.identifier == id:
            s.calculate_market()
            return jsonify(s.convert())


@app.post("/buy_raw")
def buy_raw():
    data = request.form
    id = data.get("id")
    name = data.get("name")
    materials = data.get("materials")
    material_price = data.get("material_price")
    status = False

    try:
        materials = int(materials)
        material_price = int(material_price)
    except ValueError:
        return {"status": status}

    for s in session.sessions:
        if s.identifier == id:
            for player in s.players:
                if player.nickname == name:
                    if 0 < materials <= s.materials and s.material_price <= material_price * materials <= player.money:
                        status = s.submit_buy_raw_application(
                            BuyRawApplication(name, s.month + 1, materials, material_price))

    return {"status": status}


@app.post("/produce")
def produce():
    data = request.form
    id = data.get("id")
    name = data.get("name")
    planes = data.get("planes")
    status = False

    try:
        planes = int(planes)
    except ValueError:
        return {"status": False}

    for s in session.sessions:
        if s.identifier == id:
            for player in s.players:
                if player.nickname == name:
                    if 0 < planes <= player.factories and player.money > planes * 2000 and player.materials >= planes:
                        status = s.submit_produce_application(ProduceApplication(name, s.month + 1, planes))
                        player.materials -= 1
                        player.money -= planes * 2000
    return {"status": status}


@app.post("/sell_planes")
def take_part_in_auction():
    data = request.form
    id = data.get("id")
    name = data.get("name")
    planes = data.get("planes")
    money = data.get("money")
    status = False

    try:
        planes = int(planes)
        money = int(money)
    except ValueError:
        return {"status": status}

    for s in session.sessions:
        if s.identifier == id:
            for player in s.players:
                if player.nickname == name:
                    if 0 < planes <= s.planes and 0 < money <= s.plane_price:
                        status = s.submit_sell_planes_application(
                            SellPlanesApplication(name, s.month + 1, planes, money))
    return {"status": status}


@app.post("/build")
def create_factory():
    data = request.form
    id = data.get("id")
    name = data.get("name")
    status = False

    for s in session.sessions:
        if s.identifier == id:
            for player in s.players:
                if player.nickname == name:
                    if player.money > 2500 and player.factories + s.count_create_factory_applications_by_name(name):
                        status = s.submit_create_factory_application(Application(name, s.month + 4))
                        player.money -= 2500
    return {"status": status}


# дописать логику
# прошло 3 недели, надо всё таки дописать
@app.post("/finish")
def finish():
    data = request.form
    id = data.get("id")
    name = data.get("name")
    status = True

    for s in session.sessions:
        if s.identifier == id:
            if name not in s.ready_players:
                s.ready_players.add(name)
                s.logs += name + " завершил ход в этом месяце"
            if len(s.players) == len(s.ready_players):
                s.month += 1
                s.finish_buy_raw_applications()
                s.finish_create_factory_applications()
                s.finish_produce_application()
                s.finish_auction()
                for player in s.players:
                    player.money -= 300 * player.materials
                    player.money -= 500 * player.planes
                    player.money -= 1_000 * player.factories
                    if player.money <= 0:
                        player.is_bankrupt = True
                        s.players.remove(player)
                s.leveling_market()
                s.ready_players = set()
            if s.month == 13 or len(s.players) == 1:
                status = False
    return jsonify({"status": status})


# app.run("0.0.0.0", 5000)
