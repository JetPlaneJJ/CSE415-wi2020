'''DBG_agent.py
by Russell Kook and Jia-Jia (Jay) Lin
UWNetIDs:
Student Numbers:

Assignment 3, in CSE 415, Winter 2020
This file contains our problem formulation of Deterministic
Simplified Backgammon (DSBG).
'''

from backgState import *

class our_agent:
    # Initializes the Agent
    def __init__(self, old=None):
        self.num_states = 0
        self.cutoffs = 0
        self.prune = False
        self.max_depth = 10000
        self.static_eval = None

    # Turns on and off AlphaBeta, and resets counters
    def useAlphaBetaPruning(prune = False):
        self.num_states = 0
        self.cutoffs = 0
        self.prune = not self.prune

    # this method returns a tuple (number of states and cutoffs)
    def statesAndCutoffsCounts():
        return (self.num_states, self.cutoffs)

    # Sets a specific limit on the depth of agent's searches
    def setMaxPly(maxply=-1):
        self.max_depth = maxply

    # Use the special static eval. function
    def useSpecialStaticEval(func):
        self.static_eval = func

# The Static Evaluation itself, apply to current state
# Count all whites moved out of start corner (positive)
# vs red moved out of its start corner (negative)
def staticEval(someState):
    w = state.whose_move
    red = 0
    white = 0
    # how many whites are in its goal corner (triangles 19-24)
    for triangle in someState.pointLists[19:25]:
        for pieces in triangle:
            if pieces == 0: # if the value is white (W=0)
                white += 1
    # how many reds are in its goal corner (triangles 1-6)
    for triangle in someState.pointLists[1:7]:
        for pieces in triangle:
            if pieces == 1: # if the value is red (R=1)
                red += 1
    return white - red


# Alpha-Beta Pruning, add this to minimax function
# alpha = -1000000000 beta = 1000000000000
# update at current node when possible
# if alpha >= beta:
#   ignore other children


# Moves the Piece
def move(state, die1, die2):
    w = state.whose_move
    print("I'm playing "+get_color(w))
    ans = input("or enter Q to quit: ")
    return ans
    #return "Q" # quit
    
      
