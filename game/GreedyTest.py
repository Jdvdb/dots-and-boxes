# Created by Jordan Van Den Bruel & Danny Zaiter
import DBNode
import DotsAndBoxes
import MCTS
import random
import copy

"""
Plays a random move from the current node in the tree
Arguments: node = DBNode representing the current state of the game
Returns a random child ID of that node
"""


def greedyMove(currentGame):
    maxScore = -1
    tempScore = -1
    bestMove = (-1, -1, -1)
    for move in currentGame.moves:
        tempGame = copy.deepcopy(currentGame)
        (direction, dotInd, lineInd) = move
        tempGame.addLine(direction, dotInd, lineInd)

        tempScore = tempGame.P2Score - currentGame.P2Score
        if tempScore > maxScore:

            maxScore = tempScore
            bestMove = move

    return bestMove


"""
Driver function that will prepare the tests and print the result
"""


def getTestData():
    # NOTE number of games played
    games = 25.0
    gamesPlayed = 0.0

    # number of MCTS wins
    MCTSWin = 0.0
    # number of Greedy wins
    GreedyWin = 0.0

    # total score for MCTS and Greedy
    scores = [0.0, 0.0]

    # NOTE value that would be used to manipulate how long thinking is
    brainPower = 1.0

    print("TEST INFO:")
    print("Games to be played:", int(games))
    print("Brain Power Given:", brainPower)
    print("Rollouts while lines remaining is greater than 22:", int(brainPower*3500))
    print("Rollouts while lines remaining is greater than 16 and less than or equal to 22:", int(
        brainPower*8000))
    print("Rollouts while lines remaining is greater than 12 and less than or equal to 16:", int(
        brainPower*11000))
    print("Rollouts while lines remaining is greater than 0 and less than or equal to 12:", int(
        brainPower*13000))
    print()
    print("-----------------")
    print()
    print("Game Results:")
    print()

    # simulate the games
    while gamesPlayed < games:
        print("Game", int(gamesPlayed))
        tempScores = playGame(brainPower)

        # add the scores from these games to the total scores
        scores[0] += tempScores[0]
        scores[1] += tempScores[1]

        # increment the win value appropriately
        if tempScores[0] > tempScores[1]:
            MCTSWin += 1.0
        else:
            GreedyWin += 1.0
        print("P1:", tempScores[0], "P2:", tempScores[1])
        print()

        gamesPlayed += 1.0
    print("-----------------")
    print()
    print(games, "games finished.")
    print("MCTS WINS:", MCTSWin)
    print("Greedy WINS:", GreedyWin)
    print()
    print("AVG. MCTS SCORE:", float(scores[0]) / float(games))
    print("AVG. Greedy SCORES:", float(scores[1]) / float(games))
    print()
    print("MCTS WIN RATIO:", MCTSWin / games)
    print("Greedy WIN RATIO", GreedyWin / games)


"""
Function to play a simulation with a greedy opponent
Arguments: brainPower: the brain power desired for the simulation
Returns: a tuple a (P1/AI score, P2/Human score)
"""


def playGame(brainPower):
    # temp game for the simulation
    tempGame = DotsAndBoxes.DotsAndBoxes()

    # value for creating IDs
    currentId = 0

    # root node for the tree
    root = DBNode.DBNode(tempGame, currentId, -1, (-1, 0, 0))
    currentId += 1

    # dictionary that will act as the game tree
    tree = dict()
    tree[root.id] = root

    while True:
        if not tempGame.player:
            move = greedyMove(tempGame)
            (direction, dotInd, lineInd) = move
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
                    tree[currentId] = newNode
                    nextNode = newNode.id
                    currentId += 1

            # update the root for the computer
            root = tree[nextNode]

        else:
            if len(root.board.moves) < 12:
                rollouts = 13000
            elif len(root.board.moves) < 16:
                rollouts = 11000
            elif len(root.board.moves) < 22:
                rollouts = 8000
            else:
                rollouts = 3500
            rollouts *= brainPower
            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, rollouts)

            # update the root
            root = tree[nextComputerId]

        tempGame = root.board

        # root.board.printBoard()

        if root.board.checkEnd():
            return (root.board.P1Score, root.board.P2Score)


# right now, assume computer plays first
if __name__ == "__main__":
    getTestData()
