import math

from settings import *
from renderer import *
import pygame


# This is the RayCasting class, which is used for rendering 3D objects in the game
class RayCasting:
    # The constructor for the RayCasting class
    def __init__(self, game):
        # The game object
        self.game = game
        # The result of the ray casting
        self.ray_casting_result = []
        # The objects to be rendered
        self.objects_to_render = []
        # The textures for the walls
        self.textures = self.game.object_renderer.wall_textures

    # This method gets the objects to be rendered
    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            # judge the size of wall column texture and its position
            if proj_height < num * size:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, 0.5 * num * size - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * num * size / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, num * size))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    # calculate the 3D view of the player
    def ray_cast(self):
        # initialize the ray casting result list
        self.ray_casting_result = []
        # get the player's position and position in map
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1

        # calculate the angle of the first ray
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        # loop through all the rays
        for ray in range(NUM_RAYS):
            # calculate the sine and cosine of the ray angle
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # calculate the y-coordinate of the horizontal intersection point and the change in y
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            # calculate the depth and x-coordinate of the horizontal intersection point
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            # calculate the change in depth and x-coordinate for each step
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            # loop through all the steps
            for i in range(MAX_DEPTH):
                # get the tile at the current position
                tile_hor = int(x_hor), int(y_hor)
                # if the tile is in the map or the snake body, set the horizontal texture and break the loop
                if tile_hor in self.game.map.mmap:
                    texture_hor = self.game.map.mmap[tile_hor]
                    break
                if tile_hor in self.game.player.body[2:]\
                        and (tile_hor[0] - self.game.player.x) ** 2 +\
                        (tile_hor[1] - self.game.player.y) ** 2 <= PLATER_VIEW ** 2:
                    texture_hor = 2
                    break
                # update the x and y coordinates and depth
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # calculate the x-coordinate of the vertical intersection point and the change in x
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            # calculate the depth and y-coordinate of the vertical intersection point
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            # calculate the change in depth and y-coordinate for each step
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            # loop through all the steps
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.mmap:
                    texture_vert = self.game.map.mmap[tile_vert]
                    break
                if tile_vert in self.game.player.body[2:]\
                        and (tile_vert[0] - self.game.player.x) ** 2 +\
                        (tile_vert[1] - self.game.player.y) ** 2 <= PLATER_VIEW ** 2:
                    texture_vert = 2
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # determine which intersection point is closer and set the depth, texture, and offset accordingly
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # adjust the depth based on the player's angle and calculate the projected height of the wall
            depth *= math.cos(self.game.player.angle - ray_angle)
            proj_height = SCREEN_DIST / (depth + 0.0001)
            # add the result to the ray casting result list
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # increment the ray angle by the delta angle
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()