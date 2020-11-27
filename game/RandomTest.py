# Created by Jordan Van Den Bruel & Danny Zaiter
import DBNode
import DotsAndBoxes
import MCTS
import random

"""
Plays a random move from the current node in the tree
Arguments: node = DBNode representing the current state of the game
Returns a random child ID of that node
"""


def randomMove(node):
    randomId = random.sample(node.children, 1)
    return randomId[0]


"""
Driver function that will prepare the tests and print the result
"""


def getTestData():
    # NOTE number of games played
    games = 100.0
    gamesPlayed = 0.0

    # number of MCTS wins
    MCTSWin = 0.0
    # number of random wins
    RandomWin = 0.0

    # total score for MCTS and Random
    scores = [0.0, 0.0]

    # NOTE value that would be used to manipulate how long thinking is
    brainPower = 0.1

    print("TEST INFO:")
    print("Games to be played:", int(games))
    print("Brain Power Given:", brainPower)
    print("Rollouts while lines remaining is greater than 22:", int(brainPower*3000))
    print("Rollouts while lines remaining is greater than 16 and less than or equal to 22:", int(
        brainPower*7500))
    print("Rollouts while lines remaining is greater than 12 and less than or equal to 16:", int(
        brainPower*10000))
    print("Rollouts while lines remaining is greater than 0 and less than or equal to 12:", int(
        brainPower*12500))
    print()
    print("-----------------")
    print()
    print("Game Results:")
    print()

    # simulate the games
    while gamesPlayed < games:
        print("Game", int(gamesPlayed))
        tempScores = playGame(brainPower)

        # add the scores from these games to the total score
        scores[0] += tempScores[0]
        scores[1] += tempScores[1]

        # increment the win value appropriately
        if scores[0] > scores[1]:
            MCTSWin += 1.0
        else:
            RandomWin += 1.0
        print("P1:", tempScores[0], "P2:", tempScores[1])
        print()

        gamesPlayed += 1.0
    print("-----------------")
    print()
    print(games, "games finished.")
    print("MCTS WINS:", MCTSWin)
    print("RANDOM WINS:", RandomWin)
    print()
    print("AVG. MCTS SCORE:", scores[0] / games)
    print("AVG. RANDOM SCORES:", scores[1] / games)
    print()
    print("MCTS WIN RATIO:", MCTSWin / games)
    print("RANDOM WIN RATIO", RandomWin / games)


"""
Function to play a simulation with a random opponent
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
            nextNode = randomMove(root)

            # update the root for the computer
            root = tree[nextNode]

        else:
            if len(root.board.moves) < 12:
                rollouts = 12500
            elif len(root.board.moves) < 16:
                rollouts = 10000
            elif len(root.board.moves) < 22:
                rollouts = 7500
            else:
                rollouts = 3000
            rollouts *= brainPower
            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, rollouts)
            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, rollouts)

            # update the root
            root = tree[nextComputerId]

        if root.board.checkEnd():
            return (root.board.P1Score, root.board.P2Score)


if __name__ == "__main__":
    getTestData()
