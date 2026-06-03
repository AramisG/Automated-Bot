#greet, make_money, mine, bag_fries
import protocol
import time
import ast
import random
import config

working = False
last_mine_time = 0

def follow(ws,id,data):
    if data[1]['action'] == 'send_position' and int(data[1]['args']['id']) == id:
        protocol.send_action(ws, "send_position", {"x": int(data[1]['args']['x'] + random.randint(1,50)), "y": int(data[1]['args']['y'])+ random.randint(1,50)})

def greet(ws,data):
    name = "Flint"
    greetings = ['Hiya', 'Whats up', 'Nice to see you', 'leave me alone bro', 'Hey', 'Sup']
    try:
        if data[1]['action'] == 'send_message' and name.lower() in data[1]['args']['message'].lower():
            protocol.send_action(ws, 'send_message', {"message": greetings[random.randint(0,(len(greetings)) - 1 )]})
            protocol.send_action(ws, 'send_frame', {'set': False, 'frame': 25})
        else:
            return
    except (UnboundLocalError, KeyError, IndexError, TypeError) as e:
        pass

def player_add(players,data):
        if data[1]['action'] == "add_player":
            if str(data[1]['args']['user']['id']) not in players:
                players[str(data[1]['args']['user']['id'])] = {"username": data[1]['args']['user']['username'],
                                                                  "displayName": data[1]['args']['user']['displayName']}
        else:
            return
def mine(ws):
    global last_mine_time
    protocol.send_action(ws,'send_frame', {'set': True, 'frame': 26})
    protocol.send_action(ws,'mine',{})
    
    last_mine_time = time.time()
            

def check_mining(ws,data):
    global working
    try:
        if data[1]['action'] == 'send_message' and data[1]['args']['id'] == 274747 and data[1]['args']['message'].lower() == 'shifts up':
            working = False
            time.sleep(2)
            protocol.send_action(ws,"send_message", {"message": "IM FREE!!"})
            time.sleep(1)
            protocol.send_action(ws,"join_room",{'room':config.ROOMS['welcome_room']})
            return
    except (KeyError, IndexError, TypeError) as e:
        return

    if time.time() - last_mine_time >= 60:
        mine(ws)

def bag_fries(ws):

    body = ["hand","neck","body","head","feet", "face"]
    protocol.send_action(ws,"join_room",{'room':config.ROOMS['cave']})
    time.sleep(.5)
    protocol.send_action(ws, "send_message",{"message": "Time to put the fries in the bag!"})
    time.sleep(.5)
    for values in body:
        protocol.send_action(ws,"remove_item", {'type': values})
        time.sleep(.2)
    
    protocol.send_action(ws,'update_player', {'item': 429})
    time.sleep(.5)
    protocol.send_action(ws,"send_position", {'x': 825 + random.randint(-15,15), 'y': 734 + random.randint(-15,15)})

def make_money(ws, data):
    start = "get to work"
    global working
    
    try: 
        if not working and data[1]['action'] == 'send_message' and data[1]['args']['id'] == 274747 and start.lower() in data[1]['args']['message'].lower():
            working = True
            time.sleep(2)
            bag_fries(ws)
            mine(ws)
        if working:
            check_mining(ws,data)
    except (UnboundLocalError, KeyError, IndexError, TypeError) as e:
        return