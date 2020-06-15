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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        score = float("-inf")
        currentFood = currentGameState.getFood()
        currentFoodList = currentFood.asList()

        # force the pacman does not stop his movement
        if (action == "stop"):
            return float("-inf")

        # find the distance between ghost and pacman
        for ghost in newGhostStates:
            if(newPos == ghost.getPosition()):
                # if the location of pacman is equal to the location of ghost then return infinite
                if(newScaredTimes[0] == 0):
                    return float("-inf")

        # find the distance between the food and pacman then get the minimal distance
        for food in currentFoodList:
            foodDis = -1*(manhattanDistance(food, newPos))
            if (foodDis > score):
                score = foodDis
        return score

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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

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

        #minValue function will return the minimal value of the ghost
        def minValue(gameState, numAgent, depth):
            result = [float("inf"),"null"]
            #if the ghost does not have further action, then return its evaluation value
            if (len(gameState.getLegalActions(numAgent)) == 0):
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(numAgent)
            #otherwise, find all the possible action that ghost will take
            for action in actions:
                state = gameState.generateSuccessor(numAgent, action)
                #find the value of action that next agent will take in next turn
                value = chooseMinMax(state, numAgent + 1, depth)
                #calculate the minimal value of the ghost
                if(type(value) is not list):
                    if(value < result[0]):
                        result[0] = value
                        result[1] = action
                else:
                    if(value[0] < result[0]):
                        result[0] = value[0]
                        result[1] = action
            return result

        #maxValue function will return the maximal value of pacman
        def maxValue(gameState, numAgent, depth):
            result = [float("-inf"),"null"]
            actions = gameState.getLegalActions(numAgent)
            #if the pacman does not have further action, then return its evaluation value
            if (len(actions) == 0):
                return self.evaluationFunction(gameState)
            #find all possible actions that pacman will take
            for action in actions:
                state = gameState.generateSuccessor(numAgent, action)
                #find the value of action that the next agent will take in next turn
                value = chooseMinMax(state, numAgent + 1, depth)
                #calculate the maximal value of the pacman
                if(type(value) is not list):
                    if(value > result[0]):
                        result[0] = value
                        result[1] = action
                else:
                    if(value[0] > result[0]):
                        result[0] = value[0]
                        result[1] = action
            return result

        #chooseMinMax function will return the minimax value of pacman
        def chooseMinMax(gameState, numAgent, depth):
            #if both the ghost and pacman has taken the action in a turn,
            # then add 1 to the variable depth and reset the numAgent to 0
            if(numAgent >= gameState.getNumAgents()):
                depth = depth + 1
                numAgent = 0
            #if the turn is finished, then return the evaluation value of that agent
            if (depth == self.depth):
                return self.evaluationFunction(gameState)
            #if the agent is pacman, then find the maximal value of pacman that it can have in that turn
            elif(numAgent == 0):
                return maxValue(gameState, numAgent, depth)
            #otherwise, find the minimal value of ghost that it can have in that turn
            else:
                return minValue(gameState, numAgent, depth)

        answer = chooseMinMax(gameState, 0, 0)
        return answer[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        #expectValue function will return the expected value of ghost
        def expectValue(gameState, numAgent, depth):
            count = 0
            result = [count,"null"]
            #if the ghost does not have further action, then return its evaluation value
            if (len(gameState.getLegalActions(numAgent)) == 0):
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(numAgent)
            #find all possible actions that ghost will take
            for action in actions:
                state = gameState.generateSuccessor(numAgent, action)
                #find the value of next agent that it will have in the next turn
                value = chooseExpectiMax(state, numAgent + 1, depth)
                #calculate the expected value of ghost
                if(type(value) is not list):
                    count = count + value
                else:
                    count = count + value[0]
                    result[1] = actions
            result[0] = count/len(actions)
            return result

        #maxValue function will return the maximal value of pacman
        def maxValue(gameState, numAgent, depth):
            result = [float("-inf"),"null"]
            actions = gameState.getLegalActions(numAgent)
            #if the pacman does not have further action, then return its evaluation value
            if (len(actions) == 0):
                return self.evaluationFunction(gameState)
            #find all possible actions that pacman will take
            for action in actions:
                state = gameState.generateSuccessor(numAgent, action)
                #find the value of action that the next agent will take in next turn
                value = chooseExpectiMax(state, numAgent + 1, depth)
                #calculate the maximal value of the pacman
                if(type(value) is not list):
                    if(value > result[0]):
                        result[0] = value
                        result[1] = action
                else:
                    if(value[0] > result[0]):
                        result[0] = value[0]
                        result[1] = action
            return result

        #chooseExpectiMax function will return the expectimax value of agent
        def chooseExpectiMax(gameState, numAgent, depth):
            #if both the ghost and pacman has taken the action in a turn,
            # then add 1 to the variable depth and reset the numAgent to 0
            if(numAgent >= gameState.getNumAgents()):
                depth = depth + 1
                numAgent = 0
            #if the turn is finished, then return the evaluation value of that agent
            if (depth == self.depth):
                return self.evaluationFunction(gameState)
            #if the agent is pacman, then find the maximal value of pacman that it can have in that turn
            elif(numAgent == 0):
                return maxValue(gameState, numAgent, depth)
            #otherwise, find the expected value of ghost that it can have in that turn
            else:
                return expectValue(gameState, numAgent, depth)

        answer = chooseExpectiMax(gameState, 0, 0)
        return answer[1]



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
