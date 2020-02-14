'''jial8_VI.py
Name: Jia-Jia (Jay) Lin
Student ID: 1820474
CSE415 Winter 2020
Value Iteration for Markov Decision Processes.
'''

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
   return "Lin, Jia-Jia" # For an autograder.

Vkplus1 = {}
Q_Values_Dict = {}
one_step_ofVI_called = 0

# 1 iteration of Value Iteration from the given MDP information plus the current state values,
# which are provided in a dictionary Vk whose keys are states and whose values are floats.
def one_step_of_VI(S, A, T, R, gamma, Vk):
   '''S is list of all the states defined for this MDP.
   A is a list of all the possible actions.
   T is a function representing the MDP's transition model.
   R is a function representing the MDP's reward function.
   gamma is the discount factor.
   The current value of each state s is accessible as Vk[s].
   '''

   '''Your code should fill the dictionaries Vkplus1 and Q_Values_dict
   with a new value for each state, and each q-state, and assign them
   to the state's and q-state's entries in the dictionaries, as in
       Vkplus1[s] = new_value
       Q_Values_Dict[(s, a)] = new_q_value

   Also determine delta_max, which we define to be the maximum
   amount that the absolute value of any state's value is changed
   during this iteration.
   '''
   global Q_Values_Dict
   # initial states
   delta = 0
   q = 0
   v = -100000000000
   # for every s a s' pairing, do the iteration thing
   for s in S:
      for a in A:
         q = 0
         for endState in S:
            # find sums Q value first before V, use Q formula from homework
            q += T(s, a, endState) * (R(s,a,endState)+gamma*Vk[endState])
            Q_Values_Dict[(s,a)] = q;
            # New V, given the max from Q sums
            Vkplus1[state] = max(v, q);
            # update delta to the largest change
            change = Vkplus1[state] - Vk[state];
            delta = max(delta, abs(change));
   one_step_of_VI_called += 1
   return Vkplus1, delta_max


def return_Q_values(S, A):
   '''Return the dictionary whose keys are (state, action) tuples,
   and whose values are floats representing the Q values from the
   most recent call to one_step_of_VI. This is the normal case, and
   the values of S and A passed in here can be ignored.
   However, if no such call has been made yet, use S and A to
   create the answer dictionary, and use 0.0 for all the values.
   '''
   if one_step_ofVI_called < 1:
      # if there is nothing in dictionary yet, make everything 0.0
      for s in S:
         for a in A:
            Q_Values_Dict[(s, a)] = 0.0
   return Q_Values_Dict

Policy = {}
def extract_policy(S, A):
   '''Return a dictionary mapping states to actions. Obtain the policy
   using the q-values most recently computed.  If none have yet been
   computed, call return_Q_values to initialize q-values, and then
   extract a policy.  Ties between actions having the same (s, a) value
   can be broken arbitrarily.
   '''
   global Policy
   Policy = {}
   # Add code here
   if one_step_of_VI_called < 1:
      return_Q_values(S,A)
   # go through each state and action to see which action is the best
   best_action = None
   best_q = -100000000000
   for s in S:
      for a in A:
         # is this the max q value so far
         if best_q == min(best_q, Q_Values_Dict[(s,a)]):
            best_q = Q_Values_Dict[(s,a)]
            best_action = a
         # update state with best action so far
         Policy[s] = best_action
   return Policy

'''Return the action that your current best policy implies for state s.'''
def apply_policy(s):
   global Policy
   return Policy[s]


