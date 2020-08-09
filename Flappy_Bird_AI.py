import pygame
import neat
import time
import random
import os
pygame.font.init()

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

STAT_FONT = pygame.font.SysFont("comincsans", 50)

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

"""
---------------BASE CLASS---------------
"""

# Base is represented by 2 images moving across the screen made to look like
# 1 continous moving image
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # If either image are off the screen cycle them back behind the other image
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

# Draws all the objects onto the current frame
def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH -10 -text.get_width(), 10))

    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()

"""
---------------FITNESS FUNCTION---------------
"""

def eval_genomes(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, genome in genomes:
        # Set up nerual network for each genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        genome.fitness = 0
        ge.append(genome)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Determine which pipe is the next pipe to go through if multiple are on the screen
        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_idx = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            # Pass input values to the neural network
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))
            if output[0] > 0.5:
                # Jump if confidence > 0.5
                bird.jump()


        add_pipe = False
        remove_list = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # Check is bird passed pipe and indicate to add new pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # if pipe is off the screen remove it
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_list.append(pipe)


            pipe.move()

        # Adds new random pipe to game
        if add_pipe:
            score += 1
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(600))

        for pipe in remove_list:
            pipes.remove(pipe)

        # Check if birds hit the ground or go too high
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        base.move()
        draw_window(win, birds, pipes, base, score)

def run(config_path):
    # Sets up the neat module using config file paramters
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # Generates population based on paramters in the config file
    population = neat.Population(config)
    # Provides console output giving stats on current generation
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    # Pass fitness function and number of generations to run for
    winner = population.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-flappy-bird.txt")
    run(config_path)
