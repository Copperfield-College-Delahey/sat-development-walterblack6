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

TILE_SIZE = 64  # Size of each tile in pixels

# Lazy-load sprites
chest_img = None
goal_img = None
floor_img = None
wall_img = None

def draw_map(screen, tile_map: list[list[int]]) -> None:
    global chest_img, goal_img, wall_img, floor_img
    if chest_img is None or goal_img or wall_img or floor_img is None:
        base_path = os.path.dirname(__file__)
        chest_img = pygame.image.load(os.path.join(base_path, "assets", "sprites", "chest.png")).convert_alpha()
        chest_img = pygame.transform.scale(chest_img, (TILE_SIZE, TILE_SIZE))
        goal_img = pygame.image.load(os.path.join(base_path, "assets", "sprites", "goal.png")).convert_alpha()
        goal_img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))
        floor_img = pygame.image.load(os.path.join(base_path, "assets", "sprites", "floor.png")).convert_alpha()
        floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))
        wall_img = pygame.image.load(os.path.join(base_path, "assets", "sprites", "wall.png")).convert_alpha()
        wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

    colours: Dict[int, Tuple[int, int, int]] = {
    }
    
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