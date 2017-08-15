# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newDir = successorGameState.getPacmanState().getDirection()

        #print "newPos:", newPos, 
        #print "newFood:", newFood
        #print "newGhostPos:", successorGameState.getGhostPositions()
        #print  "newScaredTimes:",newScaredTimes
        "*** YOUR CODE HERE ***"
        """
        EAST = Directions.EAST
        WEST = Directions.WEST
        NORTH = Directions.NORTH
        SOUTH = Directions.SOUTH
        (x,y) = newPos

        for newGhostState in successorGameState.getGhostStates():
            ghostPosn = newGhostState.configuration.getPosition() 
            ghostDir = newGhostState.configuration.getDirection() 

            if (newPos == ghostPosn):
               return -99999

            (gx1, gy1) = ghostPosn

            # Check if pacman and Ghost will collide
            if (x+1 == gx1) and (y == gy1):
               if newDir == EAST and ghostDir == WEST:
                  return -99999

            if (x-1 == gx1) and (y == gy1):
               if newDir == WEST and ghostDir == EAST:
                  return -99999

            if (x == gx1) and (y+1 == gy1):
               if newDir == NORTH and ghostDir == SOUTH:
                  return -99999

            if (x == gx1) and (y-1 == gy1):
               if newDir == SOUTH and ghostDir == NORTH:
                  return -99999
        """

        flag = 0
        ghost_cost = 0
        for GhostState in successorGameState.getGhostStates():
            ghostPosn = GhostState.configuration.getPosition()
            if not flag:
                flag = 1
                tmp = manhattanDistance(newPos, ghostPosn)
            else:
                tmp = min(tmp, manhattanDistance(newPos, ghostPosn))
        if tmp > 0:
            ghost_cost = (10.0)/tmp

        food_award = 0
        flag = 0
        for foodPos in newFood.asList():
            if not flag:
               flag = 1
               tmp = manhattanDistance(newPos, foodPos)
            else:
               tmp = min(tmp, manhattanDistance(newPos, foodPos))
        if tmp > 0:
            food_award = (10)/tmp

        return (successorGameState.getScore()-ghost_cost+food_award)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def isTerminal(self, state, depth, agent):
        return depth == self.depth or \
               state.isWin() or \
               state.isLose() or \
               state.getLegalActions(agent) == 0

    def evaluate(self, gameState, depth, agentIndex):

        if self.isTerminal(gameState, depth, agentIndex):
            return [self.evaluationFunction(gameState), Directions.STOP]

        ret = []
        scores = []
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            newGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex < gameState.getNumAgents()-1:
                elem = self.evaluate(newGameState, depth, agentIndex+1)
                scores.append([elem[0], action])
            else:
                elem = self.evaluate(newGameState, depth+1, 0)
                scores.append([elem[0], action])

        # print "depth: agentIndex: scores :", depth, agentIndex,scores

        if agentIndex == 0:
            max_entry_f = 0
            for entry in scores:
                #if len(entry) > 0:
                    #print "1. ret : entry", ret, entry
                if not max_entry_f:
                    max_entry_f = 1
                    ret = entry
                else:
                    if ret[0] <= entry[0]:
                       ret = entry
        else:
            min_entry_f = 0
            for entry in scores:
                #if len(entry) > 0:
                    #print "2. ret : entry", ret, entry
                if not min_entry_f:
                    min_entry_f = 1
                    ret = entry 
                else:
                    if ret[0] > entry[0]:
                       ret = entry
           
        return ret

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        ret = self.evaluate(gameState, 0, 0)
        return ret[1]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def isTerminal(self, state, depth, agent):
        return depth == self.depth or \
               state.isWin() or \
               state.isLose() or \
               state.getLegalActions(agent) == 0

    def evaluate(self, gameState, alpha, beta, depth, agentIndex):
        if self.isTerminal(gameState, depth, agentIndex):
           return [self.evaluationFunction(gameState), Directions.STOP]
        
        scores = []
        ret = []
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            newGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex < gameState.getNumAgents()-1:
                elem = self.evaluate(newGameState, alpha, beta, depth, agentIndex + 1)
                scores.append([elem[0], action])
            else:
                elem = self.evaluate(newGameState, alpha, beta, depth+1, 0)
                scores.append([elem[0], action])

            if agentIndex != 0:
                # Min Node. Modify beta, compare elem to alpha.
                if elem[0] < alpha:
                    break

                if elem[0] < beta:
                    beta = elem[0]
            else:
                # Max Node. Modify alpha, compare elem to beta.
                if elem[0] > beta:
                    break

                if alpha < elem[0]:
                    alpha = elem[0]

        if agentIndex == 0:
            max_elem_f = 0
            for elem in scores:
                if not max_elem_f:
                    res = elem
                    max_elem_f = 1
                else:
                    if res[0] < elem[0]:
                        res = elem
        else:
            min_elem_f = 0
            for elem in scores:
                if not min_elem_f:
                    res = elem
                    min_elem_f = 1
                else:
                    if res[0] > elem[0]:
                        res = elem

        return res

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        elem = self.evaluate(gameState, -99999, 99999, 0, 0)
        return elem[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def isTerminal(self, state, depth, agent):
        return depth == self.depth or \
               state.isWin() or \
               state.isLose() or \
               state.getLegalActions(agent) == 0

    def evaluate(self, gameState, depth, agentIndex):
        if self.isTerminal(gameState, depth, agentIndex):
            return [self.evaluationFunction(gameState), Directions.STOP]

        scores = []
        res = []
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            newGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex < gameState.getNumAgents() - 1:
                elem = self.evaluate(newGameState, depth, agentIndex+1)
                scores.append([elem[0], action])
            else:
                elem = self.evaluate(newGameState, depth+1, 0)
                scores.append([elem[0], action])

        if agentIndex == 0:
            max_elem_f = 0
            for elem in scores:
                if not max_elem_f:
                    max_elem_f = 1
                    res = elem
                else:
                    if res[0] < elem[0]:
                        res = elem
        else:
            val = 1.0
            for elem in scores:
                val += elem[0]
            res = [(val*1.0)/len(legalActions), Directions.STOP]

        return res

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        elem = self.evaluate(gameState, 0, 0)
        return elem[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    val = currentGameState.getScore()
    newFood = currentGameState.getFood()
    min_food_f = 0
    minDist = 0
    WEIGHT_OF_FOOD = 10.0
    WEIGHT_OF_GHOST = 10.0
    WEIGHT_OF_SCARED = 50.0

    for foodLoc in newFood.asList():
        if not min_food_f:
            min_food_f = 1
            minDist = manhattanDistance(newPos,foodLoc)
        else:
            if manhattanDistance(newPos,foodLoc) < minDist:
                minDist = manhattanDistance(newPos,foodLoc)

    if minDist > 0:
        val += WEIGHT_OF_FOOD/minDist

    for ghost in currentGameState.getGhostStates():
        #print ghost, ghost.getPosition(), ghost.scaredTimer
        #print "done"
        ghostDist = manhattanDistance(newPos, ghost.getPosition())
        if ghostDist > 0:
            if ghost.scaredTimer > 0:
                val += WEIGHT_OF_SCARED/ghostDist
            else:
                val -= WEIGHT_OF_GHOST/ghostDist
            
    #for ghost in currentGameState.getGhostStates():
    #    if manhattanDistance(newPos, 
    
    return val
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

