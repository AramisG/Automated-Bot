import  client
import time
import  protocol
def main():
    players = protocol.player_load()
    ws = client.login(players)
    time.sleep(1)
    protocol.send_action(ws, "send_message",  {"message": "Hello!"})
        # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        protocol.player_dump(players)
        print("Stopped.")
        ws.close()

if __name__ == "__main__":
    main()