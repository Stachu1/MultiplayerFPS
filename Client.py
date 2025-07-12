import os, sys, threading, socket, time, pickle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from Game.Game import Game


class Client:
    def __init__(self, addr=('localhost', 8080)):
        self.game = Game()
        self.addr = addr
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_packet_size = 4096
        self.ping = None
    
    
    def connect(self):
        self.conn.connect(self.addr)
        game_data = pickle.loads(self.conn.recv(self.max_packet_size))
        return game_data
    
    
    def run(self):
        game_data = self.connect()
        self.game.player = game_data['player']
        self.game.world.map = game_data['world_map']
        
        self.game.run()
    
    
    def thread(self):
        while self.game.running:
            recv = pickle.dumps(self.player)
            start_time = time.monotonic()
            self.client.send(recv)
            reply = self.client.recv(self.max_packet_size)
            self.ping = round((time.monotonic() - start_time) * 1000)
            self.conn.send(pickle.loads(reply))


if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else exit('Usage: python client.py <server_ip> <server_port>')
    port = int(sys.argv[2]) if len(sys.argv) > 2 else exit('Usage: python client.py <server_ip> <server_port>')
    client = Client(addr=(ip, port))
    client.run()
