# Driver Code For The Game
import DBNode
import DotsAndBoxes
import MCTS

if __name__ == "__main__":
    # all of this is test stuff right now
    print('play game')
    tempGame = DotsAndBoxes.DotsAndBoxes()

    # for i in range(7):
    #     for j in range(8):
    #         tempGame.addLine(0, i, j)

    # for i in range(10):
    #     for j in range(6):
    #         tempGame.addLine(1, i, j)

    tempGame.printBoard()
