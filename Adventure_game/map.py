tile_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 2, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

import pygame
from typing import Dict, Tuple #added by ai

TILE_SIZE = 64

def draw_map(screen, tile_map: list[list[int]]) -> None: #list[list[int]] added by ai to fix error
    # Define colors for each tile type: 0 = floor, 1 = wall, 2 = object, 3 = goal
    colours: Dict[int, Tuple[int, int, int]] = { # Dict[int, Tuple[int, int, int]] added by ai to fix error of "Type annotation not supported for this statement"
        0: (240, 240, 240), # floor
        1: (50, 50, 50),    # wall
        2: (255, 215, 0),   # object
        3: (0, 255, 0)      # goal
    }
    
    # Loop through each row and column in the tile map
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            # Draw a rectangle for each tile at the correct position and color
            pygame.draw.rect(
                screen,
                colours[tile],  # Color based on tile type
                pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Position and size of the tile
            )