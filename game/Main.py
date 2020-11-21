# Driver Code For The Game
import DBNode
import DotsAndBoxes
import MCTS
from pdb import set_trace as bp


def endGame(board):
    print("game done, work on this later...", board.boxes)


# right now, assume computer plays first
if __name__ == "__main__":
    # all of this is test stuff right now
    print('play game')
    tempGame = DotsAndBoxes.DotsAndBoxes()

    # value for creating IDs
    currentId = 0

    # root node for the tree
    root = DBNode.DBNode(tempGame, currentId, -1, (-1, 0, 0))
    currentId += 1

    # dictionary that will act as the game tree
    tree = dict()
    tree[root.id] = root

    # greed value to be used in MCTS
    greed = 1

    # number of rollouts to be performed
    rollouts = 800

    # flag to keep playing the game
    playing = True

    # TODO if player ever goes first, add a flag and special method for firstMove

    while playing:
        if not tempGame.player:
            print('Pick a move')
            move = input().split(" ")
            for i in range(3):
                move[i] = int(move[i])

            move = tuple(move)
            (direction, dotInd, lineInd) = move

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
                    newNode.board.addLine(direction, dotInd, lineInd)
                    nextNode = newNode.id
                    currentId += 1

                    # add new node to the tree
                    tree[newNode.id] = newNode

                # check to see if finished the game
                if tempGame.checkEnd():
                    endGame(tempGame)

                # update the root for the computer
                root = tree[nextNode]

            else:
                print("There is already a line there, try again")

        else:
            # this means computer turn
            print("Computer is thinking...")

            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, rollouts, greed)

            # update the root
            root = tree[nextComputerId]

        # stats to read after each move
        print("tree size:", len(tree))
        print("last move:", root.newMove)
        tempGame = root.board
        tempGame.printBoard()
        if root.board.player:
            print("next player: AI")
        else:
            print("next player: human")
