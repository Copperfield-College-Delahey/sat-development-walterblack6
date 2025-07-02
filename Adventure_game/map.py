import pickle #test code will delet or change later
import pygame

TILE_SIZE = 50

def load_mpy_map(filename):
    """Load a .mpy map file (pickled 2D list) and return the map data."""
    with open(filename, "rb") as f:
        map_data = pickle.load(f)
    return map_data

def draw_map(screen, map_data):
    """Draw the map on the screen."""
    colors = {
        1: (100, 100, 100),  # Wall
        0: (200, 255, 200),  # Floor
    }
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            color = colors.get(tile, (255, 255, 255))
            pygame.draw.rect(
                screen,
                color,
                (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )