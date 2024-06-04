import pygame
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        # Initialize game instance
        self.game = game
        # Initialize game screen
        self.screen = game.screen
        # Load wall textures
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/image/sky1.jpg', (num * size, 0.5 * num * size))
        # Initialize sky offset
        self.sky_offset = 0

    def draw(self):
        # Draw background
        self.draw_background()
        # Render game objects
        self.render_game_objects()

    def draw_background(self):
        # Update sky offset
        self.sky_offset = (self.sky_offset + self.game.player.dangle * PLAYER_ROT_SPEED) % (num * size)
        # Draw sky image
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + num * size, 0))
        # Load floor image
        self.floor = pygame.image.load('resources/image/floor.jpg')

        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, 0.5 * num * size, num * size, num * size))

    def render_game_objects(self):
        # Sort objects_to_render
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            # Draw game object
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        # Load texture
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            # Load wall texture
            1: self.get_texture('resources/image/wall1.jpg'),
            # Load snake texture
            2: self.get_texture('resources/image/pink.png'),
            # Load portal texture
            3: self.get_texture('resources/image/shuffle.png')
        }