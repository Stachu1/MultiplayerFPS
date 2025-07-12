import pygame, numpy as np
from Game.Player import Player
from Game.World import World
from Game.Engine import Engine


class Game:
    def __init__(self, screen_size=(1200, 700), fps_target=60, ):
        pygame.init()
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.fps_target = fps_target
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("MultiplayerFPS")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        
        # Initialize game objects
        self.player = Player(1.5, 1.5, 0)
        self.world = World()
        self.engine = Engine(self.screen_width, self.screen_height)
        
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
        
        speed_sacle = 60 / self.clock.get_fps() if self.clock.get_fps() > 0 else 1
        
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
            self.player.rotate_left()
        if self.keys_pressed['right']:
            self.player.rotate_right()
        
        # Wall sliding collision detection
        # Try moving on X axis first
        self.player.x += dx
        if self.world.is_wall(self.player.x, self.player.y):
            self.player.x = old_x  # Revert X movement if hitting wall
        
        # Then try moving on Y axis
        self.player.y += dy
        if self.world.is_wall(self.player.x, self.player.y):
            self.player.y = old_y  # Revert Y movement if hitting wall
    
    
    def render(self):
        self.engine.render(self.screen, self.player, self.world)
        
        # Draw debug top-down view
        self.engine.render_debug(self.screen, self.player, self.world)
        
        # Draw FPS
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(f"FPS: {fps}", True, (255, 0, 0))
        self.screen.blit(fps_text, (10, 10))
        
        # Draw position debug info
        pos_text = self.font.render(f"x: {self.player.x:.2f} y: {self.player.y:.2f}", True, (0, 255, 255))
        self.screen.blit(pos_text, (10, 30))
        
        pygame.display.flip()
    

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            # self.clock.tick(self.fps_target)
            self.clock.tick()
        
        pygame.quit()