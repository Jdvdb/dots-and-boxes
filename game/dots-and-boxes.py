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
DOT_RADIUS = 10
DOT_SPACING = 50
DOT_CENTER_HEIGHT = 300
DOT_CENTER_WIDTH = 400


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
    
    #draw dots
    
    #pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH , DOT_CENTER_HEIGHT), DOT_RADIUS)
    
    rows = 6 # of dots
    cols = 6 # of dots
    
    
    #this loop will only work for odd rows and columns
    if (rows%2 != 0 and cols%2 != 0):
        for i in range(-(rows-rows//2)+1, rows-rows//2):
            for j in range(-(cols-cols//2)+1, cols-cols//2):
                pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH + (i*DOT_SPACING), DOT_CENTER_HEIGHT + (j*DOT_SPACING)), DOT_RADIUS)
            
    #this loop will only work for even rows and columns
    if (rows%2 == 0 and cols%2 == 0):
        for i in range(-(rows-rows//2), rows-rows//2):
            for j in range(-(cols-cols//2), cols-cols//2):
                pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH + ((2*i+1)*DOT_SPACING//2), DOT_CENTER_HEIGHT + ((2*j+1)*DOT_SPACING//2)), DOT_RADIUS)
    
    
    
    
    
    

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
