'''jial8_VI.py
Name: Jia-Jia (Jay) Lin
Student ID: 1820474
CSE415 Winter 2020
Value Iteration for Markov Decision Processes.
'''


# Edit the returned name to ensure you get credit for the assignment.
def student_name():
    return "Lin, Jia-Jia"  # For an autograder.


# fields
Vkplus1 = {}
Q_Values_Dict = {}
Policy = {}

# 1 iteration of Value Iteration from the given MDP information plus the current state values,
# which are provided in a dictionary Vk whose keys are states and whose values are floats.
def one_step_of_VI(S, A, T, R, gamma, Vk):
    global Q_Values_Dict
    global Vkplus1
    delta_max = 0
    # for every s a s' pairing, do the iteration
    for s in S:
        v = float("-inf")
        for a in A:
            q = 0
            for endState in S:
                q += (T(s, a, endState) * (R(s, a, endState) + gamma*Vk[endState]))
            Q_Values_Dict[(s, a)] = q
            v = max(v,q)
        # New V, given the max from Q sums
        Vkplus1[s] = v
        delta_max = max(delta_max, abs(Vkplus1[s] - Vk[s]))
    return Vkplus1, delta_max


def return_Q_values(S, A):
    '''Return the dictionary whose keys are (state, action) tuples,
    and whose values are floats representing the Q values from the
    most recent call to one_step_of_VI. This is the normal case, and
    the values of S and A passed in here can be ignored.
    However, if no such call has been made yet, use S and A to
    create the answer dictionary, and use 0.0 for all the values.
    '''
    global Q_Values_Dict
    # if empty dictionary
    if not bool(Q_Values_Dict): # TODO get rid of bool 
        # if there is nothing in dictionary yet, make everything 0.0
        for s in S:
            for a in A:
                Q_Values_Dict[(s, a)] = 0.0
    return Q_Values_Dict

def extract_policy(S, A):
    """Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.  If none have yet been
    computed, call return_Q_values to initialize q-values, and then
    extract a policy.  Ties between actions having the same (s, a) value
    can be broken arbitrarily.
    """
    global Policy
    if not Q_Values_Dict:
        return_Q_values(S, A) # not a return statement!
    #best_q = max(Policy.items(), key=Policy.get()]
    for s in S:
        best_action = A[0]
        best_q = float("-inf")
        for a in A:
            # is this the max q value so far?
            new_q = Q_Values_Dict[(s, a)]
            if new_q > best_q:
                best_q = new_q
                best_action = a
        Policy[s] = best_action
    return Policy


def apply_policy(s):
    # Return the action that your current best policy implies for state s.
    global Policy
    return Policy[s]

