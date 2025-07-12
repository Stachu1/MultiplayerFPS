import pygame, numpy as np
from Game.Player import Player
from Game.World import World
from Game.Engine import Engine


class Game:
    def __init__(self, screen_size=(1200, 700), fps_target=60):
        pygame.init()
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.fps_target = fps_target
        self.ping = 999
        self.hit_mark_frame = 0
        self.all_players = []
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption('MultiplayerFPS')
        self.font = pygame.font.SysFont('Arial', 18)
        self.clock = pygame.time.Clock()
        self.hit_sound = pygame.mixer.Sound('game/hit.wav')
        
        # Initialize game objects
        self.player = Player()
        self.world = World()
        self.engine = Engine(self.screen_width, self.screen_height)
        
        # Input state
        self.keys_pressed = {
            'w': False, 'a': False, 's': False, 'd': False,
            'left': False, 'right': False, 'mouse_left': False,
            'shoot': False, 'space': False
        }
        
        # Mouse settings
        self.mouse_visible = False
        pygame.mouse.set_visible(self.mouse_visible)
        pygame.event.set_grab(not self.mouse_visible)
        self.mouse_sensitivity = 0.002
        
        self.running = True
    
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.mouse_visible:
                        self.running = False
                    else:
                        self.mouse_visible = True
                        pygame.mouse.set_visible(self.mouse_visible)
                        pygame.event.set_grab(not self.mouse_visible)
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
                elif event.key == pygame.K_SPACE:
                    self.keys_pressed['space'] = True
                    self.keys_pressed['shoot'] = True
            
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
                elif event.key == pygame.K_SPACE:
                    self.keys_pressed['space'] = False
            
            elif event.type == pygame.MOUSEMOTION:
                # Mouse look
                mouse_dx = event.rel[0]
                self.player.angle += mouse_dx * self.mouse_sensitivity
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.keys_pressed['mouse_left'] = True
                    self.keys_pressed['shoot'] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.keys_pressed['mouse_left'] = False
                    if self.mouse_visible:
                        self.mouse_visible = False
                        pygame.mouse.set_visible(self.mouse_visible)
                        pygame.event.set_grab(not self.mouse_visible)
    
    
    def update(self, current_fps=60):
        # Store old position for collision detection
        old_x, old_y = self.player.x, self.player.y
        
        current_fps = self.clock.get_fps()
        speed_sacle = 60 / current_fps if current_fps > 0 else 1
        
        # Calculate movement deltas
        dx, dy = 0, 0
        
        # Handle movement
        if self.keys_pressed['w']:
            dx += np.cos(self.player.angle) * self.player.speed * speed_sacle
            dy += np.sin(self.player.angle) * self.player.speed * speed_sacle
        if self.keys_pressed['s']:
            dx -= np.cos(self.player.angle) * self.player.speed * speed_sacle
            dy -= np.sin(self.player.angle) * self.player.speed * speed_sacle
        if self.keys_pressed['a']:
            dx += np.cos(self.player.angle - np.pi/2) * self.player.speed * speed_sacle
            dy += np.sin(self.player.angle - np.pi/2) * self.player.speed * speed_sacle
        if self.keys_pressed['d']:
            dx += np.cos(self.player.angle + np.pi/2) * self.player.speed * speed_sacle
            dy += np.sin(self.player.angle + np.pi/2) * self.player.speed * speed_sacle
        
        # Handle rotation (arrow keys)
        if self.keys_pressed['left']:
            self.player.angle -= self.player.rotation_speed
        if self.keys_pressed['right']:
            self.player.angle += self.player.rotation_speed
        
        # Try moving on X axis
        self.player.x += dx
        if self.world.is_wall(self.player.x, self.player.y):
            self.player.x = old_x  # Revert X movement if hitting wall
        
        # Try moving on Y axis
        self.player.y += dy
        if self.world.is_wall(self.player.x, self.player.y):
            self.player.y = old_y  # Revert Y movement if hitting wall
        
        # Handle shooting logic here
        if self.keys_pressed['shoot']:
            self.keys_pressed['shoot'] = False
            hit_info = self.engine.cast_ray_for_players(self.player.x, self.player.y, self.player.angle, self.all_players, exclude_player_id=self.player.id)
            if hit_info is not None:
                distance_target, _, _, target = hit_info
                distance_wall, _, _ = self.engine.cast_ray(self.world, self.player.x, self.player.y, self.player.angle)
                if distance_target < distance_wall:
                    self.player.damage_given += self.player.hit_damage
                    self.player.damage_queue.append({'id': target.id, 'damage': self.player.hit_damage})
                    self.hit_mark_frame = 5
                    self.hit_sound.play()
    
    
    def render(self):
        self.engine.render(self.screen, self.player, self.all_players, self.world)
        
        # Draw debug top-down view
        self.engine.render_debug(self.screen, self.player.id, self.all_players, self.world)
        
        # Draw FPS
        fps = str(int(self.clock.get_fps()))
        info = self.font.render(f'{fps} fps   {self.ping:.2f} ms', True, (255, 0, 0))
        self.screen.blit(info, (10, 10))
        
        # Draw position debug info
        pos_text = self.font.render(f'x: {self.player.x:.2f} y: {self.player.y:.2f}', True, (0, 255, 255))
        self.screen.blit(pos_text, (10, 30))
        
        # Draw HP
        color = (0, 255, 0) if self.player.health > 50 else (255, 255, 0) if self.player.health > 20 else (255, 0, 0)
        pos_text = self.font.render(f'HP: {int(self.player.health)}', True, color)
        self.screen.blit(pos_text, (10, self.screen_height - 30))
        
        # Draw crosshair
        if self.hit_mark_frame:
            self.hit_mark_frame -= 1
            size = 10 - self.hit_mark_frame
            pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width // 2 - size - 1, self.screen_height // 2 - size - 1), (self.screen_width // 2 + size, self.screen_height // 2 + size), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width // 2 - size - 1, self.screen_height // 2 + size - 1), (self.screen_width // 2 + size, self.screen_height // 2 - size), 2)
        
        pygame.draw.circle(self.screen, (0, 0, 0), (self.screen_width // 2, self.screen_height // 2), 3)
        pygame.draw.circle(self.screen, (255, 0, 0), (self.screen_width // 2, self.screen_height // 2), 2)
        
        pygame.display.flip()
    

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(self.fps_target)
            
            if self.player.health <= 0:
                print(f'\33[31mYou died!\33[0m\nKills: {self.player.kills}\nDamage: {self.player.damage_given}')
                self.running = False
        
        pygame.quit()
