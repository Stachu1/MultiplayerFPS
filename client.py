from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time, os, numpy as np, random, sys, copy, pygame, pickle
from PIL import Image, ImageDraw
from struct import unpack
from colorama import Fore, init
init()




class Player:
    def __init__(self, id, x, y, r):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
    
    def generate_rays(self, fov, resolution):
        rays = []


class World:
    def __init__(self):
        self.walls = [Wall(100, 100, 100, 400), Wall(100,400, 600,400), Wall(200,200, 300, 300)]


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.A = (x1, y1)
        self.B = (x2, y2)



class Game:
    def __init__(self):
        self.screen_size = (1200,800)
        self.fov = 100
        self.render_resolution = 400

        
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("FPS client")
        # self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.font = pygame.font.SysFont("Arial", 18)

        # self.network = Network("127.0.0.1", 6968)
        # id, x, y, color = self.network.connect()
        # print(f"Identity: {id} {x} {y} {color}")
        
        self.player = Player(0, 500, 500, 10)
        
        self.enemy_list = []
        self.enemy_list.append(Player(0, 800, 500, 10))
        
        
        self.world = World()
        

    def run(self):
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        exit()
                        
                if pygame.mouse.get_pressed()[0]:
                    self.mouse_button = True
                else:
                    self.mouse_button = False


            self.screen.fill((0, 0, 0))            
        
            self.screen.blit(self.update_fps(), (10, 10))
            self.blit_players()
            self.blit_walls()
            
            pygame.display.flip()
            self.clock.tick(60)

    
    
    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(f"FPS: {fps}", 1, pygame.Color("white"))
        return fps_text

    
    def blit_players(self):
        pygame.draw.circle(self.screen, (0,255,0), (self.player.x, self.screen_size[1] - self.player.y), 10, 10)
        for enemy in self.enemy_list:
            pygame.draw.circle(self.screen, (255,0,0), (enemy.x, self.screen_size[1] - enemy.y), 10, 10)
        return True
    
    def blit_walls(self):
        for wall in self.world.walls:
            pygame.draw.line(self.screen, (255,255,255), (wall.x1, self.screen_size[1] - wall.y1), (wall.x2, self.screen_size[1] - wall.y2))
        return True
        
        


game = Game()
game.run()