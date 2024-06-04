import sys
import random
import time

from raycasting import *
from map import *
from player import *
from renderer import *
from sprite_object import *
from buttons import *


# This is the main game class
class Game:
    # This is the constructor method
    def __init__(self):
        # Initialize the pygame module
        pygame.init()
        # Set the display mode
        self.screen = pygame.display.set_mode(RES)
        # Create a clock object
        self.clock = pygame.time.Clock()
        # Initialize delta_time
        self.delta_time = 1
        # Start a new game
        self.new_game()

    # This method starts a new game
    def new_game(self):
        # Initialize game variables
        self.start = 1
        self.restart = 0
        self.dead = 0
        # Create game objects
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.fruit_x, self.fruit_y = 0, 0
        # Randomize the fruit position
        self.randomize()
        # Create more game objects
        self.fruit = Fruit(self)
        self.button = Button(self)
        # Set up game events
        self.SCREEN_UPDATE1 = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE1, int(1000 / 3))
        self.SCREEN_UPDATE2 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SCREEN_UPDATE2, int(1000 / 4))
        self.SCREEN_UPDATE3 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SCREEN_UPDATE3, int(1000 / 5))
        self.SCREEN_UPDATE4 = pygame.USEREVENT + 3
        pygame.time.set_timer(self.SCREEN_UPDATE4, int(1000 / 7))
        # Set the accelerate event
        self.accelerate = self.SCREEN_UPDATE1
        # Load and play the background music
        pygame.mixer.music.load('resources/music/music.mp3')
        pygame.mixer.music.play(-1)

    # This method updates the game state
    def update(self):
        # Update game objects
        self.button.start()
        self.button.pause()
        self.button.counter()
        self.player.update()
        self.raycasting.update()
        self.fruit.update(self)
        # Check for collisions
        self.check_incident()
        # Update the display
        pygame.display.flip()
        # Update delta_time
        self.delta_time = self.clock.tick(FPS)
        # Update the window caption
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    # This method checks for collisions
    def check_incident(self):
        self.check_collision()
        self.player.check_collision()

    # This method checks for collisions with the fruit
    def check_collision(self):
        if [self.fruit_x, self.fruit_y] == [self.player.body[0].x, self.player.body[0].y]:
            # Play a sound when the player eats a fruit
            if self.button.count % 2:
                self.player.sound2.play()
            else:
                self.player.sound1.play()
            # Randomize the fruit position
            self.randomize()
            # Add a block to the player
            self.player.add_block()

    # This method draws the game objects
    def draw(self):
        # Fill the screen with a color
        self.screen.fill((240, 240, 240))
        # Draw game objects
        self.object_renderer.draw()
        self.map.draw()
        self.player.draw()

    # This method checks for user events
    def check_event(self):
        for event in pygame.event.get():
            # Check for quit event
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # Quit the game
                pygame.quit()
                sys.exit()
            # Check for accelerate event
            if event.type == self.accelerate:
                self.player.upd_snake()
            # Check for key press event
            if event.type == pygame.KEYDOWN:
                # Check for left key press
                if event.key == pygame.K_LEFT:
                    # Change the player direction
                    if self.player.direction == Vector2(-1, 0)\
                            and game.player.body[0].y - game.player.body[1].y != -1\
                            and game.player.body[0].y - game.player.body[1].y != 39:
                        self.player.direction = Vector2(0, 1)
                    elif self.player.direction == Vector2(1, 0)\
                            and game.player.body[0].y - game.player.body[1].y != 1\
                            and game.player.body[0].y - game.player.body[1].y != -39:
                        self.player.direction = Vector2(0, -1)
                    elif self.player.direction == Vector2(0, -1)\
                            and game.player.body[0].x - game.player.body[1].x != 1\
                            and game.player.body[0].x - game.player.body[1].x != -39:
                        self.player.direction = Vector2(-1, 0)
                    elif self.player.direction == Vector2(0, 1)\
                            and game.player.body[0].x - game.player.body[1].x != -1\
                            and game.player.body[0].x - game.player.body[1].x != 39:
                        self.player.direction = Vector2(1, 0)
                # Check for right key press
                elif event.key == pygame.K_RIGHT:
                    # Change the player direction
                    if self.player.direction == Vector2(-1, 0) and game.player.body[0].y - game.player.body[1].y != 1:
                        self.player.direction = Vector2(0, -1)
                    elif self.player.direction == Vector2(1, 0)\
                            and game.player.body[0].y - game.player.body[1].y != -1:
                        self.player.direction = Vector2(0, 1)
                    elif self.player.direction == Vector2(0, -1)\
                            and game.player.body[0].x - game.player.body[1].x != -1\
                            and game.player.body[0].x - game.player.body[1].x != 39:
                        self.player.direction = Vector2(1, 0)
                    elif self.player.direction == Vector2(0, 1)\
                            and game.player.body[0].x - game.player.body[1].x != 1\
                            and game.player.body[0].x - game.player.body[1].x != -39:
                        self.player.direction = Vector2(-1, 0)

    # This method runs the game loop
    def run(self):
        flag = True
        while 1:
            # Draw the game objects
            self.draw()
            if self.start:
                # Unpause the game music
                pygame.mixer.music.unpause()
                # Update the game state
                self.update()
                # Check for user events
                self.check_event()
                if flag:
                    self.press_to_start()
                    flag = False
            elif not self.dead:
                # Pause the game music
                pygame.mixer.music.pause()
                for event in pygame.event.get():
                    # Check for quit event
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        # Quit the game
                        pygame.quit()
                        sys.exit()
                # Start the game
                self.button.start()
            else:
                # Fade out the game music
                pygame.mixer.music.fadeout(1000)
                for event in pygame.event.get():
                    # Check for quit event
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        # Quit the game
                        pygame.quit()
                        sys.exit()
                    # Check for space key press
                    if event.type == pygame.K_DOWN and event.key == pygame.K_SPACE:
                        self.start = 1
                # Restart the game
                self.button.restart()
                if self.restart:
                    # Start a new game
                    self.new_game()
                    self.start = 1

    # This method randomizes the fruit position
    def randomize(self):
        a, b = random.randint(0, num - 1), random.randint(0, num - 1)
        while (a, b) in self.map.mmap or Vector2(a, b) in self.player.body or a == 0 or a == 41 or b == 0 or b == 41:
            a, b = random.randint(0, num - 1), random.randint(0, num - 1)
        self.fruit_x, self.fruit_y = a, b

    # This method is called when the player fails
    def fail(self):
        self.dead = 1
        self.button.restart()
        FAIL_FONT = pygame.font.Font(None, 60)
        text = FAIL_FONT.render('YOU\'RE DEAD!', True, 'red')
        self.screen.blit(text, (380, 480))
        pygame.display.update()
        self.start = 0

    # This method is called to start the game
    def press_to_start(self):
        self.start = 0
        PRESS_FONT = pygame.font.SysFont("MicrosoftYaHei", 40)
        text = PRESS_FONT.render('PRESS ANY KEY TO START', True, 'black')
        self.screen.blit(text, (380, 470))
        pygame.display.update()


# This is the main entry point of the program
if __name__ == '__main__':
    # Create a game object
    game = Game()
    # Run the game
    game.run()
