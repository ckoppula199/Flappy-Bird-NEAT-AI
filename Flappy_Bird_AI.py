import pygame
import neat
import time
import random
import os

# Screen Dimensions
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Load Images used in the game
# Stores the 3 images of the bird and makes them twice as large as the original image
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) # Pipe images
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))     # Background image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png'))) # Base (floor) image

"""
---------------BIRD CLASS---------------
"""

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
        self.img_count = 0 # Keeps track of which image of the bird is being shown and how many frames it's been shown for
        self.img = self.IMGS[0] # Image of bird to display

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    # To be called on every bird at every frame
    def move(self):
        self.tick_count += 1

        # displacement determines how many pixels we move up or down in the current frame
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # 'Terminal velocity' limits how much it will move up or down
        if d >= 16:
            d = 16

        # If moving upwards, move up a bit more, just makes the game look more fluid and nicer
        if d < 0:
            d -= 2

        self.y = self.y + d

        # If moving upwards
        if d < 0 or self.y < self.height + 50:
            # Prevents tilting bird completly backwards.
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # Changes bird form looking like it faces upwards to downwards
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # Change image being shown based on how many frames have passed to make it
        # look like the bird is flapping its wings
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If bird facing down set it to neutral wings
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Below lines taken from StackOverflow
        # Rotates image around top left pixel
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # Moves image to make it look like it rotated around the centre
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


"""
---------------PIPE CLASS---------------
"""

class Pipe(object):
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        # Keeps track of where the top and bottom of the pipe is going to be drawn
        self.top = 0
        self.bottom = 0
        # Images for top and bottom pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False # Checks if bird has passed the pipe
        self.set_height()

    # Works out the position to place the pipe images
    def set_height(self):
        self.height = random.randrange(40, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # Gets masks of the bird and pipes to detect if pixels of the image collided
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Offset is how far away the top left corners are from each other
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Below 2 variable will be None if no collision occured
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bottom_point:
            return True

        return False




def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()
        draw_window(win, bird)
    pygame.quit()
    quit()


main()
