# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # create a list called explored to store the explored state
    # create a list called result to store the actions
    # create a stack called stack to store the state and result
    explored = []
    result = []
    stack = util.Stack()
    # find the start state called start in the problem,
    # and push the start state and the result into the stack
    start = problem.getStartState()
    stack.push((start,result))
    while(stack.isEmpty() == False):
        # pop the last state in the stack
        start,result = stack.pop()
        # if the state is the goal state, then return the result
        if(problem.isGoalState(start) == True):
            return result
        # otherwise add the state into the explored
        explored.append(start)
        # find the successor of the state
        successor = problem.getSuccessors(start)
        # in all successors of the state, if explored does not find that successor,
        # add the action of the successor into result
        # and push the successor and new result into the stack
        for success in successor:
            if(explored.count(success[0]) == 0):
                stack.push((success[0],result + [success[1]]))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # create a list called explored to store the explored state
    # create a list called result to store the action
    # create a queue called queue to store the state and result
    explored = []
    result = []
    queue = util.Queue()
    # find the start state from the problem and push the start state and result into the queue
    start = problem.getStartState()
    queue.push((start, result))
    explored.append(start)
    while(queue.isEmpty() == False):
        # pop the state and result from the queue
        start, result = queue.pop()
        # if the state is the goal state, return the result
        if(problem.isGoalState(start) == True):
            return result
        # find the successor of the state
        successor = problem.getSuccessors(start)
        # for all successors of the state, if the successor does not include in explored, then store the successor into the explored
        # add the action of the successor into the result, and store the successor state and new result into the queue
        for success in successor:
            if(explored.count(success[0]) == 0):
                explored.append(success[0])
                queue.push((success[0], result + [success[1]]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # create a list called explored to store the explored state
    # create a list called result to store the actions
    # create a priority queue called priQueue to store the state and result
    explored = []
    result = []
    priQueue = util.PriorityQueue()
    # find the start state from the problem
    start = problem.getStartState()
    # push the depth, start state and result into the priQueue and explored list
    priQueue.push((0, start, result), 0)
    explored.append(start)
    while(priQueue.isEmpty() == False):
        # pop the distance between start state and current state(called depth), current state, and result
        depth, start, result = priQueue.pop()
        # if the current state is the goal state, then return result
        if(problem.isGoalState(start) == True):
            return result
        # find the successors of the current state
        successor = problem.getSuccessors(start)
        for success in successor:
            # if the successor of the current state does not find in the explored, then add the successor state into the explored
            # add the action cost of the successor into the depth and add the action of the successor into the result
            # update new depth, successor state and new result with the priority of new depth in the priority queue
            if(explored.count(success[0]) == 0):
                explored.append(success[0])
                priQueue.update((depth + success[2], success[0], result + [success[1]]), depth + success[2])
            # if the successor of the current state is the goal state, then add the action cost of the successor into the depth
            # and add the action of the successor into the result. Update new depth, successor state
            # and new result with the priority of new depth in the priority queue
            if(problem.isGoalState(success[0]) == True):
                priQueue.update((depth + success[2], success[0], result + [success[1]]), depth + success[2])
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # create a list called explored to store explored state
    # create a list called result to store the action
    # create a priority queue called priQueue to store the state and the result
    explored = []
    result = []
    priQueue = util.PriorityQueue()
    # find the start state from the problem
    start = problem.getStartState()
    # push the distance, start state and result with priority of 0 into the priority queue
    priQueue.push((0, start, result), 0)
    # store the start state into the explored
    explored.append(start)
    while(priQueue.isEmpty() == False):
        # pop the distance between start state and current state(called distance), current state, and result
        distance, start, result = priQueue.pop()
        # if the current state is the goal state then return the result
        if(problem.isGoalState(start) == True):
            return result
        # otherwise, find the successors of the current state
        successor = problem.getSuccessors(start)
        for success in successor:
            # if the successor of the current state does not find in the explored, then add the successor of the current state into the explored
            # add the action cost of the successor in the distance and add the action of the successor in the result
            # set the priority as the sum of new distance and the result of heuristic(successor state, problem)
            # update the new distance, successor state and new result with the new priority in the priority queue
            if(explored.count(success[0]) == 0):
                explored.append(success[0])
                priQueue.update((distance + success[2], success[0], result + [success[1]]), distance + success[2] + heuristic(success[0],problem))
            # if the successor state is the goal state, then add the action cost of the successor in the distance and add the action of the successor in the result
            # se the priority as the sum of new distance and the result of heuristic(successor state, problem)
            # update the new distance, successor state and new result with the new priority in the priority queue
            if(problem.isGoalState(success[0]) == True):
                priQueue.update((distance + success[2], success[0], result + [success[1]]), distance + success[2] + heuristic(success[0],problem))
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
