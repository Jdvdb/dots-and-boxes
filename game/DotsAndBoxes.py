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

        # True means AI will make the next move, False means Human will make the next move
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
        # TODO: add check at the start to make sure given moves are legal to avoid bugs
        # TODO; more rigorous error testing, seems good but I'm not 100% sure things are good
        """
        Add a line to the current board game, remove it from the set, and switch players
        direction: 0 for horizontal line, 1 for vertical line
        dotInd: if horizontal, the row # the line will be in
        lineInd: if horizontal, the actual gap the line would be drawn in
        Returns True if a valid move, false otherwise
        """

        if direction == 0:
            # make sure inputs are valid for horizontal pieces
            if dotInd >= self.rowDots or lineInd >= self.rowSpaces:
                print("Invalid move, out of bounds")
                return False
            if self.rows[dotInd][lineInd] == 1:
                print('A line already exists there, try again')
                return False
            self.rows[dotInd][lineInd] = 1
            self.moves.remove((0, dotInd, lineInd))
        else:
            # make sure moves are valid for vertical pieces
            if dotInd >= self.colDots or lineInd >= self.colSpaces:
                print("Invalid move, out of bounds")
                return False
            if self.cols[dotInd][lineInd] == 1:
                print("A line already exists there, try again")
                return False
            self.cols[dotInd][lineInd] = 1
            self.moves.remove((1, dotInd, lineInd))
        # after adding line, check if the player got a point and then see if the game is over
        goAgain = self.checkPoint(direction, dotInd, lineInd)

        # switch the player
        if not goAgain:
            self.player = not self.player

        return True

    def checkPoint(self, direction, dotInd, lineInd):
        """
        Checks if the given move creates a box
        direction: 0 for horizontal line, 1 for vertical line
        dotInd: if horizontal, the row # the line will be in
        lineInd: if horizontal, the actual gap the line would be drawn in
        No values returned
        """
        # this will be the value added to player score at the end
        pointEarned = 0
        if direction == 0:
            # check if there is a line above and then see if you can make a box
            if dotInd > 0:
                if self.rows[dotInd - 1][lineInd] and self.cols[lineInd][dotInd-1] and self.cols[lineInd][dotInd-1]:
                    pointEarned = 1
            # check if there is a line bellow and then see if you can make a box
            if dotInd < self.rowDots - 1:
                if self.rows[dotInd + 1][lineInd] and self.cols[lineInd][dotInd] and self.cols[lineInd+1][dotInd]:
                    pointEarned = 1
        else:
            if dotInd > 0:
                # check if there is a line to the left and then see if you can make a box
                if self.cols[dotInd - 1][lineInd] and self.rows[lineInd][dotInd-1] and self.rows[lineInd+1][dotInd-1]:
                    pointEarned = 1
                    # check if there is a line to the right and then see if you can make a box

            if dotInd < self.colDots - 1:
                if self.cols[dotInd - 1][lineInd] and self.rows[lineInd][dotInd] and self.rows[lineInd+1][dotInd]:
                    pointEarned = 1

        # add earned points to the correct player
        if self.player:
            self.P1Score += pointEarned
        else:
            self.P2Score += pointEarned

        # if player should go again, return true
        if pointEarned > 0:
            return True
        else:
            return False

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
        # print arrays
        print("row and col")
        print(self.rows)
        print(self.cols)
        # show player scores and turn
        if self.player:
            print("Player turn: P1")
        else:
            print("Player turn: P2")
        print("P1 Score:", self.P1Score)
        print("P2 Score:", self.P2Score)
        print("board:")
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
            if col < self.colSpaces:
                for row in range(self.colDots):
                    if self.cols[row][col] == 0:
                        print("  ", end="")
                    else:
                        print("| ", end="")
            print()
