import pygame
import os
import constants

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

WIDTH = 800
HEIGHT = 600
GAME_WIDTH = 500
GAME_HEIGHT = 500


def setup(screen):
    # modify screen to hold information for out game
    pygame.display.set_caption("Dots and Boxes")

    font = pygame.font.Font(constants.title, 40)

    # set the background colour of the screen
    screen.fill(WHITE)

    # this will draw an outline of the game board
    pygame.draw.rect(screen, BLACK, (WIDTH/2 - GAME_WIDTH/2 + 10,
                                     HEIGHT/2 - GAME_HEIGHT/2, GAME_WIDTH, GAME_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - GAME_WIDTH/2 + 15,
                                     HEIGHT/2 - GAME_HEIGHT/2 + 5, GAME_WIDTH - 10,  GAME_HEIGHT - 10))

    text = font.render('Dots and Boxes', True, GREEN, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH/2, 20)

    screen.blit(text, text_rect)

    pygame.display.update()


def main():
    # initialize pygame and create the screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    print('test')
    print(os.listdir())

    setup(screen)
    # variable that tells you when the game ends
    running = True

    # game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


if __name__ == "__main__":
    main()
