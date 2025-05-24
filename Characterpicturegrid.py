print("Chethan U, 1AY24AI025, SEC-M")
# CharacterPictureGrid.py

import sys
import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE

# CONFIGURATION

# Size of each cell (pixels)
CELL_SIZE = 64

# Grid dimensions (in cells)
GRID_WIDTH = 8
GRID_HEIGHT = 6

# Mapping from 2-letter code → image filename
# (Place your image files in the same directory)
CHAR_PIC_DICT = {
    'AL': 'alien.png',
    'SP': 'spaceship.png',
    'ST': 'star.png',
    'PL': 'planet.png',
    'AS': 'asteroid.png',
    # add more codes/images here…
}

# The grid itself: list of rows, each a list of 2-letter codes
# Must be GRID_HEIGHT rows of GRID_WIDTH entries each.
# Example pattern; replace with your own design!
GRID_LAYOUT = [
    ['AL','SP','ST','PL','AS','AL','SP','ST'],
    ['SP','ST','PL','AS','AL','SP','ST','PL'],
    ['ST','PL','AS','AL','SP','ST','PL','AS'],
    ['PL','AS','AL','SP','ST','PL','AS','AL'],
    ['AS','AL','SP','ST','PL','AS','AL','SP'],
    ['AL','SP','ST','PL','AS','AL','SP','ST'],
]

def load_and_scale_images(cell_size):
    """Load each image once and scale to (cell_size × cell_size)."""
    images = {}
    for code, filename in CHAR_PIC_DICT.items():
        try:
            img = pygame.image.load(filename)
        except pygame.error as e:
            print(f"Could not load image for code '{code}': {filename}")
            raise SystemExit(e)
        images[code] = pygame.transform.scale(img, (cell_size, cell_size))
    return images

def main():
    pygame.init()
    window_size = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Character Picture Grid")

    # Preload and scale all images
    images = load_and_scale_images(CELL_SIZE)

    clock = pygame.time.Clock()

    while True:
        # Handle events
        for evt in pygame.event.get():
            if evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Draw the grid
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                code = GRID_LAYOUT[row][col]
                img = images.get(code)
                if img:
                    screen.blit(img, (col * CELL_SIZE, row * CELL_SIZE))
                else:
                    # draw a red square for unknown codes
                    rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (255,0,0), rect)

        pygame.display.flip()
        clock.tick(30)  # limit to 30 FPS

if __name__ == "__main__":
    main()
