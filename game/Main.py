# Driver Code For The Game
import DBNode
import DotsAndBoxes
import MCTS

if __name__ == "__main__":
    # all of this is test stuff right now
    print('play game')
    tempGame = DotsAndBoxes.DotsAndBoxes()
    tempGame.addLine(0, 0, 0)
    tempGame.addLine(0, 4, 3)
    tempGame.addLine(0, 4, 7)
    tempGame.addLine(1, 0, 4)
    tempGame.printBoard()
