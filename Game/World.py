import random

class World:
    def __init__(self):
        # Simple grid-based map (1 = wall, 0 = empty space)
        self.map = [
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
    
    
    def load(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.map = []
            for line in lines:
                row = [int(char) for char in line.strip().replace(' ', '')]
                self.map.append(row)
    
    
    def random_spawn(self):
        empty_cells = [(x, y) for y in range(len(self.map)) for x in range(len(self.map[0])) if self.map[y][x] == 0]
        if not empty_cells:
            raise ValueError("No empty cells available for spawning")
        return random.choice(empty_cells)
    
    
    def is_wall(self, x, y):
        grid_x = int(x)
        grid_y = int(y)
        
        # Check bounds
        if grid_x < 0 or grid_x >= len(self.map[0]) or grid_y < 0 or grid_y >= len(self.map):
            return True  # Treat out of bounds as walls
        
        return self.map[grid_y][grid_x] == 1
