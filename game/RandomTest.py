# Driver Code For The Game
import DBNode
import DotsAndBoxes
import MCTS
import random
from pdb import set_trace as bp


def randomMove(node):
    randomId = random.sample(node.children, 1)
    return randomId[0]


def getTestData():
    # number of games played
    games = 100.0
    gamesPlayed = 0.0

    # number of MCTS wins
    MCTSWin = 0.0
    # number of random wins
    RandomWin = 0.0

    # total score for MCTS and Random
    scores = [0.0, 0.0]

    # number of rollouts for sim
    rollouts = 100

    print("TEST INFO:")
    print("Games to be played:", int(games))
    print("Simulations:", rollouts, "per turn")
    print()
    print("-----------------")
    print()
    print("Game Results:")
    print()

    while gamesPlayed < games:
        print("Game", int(gamesPlayed))
        tempScores = playGame(rollouts)

        scores[0] += tempScores[0]
        scores[1] += tempScores[1]

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


def playGame(totalRollouts):
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

    nextComputerId, currentId = MCTS.MCTS(
        tree, currentId, root.id, totalRollouts)

    while True:
        if not tempGame.player:
            nextNode = randomMove(root)

            # update the root for the computer
            root = tree[nextNode]

        else:
            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, totalRollouts)

            # update the root
            root = tree[nextComputerId]

        if root.board.checkEnd():
            return (root.board.P1Score, root.board.P2Score)


# right now, assume computer plays first
if __name__ == "__main__":
    getTestData()
