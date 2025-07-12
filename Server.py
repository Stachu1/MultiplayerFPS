import socket, sys, random, time, threading, math, pickle, numpy as np
from datetime import datetime
from PIL import Image, ImageDraw
from colorama import Fore, init
init()









def load_map(filename):
    img = np.array(Image.open(filename))
    for line_index, line in enumerate(img):
        for pixel_index, pixel in enumerate(line):
            if pixel[0] == 0:
                
                print(line_index, pixel_index)


load_map("map.jpg")


# while True:     # * Main loop for accepting connections
#     conn, addr = s.accept()
#     print("Connected to:", addr)

#     currentId = currentId + 1
#     player = Player(currentId)
#     players.append(player)

#     print("Created player, id:", currentId, datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))

#     threading.Thread(target=threaded_client, args=(conn, player,)).start()