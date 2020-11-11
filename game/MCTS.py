# Function and all necessary components for MCTS
import DotsAndBoxes
import DBNode
import random
import math

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
            # BUG: make sure this does not turn the children set into a tuple
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
    # this is the value that will be returned
    bestId = -1
    # this will be the value for the most promising node
    maxUCT = -math.inf
    # this is the number of times the parent node was visited
    parentSimulations = currentNode.visitCount

    # iterate through each child
    # TODO: mess around with constants for good balance
    for childId in currentNode.children:
        # testNode is the node being investigated
        testNode = tree[childId]

        exploit = currentNode.reward / currentNode.visitCount
        explore = 20*math.sqrt(math.log(parentSimulations) /
                               currentNode.visitCounts)

        # UCT is based on exploration and exploitation
        testUCT = exploit + explore

        if maxUCT < testUCT:
            bestId = childId
            maxUCT = testUCT
    return bestId


"""
Expands the tree by adding all of the children of some node
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
currentId: the ID value that should be used to start assigning values to the children
"""


def expand(tree, currentNode, currentId):
    # create a child for each available node in the game's available moves
    for move in currentNode.board.moves:
        # create a game with the new move
        tempGame = currentNode.board
        tempGame.addLine(move)

        # create this new state in the tree and add it as a child to the current node
        tree[currentId] = DBNode(tempGame, currentId, currentNode.id, move)
        currentNode.addChild(currentId)

        # increment the ID
        currentId += 1


"""
Will play out one full game of dots and boxes randomly
currentNode: the current piece being investigated
Returns a reward found from P1score-P2score
"""


def rollout(currentNode):
    # node that will be used for simulation
    tempNode = currentNode
    # flag for when simulation finishes
    finished = False

    while not finished:
        # BUG: make sure tuple here does not change the set
        # select a random move available in the game
        play = random.choice(tuple(tempNode.children))
        # this will return True if the game is done
        finished = tempNode.board.addLine(play)

    return tempNode.board.P1Score - tempNode.board.P2Score


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
    # modifier for the reward value TODO check it
    rewardMultiplier = 1

    # traverse back up the tree
    while currentNode.id != rootId:
        currentNode.visitCount += 1

        # TODO modify how reward multiplier works based on player vs computer win

        # set the current node to the parent
        currentNode = tree[currentNode.parent]

    # update the root's visit and reward values too
    currentNode.visitCount += 1
    currentNode.reward += rewardMultiplier * reward


"""
Finds the best move to play at the end of the simulation
tree: dictionary with IDs as keys and their respectives nodes as the values
root: the root node for this simulation
Returns the ID of the next most promising game state
"""


def maxChild(tree, currentNode):
    # values for the max win score and the node's ID
    maxValue = -math.inf
    maxId = 0

    for child in currentNode.children:
        tempNode = tree[child]
        # best node has the greatest reward compared to visit count
        winValue = tempNode.reward / tempNode.visitCount

        if winValue > maxValue:
            maxValue = winValue
            maxId = child

        print("Move:", tempNode.move, "Win Value:",
              winValue, "Visits:", tempNode.visitCount)

    return maxId
