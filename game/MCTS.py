# Function and all necessary components for MCTS
import DotsAndBoxes
import DBNode
import random

# NOTE right now it is assumed computer is P1, this will be fixed once the code works

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
    # generate random seed for simulations
    random.seed()

    # get the root of the tree and increment ID counter
    root = tree[rootId]
    currentId += 1

    # this is the node referenced when traversing the tree
    currentNode = root

    # this will keep track of how many rollouts have been completed
    numRollouts = 0
    while numRollouts < rollouts:
        # start currentNode at the root
        currentNode = tree[root.id]

        # depth of the tree before simulation
        depth = 0

        # traverse to the end of the tree based on UCT
        while len(currentNode.children) != 0:
            depth += 1
            nextNodeId = UCT(tree, currentNode)
            currentNode = tree[nextNodeId]

        # first check if a node should have neighbours and if it does, then add them to children
        if not currentNode.checkEnd():
            expand(tree, currentNode, currentId)

        # if no children were found, then backpropogate this value
        if len(currentNode.children) == 0:
            # the reward will be calculated as (p1score - p2score)/depth in the algorithm
            reward = currentNode.P1Score - currentNode.P2Score
            # add greedyness to the reward
            reward *= greed

            # back propogate the value up the tree and increase numRollouts
            backPropogation(tree, currentNode, reward, rootId, depth)
            numRollouts += 1
        # if children were found, then begin a rollout from a random position
        else:
            # bug warning: make sure this does not turn the children set into a tuple
            randChild = random.choice(tuple(currentNode.children))
            currentNode = tree[randChild]
            depth += 1

            # perform a rollout on the child and collect the reward
            reward = rollout(currentNode)
            # add greedyness to the reward if applicable
            reward *= greed

            # back propogate the value up the tree and increase numRollouts
            backPropogation(tree, currentNode, reward, rootId, depth)
            numRollouts += 1

        # find the best child of the root node and return the id
        bestNodeId = maxChild(tree, root)
        return bestNodeId


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
Returns a reward found from P1score-P2score
"""


def rollout(currentNode):
    pass


"""
Back propogates return from simulated game up the tree
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
reward: the reward found from the rollout at currentNode
rootId: the ID of the root node in this simulation
depth: the current depth of the node in the tree
No return
"""


def backPropogation(tree, currentNode, reward, rootId, depth):
    pass


"""
Finds the best move to play at the end of the simulation
tree: dictionary with IDs as keys and their respectives nodes as the values
root: the root node for this simulation
Returns the ID of the next most promising game state
"""


def maxChild(tree, currentNode):
    pass
