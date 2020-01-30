''' EightPuzzleWithHamming.py
by Jia-Jia (Jay) Lin
UWNetID: jial8
Student number: 1820474

Assignment 2, in CSE 415, Winter 2020.
This file contains my Eight Puzzle implementation with the Hamming heuristic.
'''
from EightPuzzle import * 

# Correct positions of each numbered tile
GOAL = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

def h(s):
  '''Return an estimate of the Hamming distance
  between a state and the goal (how many tiles out of place? Do not count 0)'''
  incorrect_tiles = 0
  row = 0
  col = 0 
  while row < 3:
    while col < 3:
      # if the tile is in the wrong place and it's not a 0
      if GOAL[row][col] != s.b[row][col] and s.b[row][col] != 0:
        incorrect_tiles += 1
      col +=1
    row +=1
    col = 0
  return incorrect_tiles
