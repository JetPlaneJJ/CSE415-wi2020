'''SBG_agent.py
by Russell Kook and Jia-Jia (Jay) Lin
UWNetIDs: russkook, jial8
Student Numbers:  , 1820474

Assignment 3, in CSE 415, Winter 2020
This file contains our problem formulation of Stochastic
Simplified Backgammon (DSBG).
'''
from backgState import *

# THIS IS FOR RANDOM DICE ROLLS!!!!!!
class SBG:
  # Initializes the Agent
  def __init__(self, old=None):
    self.num_states = 0
    self.cutoffs = 0
    self.prune = False
    self.max_depth = 10000
    self.function = None
    self.best_state = None
    self.state_dict = None

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

  # set up uniform distribution
  def useUniformDistribution():
    pass # we are using uniform distribution 

  # probability value for dice
  def probability(die1,die2):
    if (die1 + die2 == 7):
      return 1
    return (1/36)

  def expectimax(self, board, whoseMove, plyLeft, die1, die2):
    # if the state is a terminal state, return value
    if (plyLeft == 0):
      if not (self.function == None):
        return self.function(board)
      else:
        return self.staticEval(board)
    # if currently the maximizing player (White) 
    if(whoseMove == 0): 
      maxEval = -100000
      for s in self.successors(board, whoseMove, die1, die2): 
        newVal = self.expectimax(s,self.other(whoseMove), plyLeft-1,die1,die2)
        if(newVal > maxEval):
            maxEval = newVal
            self.best_state = s
      return maxEval
    else:
      v = 0
      p = self.probability(die1,die2)
      v += p*self.expectimax(s,board,whoseMove,plyLeft,die1,die2)
      return v
  def successors(self, board, whose_move, die1, die2):
    original_state = board
    self.state_dict = {}
    for a in range(26):
      for j in range(26):
        current_state = original_state
        new_state = None
        print(get_color(whose_move)+' to play...')
        move = ""
        if(a == 25):
          move = "p"
        elif(j == 25):
          move = str(a) + ",p"
        else:   
          move= ""+str(a)+","+str(j)
        print(get_color(whose_move), "moves from: ", move)
        if move in ["Q", "q"]:
          print('Agent '+get_color(whose_move)+' resigns. Game OVER!')
          continue
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
            self.num_states = self.num_states + 1
            self.state_dict[current_state] = ""+str(a)+","+str(j)
            yield current_state
            continue
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
          for i in range(2):
            if i==1 and checker2 in ['P','p']:
              print("OK. Pass is accepted for the other die.")
              new_state = bgstate(current_state)
              new_state.whose_move=1-whose_move
              current_state = new_state
              continue
            pt = int([checker1, checker2][i])
            print(pt)
            if pt==0:
              # Player must have a checker on the bar.
              if not whose_move in current_state.bar:
                print("You don't have any checkers on the bar.")
                break
              new_state = self.handle_move_from_bar(current_state, whose_move, dice_list[i])
              if not new_state:
                print("Move from bar is illegal.")
                break
              current_state = new_state
              continue
            # Now make sure player does NOT have a checker on the bar.
            if self.any_on_bar(current_state, whose_move):
              print("Illegal to move a checker from a point, when you have one on the bar.")
              break
            if pt < 1 or pt > 24:
              print(pt, "is not a valid point number.")
              break
            if not whose_move in current_state.pointLists[pt-1]:
              print("No "+get_color(whose_move)+" checker available at point "+str(pt))
              break
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
              break
            dest_pt_list = current_state.pointLists[dest_pt-1]
            if len(dest_pt_list) > 1 and dest_pt_list[0]!=whose_move:
              print("Point "+str(dest_pt)+" is blocked. You can't move there.")
              break
            if not new_state:
              new_state = bgstate(current_state)
            new_state.pointLists[pt-1].pop()
            # If the destination point contains a single opponent, it's hit.
            new_state = self.hit(new_state, dest_pt_list, dest_pt)
            # Now move the checker into the destination point.
            new_state.pointLists[dest_pt-1].append(whose_move)
            current_state = new_state
            if(i == 1):
                self.num_states = self.num_states + 1
                self.state_dict[current_state] = ""+str(a)+","+str(j)
                yield current_state


    

