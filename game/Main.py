# Driver Code For The Game
import DBNode
import DotsAndBoxes
import MCTS

if __name__ == "__main__":
    # all of this is test stuff right now
    print('play game')
    tempGame = DotsAndBoxes.DotsAndBoxes()

    tempGame.addLine(1, 2, 5)
    tempGame.addLine(0, 6, 2)
    tempGame.addLine(0, 5, 2)
    tempGame.addLine(1, 3, 5)

    tempGame.printBoard()
