# load/save players.json
import requests
import time
import json
import base64
import msgpack
import threading
import websocket
import ast
import random
from msgpack import ExtType
def player_load():
    with open("players.json", 'r') as file:
        players = json.load(file)
        return players
    
def player_dump(players):
    with open("players.json",'w') as file:
        json.dump(players, file)