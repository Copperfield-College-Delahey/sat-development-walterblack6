import pygame
import os
import random
from typing import Dict, Tuple  # For type hints
from item import create_health_potion, create_sword, create_key, create_armor

# Map generation parameters
MAP_WIDTH = 30
MAP_HEIGHT = 25
BOSS_ROOM_WIDTH = 8
BOSS_ROOM_HEIGHT = 6

# Track opened chests
opened_chests = set()

def is_chest_opened(x, y):
    # Check if a chest at the given position has been opened
    return (x, y) in opened_chests

def mark_chest_opened(x, y):
    # Mark a chest as opened
    opened_chests.add((x, y))

def reset_chests():
    # Reset all chests to unopened state
    opened_chests.clear()

def generate_maze(width, height):
    # Generate a random maze using a recursive backtracking algorithm
    # Initialize maze with walls
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve_path(x, y):
        # Recursively carve paths through the maze
        maze[y][x] = 0
        # Define directions: up, right, down, left
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 < new_x < width - 1 and 0 < new_y < height - 1 and 
                maze[new_y][new_x] == 1):
                # Carve path between current cell and new cell
                maze[y + dy//2][x + dx//2] = 0
                maze[new_y][new_x] = 0
                carve_path(new_x, new_y)
    
    # Start carving from a random odd position
    start_x = random.randrange(1, width - 1, 2)
    start_y = random.randrange(1, height - 1, 2)
    carve_path(start_x, start_y)
    # Ensure starting area is clear (top-left corner)
    maze[1][1] = 0
    maze[1][2] = 0
    maze[2][1] = 0
    return maze

def add_chests_to_maze(maze, num_chests=15):
    # Add chests to random floor tiles in the maze
    floor_positions = [(x, y) for y in range(len(maze)) for x in range(len(maze[0])) if maze[y][x] == 0]
    if len(floor_positions) > num_chests:
        chest_positions = random.sample(floor_positions, num_chests)
        for x, y in chest_positions:
            maze[y][x] = 2  # Set to chest tile
    return maze

def create_boss_room(maze):
    # Add a boss room at the end of the maze
    # Find the rightmost floor tile to place the boss room entrance
    entrance_x = 0
    entrance_y = 0
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 0 and x > entrance_x:
                entrance_x = x
                entrance_y = y
    # Create boss room entrance
    maze[entrance_y][entrance_x] = 3  # Entrance to boss room
    boss_room_start_x = entrance_x + 1
    # Extend maze to accommodate boss room
    for row in maze:
        row.extend([1] * BOSS_ROOM_WIDTH)
    # Create boss room floor
    for y in range(len(maze)):
        for x in range(boss_room_start_x, len(maze[0])):
            if y < len(maze) - 2:  # Leave walls at top and bottom
                maze[y][x] = 4  # Boss room floor
    # Add boss in the center of the boss room
    boss_x = boss_room_start_x + BOSS_ROOM_WIDTH // 2
    boss_y = len(maze) // 2
    maze[boss_y][boss_x] = 5  # Boss tile
    # Add final goal at the far right of the boss room
    goal_x = len(maze[0]) - 2
    goal_y = len(maze) // 2
    maze[goal_y][goal_x] = 6  # Final goal tile
    return maze

def generate_map():
    # Generate a complete random map with maze, chests, and boss room
    maze = generate_maze(MAP_WIDTH, MAP_HEIGHT)
    maze = add_chests_to_maze(maze, num_chests=20)
    maze = create_boss_room(maze)
    return maze

# Generate the initial map
tile_map = generate_map()

# Define colours for tile types (used if no sprite is available)
colours = {
    4: (200, 0, 200),   # Boss room floor (purple)
    5: (255, 0, 0),     # Boss (red)
    6: (0, 255, 0),     # Final goal (green)
}

TILE_SIZE = 64  # Size of each tile in pixels

def load_sprite(filename):
    # Load a sprite from the assets/sprites folder and resize to TILE_SIZE
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "assets", "sprites", filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

# Lazy-load sprites
chest_img = None
goal_img = None
floor_img = None
wall_img = None
boss_img = None
boss_floor_img = None

def draw_map(screen, tile_map_param: list[list[int]] | None = None, camera_x: float = 0, camera_y: float = 0) -> None:
    # Draw the map with a given camera offset
    global chest_img, goal_img, wall_img, floor_img, boss_img, boss_floor_img, tile_map
    if tile_map_param is None:
        tile_map_param = tile_map
    if chest_img is None or goal_img is None or wall_img is None or floor_img is None:
        chest_img = load_sprite("chest.png")
        goal_img = load_sprite("goal.png")
        floor_img = load_sprite("floor.png")
        wall_img = load_sprite("wall.png")
    if boss_img is None:
        try:
            boss_img = load_sprite("boss.png")
        except:
            boss_img = None
    if boss_floor_img is None:
        try:
            boss_floor_img = load_sprite("boss_floor.png")
        except:
            boss_floor_img = None
    # Draw each tile based on its type
    for y, row in enumerate(tile_map_param):
        for x, tile in enumerate(row):
            pos = (x * TILE_SIZE - int(camera_x), y * TILE_SIZE - int(camera_y))
            if tile == 2:
                screen.blit(chest_img, pos)
            elif tile == 3:
                screen.blit(goal_img, pos)
            elif tile == 0:
                screen.blit(floor_img, pos)
            elif tile == 1:
                screen.blit(wall_img, pos)
            elif tile == 4:
                if boss_floor_img:
                    screen.blit(boss_floor_img, pos)
                else:
                    pygame.draw.rect(screen, colours[4], pygame.Rect(*pos, TILE_SIZE, TILE_SIZE))
            elif tile == 5:
                if boss_img:
                    screen.blit(boss_img, pos)
                else:
                    pygame.draw.rect(screen, colours[5], pygame.Rect(*pos, TILE_SIZE, TILE_SIZE))
            elif tile == 6:
                screen.blit(goal_img, pos)
            else:
                pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(*pos, TILE_SIZE, TILE_SIZE))

