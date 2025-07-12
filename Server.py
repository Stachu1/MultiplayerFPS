import socket, sys, random, time, threading, math, pickle, numpy as np
from datetime import datetime
from Game.Player import Player
from Game.World import World


def threaded_client(conn, player):
    init_msg = {'player': player, 'world_map': world.map}
    conn.send(pickle.dumps(init_msg))

    while True:
        try:
            recv = conn.recv(4096)

            if not recv:
                break
            else:
                player = pickle.loads(recv)
                reply = pickle.dumps(players)
                print(f'R:{sys.getsizeof(recv)}    T:{sys.getsizeof(reply)}')
                conn.send(reply)    # Send reply
                
        except OSError as e:
            break
    print(f'\33[31mConnection Closed Player ID: {player.id} \33[0m')
    for p in players:       # Remove player
        if p.id == player.id:
            players.remove(p)
    conn.close()



def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address



world = World()
world.load('maps/map_1.txt')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = get_local_ip()
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(f'\33[31mError binding to port {port}: {e}\33[0m')

s.listen()
print(f'{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')} Waiting for a connections ip: {server_ip} port: {port}')


next_player_id = 1
players = []
connections = []


try:
    while True:
        conn, addr = s.accept()
        print(f'\33[32mConnected to: {addr[0]} {addr[1]}', end=' ')

        spawn_x, spawn_y = world.random_spawn()
        player = Player(next_player_id, spawn_x, spawn_y, random.uniform(0, 2 * np.pi))
        players.append(player)
        
        print(f'Player ID: {next_player_id}\33[0m')
        
        next_player_id += 1

        threading.Thread(target=threaded_client, args=(conn, player,)).start()
        connections.append(conn)
        
except KeyboardInterrupt:
    server_running = False
    print("Closing...")
    for conn in connections:
        conn.close()
    
except Exception as e:
    print(f'\33[31mError: {e}\33[0m')
    