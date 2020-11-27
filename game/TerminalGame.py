# Driver Code For The Game
import DBNode
import DotsAndBoxes
import random
import MCTS

# NOTE: This is a value you can modify to give the computer more/less time to think, 1 is standard
BRAIN_POWER = 1


def endGame(board):
    print("Game Done")
    print("P1:", board.P1Score, "P2:", board.P2Score)
    if board.P1Score > board.P2Score:
        print("AI Won!")
    else:
        print("Human Won!")
    quit()


# right now, assume computer plays first
if __name__ == "__main__":
    # all of this is test stuff right now
    tempGame = DotsAndBoxes.DotsAndBoxes()

    # value for creating IDs
    currentId = 0

    # root node for the tree
    root = DBNode.DBNode(tempGame, currentId, -1, (-1, 0, 0))
    currentId += 1

    # dictionary that will act as the game tree
    tree = dict()
    tree[root.id] = root

    # this is a placeholder for what MCTS will use to determine number of rollouts
    rollouts = 1

    # flag to keep playing the game
    playing = True

    nextComputerId, currentId = MCTS.MCTS(
        tree, currentId, root.id, rollouts)

    while playing:
        # this is for P2/Human turn
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

        # this is for P1/AI
        else:
            print("Computer is thinking...")

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
