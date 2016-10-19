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

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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

        best_score, best_direction = float("-inf"), None
        for temp_direction in gameState.getLegalActions(0):
            score = self.minMax(gameState.generateSuccessor(0, temp_direction), 1)
            if score > best_score:
                best_score = score
                best_direction = temp_direction
                # print ('Best_Score: %i Score: %i, Dir: %s, isMax: %s' % (best_score, score, best_direction, isMaxPlayer))
        return best_direction

        util.raiseNotDefined()

    def minMax(self, gameState, depth):
        inf = float("inf")
        agent = depth % gameState.getNumAgents()
        # print 'D:%i, isMax: %s' % (depth, isMaxPlayer)

        if depth == gameState.getNumAgents() * self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if agent == 0:
            best_score = -inf
            for direction in gameState.getLegalActions(agent):
                temp_score = self.minMax(gameState.generateSuccessor(agent, direction), depth + 1)
                if temp_score > best_score:
                    best_score = temp_score
            return best_score
        else:
            best_score = inf
            for direction in gameState.getLegalActions(agent):
                temp_score = self.minMax(gameState.generateSuccessor(agent, direction), depth + 1)
                if temp_score < best_score:
                    best_score = temp_score
            return best_score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        alpha, beta = -float("inf"), float("inf")
        # agent = self.depth % gameState.getNumAgents()
        # best_score = -float("inf")
        best_direction = None

        for temp_direction in gameState.getLegalActions(0):
            score = self.alphaBeta(gameState.generateSuccessor(0, temp_direction), 1, alpha, beta)
            if score > alpha:
                # best_score = score
                best_direction = temp_direction
            alpha = max(alpha, score)
        return best_direction


        util.raiseNotDefined()

    def alphaBeta(self, gameState, depth, alpha, beta):
        inf = float("inf")
        agent = depth % gameState.getNumAgents()

        if depth == gameState.getNumAgents() * self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if agent == 0:
            temp_score = -inf
            for direction in gameState.getLegalActions(agent):
                temp_score = max(temp_score, self.alphaBeta(gameState.generateSuccessor(agent, direction), depth + 1, alpha, beta))
                if temp_score > beta:
                    return temp_score
                alpha = max(alpha, temp_score)
            return temp_score
        else:
            temp_score = inf
            for direction in gameState.getLegalActions(agent):
                temp_score = min(temp_score, self.alphaBeta(gameState.generateSuccessor(agent, direction), depth + 1, alpha, beta))
                if temp_score < alpha:
                    return temp_score
                beta = min(beta, temp_score)
            return temp_score




    # def minValue(self, gameState, alpha, beta):
    #     score = float("inf")
    #     agent = self.depth % gameState.getNumAgents()
    #
    #     for direction in gameState.getLegalActions(agent):
    #         score = self.minValue(gameState.generateSuccessor(agent, direction), alpha, beta)
    #         if score < alpha:
    #             return score
    #         beta = min(beta, score)
    #     return score

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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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

