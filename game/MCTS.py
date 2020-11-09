# Function and all necessary components for MCTS
import DotsAndBoxes
import DBNode

"""
Driver of the MCTS algorithm
tree: dictionary with IDs as keys and their respective nodes as the value
currentId: the next ID value to be used in children creation
rootId: ID of the root for this search
rollouts: number of rollouts to be performed
greed: determine how much the algorithm favours quick moves
Returns the ID of the next move the AI will choose
"""


def MCTS(tree, currentId, rootId, rollouts, greed):
    pass


"""
Selects next node to explore based on Upper Confidence Bounds applied to Trees
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
Returns the ID of the next node to be explored
"""


def UCT(tree, currentNode):
    pass


"""
Expands the tree by adding all of the children of some node
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
currentId: the ID value that should be used to start assigning values to the children
"""


def expand(tree, currentNode, currentId):
    pass


"""
Will play out one full game of dots and boxes randomly
currentNode: the current piece being investigated
Returns a tuple containing (computer, player) scores
"""


def rollout(currentNode, depth):
    pass


"""
Back propogates return from simulated game up the tree
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
reward: the reward found from the rollout at currentNode
rootId: the ID of the root node in this simulation
"""


def backPropogation(tree, currentNode, reward, rootId):
    pass


"""
Finds the best move to play at the end of the simulation
tree: dictionary with IDs as keys and their respectives nodes as the values
root: the root node for this simulation
Returns the ID of the next most promising game state
"""


def maxChild(tree, currentNode):
    pass
