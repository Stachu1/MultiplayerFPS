import pygame, numpy as np

class Engine:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fov = np.pi / 3  # 60 degrees field of view
        self.num_rays = screen_width // 10  # Ray resolution
        self.max_depth = 15  # Maximum render distance
        self.distance_resolution = 0.1
        self.background = pygame.transform.scale(pygame.image.load('background.png'), (self.screen_width, self.screen_height))
    
    
    def cast_ray(self, world, start_x, start_y, angle):
        # Ray casting using DDA algorithm
        sin_a = np.sin(angle)
        cos_a = np.cos(angle)
        
        for depth in range(0, int(self.max_depth / self.distance_resolution)):
            target_x = start_x + depth * cos_a * self.distance_resolution
            target_y = start_y + depth * sin_a * self.distance_resolution
            
            if world.is_wall(target_x, target_y):
                return depth * self.distance_resolution, target_x, target_y
        
        # Return max depth with end position
        end_x = start_x + self.max_depth * cos_a
        end_y = start_y + self.max_depth * sin_a
        return self.max_depth, end_x, end_y
    
    
    def render(self, screen, player, world):
        # Clear screen
        screen.blit(self.background, (0, 0))
        
        # Cast rays and draw walls
        self.ray_data = []  # Store ray data for debug rendering
        
        for ray_id in range(self.num_rays):
            # Calculate ray angle
            ray_angle = player.angle - self.fov / 2 + (ray_id / self.num_rays) * self.fov
            
            # Cast ray
            distance, hit_x, hit_y = self.cast_ray(world, player.x, player.y, ray_angle)
            
            # Store ray data for debug view
            self.ray_data.append({
                'angle': ray_angle,
                'distance': distance,
                'hit_x': hit_x,
                'hit_y': hit_y
            })
            
            # Fix fisheye effect
            distance *= np.cos(ray_angle - player.angle)
            
            # Calculate wall height
            wall_height = min(self.screen_height, self.screen_width / (distance + 0.0001))
            
            # Calculate wall color based on distance (darker = farther)
            color_intensity = max(0.05, 1 - distance / self.max_depth)
            wall_color = (int(255 * color_intensity), int(255 * color_intensity), int(255 * color_intensity))
            
            # Draw wall slice
            wall_x = ray_id * (self.screen_width / self.num_rays)
            wall_y = (self.screen_height - wall_height) / 2
            wall_width = self.screen_width / self.num_rays + 1
            
            pygame.draw.rect(screen, wall_color, (wall_x, wall_y, wall_width, wall_height))
    
    
    def render_debug(self, screen, player_id, all_players, world, debug_size=200):
        # Draw debug view in top-right corner
        debug_x = self.screen_width - debug_size - 10
        debug_y = 10
        
        # Scale factor to fit the world in the debug view
        scale = debug_size / 16  # 16 is the grid size
        
        # Draw debug background
        pygame.draw.rect(screen, (50, 50, 50), (debug_x, debug_y, debug_size, debug_size))
        
        # Draw grid and walls
        for y in range(len(world.map)):
            for x in range(len(world.map[0])):
                if world.map[y][x] == 1:  # Wall
                    wall_rect = pygame.Rect(
                        debug_x + x * scale+1,
                        debug_y + y * scale+1,
                        scale-1,
                        scale-1
                    )
                    pygame.draw.rect(screen, (255, 255, 255), wall_rect)
        
        for player in all_players:
            # Draw player
            player_debug_x = debug_x + player.x * scale
            player_debug_y = debug_y + player.y * scale
            pygame.draw.circle(screen, (0, 255, 0), (int(player_debug_x), int(player_debug_y)), 3)
            
            # Draw player direction
            dir_end_x = player_debug_x + np.cos(player.angle) * 20
            dir_end_y = player_debug_y + np.sin(player.angle) * 20
            pygame.draw.line(screen, (0, 255, 0), (player_debug_x, player_debug_y), (dir_end_x, dir_end_y), 2)
            
            # Draw rays if we have ray data
            if player.id == player_id and hasattr(self, 'ray_data'):
                for ray in self.ray_data:
                    # Draw ray line
                    ray_end_x = debug_x + ray['hit_x'] * scale
                    ray_end_y = debug_y + ray['hit_y'] * scale
                    pygame.draw.line(screen, (0, 0, 255), (player_debug_x, player_debug_y), (ray_end_x, ray_end_y), 1)
                    
                    # Draw hit point
                    pygame.draw.circle(screen, (255, 0, 0), (int(ray_end_x), int(ray_end_y)), 2)
