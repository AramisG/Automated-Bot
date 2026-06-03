#login, join server, websocket setup
import protocol
import handlers
import  config
import requests
import time
import json
import base64
import msgpack
import threading
import websocket
import ast
import random
import  client
from msgpack import ExtType
import os
from dotenv import load_dotenv
from pathlib import Path




def login(players):
    BASE_DIR = Path(__file__).resolve().parent
    ENV_FILE = BASE_DIR / ".env"
    load_dotenv(ENV_FILE, override = True)

    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    SECRET = os.getenv("SECRET")

    session = requests.Session()
    url = "https://play.cpjourney.net/world/login/"
    url2 = "https://play.cpjourney.net/world/marshmallow/"
    headers = {"Content-Type": "text/plain;charset=UTF-8"}
    

    # Login
    sid = json.loads(session.get(url, params=protocol.params()).text[1:])["sid"]
    session.post(url, params=protocol.params(sid), data=protocol.encode({"type": 0, "data": ExtType(code=0, data=b'\x00'), "nsp": "/"}), headers=headers)
    time.sleep(0.5)
    session.get(url, params=protocol.params(sid))
    session.post(url, params=protocol.params(sid), data=protocol.encode({
        "type": 2,
        "data": ["message", {"action": "login", "args": {
            "username": USERNAME,
            "password": PASSWORD,
            "secret": SECRET
        }}],
        "options": {"compress": True},
        "nsp": "/"
    }), headers=headers)
    time.sleep(0.5)
    login_reply = protocol.decode(session.get(url, params=protocol.params(sid)).text)
    key = login_reply["data"][1]["args"]["key"]
    print("Got key:", key)

    # World server
    server_sid = json.loads(session.get(url2, params=protocol.params()).text[1:])["sid"]
    session.post(url2, params=protocol.params(server_sid), data=protocol.encode({"type": 0, "data": ExtType(code=0, data=b'\x00'), "nsp": "/"}), headers=headers)
    time.sleep(0.5)
    session.get(url2, params=protocol.params(server_sid))
    session.post(url2, params=protocol.params(server_sid), data=protocol.encode({ 
        "type": 2,
        "data": ["message", {"action": "game_auth", "args": {
            "username": os.getenv("USERNAME"),
            "key": key,
            "createToken": False,
            "joinInvis": False,
            "takeoverMascot": ExtType(code=0, data=b'\x00')
        }}],
        "options": {"compress": True},
        "nsp": "/"
    }), headers=headers)
    time.sleep(0.5)
    session.get(url2, params=protocol.params(server_sid))
    session.post(url2, params=protocol.params(server_sid), data=protocol.encode({
        "type": 2,
        "data": ["message", {"action": "join_server", "args": {}}],
        "options": {"compress": True},
        "nsp": "/"
    }), headers=headers)
    print("Joined! Upgrading to WebSocket...")

    ws = websocket.WebSocketApp(
        f"wss://play.cpjourney.net/world/marshmallow/?EIO=4&transport=websocket&sid={server_sid}",
        on_open= handlers.on_open,
        on_message= lambda ws, message: handlers.on_message_with_probe(ws, message, players),
        on_error= handlers.on_error,
        on_close= handlers.on_close,
        header={"Origin": "https://play.cpjourney.net", "User-Agent": "Mozilla/5.0"}
    )

    ws_thread = threading.Thread(target=ws.run_forever, daemon=True)
    ws_thread.start()

    return ws
