# Driver Code For The Game
import DBNode
import DotsAndBoxes
import MCTS
import random
from pdb import set_trace as bp


def endGame(board):
    print("game done, work on this later...", board.boxes)
    quit()


def randomMove(node):
    randomId = random.sample(node.children, 1)
    return randomId[0]


# right now, assume computer plays first
if __name__ == "__main__":
    # all of this is test stuff right now
    print('loading')
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
    rollouts = 2000

    # flag to keep playing the game
    playing = True

    # TODO if player ever goes first, add a flag and special method for firstMove

    nextComputerId, currentId = MCTS.MCTS(
        tree, currentId, root.id, rollouts)

    while playing:
        if not tempGame.player:
            nextNode = randomMove(root)
            # check to see if finished the game
            if tempGame.checkEnd():
                endGame(tempGame)

            # update the root for the computer
            root = tree[nextNode]

        else:
            # this means computer turn
            print("Computer is thinking...")

            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, rollouts)

            # update the root
            root = tree[nextComputerId]

            if root.board.checkEnd():
                endGame(root.board)

        # stats to read after each move
        print("tree size:", len(tree))
        print("last move:", root.newMove)
        tempGame = root.board
        tempGame.printBoard()
        if root.board.player:
            print("next player: AI")
        else:
            print("next player: human")
