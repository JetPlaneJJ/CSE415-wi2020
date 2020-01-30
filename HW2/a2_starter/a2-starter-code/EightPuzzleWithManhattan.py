''' AStar.py
by Jia-Jia (Jay) Lin
UWNetID: jial8
Student number: 1820474

Assignment 2, in CSE 415, Winter 2020.
This file contains my EightPuzzle Manhattan heuristic implementation.
'''
from EightPuzzle import *

# Correct positions of each numbered tile
GOAL = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]
# Correct positions of each numbered tile (row, col)
LOC = {0:(0,0),1:(0,1),2:(0,2),
       3:(1,0), 4:(1,1),5:(1,2),
       6:(2,0),7:(2,1),8:(2,2)}

def h(s):
  '''Return Manhattan heuristic (total)'''
  total_dist = 0
  row = 0
  col = 0
  while row < 3:
    while col < 3:
      # if the tile is in the wrong place and it's not a 0
      if GOAL[row][col] != s.b[row][col] and s.b[row][col] != 0:
        goal = LOC[s.b[row][col]]
        total_dist += abs(row - goal[0]) + abs(col-goal[1])
      col +=1
    row +=1
    col = 0
  return total_dist
