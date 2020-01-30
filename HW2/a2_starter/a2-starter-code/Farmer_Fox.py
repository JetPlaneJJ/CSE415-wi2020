'''Farmer_Fox.py
by Jia-Jia (Jay Lin
UWNetID: jial8
Student number: 1820474

Assignment 2, in CSE 415, Winter 2020.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

#<COMMON_CODE>
PROBLEM_NAME = 'Farmer_Fox'
PROBLEM_VERSION = '1.0'
F=0  # array index to access farmer count
f=1  # same for Fox
C=2  # same for Chicken
G=3  # same for Grain
LEFT=0 # same idea for left side of river
RIGHT=1 # right side of river

class State():
    def __init__(self, d=None):
        if d==None:
            # each bracket per object/person, boat 0 = boat is on the left
            d = {'people':[[1,0],[1,0],[1,0],[1,0]], 'boat':LEFT} 
        self.d = d
        
    def __eq__(self,s2):
        for prop in ['people', 'boat']:
            if self.d[prop] != s2.d[prop]: return False
        return True
    
    def __str__(self):
        # Produces a textual description of the current state.
        p = self.d['people']
        # Objects currently on the left of the river
        txt = "\nLeft of River: "
        txt += "Farmer: "+str(p[F][LEFT])
        txt += " fox: "+str(p[f][LEFT])
        txt += " Chicken: "+str(p[C][LEFT])
        txt += " Grain: "+str(p[G][LEFT])
        # Objects on the right
        txt += "\nRight of River: "
        txt += "Farmer: "+str(p[F][RIGHT])
        txt += " fox: "+str(p[f][RIGHT])
        txt += " Chicken: "+str(p[C][RIGHT])
        txt += " Grain: "+str(p[G][RIGHT])
        side='left'
        if self.d['boat']==1: side='right'
        txt += "\nThe boat is on the "+side+"."
        return txt
    
    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        # this below line is questionable...
        news.d['people']=[self.d['people'][person][:] for person in [F,f,C,G]]
        news.d['boat'] = self.d['boat']
        return news
    
    def can_move(self,Object):
        # Tests whether it's legal to move
        side = self.d['boat'] # Where the boat is.
        p = self.d['people']
        if p[F][side] < 1: return False # Need Farmer to steer from current side
        if Object == 'f':
            if p[f][side] < 1: return False # Fox must be on the correct side
            if p[C][side] > 0 and p[G][side] > 0: return False # can't leave the C and G alone
        if Object == 'C':
            if p[C][side] < 1: return False # Chicken must be on the correct side
            # can leave the Fox and Grain alone
        if Object == 'G':
            if p[G][side] < 1: return False
            if p[f][side] > 0 and p[C][side] > 0: return False # can't leave the f and C alone
        if Object == 'F':
            if p[G][side] > 0 and p[C][side] > 0: return False # can't leave the C and G alone
            if p[f][side] > 0 and p[C][side] > 0: return False # can't leave the f and C alone
        return True

    def move(self,Object):
        '''Assuming it's legal to make the move, this computes
        the new state, moving the boat carrying an object'''
        news = self.copy()      # start with a deep copy.
        side = self.d['boat']       
        p = news.d['people']        
        p[F][side] = 0     # Remove Farmer from that side.
        p[F][1-side] = 1
        if Object == 'f':
            p[f][side] = 0
            p[f][1-side] = 1
        if Object == 'C':
            p[C][side] = 0
            p[C][1-side] = 1
        if Object == 'G':
            p[G][side] = 0
            p[G][1-side] = 1
        news.d['boat'] = 1-side # Move the boat
        return news

def goal_test(s):
    # If all objects are on the right, then s is a goal state.
    p = s.d['people']
    return (p[F][RIGHT]==1 and p[f][RIGHT]==1 and p[C][RIGHT]==1 and p[G][RIGHT]==1)

def goal_message(s):
    return "Wow you solved the puzzle :)"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf
    def is_applicable(self, s):
        return self.precond(s)
    def apply(self, s):
        return self.state_transf(s)

#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'people':[[1, 0], [1, 0], [1, 0], [1, 0]], 'boat':LEFT})
#</INITIAL_STATE>

#<OPERATORS>
choices = ['f','C','G','F']

OPERATORS = [Operator(
    "Have the Farmer (F) cross the river with the...",
    # "Object" catches all inputs (with Fox (f), Chicken (C), Grain (G), and only Farmer(F))
    lambda step1, Object=o: step1.can_move(Object), 
    lambda step2, Object=o: step2.move(Object) ) 
    for o in choices]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
