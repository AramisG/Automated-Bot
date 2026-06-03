#encode, decode, params, send_action
import time
import json
import base64
import msgpack
from msgpack import ExtType
from pathlib import Path

def encode(data) -> str:
    packed = msgpack.packb(data, use_bin_type=True)
    return "b" + base64.b64encode(packed).decode("utf-8")

def decode(text):
    try:
        return msgpack.unpackb(base64.b64decode(text[1:]), raw=False)
    except:
        try:
            return msgpack.unpackb(base64.b64decode(text), raw=False)
        except:
            return text

def params(sid=None):
    p = {"EIO": 4, "transport": "polling", "t": str(int(time.time() * 1000))}
    if sid:
        p["sid"] = sid
    return p

def send_action(ws, action, args):
    payload = encode({
        "type": 2,
        "data": ["message", {"action": action, "args": args}],
        "options": {"compress": True},
        "nsp": "/"
    })
    ws.send(payload)
    
def player_load():
    with open("data\players.json", 'r') as file:
        players = json.load(file)
    
def player_dump(players):
    with open("data\players.json",'w') as file:
        json.dump(players, file)
        