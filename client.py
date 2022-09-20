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
            rays.append(Ray(-np.cos(a), -np.sin(a)))
        return rays


class Ray:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
        self.fov = 90
        self.render_resolution = 120
        self.render_distance = 2000

        
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("FPS client")
        # self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.font = pygame.font.SysFont("Arial", 18)
        
        self.player = Player(0, 1000, 300)
        
        self.enemy_list = []
        self.enemy_list.append(Player(0, 800, 500))
        
        self.world = World()
        
        
        
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.mouse_button = False
        self.left_pressed = False
        self.right_pressed = False
        self.speed = 4
        

    def run(self):
        self.running = True
        
        while self.running:
            self.update_keyboard()
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            # self.player.r = np.arctan2(self.player.y-self.mouse_y, self.player.x-self.mouse_x)
            
            
            self.update_player()
            self.render_frame()
            # self.dev_mode_render()
            
            pygame.display.flip()
            self.clock.tick(60)
        return False
    
    
    
    def update_player(self):
        self.player.rays = self.player.generate_rays(self.fov, self.render_resolution)
        self.Vx = 0
        self.Vy = 0
        if self.a_pressed and not self.d_pressed:
            self.Vx = -self.speed
        if self.d_pressed and not self.a_pressed:
            self.Vx = self.speed
        if self.w_pressed and not self.s_pressed:
            self.Vy = -self.speed
        if self.s_pressed and not self.w_pressed:
            self.Vy = self.speed
        if self.w_pressed and self.d_pressed:
            self.Vx, self.Vy = self.vectro_scale(self.speed, -self.speed, self.speed)
        if self.s_pressed and self.d_pressed:
            self.Vx, self.Vy = self.vectro_scale(self.speed, self.speed, self.speed)
        if self.s_pressed and self.a_pressed:
            self.Vx, self.Vy = self.vectro_scale(-self.speed, self.speed, self.speed)
        if self.w_pressed and self.a_pressed:
            self.Vx, self.Vy = self.vectro_scale(-self.speed, -self.speed, self.speed)
        
        if self.left_pressed and not self.right_pressed:
            self.player.r = self.player.r - 0.05
        if self.right_pressed and not self.left_pressed:
            self.player.r = self.player.r + 0.05
            
        _Vx = self.Vx*np.cos(self.player.r - np.pi/2) - self.Vy*np.sin(self.player.r - np.pi/2)
        _Vy = self.Vy*np.cos(self.player.r - np.pi/2) + self.Vx*np.sin(self.player.r - np.pi/2)
        
        self.Vx = _Vx
        self.Vy = _Vy
        
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
                    if event.key == pygame.K_LEFT:
                        self.left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        self.right_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.a_pressed = False
                    if event.key == pygame.K_d:
                        self.d_pressed = False
                    if event.key == pygame.K_w:
                        self.w_pressed = False
                    if event.key == pygame.K_s:
                        self.s_pressed = False
                    if event.key == pygame.K_LEFT:
                        self.left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        self.right_pressed = False
                if pygame.mouse.get_pressed()[0]:
                    self.mouse_button = True
                else:
                    self.mouse_button = False
    
    
    def render_frame(self):
        self.screen.fill((0,0,0))
        self.screen.fill((0,0,255), (0, self.screen_size[1]//2, self.screen_size[0], self.screen_size[1]//2))
        ray_lenghts = self.get_ray_lenghts()
        line_width = self.screen_size[0] / self.render_resolution
        for index, value in enumerate(ray_lenghts):
            line_height = int(self.map(value, 0, self.render_distance, self.screen_size[1], 0))
            brightness = line_height / self.screen_size[1]
            rect = pygame.Rect(line_width * index, (self.screen_size[1] - line_height) // 2, line_width, line_height)
            pygame.draw.rect(self.screen, np.array((255,255,255))*brightness, rect)
        self.screen.blit(self.update_fps(), (10, 10))
    
    
    def get_ray_lenghts(self):
        ray_lenghts = []
        for ray in self.player.rays:
            intersection_point = False
            for wall in self.world.walls:
                point = self.check_for_line_line_intersection((wall.A, wall.B), ((self.player.x, self.player.y), (ray.x * self.render_distance + self.player.x, ray.y * self.render_distance + self.player.y)))
                if point is not False:
                    if intersection_point is False:
                        intersection_point = point
                    elif self.get_distance((self.player.x, self.player.y), point) < self.get_distance((self.player.x, self.player.y), intersection_point):
                        intersection_point = point
            if intersection_point is not False:
                ray_lenght = self.get_distance((self.player.x, self.player.y), intersection_point)
                if ray_lenght <= self.render_distance:
                    ray_lenghts.append(self.get_distance((self.player.x, self.player.y), intersection_point))
                else:
                    ray_lenghts.append(self.render_distance)
            else:
                ray_lenghts.append(self.render_distance)
        return ray_lenghts
    
    
    def check_for_line_line_intersection(self, line1, line2):
        x1 = line1[0][0]
        x2 = line1[1][0]
        x3 = line2[0][0]
        x4 = line2[1][0]
        y1 = line1[0][1]
        y2 = line1[1][1]
        y3 = line2[0][1]
        y4 = line2[1][1]
        
        d = ((x1-x2) * (y3-y4) - (y1-y2) * (x3-x4))
        if d == 0:
            return False
        
        t = ((x1-x3) * (y3-y4) - (y1-y3) * (x3-x4)) / d
        u = -((x1-x2) * (y1-y3) - (y1-y2) * (x1-x3)) / d
        
        if t > 0 and t < 1 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        return False    
                    
    def dev_mode_render(self):
        self.screen.fill((0, 0, 0))   
        self.dev_blit_walls()
        self.dev_blit_rays()
        self.dev_blit_players()
        self.screen.blit(self.update_fps(), (10, 10))
    
    def dev_blit_rays(self):
        for ray in self.player.rays:
            intersection_point = False
            for wall in self.world.walls:
                point = self.check_for_line_line_intersection((wall.A, wall.B), ((self.player.x, self.player.y), (ray.x * self.render_distance + self.player.x, ray.y * self.render_distance + self.player.y)))
                if point is not False:
                    if intersection_point is False:
                        if self.get_distance((self.player.x, self.player.y), point) < self.render_distance:
                            intersection_point = point
                    elif self.get_distance((self.player.x, self.player.y), point) < self.get_distance((self.player.x, self.player.y), intersection_point):
                        intersection_point = point
                        
            if intersection_point != False:
                pygame.draw.line(self.screen, (0,0,255), (self.player.x, self.player.y), intersection_point)
            else:
                pygame.draw.line(self.screen, (0,0,255), (self.player.x, self.player.y), (ray.x * self.render_distance + self.player.x, ray.y * self.render_distance + self.player.y))
    
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
    
    def get_distance(self, p1, p2, sqrt=True):
        d = np.power(np.subtract(p1[0], p2[0]), 2) + np.power(np.subtract(p1[1], p2[1]), 2)
        if sqrt:
            d = np.sqrt(d)
        return d
        
    def map(self, v, fromMin, fromMax, toMin, toMax):
        fromSpan = fromMax - fromMin
        toSpan = toMax - toMin
        valueScaled = float(v - fromMin) / float(fromSpan)
        return toMin + (valueScaled * toSpan)
        


game = Game()
game.run()