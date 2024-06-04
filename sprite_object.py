import pygame
from settings import *


# This class represents a fruit in the game
class Fruit:
    # The constructor for the Fruit class
    def __init__(self, game, path='resources/image/fruit.png', scale=0.5, shift=0.5):
        # Initializing the game, player and fruit's position
        self.game = game
        self.player = game.player
        self.x, self.y = game.fruit_x, game.fruit_y

        # Loading the fruit image and getting its properties
        self.image = pygame.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()

        # Initializing other properties of the fruit
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.fruit_half_width = 0
        self.FRUIT_SCALE = scale
        self.FRUIT_HEIGHT_SHIFT = shift

    # This method calculates the projection of the fruit on the screen
    def get_fruit_projection(self):
        # Calculating the projection size
        proj = SCREEN_DIST / self.norm_dist * self.FRUIT_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # Scaling the image according to the projection size
        image = pygame.transform.scale(self.image, (proj_width, proj_height))

        # Calculating the position of the fruit on the screen
        self.fruit_half_width = proj_width // 2
        height_shift = proj_height * self.FRUIT_HEIGHT_SHIFT
        pos = self.screen_x - self.fruit_half_width, 0.5 * num * size - proj_height // 2 + height_shift

        # Adding the fruit to the list of objects to render
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    # This method calculates the position of the fruit relative to the player
    def get_fruit(self):
        # Calculating the distance between the fruit and the player
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        # Calculating the angle between the player's view and the fruit
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        # Calculating the position of the fruit on the screen
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # Calculating the distance between the player and the fruit
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)

        # If the fruit is in the player's field of view, calculate its projection
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (num * size + self.IMAGE_HALF_WIDTH):
            self.get_fruit_projection()

        # Drawing the fruit on the screen
        if (self.x - self.game.player.x) ** 2 + (self.y - self.game.player.y) ** 2 <= PLATER_VIEW ** 2:
            fruit_rect = pygame.Rect(self.x * s_size, self.y * s_size, s_size, s_size)
            pygame.draw.rect(self.game.screen, 'yellow', fruit_rect)

    # This method updates the position of the fruit
    def update(self, game):
        self.x, self.y = game.fruit_x, game.fruit_y
        self.get_fruit()