def can_move(x: int, y:int) -> bool:
    # Check if player can move to a specific position (not a wall)
    global tile_map
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    if tile_y < 0 or tile_y >= len(tile_map) or tile_x < 0 or tile_x >= len(tile_map[0]):
        return False
    tile_type = tile_map[tile_y][tile_x]
    if tile_type == 1:  # Wall
        return False
    return True

def get_tile(x, y):
    # Get the tile type at a specific position
    global tile_map
    return tile_map[y // TILE_SIZE][x // TILE_SIZE]

def regenerate_map():
    # Generate a new random map and reset chest states
    global tile_map, chest_img, goal_img, floor_img, wall_img, boss_img
    tile_map = generate_map()
    reset_chests()
    chest_img = None
    goal_img = None
    floor_img = None
    wall_img = None
    boss_img = None
    print(f"Map regenerated. New dimensions: {len(tile_map[0])}x{len(tile_map)}")
    print(f"Starting area tile: {tile_map[1][1]}")

def validate_player_position(player_x, player_y):
    # Validate that the player position is within bounds and not on a wall
    global tile_map
    tile_x = player_x // TILE_SIZE
    tile_y = player_y // TILE_SIZE
    if tile_y < 0 or tile_y >= len(tile_map) or tile_x < 0 or tile_x >= len(tile_map[0]):
        return False
    tile_type = tile_map[tile_y][tile_x]
    return tile_type != 1

def debug_collision(x, y):
    # Debug function to check collision at a given pixel position
    global tile_map
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    print(f"Debug collision at ({x}, {y}) -> tile ({tile_x}, {tile_y}) -> type {tile_map[tile_y][tile_x]}")
    return can_move(x, y)

def get_random_item():
    # Return a random item for chest contents
    items = [
        create_health_potion,
        create_sword,
        create_key,
        create_armor
    ]
    weights = [0.4, 0.3, 0.2, 0.1]  # Weighted probabilities
    creator_func = random.choices(items, weights=weights, k=1)[0]
    return creator_func()
