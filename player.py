from settings import*
import pygame
import math
from pygame.math import Vector2


# Class for the player object
class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.speed = 3
        self.body = [Vector2(self.x, self.y), Vector2(self.x - 1, self.y), Vector2(self.x - 2, self.y)]
        self.angle = PLAYER_ANGLE
        self.direction = Vector2(1, 0)
        self.dangle = 0
        self.new_block = False
        self.left = 0
        self.right = 0
        self.shuffle = [0, 0, 0, 0]

        # load snake image
        self.head_up = pygame.image.load('resources/image/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('resources/image/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('resources/image/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('resources/image/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('resources/image/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('resources/image/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('resources/image/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('resources/image/tail_right.png').convert_alpha()

        # load sound effects
        self.sound1 = pygame.mixer.Sound('resources/music/effect.wav')
        self.sound2 = pygame.mixer.Sound('resources/music/effect0.wav')

    # how the snake move
    def move_snake(self):
        # judge if the snake is turning left or right
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1, 0):
            if self.direction == Vector2(0, 1):
                self.right = 1
                self.left = 0
            if self.direction == Vector2(0, -1):
                self.right = 0
                self.left = 1
            if self.direction == Vector2(1, 0):
                self.right = 0
                self.left = 0
                self.angle = 0
        if head_relation == Vector2(-1, 0):
            if self.direction == Vector2(0, -1):
                self.right = 1
                self.left = 0
            if self.direction == Vector2(0, 1):
                self.right = 0
                self.left = 1
            if self.direction == Vector2(-1, 0):
                self.right = 0
                self.left = 0
                self.angle = math.pi
        if head_relation == Vector2(0, 1):
            if self.direction == Vector2(-1, 0):
                self.right = 1
                self.left = 0
            if self.direction == Vector2(1, 0):
                self.right = 0
                self.left = 1
            if self.direction == Vector2(0, 1):
                self.right = 0
                self.left = 0
                self.angle = 0.5 * math.pi
        if head_relation == Vector2(0, -1):
            if self.direction == Vector2(1, 0):
                self.right = 1
                self.left = 0
            if self.direction == Vector2(-1, 0):
                self.right = 0
                self.left = 1
            if self.direction == Vector2(0, -1):
                self.right = 0
                self.left = 0
                self.angle = 1.5 * math.pi
        # if eats a fruit, then add a block to the body of snake
        if self.new_block:
            bodyc = self.body[:]
            bodyc.insert(0, bodyc[0] + self.direction)
            self.body = bodyc[:]
            self.new_block = False
        # if snake head is on the edge of the map, shift the head block to the other side of the map
        elif self.shuffle[0] == 1:
            bodyc = self.body[:-1]
            bodyc.insert(0, Vector2(40, bodyc[0].y))
            self.body = bodyc[:]
            self.shuffle[0] = 0
        elif self.shuffle[1] == 1:
            bodyc = self.body[:-1]
            bodyc.insert(0, Vector2(1, bodyc[0].y))
            self.body = bodyc[:]
            self.shuffle[1] = 0
        elif self.shuffle[2] == 1:
            bodyc = self.body[:-1]
            bodyc.insert(0, Vector2(bodyc[0].x, 40))
            self.body = bodyc[:]
            self.shuffle[2] = 0
        elif self.shuffle[3] == 1:
            bodyc = self.body[:-1]
            bodyc.insert(0, Vector2(bodyc[0].x, 1))
            self.body = bodyc[:]
            self.shuffle[3] = 0
        # move normally
        else:
            bodyc = self.body[:-1]
            bodyc.insert(0, bodyc[0] + self.direction)
            self.body = bodyc[:]
        # change the camera position
        self.x = bodyc[0].x
        self.y = bodyc[0].y

    def add_block(self):
        self.new_block = True

    # how the camera move
    def movement(self):
        speed_x = self.direction.x / FPS * self.speed
        speed_y = self.direction.y / FPS * self.speed

        if self.left:
            self.angle -= 0.5 * self.speed * math.pi / FPS
            self.dangle = -5000
        elif self.right:
            self.angle += 0.5 * self.speed * math.pi / FPS
            self.dangle = 5000
        else:
            self.dangle = 0
        self.angle %= math.tau

        self.x += speed_x
        self.y += speed_y

    # check if the snake head crush into the snake body or the wall
    def check_collision(self):
        if (self.body[0].x, self.body[0].y) in self.game.map.mmap \
                and self.game.map.mmap[self.body[0].x, self.body[0].y] == 1:
            self.game.fail()
        if self.body[0].x == 1 and self.direction == Vector2(-1, 0):
            self.shuffle[0] = 1
        if self.body[0].x == 40 and self.direction == Vector2(1, 0):
            self.shuffle[1] = 1
        if self.body[0].y == 1 and self.direction == Vector2(0, -1):
            self.shuffle[2] = 1
        if self.body[0].y == 40 and self.direction == Vector2(0, 1):
            self.shuffle[3] = 1
        for block in self.body[1:]:
            if block == self.body[0]:
                self.game.fail()

    # draw the snake
    def draw(self):
        head_relation = self.body[0] - self.body[1]
        tail_relation = self.body[-2] - self.body[-1]
        # draw the view of the snake
        pygame.draw.circle(self.game.screen, 'white', (self.x * s_size + 0.5 * s_size, self.y * s_size + 0.5 * s_size),
                           PLATER_VIEW * (s_size + 1), 2)
        for index, block in enumerate(self.body):
            x_pos = int(block.x * s_size)
            y_pos = int(block.y * s_size)
            brect = pygame.Rect(x_pos, y_pos, s_size, s_size)
            # apply image to the snake head
            if index == 0:
                if head_relation == Vector2(-1, 0) or head_relation == Vector2(39, 0):
                    self.head = self.head_left
                    self.head = pygame.transform.scale(self.head, (30 * s_size / 15, 22 * s_size / 15))
                    brect = pygame.Rect(x_pos - s_size, y_pos - s_size / 3, s_size, s_size)
                if head_relation == Vector2(1, 0) or head_relation == Vector2(-39, 0):
                    self.head = self.head_right
                    self.head = pygame.transform.scale(self.head, (30 * s_size / 15, 22 * s_size / 15))
                    brect = pygame.Rect(x_pos, y_pos - s_size / 3, s_size, s_size)
                if head_relation == Vector2(0, 1) or head_relation == Vector2(0, -39):
                    self.head = self.head_down
                    self.head = pygame.transform.scale(self.head, (22 * s_size / 15, 30 * s_size / 15))
                    brect = pygame.Rect(x_pos - s_size * 2 / 15, y_pos, s_size, s_size)
                if head_relation == Vector2(0, -1) or head_relation == Vector2(0, 39):
                    self.head = self.head_up
                    self.head = pygame.transform.scale(self.head, (22 * s_size / 15, 30 * s_size / 15))
                    brect = pygame.Rect(x_pos - s_size / 5, y_pos - s_size, s_size, s_size)
                self.game.screen.blit(self.head, brect)
            # apply image to the snake tail
            elif index == len(self.body) - 1:
                if tail_relation == Vector2(-1, 0) or tail_relation == Vector2(39, 0):
                    self.tail = self.tail_left
                    self.tail = pygame.transform.scale(self.tail, (18 * s_size / 15, 15 * s_size / 15))
                    crect = pygame.Rect(x_pos, y_pos + s_size / 15, s_size, s_size)
                if tail_relation == Vector2(1, 0) or tail_relation == Vector2(-39, 0):
                    self.tail = self.tail_right
                    self.tail = pygame.transform.scale(self.tail, (18 * s_size / 15, 15 * s_size / 15))
                    crect = pygame.Rect(x_pos - s_size / 5, y_pos + s_size / 15, s_size, s_size)
                if tail_relation == Vector2(0, 1) or tail_relation == Vector2(0, -39):
                    self.tail = self.tail_down
                    self.tail = pygame.transform.scale(self.tail, (15 * s_size / 15, 18 * s_size / 15))
                    crect = pygame.Rect(x_pos - s_size / 15, y_pos - s_size / 5, s_size, s_size)
                if tail_relation == Vector2(0, -1) or tail_relation == Vector2(0, 39):
                    self.tail = self.tail_up
                    self.tail = pygame.transform.scale(self.tail, (15 * s_size / 15, 18 * s_size / 15))
                    crect = pygame.Rect(x_pos - s_size / 15, y_pos, s_size, s_size)
                self.game.screen.blit(self.tail, crect)
            # draw the snake body
            else:
                pygame.draw.rect(self.game.screen, (244, 167, 238), brect)


    def update(self):
        self.movement()

    def upd_snake(self):
        self.move_snake()

    @property
    def pos(self):
        return self.x + 0.5, self.y + 0.5

    @property
    def map_pos(self):
        return int(self.x + 0.5), int(self.y + 0.5)
