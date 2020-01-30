'''DBG_agent.py
by Russell Kook and Jia-Jia (Jay) Lin
UWNetIDs: russkook, jial8
Student Numbers:  , 1820474

Assignment 3, in CSE 415, Winter 2020
This file contains our problem formulation of Deterministic
Simplified Backgammon (DSBG).
'''
from backgState import *

class DSBG:
  # Initializes the Agent
  def __init__(self, old=None):
    self.num_states = 0
    self.cutoffs = 0
    self.prune = False
    self.max_depth = 4
    self.function = None
    self.best_state = None
    self.state_dict = None

  # Turns on and off AlphaBeta, and resets counters
  def useAlphaBetaPruning(self, prune = False):
    self.num_states = 0
    self.cutoffs = 0
    self.prune = not self.prune # ask about this

  # Returns a tuple (number of states and cutoffs)
  def statesAndCutoffsCounts(self):
    return (self.num_states, self.cutoffs)

  # Sets a specific limit on the depth of agent's searches
  def setMaxPly(self, maxply=-1):
    self.max_depth = maxply

  # Use the special static eval. function
  def useSpecialStaticEval(self, func):
    self.function = func

  # The Static Evaluation Function
  # Count all whites moved out of start corner (positive)
  # vs red moved out of its start corner (negative)
  def staticEval(self, someState):
    # w = state.whose_move
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
  
  # Minimax algorithm with OPTIONAL alpha-beta pruning
  # board = current state of the board
  # alpha and beta = only matters if self.prune = True
  # plyLeft = number of plays left
  # if the length of stack == maxDepth
  def minimax(self,board,alpha,beta,whoseMove,plyLeft,die1,die2):
      # provisional value of search
      provisional = 0
      # If there are no more plays left (game ended)
      if(plyLeft == 0): #might need to change if plyLeft is -1
        if not (self.function == None):
          # Use TA's static eval function
          return self.function(board)
        else:
          return self.staticEval(board)     
      # if currently the maximizing player (White) 
      if(whoseMove == 0): 
        provisional = 100000
        # for each child state 's' in a list 'successors'
        for s in self.successors(board, whoseMove): 
          newVal = self.minimax(s,board,alpha,beta,self.other(whoseMove), plyLeft-1,die1,die2)
          maxEval = max(provisional, newVal)
          # only check for alpha beta if self.prune = True
          if (self.prune):
            alpha = max(alpha,newVal)
            if beta <= alpha:
              break
          return maxEval
      # if currently the minimizing player (Red)
      else:
        provisional = -100000           
        for s in self.successors(board, whoseMove, die1, die2):
          newVal = self.minimax(s,board,alpha,beta,self.other(whoseMove), plyLeft-1, die1, die2)
          minEval = min(provisional,newVal)
          # only check for alpha beta if self.prune = True
          if (self.prune):
            beta = min(beta,eval)
            if beta <= alpha:
              break
          return minEval

  # Returns the opposite player
  def other(self, whoseMove):
      return 1 - whoseMove

  # Returns a list of child states of a given board
  def successors(self, board, whose_move, die1, die2):
    # Keeps a copy of the original board
    original_state = board
    #state_list = []
    self.state_dict = {}
    # Iterate through all possible moves
    for a in range(26):
      for j in range(26):
        current_state = original_state
        new_state = None
        print(get_color(whose_move)+' to play...')
        move = ""
        # Agent passes
        if(a == 25):
          move = "p"
        elif(j == 25):
          move = str(a) + "p"
        # a numbered move like (1,10)
        else:   
          move= ""+str(a)+","+str(j)
          print(get_color(whose_move), "moves from: ", move)
        # If quitting the game
        if move in ["Q", "q"]:
          print('Agent '+get_color(whose_move)+' resigns. Game OVER!')
          break;
        # If passing their turn
        if move in ["P", "p"]:
          print('Agent '+get_color(whose_move)+' passes.')
          if self.moves_exist(current_state, whose_move, die1, die2):
            print("Moves exist. Passing is not allowed!")
            continue
          else:
            print("OK. Pass is accepted for this turn.")
            new_state = bgstate(current_state)
            new_state.whose_move=1-whose_move
            current_state = new_state
            state_list.append(current_state)
            self.state_dict[current_state] = ""+str(a)+","+str(j)
            print(len(self.state_dict))
            continue
        # If NOT passing
        else:
          try:
            move_list = move.split(',')
            if len(move_list)==3 and move_list[2] in ['R','r']:
              dice_list = [die2, die1]
            else:
              dice_list = [die1, die2]
            checker1, checker2 = move_list[:2]
          except:
            print("Invalid type of move: ", move)
            continue
        # Just in case the player wants to pass after the first checker is moved:
        for i in range(2):
          if i==1 and checker2 in ['P','p']:
            print("OK. Pass is accepted for the other die.")
            new_state = bgstate(current_state)
            new_state.whose_move=1-whose_move
            current_state = new_state
            continue
        pt = int([checker1, checker2][i])
        # Check first for a move from the bar:
        if pt==0:
          # Player must have a checker on the bar.
          if not whose_move in current_state.bar:
            print("You don't have any checkers on the bar.")
            continue
          new_state = self.handle_move_from_bar(current_state, whose_move, dice_list[i])
          if not new_state:
            print("Move from bar is illegal.")
            continue
          current_state = new_state
          continue
        # Now make sure player does NOT have a checker on the bar.
        if self.any_on_bar(current_state, whose_move):
          print("Illegal to move a checker from a point, when you have one on the bar.")
          continue
        # Is checker available on point pt?
        if pt < 1 or pt > 24:
          print(pt, "is not a valid point number.")
          continue
        if not whose_move in current_state.pointLists[pt-1]:
          print("No "+get_color(whose_move)+" checker available at point "+str(pt))
          continue
        # Determine whether destination is legal.
        die = dice_list[i]
        if whose_move==W:
          dest_pt = pt + die
        else:
          dest_pt = pt - die
        if dest_pt > 24 or dest_pt < 1:
          born_off_state = self.bear_off(current_state, pt, dest_pt, whose_move)
          if born_off_state:
            current_state = born_off_state
            continue
          print("Cannot bear off this way.")
          continue    
        dest_pt_list = current_state.pointLists[dest_pt-1]
        if len(dest_pt_list) > 1 and dest_pt_list[0]!=whose_move:
          print("Point "+str(dest_pt)+" is blocked. You can't move there.")
          continue
        # So this checker's move is legal. Update the state.
        if not new_state:
          new_state = bgstate(current_state)
        # Remove checker from its starting point.
        new_state.pointLists[pt-1].pop()
        # If the destination point contains a single opponent, it's hit.
        new_state = self.hit(new_state, dest_pt_list, dest_pt)
        # Now move the checker into the destination point.
        new_state.pointLists[dest_pt-1].append(whose_move)
        current_state = new_state
        # return THIS current state!!!!
        yield current_state
        # do not do this... state_list.append(current_state)
        self.state_dict[current_state] = ""+str(a)+","+str(j)
        print(len(self.state_dict))
    #return state_list 
                
  # finds the best child state using minimax 
  def move(self, state, die1, die2):
      print("in move")
      self.state_dict = None
      self.setMaxPly(1)
      alpha = -100000000
      beta = 100000000
      self.minimax(self, state, alpha, beta, state.whose_move, self.max_depth, die1, die2)
      return self.state_dict[self.best_state]

  def hit(self, new_state, dest_pt_list, dest_pt):
    opponent = 1-new_state.whose_move
    if len(dest_pt_list)==1 and dest_pt_list[0]==opponent:
      if opponent==W:
        new_state.bar.insert(W, 0)
      else:
        new_state.bar.append(R)
      new_state.pointLists[dest_pt-1]=[]
    return new_state

  def bear_off(self, state, src_pt, dest_pt, who):
    if not self.bearing_off_allowed(state, who): 
      return False
    pl = state.pointLists[src_pt-1]
    if pl==[] or pl[0]!=who:
      print("Cannot bear off from point "+src(src_pt))
      return False
    good = False
    if who==W:
      if dest_pt==25:
          good = True
      elif dest_pt==26:
          for point in range(18,src_pt-1):
            if W in state.pointLists[point]: return False
          good = True
    elif who==R:
      if dest_pt==0:
          good = True
      elif dest_pt== -1:
          for point in range(src_pt, 6):
            if R in state.pointLists[point]: return False
          good = True
    if not good: return False 
    born_off_state = bgstate(state)
    born_off_state.pointLists[src_pt-1].pop()
    if who==W: born_off_state.white_off.append(W)
    else:  born_off_state.red_off.append(R)
    return born_off_state

  def forfeit(self, who):
    global DONE
    print("Player "+get_color(who)+" forfeits the game and loses.")
    DONE = True

  def moves_exist(self, state, die1, die2, who):
    return False  # placeholder.

  def any_on_bar(self, state, who):
    return who in state.bar

  def remove_from_bar(self, new_state, who):
    if who==W:
      del new_state.bar[0]
    else:
      new_state.bar.pop()
    print("After removing a "+get_color(who)+" from the bar,")
    print("  the bar is now: "+str(new_state.bar))

  def handle_move_from_bar(self, state, who, die):
    # We assume there is a piece of this color available on the bar.
    if who==W: target_point=die
    else: target_point=25-die
    pointList = state.pointLists[target_point-1]
    if pointList!=[] and pointList[0]!=who and len(pointList)>1:
        print("Cannot move checker from bar to point "+str(target_point)+" (blocked).")
        return False
    new_state = bgstate(state)
    new_state = hit(new_state, pointList, target_point)
    remove_from_bar(new_state, who)
    new_state.pointLists[target_point-1].append(who)
    return new_state

  def bearing_off_allowed(self, state, who):
    if self.any_on_bar(state, who): return False
    if who==W: point_range=range(0,18)
    else: point_range=range(6,24)
    pl = state.pointLists
    for i in point_range:
      if pl[i]==[]: continue
      if pl[i][0]==who: return False
    return True
