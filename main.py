import uuid

from flask import Flask, request, jsonify

from game import *
from profile import *
from sessions import *

app = Flask(__name__)
games = []
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
            if game.identifier == identifier:
                lobby = game
                game.players.append(Profile(name))
                access = True

    dictionary = {"access": access,
                  "identifier": lobby.identifier if access else None,
                  "players": [player.convert() for player in lobby.players] if access else None}
    return jsonify(dictionary)


app.run("0.0.0.0", 5000)
