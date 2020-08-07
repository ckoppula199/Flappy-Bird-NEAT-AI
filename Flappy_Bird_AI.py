import pygame
import neat
import time
import random
import os

# Screen Dimensions
WIN_WIDTH = 800
WIN_HEIGHT = 1000

# Load Images used in the game
# Stores the 3 images of the bird and makes them twice as large as the original image
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) # Pipe images
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))     # Background image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png'))) # Base (floor) image
