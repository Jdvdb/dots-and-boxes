# Function and all necessary components for MCTS
import DotsAndBoxes
import DBNode
import random
import math
import copy
from pdb import set_trace as bp

# NOTE right now it is assumed computer is P1, this will be fixed once the code works

"""
Driver of the MCTS algorithm
tree: dictionary with IDs as keys and their respective nodes as the value
currentId: the next ID value to be used in children creation
rootId: ID of the root for this search
rollouts: number of rollouts to be performed
greed: determine how much the algorithm favours quick moves
Returns the ID of the next move the AI will choose AND the value for currentId
"""


def MCTS(tree, currentId, rootId, rollouts, greed):
    # generate random seed for simulations
    random.seed()

    # test values to tell how many UCT vs random searches are done
    rands = 0
    ucts = 0

    # get the root of the tree and increment ID counter
    root = tree[rootId]

    # this is the node referenced when traversing the tree
    currentNode = root

    # this will keep track of how many rollouts have been completed
    numRollouts = 0
    while numRollouts < rollouts:
        # start currentNode at the root
        currentNode = tree[root.id]

        # depth of the  tree before simulation
        depth = 0

        # traverse to the end of the tree based on UCT
        while len(currentNode.children) != 0:
            depth += 1
            # decide if UCT or randomSelect should be used
            if random.random() / float(len(currentNode.board.moves) / 4) > 0.4:
                nextNodeId = UCT(tree, currentNode)
                currentNode = tree[nextNodeId]
                ucts += 1
            else:
                nextNodeId = randomSelect(tree, currentNode)
                currentNode = tree[nextNodeId]
                rands += 1

        # first check if a node should have neighbours and if it does, then add them to children
        if not currentNode.board.checkEnd():
            # note that currentId is updated at the end
            currentId = expand(tree, currentNode, currentId)

        # if no children were found, then backpropogate this value
        if len(currentNode.children) == 0:
            reward = 0

            # determine if this helps the ai or the computer
            if currentNode.board.player != root.board.player:
                # the reward will be calculated as (p1score - p2score)/depth in the algorithm
                if currentNode.board.P1Score - currentNode.board.P2Score > 0 and currentNode.board.player:
                    reward = float(1)
                elif currentNode.board.P2Score - currentNode.board.P1Score > 0 and not currentNode.board.player:
                    reward = float(1)
                else:
                    reward = float(-15)

            # if currentNode.board.player:
            #     reward += float(currentNode.board.P1Score - 2 *
            #                     currentNode.board.P2Score)/float(depth)
            # elif currentNode.board.P2Score - currentNode.board.P1Score > 0 and not currentNode.board.player:
            #     reward += float(currentNode.board.P2Score - 2 *
            #                     currentNode.board.P1Score)/float(depth)

            # old point system bellow
            # reward = currentNode.board.P1Score - currentNode.board.P2Score

            # add greedyness to the reward TODO greed may not be applicable since static win v loss values
            if reward > 0:
                reward *= greed

            # back propogate the value up the tree and increase numRollouts
            backPropogation(tree, currentNode, reward, rootId, depth)
            numRollouts += 1
        # if children were found, then begin a rollout from a random position
        else:
            randChild = random.choice(tuple(currentNode.children))
            currentNode = tree[randChild]
            depth += 1

            # perform a rollout on the child and collect the reward
            reward = rollout(currentNode, depth)
            # add greedyness to the reward if applicable
            reward *= greed

            # back propogate the value up the tree and increase numRollouts
            backPropogation(tree, currentNode, reward, rootId, depth)
            numRollouts += 1

    # find the best child of the root node and return the id
    bestNodeId = maxChild(tree, root)
    print("rands:", rands, "ucts:", ucts)
    return bestNodeId, currentId


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
    parentSimulations = float(currentNode.visitCount)

    # iterate through each child
    # TODO: mess around with constants for good balance
    for childId in currentNode.children:
        # testNode is the node being investigated
        testNode = tree[childId]

        exploit = float(testNode.reward) / float(testNode.visitCount)
        explore = 10*math.sqrt(math.log(parentSimulations) /
                               float(testNode.visitCount))

        # UCT is based on exploration and exploitation
        testUCT = exploit + explore

        if maxUCT < testUCT:
            # print("new max:", explore, exploit, testUCT)
            bestId = childId
            maxUCT = testUCT
    # print("Found best")
    return bestId


