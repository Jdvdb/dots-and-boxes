# Created by Jordan Van Den Bruel & Danny Zaiter 2020
import pygame
import os
import constants
import DBNode
import DotsAndBoxes
import MCTS
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 800
HEIGHT = 600
GAME_WIDTH = 500
GAME_HEIGHT = 500
DOT_RADIUS = 10
DOT_SPACING = 100
DOT_CENTER_HEIGHT = 300
DOT_CENTER_WIDTH = 400

# NOTE: This is a value you can modify to give the computer more/less time to think, 1 is standard
BRAIN_POWER = 1.0


def endGame(board):
    print("Game Over!")
    print("AI Score:", board.P1Score)
    print("Human Score", board.P2Score)
    if board.P1Score > board.P2Score:
        print("AI Won!")
    else:
        print("Human Won!")
    quit()


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

    # Render the title
    text = font.render('Dots and Boxes', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH/2, 20)

    screen.blit(text, text_rect)

    font = pygame.font.Font(constants.title, 25)

    # Write out scores for players
    text = font.render('Player: 0', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH-49, 10)
    screen.blit(text, text_rect)

    text = font.render('Computer: 0', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH-70, 40)
    screen.blit(text, text_rect)

    # Write out who is playing
    text = font.render('Playing Now: ', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (100, 10)
    screen.blit(text, text_rect)

    text = font.render('Computer', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (100, 40)
    screen.blit(text, text_rect)

    pygame.display.update()

    # draw dots

    #pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH , DOT_CENTER_HEIGHT), DOT_RADIUS)

    rows = 4  # of dots
    cols = 4  # of dots

    # this loop will only work for odd rows and columns
    if (rows % 2 != 0 and cols % 2 != 0):
        for i in range(-(rows-rows//2)+1, rows-rows//2):
            for j in range(-(cols-cols//2)+1, cols-cols//2):
                pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH + (i*DOT_SPACING),
                                                   DOT_CENTER_HEIGHT + (j*DOT_SPACING)), DOT_RADIUS)

    # this loop will only work for even rows and columns
    if (rows % 2 == 0 and cols % 2 == 0):
        for i in range(-(rows-rows//2), rows-rows//2):
            for j in range(-(cols-cols//2), cols-cols//2):
                pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH + ((2*i+1)*DOT_SPACING//2),
                                                   DOT_CENTER_HEIGHT + ((2*j+1)*DOT_SPACING//2)), DOT_RADIUS)


def main():
    # initialize pygame and create the screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    setup(screen)
    # variable that tells you when the game ends
    running = True

    tempGame = DotsAndBoxes.DotsAndBoxes()

    # value for creating IDs
    currentId = 0

    # root node for the tree
    root = DBNode.DBNode(tempGame, currentId, -1, (-1, 0, 0))
    currentId += 1

    # dictionary that will act as the game tree
    tree = dict()
    tree[root.id] = root

    # number of rollouts to be performed
    rollouts = 1800

    # flag to keep playing the game
    playing = True
    # array of display Rects
    row_borders = copy.deepcopy(tempGame.rows)
    col_borders = copy.deepcopy(tempGame.cols)
    boxes = copy.deepcopy(tempGame.boxes)

    # draw out the the board for the screen
    for i in range(len(row_borders)):
        for j in range(len(row_borders[i])):
            row_borders[i][j] = pygame.Rect(
                (260+j*DOT_SPACING, 145+i*DOT_SPACING), (DOT_SPACING - 2*DOT_RADIUS, DOT_RADIUS))

    for i in range(len(col_borders)):
        for j in range(len(col_borders[i])):
            col_borders[i][j] = pygame.Rect(
                (245+i*DOT_SPACING, 160+j*DOT_SPACING), (DOT_RADIUS, DOT_SPACING - 2*DOT_RADIUS))

    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            boxes[i][j] = pygame.Rect(
                (250+i*DOT_SPACING, 150+j*DOT_SPACING), (100, 100))

    # draw all rects on screen
    for i in range(len(row_borders)):
        for j in range(len(row_borders[i])):
            pygame.draw.rect(screen, WHITE, row_borders[i][j])

    for i in range(len(col_borders)):
        for j in range(len(col_borders[i])):
            pygame.draw.rect(screen, WHITE, col_borders[i][j])

    pygame.display.update()

    # main game loop
    while running:
        # get events from pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        # instructions for P2/Human turn
        if not tempGame.player:
            pos = None
            move = None

            # wait for a move to be played
            while move == None:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #gets the coordinates of a mouse click
                        pos = pygame.mouse.get_pos()

                        # check to see where on the game board someone tries to play
                        # update that rectangle to black
                        for i in range(len(row_borders)):
                            for j in range(len(row_borders[i])):
                                if row_borders[i][j].collidepoint(pos):
                                    move = (0, i, j)
                                    (direction, dotInd, lineInd) = move
                                    pygame.draw.rect(
                                        screen, BLACK, row_borders[i][j])
                                    pygame.display.update()

                        for i in range(len(col_borders)):
                            for j in range(len(col_borders[i])):
                                if col_borders[i][j].collidepoint(pos):
                                    move = (1, i, j)
                                    (direction, dotInd, lineInd) = move
                                    pygame.draw.rect(
                                        screen, BLACK, col_borders[i][j])
                                    pygame.display.update()

                        if move != None:
                            # check if that is a legal move
                            if tempGame.addLine(direction, dotInd, lineInd):
                                # find where the new move would be in the tree
                                nextNode = root.id
                                foundNextNode = False
                                for node in root.children:
                                    if tree[node].newMove == move:
                                        nextNode = node
                                        foundNextNode = True

                                if not foundNextNode:
                                    # if node not found, then create a new node in the tree for it
                                    (direction, dotInd, lineInd) = move
                                    newNode = DBNode.DBNode(
                                        tempGame, currentId, -1, move)
                                    newNode.board.addLine(
                                        direction, dotInd, lineInd)
                                    nextNode = newNode.id
                                    currentId += 1

                                    # add new node to the tree
                                    tree[newNode.id] = newNode

                                # update the root for the computer
                                root = tree[nextNode]

        # instructions for P1/AI
        else:
            # determine how many rollouts should be done based on depth into game
            if len(root.board.moves) < 12:
                rollouts = 13000
            elif len(root.board.moves) < 16:
                rollouts = 11000
            elif len(root.board.moves) < 22:
                rollouts = 8000
            else:
                rollouts = 3500
            # modify the number of rollouts by the power given by the user
            rollouts *= BRAIN_POWER
            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, rollouts)

            # update the root
            root = tree[nextComputerId]

        # update the current game board
        tempGame = root.board

        # end the game if it is done
        if tempGame.checkEnd():
            endGame(tempGame)

        # draw in the computer's most recent move
        (direction, i, j) = root.newMove

        if direction == 0:
            pygame.draw.rect(screen, BLACK, row_borders[i][j])

        else:
            pygame.draw.rect(screen, BLACK, col_borders[i][j])

        # draw filler boxes for captured squares
        for i in range(len(tempGame.boxes)):
            for j in range(len(tempGame.boxes[i])):
                if tempGame.boxes[j][i]:
                    pygame.draw.rect(screen, BLACK, boxes[i][j])

        # update score
        font = pygame.font.Font(constants.title, 25)

        text = font.render('Player: %d' % tempGame.P2Score, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH-47, 10)
        screen.blit(text, text_rect)

        text = font.render('Computer: %d' %
                           tempGame.P1Score, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH-70, 40)
        screen.blit(text, text_rect)

        #update current player
        pygame.draw.rect(screen, WHITE, (0, 0, 200, 50))
        text = font.render('Playing Now: ', True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (100, 10)
        screen.blit(text, text_rect)

        if tempGame.player:
            text = font.render('Computer', True, BLACK, WHITE)
        else:
            pygame.draw.rect
            text = font.render('Player', True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (100, 40)
        screen.blit(text, text_rect)

        #push any changes to screen 
        pygame.display.update()


if __name__ == "__main__":
    main()
