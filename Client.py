import os, sys, threading, socket, time, pickle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from Game.Game import Game


class Client:
    def __init__(self, addr=('localhost', 8080)):
        self.game = None
        self.addr = addr
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_packet_size = 2048
    
    
    def connect(self):
        self.conn.settimeout(5)
        self.conn.connect(self.addr)
        game_data = pickle.loads(self.conn.recv(self.max_packet_size))
        return game_data
    
    
    def run(self):
        try:
            game_data = self.connect()
        except (socket.timeout, ConnectionRefusedError, OSError):
            print(f'\33[31mConnection to server {self.addr[0]} {self.addr[1]} failed\33[0m')
            sys.exit(1)
        self.game = Game((1200, 700), fps_limit=0, render_scale=0.8)
        self.game.player = game_data['player']
        self.game.world.map = game_data['world_map']
        self.game.engine.render_distance = max(len(self.game.world.map), len(self.game.world.map[0]))
        threading.Thread(target=self.thread, args=()).start()
        self.game.run()
    
    
    def thread(self):
        while self.game.running:
            try:
                tx = pickle.dumps(self.game.player)
                start_time = time.monotonic()
                self.conn.send(tx)
                rx = self.conn.recv(self.max_packet_size)
                self.game.ping = (time.monotonic() - start_time) * 1000
                self.game.player.damage_queue = []
                self.game.all_players = pickle.loads(rx)
                
                for player in self.game.all_players:
                    if player.id == self.game.player.id:
                        self.game.player.health = player.health
                        self.game.player.kills = player.kills
                        break
                
            except EOFError:
                print('\33[31mServer disconnected\33[0m')
                self.game.running = False
            except Exception as e:
                print(f'\33[31mError in client thread: {e}\33[0m')
                self.game.running = False
        self.conn.close()


if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else exit('Usage: python client.py <server_ip> <server_port>')
    port = int(sys.argv[2]) if len(sys.argv) > 2 else exit('Usage: python client.py <server_ip> <server_port>')
    client = Client(addr=(ip, port))
    client.run()
