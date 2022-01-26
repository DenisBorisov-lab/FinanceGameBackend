import uuid

from flask import Flask, request, jsonify

from game import *
from profile import *
from sessions import *

app = Flask(__name__)
session = Session()


@app.route('/connect', methods=["POST"])
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


@app.route('/disconnect', methods=["POST"])
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


@app.route('/get_lobby', methods=["GET"])
def get_lobby():
    id = request.args.get("id")
    profiles = []
    for game in session.sessions:
        if game.identifier == id:
            profiles = game.players
        print(game.players)
    return {"profiles": [profile.convert() for profile in profiles]}


app.run("0.0.0.0", 5000)
