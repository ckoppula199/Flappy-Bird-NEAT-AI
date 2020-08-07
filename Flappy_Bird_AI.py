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

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25    # How much bird is going to tilt when aiming upwards or downwards
    ANIMATION_TIME = 5   # How long to show each bird animation
    ROT_VEL = 20         # How much the bird rotates on each frame

    def __init__(self, x, y):
        # x, y are the position of the bird
        self.x = x
        self.y = y
        self.tilt = 0 # How much the image is tilted, 0 is flat
        self.tick_count = 0 # Keeps track of how long since the last jump
        self.vel = 0
        self.height = self.y
        self.img_count = 0 # Keeps track of which image of the bird is being shown
        self.img = self.IMGS[0] # Image of bird to display

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    # To be called on every bird at every frame
    def move(self):
        pass
