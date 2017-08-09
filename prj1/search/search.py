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
import heapq

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
    e = Directions.EAST
    #return []
    #return  [w, w, w, w, s, s, e, s, s,w]
    return  [s, s, w, s, w, w, s, w]

def mydfs(problem, disc, instate,res):

    if disc.has_key(instate):
       return 0,[]

    disc[instate] = 1
    if problem.isGoalState(instate):
       return 1,[] 

    succ = problem.getSuccessors(instate)
    for elem in succ:
       nextState = elem[0]
       if not disc.has_key(nextState):
          ret,res = mydfs(problem, disc, nextState, res)
          if ret == 1:
             res = [elem[1]] + res
             return 1,res

    return 0, []

def non_recursive_depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    if problem.isGoalState(problem.getStartState()):
       return []

    visited = set()
    stk = util.Stack()
    stkelem = (problem.getStartState() ,0, [])
    stk.push(stkelem)

    while not stk.isEmpty():
       (cur_state, cur_cost, cur_path) = stk.pop()

       if problem.isGoalState(cur_state):
          return cur_path

       if not cur_state in visited:
          visited.add(cur_state)
          succ = problem.getSuccessors(cur_state)
          for (next_state, next_action, next_cost) in succ:
              stkelem = (next_state, cur_cost + next_cost, cur_path + [next_action])
              stk.push(stkelem)

    return []

def my_recursive_depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    disc = {}
    res = []

    if problem.isGoalState(problem.getStartState()):
       return []

    if not disc.has_key(problem.getStartState()):
       ret,res = mydfs(problem, disc, problem.getStartState(), res)
       if ret == 1:
          return res

    return []
    util.raiseNotDefined()

def depthFirstSearch(problem):
    return my_recursive_depthFirstSearch(problem)
    return non_recursive_depthFirstSearch(problem)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited = set()
    que = util.Queue()
    if problem.isGoalState(problem.getStartState()):
       return []

    qelem = (problem.getStartState(), 0, []) #node, cost, path
    que.push(qelem)

    while not que.isEmpty():
       (cur_node, cur_cost, cur_path) = que.pop()
       if (problem.isGoalState(cur_node)):
          #print "cur_path:", cur_path, cur_node
          return cur_path
       
       if cur_node in visited:
          continue

       visited.add(cur_node)
       #print "curr_node succ", cur_node
       for (next_node, next_path, next_cost) in problem.getSuccessors(cur_node):
          #print "succ", next_node
          qelem = (next_node, cur_cost+next_cost, cur_path+[next_path])
          que.push(qelem) 

    return []

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    "*** YOUR CODE HERE ***"
    heap = []
    visited = set()

    helem = (0,problem.getStartState(),[])
    heapq.heappush(heap, helem)

    while len(heap):
       (cur_cost,cur_node,cur_path) = heapq.heappop(heap)

       if problem.isGoalState(cur_node):
          return cur_path

       if cur_node in visited:
          continue

       visited.add(cur_node)
       for (next_node, next_path, next_cost) in problem.getSuccessors(cur_node):
          helem = (cur_cost+next_cost,next_node,cur_path+[next_path]) 
          heapq.heappush(heap, helem)

    return []

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    heap = []
    visited = {}
    helem = (0+ heuristic(problem.getStartState(),problem),problem.getStartState(),[])
    heapq.heappush(heap,helem)

    while len(heap):
        (cur_cost,cur_node,cur_path) = heapq.heappop(heap)
        if problem.isGoalState(cur_node):
           return cur_path

        if visited.has_key(cur_node):
           if visited[cur_node] <= cur_cost:
              continue

        visited[cur_node] = cur_cost

        for (next_node, next_path, next_cost) in problem.getSuccessors(cur_node):
           f = cur_cost # f = g + h
           h = heuristic(cur_node, problem)
           g = f-h
           helem = (g+next_cost+heuristic(next_node,problem), next_node,cur_path+[next_path])
           heapq.heappush(heap, helem)

    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
