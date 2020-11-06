# Class to play the game of dots and boxes on 8x6 dots
from pdb import set_trace as bp


class DotsAndBoxes:
    def __init__(self):
        # these values will describe how to setup rows/cols
        # there are 7 rows of dots, each with 8 spaces
        self.rowSpaces = 8
        self.rowDots = 7
        # there are 9 columns of dots, each with 6 spaces
        self.colSpaces = 6
        self.colDots = 9

        # rows describe all of the horizontal lines, 0 is empty, 1 is line
        self.rows = []
        self.intializeRows()
        # cols describe all the vertical lines, 0 is empty, 1 is line
        self.cols = []
        self.initializeCols()
        # set of empty spaces, good for random move generation
        self.moves = set()
        self.initializeMoves()

        # True means P1 will make the next move, False means P2 will make the next move
        self.player = True

        # scores for first and second player
        self.P1Score = 0
        self.P2Score = 0

    def intializeRows(self):
        for i in range(self.rowDots):
            col = []
            for j in range(self.rowSpaces):
                col.append(0)
            self.rows.append(col)

    def initializeCols(self):
        for i in range(self.colDots):
            col = []
            for j in range(self.colSpaces):
                col.append(0)
            self.cols.append(col)

    def initializeMoves(self):
        """
        Fill the moves list with all available moves at the start of the game
        No return provided
        """
        # moves for the rows array
        for row in range(self.colDots):
            for col in range(self.colSpaces):
                # 0 indicates this is a horizontal line
                self.moves.add((1, row, col))

        # moves for the col array
        for row in range(self.rowDots):
            for col in range(self.rowSpaces):
                # 1 indicates this is a vertical line
                self.moves.add((0, row, col))

    def addLine(self, direction, dotInd, lineInd):
        """
        Add a line to the current board game, remove it from the set, and switch players
        direction: 0 for horizontal line, 1 for vertical line
        dotInd: if horizontal, the row # the line will be in
        lineInd: if horizontal, the actual gap the line would be drawn in
        Returns True if this ends the game, false otherwise
        """

        if direction == 0:
            if self.rows[dotInd][lineInd] == 1:
                print('A line already exists there, try again')
                return
            self.rows[dotInd][lineInd] = 1
            self.moves.remove((0, dotInd, lineInd))
        else:
            if self.cols[dotInd][lineInd] == 1:
                print("A line already exists there, try again")
                return
            self.cols[dotInd][lineInd] = 1
            self.moves.remove((1, dotInd, lineInd))
        # after adding line, check if the player got a point and then see if the game is over
        self.checkPoint(direction, dotInd, lineInd)
        self.checkEnd()
        # switch the player
        self.player = not self.player

    def checkPoint(self, direction, dotInd, lineInd):
        """
        Checks if the given move creates a box
        direction: 0 for horizontal line, 1 for vertical line
        dotInd: if horizontal, the row # the line will be in
        lineInd: if horizontal, the actual gap the line would be drawn in
        No values returned
        """
        if direction == 0:
            pass
        else:
            pass

    def checkEnd(self):
        """
        Checks to see if the game is over yet.
        Returns True if it is, false otherwise
        """
        if len(self.moves) == 0:
            return True
        else:
            return False

    def printBoard(self):
        """
        Prints the current board state to the console
        Returns nothing
        """
        # print(self.rows)
        for col in range(self.rowDots):
            for row in range(self.colDots):
                # print dots across a row
                print('.', end="")
                if row < self.rowSpaces:
                    # print(row, col)
                    # add horizontal lines where needed
                    if self.rows[col][row] == 0:
                        print(' ', end="")
                    else:
                        print('-', end="")

            print()
            # print vertical lines where needed before next row
            if col < 6:
                for row in range(self.colSpaces):
                    if self.cols[row][col] == 0:
                        print("  ", end="")
                    else:
                        print("| ", end="")
            print()
