# MultiplayerFPS - Python Raycasting Game

A multiplayer first-person shooter built with Python using raycasting for semi-3D rendering, similar to classic games like Wolfenstein 3D and Doom.

## Features

- **Real-time multiplayer gameplay** with TCP socket networking
- **Raycasting 3D renderer** with fisheye effect correction
- **Smooth wall sliding collision detection**
- **Mini-map with real-time player positions**
- **Shooting mechanics** with hit detection and damage
- **Health system** with visual hit markers
- **Custom map support** via text files
- **Performance optimizations** with configurable render quality

## Screenshots

<img width="1200" height="733" alt="image" src="https://github.com/user-attachments/assets/bb1a9ccc-3451-4059-ae88-1e2df378a8a5" />
<img width="1200" height="733" alt="image" src="https://github.com/user-attachments/assets/944a2f1b-d2bd-4adc-a543-e779ae4b546a" />


## Requirements

- Python 3.7+
- pygame
- numpy

## Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install pygame numpy
```

3. Ensure you have the required game assets:
   - `game/background.png` - Sky/background texture
   - `game/hit.wav` - Hit sound effect

## Quick Start

### Starting the Server

```bash
# Start server on default port 8080 with default map
python server.py

# Start server on custom port with custom map
python server.py 9999 map_2.txt
```

### Connecting as Client

```bash
# Connect to server
python client.py <server_ip> <server_port>

# Example: Connect to local server
python client.py localhost 8080
```

## Controls

| Key/Input | Action |
|-----------|--------|
| **W/A/S/D** | Move forward/left/backward/right |
| **Arrow Keys** | Look left/right |
| **Mouse** | Look around (FPS-style mouse look) |
| **Left Click** | Shoot |
| **Space** | Shoot |
| **ESC** | Toggle mouse cursor / Exit game |

## Game Mechanics

### Movement
- **WASD movement** with smooth wall sliding
- **Mouse look** with adjustable sensitivity
- **Collision detection** prevents walking through walls

### Combat
- **Hitscan shooting** - instant hit detection
- **Damage system** with 10 damage per hit
- **Health system** starting at 100 HP
- **Kill tracking** for scoring

### Networking
- **TCP socket communication** for reliable data transfer
- **Real-time synchronization** of player positions and actions
- **Lag compensation** with ping display


## Map Format

Maps are defined in text files using a simple grid format:
- `1` = Wall
- `0` = Empty space

Example map file (`maps/map_1.txt`):
```
1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 1
1 0 1 0 0 1 0 1
1 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1
```

## Configuration

### Game Settings (in `Game.py`)
- `screen_size`: Window resolution (default: 1200x700)
- `fps_limit`: Frame rate limit (0 = unlimited)
- `fov`: Field of view in radians (default: 1.4)
- `render_scale`: Rendering quality (0.5-1.0, lower = better performance)

### Engine Settings (in `Engine.py`)
- `render_distance`: Maximum view distance
- `num_rays`: Ray count for rendering (affects quality)

### Player Settings (in `Player.py`)
- `speed`: Movement speed
- `rotation_speed`: Look sensitivity
- `hit_damage`: Damage per shot
- `health`: Starting health

## Development

### Adding New Features
1. **New controls**: Add to `handle_input()` in `Game.py`
2. **Game mechanics**: Modify `update()` method
3. **Rendering effects**: Edit `Engine.py` render methods
4. **Network data**: Update pickle serialization in client/server

### Creating Custom Maps
1. Create a new text file in `maps/` directory
2. Use `1` for walls, `0` for empty space
3. Ensure rectangular grid format
4. Start server with: `python server.py <port> <map_filename>`