"""
Randomly selects a child, replaces UCT at the beginning
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
Returns random child Id
"""


def randomSelect(tree, currentNode):
    randomId = random.sample(currentNode.children, 1)
    return randomId[0]


"""
Expands the tree by adding all of the children of some node
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
currentId: the ID value that should be used to start assigning values to the children
Returns the new value for currentId
"""


def expand(tree, currentNode, currentId):
    tempNode = copy.deepcopy(currentNode)
    parentId = copy.deepcopy(currentNode.id)
    # create a child for each available node in the game's available moves
    for move in tempNode.board.moves:
        # create a game with the new move
        tempGame = copy.deepcopy(currentNode.board)
        (direction, dotInd, lineInd) = move
        tempGame.addLine(direction, dotInd, lineInd)

        # create this new state in the tree and add it as a child to the current node
        tree[currentId] = DBNode.DBNode(
            tempGame, currentId, parentId, move)
        tree[parentId].addChild(currentId)

        # increment the ID
        currentId += 1
    return currentId


"""
Will play out one full game of dots and boxes randomly
currentNode: the current piece being investigated
Returns a reward for the game
"""


def rollout(currentNode, depth):
    # node that will be used for simulation
    tempNode = copy.deepcopy(currentNode)
    i = 0

    while len(tempNode.board.moves) != 0:
        i += 1
        # BUG: make sure tuple here does not change the set
        # select a random move available in the game
        play = random.choice(tuple(tempNode.board.moves))
        (direction, dotInd, lineInd) = play
        # this will return True if the game is done
        tempNode.board.addLine(direction, dotInd, lineInd)

    # if the AI won, give it a small reward, otherwise tell it not to suck and lose
    if tempNode.board.P1Score - tempNode.board.P2Score > 0 and currentNode.board.player:
        return float(1)
    elif tempNode.board.P2Score - tempNode.board.P1Score > 0 and not currentNode.board.player:
        return float(1)
    else:
        return float(-15)

    # if currentNode.board.player:
    #     return float(currentNode.board.P1Score - 2*currentNode.board.P2Score)/float(depth)
    # elif not currentNode.board.player:
    #     return float(currentNode.board.P2Score - 2*currentNode.board.P1Score)/float(depth)


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
    # determine if AI is p1 or p2
    aiPlayer = tree[rootId].board.player
    # traverse back up the tree
    while currentNode.id != rootId:
        tree[currentNode.id].visitCount += 1
        if currentNode.board.player != aiPlayer:
            tree[currentNode.id].reward += reward
        else:
            tree[currentNode.id].reward -= reward

        # TODO modify how reward multiplier works based on player vs computer win

        # set the current node to the parent
        currentNode = tree[currentNode.parent]

    # update the root's visit and reward values too
    tree[rootId].visitCount += 1
    tree[rootId].reward += reward
    tree


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

    print("total children:", len(currentNode.children))

    for child in currentNode.children:
        tempNode = tree[child]
        # best node has the greatest reward compared to visit count
        winValue = float(tempNode.reward) / float(tempNode.visitCount)
        print("Child", tree[child].newMove, "visits",
              tree[child].visitCount, "reward:", tree[child].reward, "win value:", winValue)

        if winValue > maxValue:
            maxValue = winValue
            maxId = child

        # print("Move:", tempNode.newMove, "Win Value:",
        #       winValue, "Visits:", tempNode.visitCount)

    return maxId
