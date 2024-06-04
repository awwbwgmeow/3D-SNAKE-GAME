import pygame


# This is the Button class, which is used to create and manage the game buttons
class Button:
    # This is the constructor method
    def __init__(self, game):
        # Here we are initializing the game and screen attributes
        self.game = game
        self.screen = game.screen
        self.count = 0

    # This method is used to create and manage the start button
    def start(self):
        # Here we are getting the mouse position and click status
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()

        # Here we are drawing the start button on the screen
        pygame.draw.rect(self.screen, 'white', (770, 0, 140, 40), 0)
        # Here we are setting the font and text for the start button
        START_FONT = pygame.font.SysFont("MicrosoftYaHei", 30)
        start_button = START_FONT.render('START', True, 'black')
        # Here we are blitting the start button on the screen
        self.screen.blit(start_button, (795, 0))
        # Here we are checking if the mouse is over the start button and if it is clicked
        for keys in key:
            if keys:
                self.game.start = 1
        if 770 < mouse[0] < 910 and 0 < mouse[1] < 40:
            if click[0]:
                # If the start button is clicked, we set the game start attribute to 1
                self.game.start = 1

    # This method is used to create and manage the pause button
    def pause(self):
        # Here we are getting the mouse position and click status
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Here we are drawing the pause button on the screen
        pygame.draw.rect(self.screen, 'white', (910, 0, 140, 40), 0)
        # Here we are setting the font and text for the pause button
        PAUSE_FONT = pygame.font.SysFont("MicrosoftYaHei", 30)
        pause_button = PAUSE_FONT.render('PAUSE', True, 'black')
        # Here we are blitting the pause button on the screen
        self.screen.blit(pause_button, (935, 0))
        # Here we are checking if the mouse is over the pause button and if it is clicked
        if 910 < mouse[0] < 1050 and 0 < mouse[1] < 40:
            if click[0]:
                # If the pause button is clicked, we set the game start attribute to 0
                self.game.start = 0

    # This method is used to create and manage the restart button
    def restart(self):
        # Here we are getting the mouse position and click status
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Here we are drawing the restart button on the screen
        pygame.draw.rect(self.screen, 'white', (460, 530, 140, 40), 0)
        # Here we are setting the font and text for the restart button
        RESTART_FONT = pygame.font.SysFont("MicrosoftYaHei", 30)
        restart_button = RESTART_FONT.render('RESTART', True, 'green')
        # Here we are blitting the restart button on the screen
        self.screen.blit(restart_button, (470, 530))
        # Here we are checking if the mouse is over the restart button and if it is clicked
        if 460 < mouse[0] < 600 and 530 < mouse[1] < 570:
            if click[0]:
                # If the restart button is clicked, we set the game restart attribute to 1
                self.game.restart = 1

    # This method is used to create and manage the score counter
    def counter(self):
        # Here we are drawing the counter on the screen
        pygame.draw.rect(self.screen, 'white', (430, 0, 140, 40), 0)
        # Here we are setting the font and text for the counter
        COUNTER_FONT = pygame.font.SysFont("MicrosoftYaHei", 30)
        self.count = len(self.game.player.body) - 3
        if self.count < 3:
            self.game.accelerate = self.game.SCREEN_UPDATE1
            self.game.player.speed = 3
        if 3 <= self.count < 5:
            self.game.accelerate = self.game.SCREEN_UPDATE2
            self.game.player.speed = 4
        if 5 <= self.count < 10:
            self.game.accelerate = self.game.SCREEN_UPDATE3
            self.game.player.speed = 5
        if self.count >= 10:
            self.game.accelerate = self.game.SCREEN_UPDATE4
            self.game.player.speed = 7
        start_button = COUNTER_FONT.render(f'SCORE: {self.count}', True, 'black')
        # Here we are blitting the counter on the screen
        self.screen.blit(start_button, (435, 0))
