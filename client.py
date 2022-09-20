from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time, os, numpy as np, random, sys, copy, pygame, pickle
from PIL import Image, ImageDraw
from struct import unpack
from colorama import Fore, init
init()




class Player:
    def __init__(self, id, x, y, r=0):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.Vx = 0
        self.Vy = 0
        self.size = 0.5
    
    def generate_rays(self, fov, resolution):
        fov = np.deg2rad(fov)
        rays = []
        ray2ray_angle = fov/(resolution - 1)
        for ray_id in range(resolution):
            a = (self.r - fov / 2) + ray2ray_angle * ray_id
            x = -np.cos(a)
            y = -np.sin(a)
            ray = np.array((x, y), dtype=np.float)
            rays.append(ray)
        return rays


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
        self.render_resolution = 31
        self.render_distance = 1500

        
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("FPS client")
        # self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.font = pygame.font.SysFont("Arial", 18)
        
        self.player = Player(0, 500, 500)
        
        self.enemy_list = []
        self.enemy_list.append(Player(0, 800, 500))
        
        self.world = World()
        
        
        
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.mouse_button = False
        self.speed = 4
        

    def run(self):
        self.running = True
        
        while self.running:
            self.update_keyboard()
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            self.player.r = np.arctan2(self.player.y-self.mouse_y, self.player.x-self.mouse_x)
            
                
            self.update_player()
            self.dev_mode_render()
            
            pygame.display.flip()
            self.clock.tick(60)
        return False
    
    
    
    def update_player(self):
        self.player.rays = self.player.generate_rays(self.fov, self.render_resolution)
        
        self.Vx = 0
        self.Vy = 0
        if self.a_pressed and not self.d_pressed and self.player.x >= 0:
            self.Vx = -self.speed
        if self.d_pressed and not self.a_pressed and self.player.x <= self.screen.get_width():
            self.Vx = self.speed
        if self.w_pressed and not self.s_pressed and self.player.y >= 0:
            self.Vy = -self.speed
        if self.s_pressed and not self.w_pressed and self.player.y <= self.screen.get_height():
            self.Vy = self.speed
        if self.w_pressed and self.d_pressed and self.player.y >= 0 and self.player.x <= self.screen.get_width():
            self.Vx, self.Vy = self.vectro_scale(self.speed, -self.speed, self.speed)
        if self.s_pressed and self.d_pressed and self.player.y <= self.screen.get_height() and self.player.x <= self.screen.get_width():
            self.Vx, self.Vy = self.vectro_scale(self.speed, self.speed, self.speed)
        if self.s_pressed and self.a_pressed and self.player.y <= self.screen.get_height() and self.player.x >= 0:
            self.Vx, self.Vy = self.vectro_scale(-self.speed, self.speed, self.speed)
        if self.w_pressed and self.a_pressed and self.player.y >= 0 and self.player.x >= 0:
            self.Vx, self.Vy = self.vectro_scale(-self.speed, -self.speed, self.speed)

        self.player.x += self.Vx
        self.player.y += self.Vy
    
    
    def update_keyboard(self):
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
                    if event.key == pygame.K_a:
                        self.a_pressed = True
                    if event.key == pygame.K_d:
                        self.d_pressed = True
                    if event.key == pygame.K_w:
                        self.w_pressed = True
                    if event.key == pygame.K_s:
                        self.s_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.a_pressed = False
                    if event.key == pygame.K_d:
                        self.d_pressed = False
                    if event.key == pygame.K_w:
                        self.w_pressed = False
                    if event.key == pygame.K_s:
                        self.s_pressed = False
                if pygame.mouse.get_pressed()[0]:
                    self.mouse_button = True
                else:
                    self.mouse_button = False
                    
    
    def dev_mode_render(self):
        self.screen.fill((0, 0, 0))   
        self.dev_blit_walls()
        self.dev_blit_players()
        self.dev_blit_rays()
        self.screen.blit(self.update_fps(), (10, 10))
    
    
    def dev_blit_rays(self):
        for ray in self.player.rays:
            ray = ray*self.render_distance
            pygame.draw.line(self.screen, (0,0,255), (self.player.x, self.player.y), (ray[0] + self.player.x, ray[1] + self.player.y))
        pygame.draw.line(self.screen, (255,0,0), (self.player.x, self.player.y), (-np.cos(self.player.r)*self.render_distance + self.player.x, -np.sin(self.player.r)*self.render_distance + self.player.y))
    
    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(f"FPS: {fps}", 1, pygame.Color("white"))
        return fps_text
    
    def dev_blit_players(self):
        pygame.draw.circle(self.screen, (0,255,0), (self.player.x, self.player.y), 10, 10)
        for enemy in self.enemy_list:
            pygame.draw.circle(self.screen, (255,0,0), (enemy.x, enemy.y), 10, 10)
        return True
    
    def dev_blit_walls(self):
        for wall in self.world.walls:
            pygame.draw.line(self.screen, (255,255,255), (wall.x1, wall.y1), (wall.x2, wall.y2))
        return True
    
    def vectro_scale(self, x, y, r):
        v_l = (x**2 + y**2)**0.5
        if v_l == 0:
            return 0, 0
        return x*r / v_l, y*r / v_l
        
        


game = Game()
game.run()