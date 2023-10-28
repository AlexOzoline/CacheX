
from math import floor
from referee.board import Board
from random import randrange
import random
import copy

class Node:
    def __init__(self, board):
        self.board = board


class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        # put your code here
        self.color = player
        if self.color == "red":
            self.oppColor = "blue"
        else:
            self.oppColor = "red"
        self.board = Board(n)
        self.possibleMoves = []
        self.n = n
        self.firstMove = True
        for i in range(n):
            for j in range(n):
                self.possibleMoves.append((i, j))
        


    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # put your code here
        x = randrange(self.n)
        y = randrange(self.n)
        while self.board.is_occupied((x,y)):
            x = randrange(self.n)
            y = randrange(self.n)
        return ("PLACE", x, y)
        
        
    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        
        # put your code here
        if action[0] == "STEAL":
            for i in range(self.n):
                for j in range(self.n):
                    if self.board.__getitem__((i, j)) == "red":
                        self.board.__setitem__((i, j), None)
                        self.board.place(player, (j, i))
                        return
        self.board.place(player, tuple([action[1], action[2]]))
        #print(self.board._data)



        