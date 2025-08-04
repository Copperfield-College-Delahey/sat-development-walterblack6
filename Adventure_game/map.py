import pygame
import os
from typing import Dict, Tuple  # For type hints

tile_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 2, 1, 0, 1, 3, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Define colours for unknown tile types
colours = {
    4: (0, 255, 0),   # Example: green for tile type 4
    5: (0, 0, 255),   # Example: blue for tile type 5
    # Add more tile type colors as needed
}

TILE_SIZE = 64  # Size of each tile in pixels

def load_sprite(filename):
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "assets", "sprites", filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

# Lazy-load sprites
chest_img = None
goal_img = None
floor_img = None
wall_img = None

def draw_map(screen, tile_map: list[list[int]]) -> None:
    global chest_img, goal_img, wall_img, floor_img
    if chest_img is None or goal_img is None or wall_img is None or floor_img is None:
        chest_img = load_sprite("chest.png")
        goal_img = load_sprite("goal.png")
        floor_img = load_sprite("floor.png")
        wall_img = load_sprite("wall.png")

    # Loop through each row and column in the tile map
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            if tile == 2:
                screen.blit(chest_img, pos)
            elif tile == 3:
                screen.blit(goal_img, pos)
            elif tile == 0:
                screen.blit(floor_img, pos)
            elif tile == 1:
                screen.blit(wall_img, pos)
            else:
                pygame.draw.rect(
                    screen,
                    colours.get(tile, (255, 0, 255)),  # fallback color for unknown tiles
                    pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)
                )

def can_move(x: int, y:int) -> bool:
    tile_x = x // TILE_SIZE    #conver pixel x to tile index
    tile_y = y // TILE_SIZE #convert pixel y to tile index
    # Prevent out-of-bounds movement
    if tile_y < 0 or tile_y >= len(tile_map) or tile_x < 0 or tile_x >= len(tile_map[0]):
        return False
    # Return False if wall, True otherwise
    return tile_map[tile_y][tile_x] != 1

def get_tile(x, y):
    return tile_map[y // TILE_SIZE][x // TILE_SIZE]