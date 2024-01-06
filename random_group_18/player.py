
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
        self.color = player
        self.opp_color = "blue" if self.color == "red" else "red"
        self.board = Board(n)
        self.possible_moves = []
        self.n = n
        self.first_move = True
        for i in range(n):
            for j in range(n):
                self.possible_moves.append((i, j))

    def action(self):
        if self.first_move and self.color == "blue":
            self.first_move = False
            return ("STEAL", )
        if self.first_move and self.color == "red" and self.n % 2 != 0:
            self.possible_moves.remove((int((self.n - 1) / 2), int((self.n - 1) / 2)))

        random.shuffle(self.possible_moves)
        current_node = Node(self.board)
        
        if self.n < 7:
            best_move, val = minimax(current_node, 3, True, self.n, self.color, self.opp_color, self.possible_moves, float('-inf'), float('inf'))
        else:
            best_move, val = minimax(current_node, 2, True, self.n, self.color, self.opp_color, self.possible_moves, float('-inf'), float('inf'))

        if self.first_move:
            self.first_move = False
            self.possible_moves.append((int((self.n - 1) / 2), int((self.n - 1) / 2)))
        
        return ("PLACE", best_move[0], best_move[1])

    def turn(self, player, action):
        if action[0] == "STEAL":
            for i in range(self.n):
                for j in range(self.n):
                    if self.board.__getitem__((i, j)) == "red":
                        self.board.__setitem__((i, j), None)
                        self.board.place(player, (j, i))
                        return
        self.board.place(player, tuple([action[1], action[2]]))

def minimax(node, depth, my_turn, n, color, opp_color, possible_moves, alpha, beta):
    best_move = None
    
    if depth == 0:
        return None, get_value(node, n, color, opp_color)

    if win_check(node, n) == color:
        return None, float('inf')
    elif win_check(node, n) is not None:
        return None, float('-inf')

    if my_turn:
        max_value = float('-inf')
        for i in possible_moves:
            if node.board.is_occupied(i):
                continue

            new_board = copy.deepcopy(node.board)
            new_board.place(color, i)
            child = Node(new_board)
            value = minimax(child, depth - 1, False, n, color, opp_color, possible_moves, alpha, beta)[1]

            if value > max_value:
                max_value = value
                best_move = i
            elif best_move is None:
                best_move = i

            alpha = max(alpha, value)
            if beta <= alpha:
                break

        return best_move, max_value

    else:
        min_value = float('inf')
        for i in possible_moves:
            if node.board.is_occupied(i):
                continue

            new_board = copy.deepcopy(node.board)
            new_board.place(opp_color, i)
            child = Node(new_board)
            value = minimax(child, depth - 1, True, n, color, opp_color, possible_moves, alpha, beta)[1]

            if value < min_value:
                min_value = value
                best_move = i
            elif best_move is None:
                best_move = i

            beta = min(beta, value)
            if beta <= alpha:
                break

        return best_move, min_value

def win_check(node, n):
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

def get_value(node, n, color, opp_color):
    red_count = 0
    blue_count = 0
    score = 0

    for i in node.board._data:
        for j in i:
            if j == 1:
                red_count += 1
            if j == 2:
                blue_count += 1

    for r in range(n):
        for q in range(n):
            token = node.board.__getitem__((r, q))
            if token == color:
                score -= (0.2 * abs(r - floor(n / 2.0)))
                score -= (0.2 * abs(q - floor(n / 2.0)))
            elif token == opp_color:
                score += (0.2 * abs(r - floor(n / 2.0)))
                score += (0.2 * abs(q - floor(n / 2.0)))

    if color == "red":    
        score += red_count - blue_count
    else:
        score +=  blue_count - red_count

    return score

    
    



       