'''jial8_Q_Learn.py
Implemented Q-Learning in this file by completing the implementations
of the functions whose stubs are present.
This is part of the UW Intro to AI Starter Code for Reinforcement Learning.
'''

import random

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
   return "Lin, Jia-Jia" # For an autograder.

# fields
STATES=None; ACTIONS=None; UQV_callback=None; Q_VALUES=None
is_valid_goal_state=None; Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None
Policy = {}

def setup(states, actions, q_vals_dict, update_q_value_callback,\
    goal_test, terminal, use_exp_fn=False):
    '''This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair.'''
    global STATES, ACTIONS, UQV_callback, Q_VALUES, is_valid_goal_state
    global USE_EXPLORATION_FUNCTION, Terminal_state
    STATES = states
    ACTIONS = actions
    Q_VALUES = q_vals_dict
    UQV_callback = update_q_value_callback
    is_valid_goal_state = goal_test
    Terminal_state = terminal
    USE_EXPLORATION_FUNCTION = use_exp_fn
    if USE_EXPLORATION_FUNCTION:
         # Change this if you implement an exploration function:
         print("You have not implemented an exploration function")

PREVIOUS_STATE = None
LAST_ACTION = None
def set_starting_state(s):
    '''This is called by the GUI when a new episode starts.
    Do not change this function.'''
    global INITIAL_STATE, PREVIOUS_STATE
    print("In Q_Learn, setting the starting state to "+str(s))
    INITIAL_STATE = s
    PREVIOUS_STATE = s

ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9
def set_learning_parameters(alpha, epsilon, gamma):
    ''' Called by the system. Do not change this function.'''
    global ALPHA, EPSILON, CUSTOM_ALPHA, CUSTOM_EPSILON, GAMMA
    ALPHA = alpha
    EPSILON = epsilon
    GAMMA = gamma
    if alpha < 0: CUSTOM_ALPHA = True
    else: CUSTOM_ALPHA = False
    if epsilon < 0: CUSTOM_EPSILON = True
    else: CUSTOM_EPSILON = False

def update_Q_value(previous_state, previous_action, new_value):
    '''Whenever your code changes a value in Q_VALUES, it should
    also call this method, so the changes can be reflected in the
    display.
    Do not change this function.'''
    UQV_callback(previous_state, previous_action, new_value)

def handle_transition(action, new_state, r):
    global PREVIOUS_STATE
    # get the initial q value of the new state
    prev = float("-inf")
    for a in ACTIONS:
        # use q learning equation, remember ALPHA is the learning rate
        q = ((1-ALPHA)*Q_VALUES[(PREVIOUS_STATE,action)]) + ALPHA*(r + GAMMA*(max(prev, Q_VALUES[(new_state, a)])))
    # do not update if users exits and they're not on the goal state
    if (not action == "Exit" or is_valid_goal_state(PREVIOUS_STATE)):
        Q_VALUES[(PREVIOUS_STATE, action)] = q
        update_Q_value(PREVIOUS_STATE, action, q)
        PREVIOUS_STATE = new_state
    return # Nothing needs to be returned.

def choose_next_action(s, r, terminated=False):
    '''When the GUI or engine calls this, the agent is now in state s,
    and it receives reward r.
    Use this information to update the q-value for the previous state
    and action pair.  
    Then the agent needs to choose its action and return that.
    '''
    global INITIAL_STATE, PREVIOUS_STATE, LAST_ACTION, EPSILON, ALPHA
    if s == Terminal_state:
        return None
    # Unless s is the initial state, compute a new q-value for the
    # previous state and action.
    if not s == INITIAL_STATE:
        new_qval = float("-inf") # A bogus value for now.
        for a in ACTIONS:
                q = max(new_qval,Q_VALUES[(s,a)])
        q = (1-ALPHA)*Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] + ALPHA*(r+(GAMMA*q))
        # Save it in the dictionary of Q_VALUES:
        Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] = q
        # Then let the Engine and GUI know about the new Q-value.
        update_Q_value(PREVIOUS_STATE, LAST_ACTION, q)
    # try all M actions with non-zero probability, with probability 1-E = greedy, otherwise random
    action_chosen = ACTIONS[0] 
    q = float("-inf")
    # what is the best action?
    for a in ACTIONS:
        curr_q = Q_VALUES[(s,a)]
        if curr_q > q:
            action_chosen = a # best action
            q = curr_q
    if (EPSILON > 0 or CUSTOM_EPSILON) and random_choice(EPSILON):
        action_chosen = random.choice(ACTIONS)
    # goal state reached, exit
    if is_valid_goal_state(s):
        # if CUSTOM_ALPHA is True, manage alpha values over time, otherwise go with fixed value.
        if CUSTOM_ALPHA:
            ALPHA -= 0.01*ALPHA # ?????????
        if CUSTOM_EPSILON:
            EPSILON -= 0.01*EPSILON
        return "Exit"
    LAST_ACTION = action_chosen # remember this for next time
    PREVIOUS_STATE = s        #    "       "    "   "    "
    return action_chosen


def extract_policy(S, A):
    global Policy
    for s in S:
        if is_valid_goal_state(s):
            Policy[s] = "Exit"
        elif s == Terminal_state:
            Policy[s] = None
        else :
            q = float("-inf")
            best_a = A[0]
            # what is the best action?
            for a in A:
                curr_q = Q_VALUES[(s,a)]
                if curr_q > q:
                    best_a = a 
                    q = curr_q
            Policy[s] = best_a
    return Policy


# my private helper function, returns true if r<epsilon
def random_choice(epsilon):
    r = random.random()
    print(r)
    if r <= epsilon:
        return True
    return False