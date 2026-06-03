import requests
import time
import json
import base64
import msgpack
import threading
import websocket
import ast
import random
import commands
from msgpack import ExtType
#on_game_message, on_open, on_close
    # --- WebSocket handlers ---


def on_game_message(ws, message, players):
    if message == "2":
        ws.send("3")
        return
    try:
        if isinstance(message, bytes):
            decoded = msgpack.unpackb(message, raw=False)
        else:
            decoded = msgpack.unpackb(base64.b64decode(message), raw=False)
                
        data = decoded.get("data", [])

        if len(data) > 1 and isinstance(data[1], dict):
            action = data[1].get('action',{})
            args = data[1].get("args", {})
            commands.greet(ws, data)
            commands.make_money(ws, data)
            commands.player_add(players,data)

            with open("data/actions.txt", "a") as f:
                f.write(f"{data}\n")
                
            if data[1]['action'] == 'send_message':
                with open('data/chat_data.txt',"a") as f:
                    f.write(f"{args.get('message',{})}\n")
                #['message', {'action': 'add_player', 'args': {'user': {'id': 274747, 'username': 'Santa CIause', 'displayName': 'Santa CIause', 'joinTime': ExtType(code=0, data=b'\x00\x00\x01\x93\xf0)>\x18'), 'hat': 0, 'head': 414, 'face': 3037, 'face_mask': 0, 'neck': 0, 'neck_scarf': 0, 'body': 4126, 'body_shirt': 0, 'hand': 5195, 'hand_glove': 0, 'feet': 0, 'color': 5, 'photo': 0, 'flag': 0, 'transform': 0, 'x': 786, 'y': 676, 'frame': 1, 'walking': 0, 'walkingPuffleType': ExtType(code=0, data=b'\x00'), 'openSprite': ExtType(code=0, data=b'\x00'), 'mascotGiveaway': ExtType(code=0, data=b'\x00'), 'iglooOpen': 0, 'iglooBounds': 0, 'igloo_slot': 0, 'currentLayer': 1, 'fireRank': 0}}}, 'Pv6NPRj.0']



    except:
        if message not in [b"", "3", "5"]:
            #print("Undecodable:", message)
            pass
                
        

def on_message_with_probe(ws, message,players):
    if message == "3probe":
        ws.send("5")
        print("Upgraded! Listening for game events...")
        ws.on_message = lambda ws, message:on_game_message(ws,message,players)
    elif message == "2":
        ws.send("3")
    else:
        on_game_message(ws, message,players)

def on_open(ws):
    print("WebSocket connected! Sending probe...")
    ws.send("2probe")

def on_error(ws, error):
    print("WS Error:", error)

def on_close(ws, close_status, close_msg):
    print("WS Closed:", close_status, close_msg)

