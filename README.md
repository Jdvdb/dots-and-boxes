# Dots and Boxes

dots and boxes game/AI opponent for CMPUT 355 at UofA

## Project Files

constants.py - a file that holds values that would normally be kept private.
In our case, it held the font information since we used one from
https://fonts.adobe.com/fonts/lato

DBNode.py - a class for a Dots and Boxes Node used in MCTS

DotsAndBoxes.py - a class for a game of Dots and Boxes

Game.py - driver for game intended for AI vs Human.
Note that at the start of the file, BRAIN_POWER can be adjusted to change
the time given to the computer to think. 1 is default value. It is simply
a multiplier for the number of rollouts used in a game

GreedyTest.py - a program that will simulate a desired number of games
against a greedy opponent that we programmed. It will play randomly
unless it knows a certain move will increase its total points. If there
is such a child, then it will pick the move that gives the most points.

MCTS.py - Driver for the Monte Carlo Tree Search Algorithm. Contains all
relevant functions to execute the algorithm with a game of Dots and Boxes.

RandomTest.py - a program that will simulate a desired number of games against a
random opponent that we programmed. It will always play a random move.

TerminalGame.py - A way to play the game in the terminal. To play a piece,
3 numbers should be given, each separated by a space with no trailing characters

fonts/Lato\* - there should be multiple Lato stored for the PyGame version.

Tests/\* - test results made by GreedyTest.py, RandomTest.py, and one hand made one. All formulated based on
last edits to MCTS.

README.md - Description of the project

License - License for the project

## Ways to Run the Project:

Game.py - Runs an interactive game of Dots and Boxes
Instructions: Before starting the game, change the value of
BRAIN_POWER in the file for desired AI strength between 0 and 2.
Ensure you have an up to date version of PyGame installed too.
In the terminal, run 'python3 Game.py'. Use your mouse to
select where you want to play whenever it is your turn.
The game closes as soon as the final move is made.
The results will be printed to the terminal

TerminalGame.py - Runs a version mainly used for testing of Dots and Boxes.
Before starting the game, change the value of
BRAIN_POWER in the file for desired AI strength between 0 and 2.
Instructions: In the terminal, run 'python3 TerminalGame.py'. When
prompted to print a move, enter 3 number separted with a space as follows:
first: 0 to represent horizontal line, 1 to represent a vertical line.
second: if using a horizontal piece, then it is the row number (0 at top, 3 at bottom).
if using a vertical piece, then it is col number (0 on the left, 3 on the right).
third: if using a horizontal piece, then it is the index of the space
(0 on the left, 2 on the right).
if using a vertical piece, then it is the index of the space (0 at the
top, 2 at the bottom)
e.g. 0 2 1

RandomTest.py - Will test the AI against a random opponent.
This can take a long time depending on brain power and games.
Before running, alter values with NOTE comments at
the top of the file for desired output.
In the terminal, run 'python3 RandomTest.py > results.txt' where
results.txt is the file you want the results stored in.

RandomTest.py - Will test the AI against a greedy opponent.
This can take a long time depending on brain power and games.
Before running, alter values with NOTE comments at
the top of the file for desired output.
In the terminal, run 'python3 RandomTest.py > results.txt' where
results.txt is the file you want the results stored in.
