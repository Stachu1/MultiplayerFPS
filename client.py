import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import numpy as np
import pygame
import math


class Player:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle  # Player's viewing angle in radians
        self.speed = 0.1
        self.rotation_speed = 0.05
        
    def move_forward(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
    
    def move_backward(self):
        self.x -= math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
    
    def strafe_left(self):
        self.x += math.cos(self.angle - math.pi/2) * self.speed
        self.y += math.sin(self.angle - math.pi/2) * self.speed
    
    def strafe_right(self):
        self.x += math.cos(self.angle + math.pi/2) * self.speed
        self.y += math.sin(self.angle + math.pi/2) * self.speed
    
    def rotate_left(self):
        self.angle -= self.rotation_speed
    
    def rotate_right(self):
        self.angle += self.rotation_speed


class World:
    def __init__(self):
        # Simple grid-based map (1 = wall, 0 = empty space)
        self.grid = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1],
            [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.cell_size = 1  # Size of each grid cell in pixels
    
    def is_wall(self, x, y):
        # Convert world coordinates to grid coordinates
        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)
        
        # Check bounds
        if grid_x < 0 or grid_x >= len(self.grid[0]) or grid_y < 0 or grid_y >= len(self.grid):
            return True  # Treat out of bounds as walls
        
        return self.grid[grid_y][grid_x] == 1


class Renderer:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fov = math.pi / 3  # 60 degrees field of view
        self.num_rays = screen_width // 2  # Ray resolution
        self.max_depth = 15  # Maximum render distance
        
    def cast_ray(self, world, start_x, start_y, angle):
        # Ray casting using DDA algorithm
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        
        for depth in range(0, self.max_depth, 2):
            target_x = start_x + depth * cos_a
            target_y = start_y + depth * sin_a
            
            if world.is_wall(target_x, target_y):
                return depth
        
        return self.max_depth
    
    def render_3d(self, screen, player, world):
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw sky
        sky_color = (135, 206, 235)  # Light blue
        pygame.draw.rect(screen, sky_color, (0, 0, self.screen_width, self.screen_height // 2))
        
        # Draw floor
        floor_color = (34, 139, 34)  # Forest green
        pygame.draw.rect(screen, floor_color, (0, self.screen_height // 2, self.screen_width, self.screen_height // 2))
        
        # Cast rays and draw walls
        for ray_id in range(self.num_rays):
            # Calculate ray angle
            ray_angle = player.angle - self.fov / 2 + (ray_id / self.num_rays) * self.fov
            
            # Cast ray
            distance = self.cast_ray(world, player.x, player.y, ray_angle)
            
            # Fix fisheye effect
            distance *= math.cos(ray_angle - player.angle)
            
            # Calculate wall height
            wall_height = min(self.screen_height, self.screen_height / (distance + 0.0001))
            
            # Calculate wall color based on distance (darker = farther)
            color_intensity = max(0.1, 1 - distance / self.max_depth)
            wall_color = (int(255 * color_intensity), int(255 * color_intensity), int(255 * color_intensity))
            
            # Draw wall slice
            wall_x = ray_id * (self.screen_width / self.num_rays)
            wall_y = (self.screen_height - wall_height) / 2
            wall_width = self.screen_width / self.num_rays + 1
            
            pygame.draw.rect(screen, wall_color, (wall_x, wall_y, wall_width, wall_height))


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("MultiplayerFPS")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        
        # Initialize game objects
        self.player = Player(1, 1, 0)  # Start player at position (200, 200)
        self.world = World()
        self.renderer = Renderer(self.screen_width, self.screen_height)
        
        # Input state
        self.keys_pressed = {
            'w': False, 'a': False, 's': False, 'd': False,
            'left': False, 'right': False
        }
        
        # Mouse settings
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mouse_sensitivity = 0.002
        
        self.running = True
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_w:
                    self.keys_pressed['w'] = True
                elif event.key == pygame.K_a:
                    self.keys_pressed['a'] = True
                elif event.key == pygame.K_s:
                    self.keys_pressed['s'] = True
                elif event.key == pygame.K_d:
                    self.keys_pressed['d'] = True
                elif event.key == pygame.K_LEFT:
                    self.keys_pressed['left'] = True
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed['right'] = True
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.keys_pressed['w'] = False
                elif event.key == pygame.K_a:
                    self.keys_pressed['a'] = False
                elif event.key == pygame.K_s:
                    self.keys_pressed['s'] = False
                elif event.key == pygame.K_d:
                    self.keys_pressed['d'] = False
                elif event.key == pygame.K_LEFT:
                    self.keys_pressed['left'] = False
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed['right'] = False
            
            elif event.type == pygame.MOUSEMOTION:
                # Mouse look
                mouse_dx = event.rel[0]
                self.player.angle += mouse_dx * self.mouse_sensitivity
    
    def update(self):
        # Store old position for collision detection
        old_x, old_y = self.player.x, self.player.y
        
        # Handle movement
        if self.keys_pressed['w']:
            self.player.move_forward()
        if self.keys_pressed['s']:
            self.player.move_backward()
        if self.keys_pressed['a']:
            self.player.strafe_left()
        if self.keys_pressed['d']:
            self.player.strafe_right()
        
        # Handle rotation (arrow keys)
        if self.keys_pressed['left']:
            self.player.rotate_left()
        if self.keys_pressed['right']:
            self.player.rotate_right()
        
        # Simple collision detection
        if self.world.is_wall(self.player.x, self.player.y):
            self.player.x, self.player.y = old_x, old_y
    
    def render(self):
        self.renderer.render_3d(self.screen, self.player, self.world)
        
        # Draw FPS
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(f"FPS: {fps}", True, pygame.Color("white"))
        self.screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            print(self.player.x, self.player.y, self.player.angle)
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()