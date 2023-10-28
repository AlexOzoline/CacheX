
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
        if self.firstMove == True and self.color == "blue":
            self.firstMove = False
            return ("STEAL", )
        if self.firstMove == True and self.color == "red" and self.n % 2 != 0:
            print("NIGAAAAAA")
            self.possibleMoves.remove((int((self.n - 1) /   2), int((self.n - 1) / 2 )))
        print((int((self.n - 1) /   2), int((self.n - 1) / 2 )))
        random.shuffle(self.possibleMoves)
        currentNode = Node(self.board)
        '''
        newBoard = copy.deepcopy(self.board)
        newBoard.place("red", (3, 3))
        newBoard.place("red", (4, 3))
        newBoard.place("blue", (4, 2))
        newNode = Node(newBoard)
        print(newBoard._data)
        best_move, val = minimax(newNode, 1, True, self.n, self.color, self.possibleMoves)
        print("best move has value = " + str(val))
        print("THE BEST MOVE IS" + str(best_move))
        '''
        best_move, val = minimax(currentNode, 3, True, self.n, self.color, self.oppColor, self.possibleMoves, float('-inf'), float('inf'))
        if self.firstMove:
            self.firstMove = False
            self.possibleMoves.append((int((self.n - 1) /   2), int((self.n - 1) / 2 )))
        print("best move has value = " + str(val))
        return ("PLACE", best_move[0], best_move[1])
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

def minimax(node, depth, myTurn, n, color, oppColor, possibleMoves, alpha, beta):
    bestMove = None
    if depth == 0:
        return None, getValue(node, n, color, oppColor)
    if winCheck(node, n) == color:
        return None, float('inf')
    elif winCheck(node, n) != None:
        return None, float('-inf')
    if myTurn:
        maxValue = float('-inf')
        for i in possibleMoves:
            #print(i)
            if node.board.is_occupied(i):
                continue
            newBoard = copy.deepcopy(node.board)
            newBoard.place(color, i)
            child = Node(newBoard)
            value = minimax(child, depth - 1, False, n, color, oppColor, possibleMoves, alpha, beta)[1]
            if value > maxValue:
                maxValue = value
                bestMove = i
            elif bestMove == None:
                bestMove = i
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return bestMove, maxValue
    else:
        minValue = float('inf')
        for i in possibleMoves:
            if node.board.is_occupied(i):
                continue
            newBoard = copy.deepcopy(node.board)
            newBoard.place(oppColor, i)
            child = Node(newBoard)
            value = minimax(child, depth - 1, True, n, color, oppColor, possibleMoves, alpha, beta)[1]
            if value < minValue:
                minValue = value
                bestMove = i
            elif bestMove == None:
                bestMove = i
            beta = min(beta, value)
            if beta <= alpha:
                break
        return bestMove, minValue




def winCheck(node, n):
    for i in range(n):
        if node.board.__getitem__((0, i)) == 'red':
            reachable = node.board.connected_coords((0, i))
            for (x, y) in reachable:
                if x == n - 1:
                    return "red"
    for i in range(n):
        if node.board.__getitem__((i, 0)) == 'blue':
            reachable = node.board.connected_coords((i, 0))
            for (x, y) in reachable:
                if y == n - 1:
                    return "blue"
    return None

def getValue(node, n, color, oppColor):
    redCount = 0
    blueCount = 0
    score = 0
    for i in node.board._data:
        for j in i:
            if j == 1:
                redCount += 1
            if j == 2:
                blueCount += 1
    for r in range(n):
        for q in range(n):
            token = node.board.__getitem__((r,q))
            if token == color:
                score += (0.2 * abs(r - (n / 2.0)))
                score += (0.2 * abs(q - (n / 2.0)))
            elif token == oppColor:
                score -= (0.2 * abs(r - (n / 2.0)))
                score -= (0.2 * abs(q - (n / 2.0)))
    if color == "red":    
        score += redCount - blueCount
    else:
        score +=  blueCount - redCount
    return score
    
    


'''
 x = randrange(self.n)
        y = randrange(self.n)
        while self.board.is_occupied((x,y)):
            x = randrange(self.n)
            y = randrange(self.n)
        return ("PLACE", x, y)
        '''