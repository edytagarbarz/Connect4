from connect4 import *
import signal
import copy
import random

infinity = 1000000
minusInfinity = -1000000
impossible = -10000000


class MiniMaxPlayer(Connect4.Player):

    def __init__(self, symbol, max_distance, time, debug):
        Connect4.Player.__init__(self, symbol, debug)
        self.time = time
        self.max_distance = max_distance + 1

    def alpha_beta_pruning(self, board, level, alpha, beta, current_max_distance, path):
        old_beta = beta
        old_alpha = alpha
        win, _ = board.end_game()
        if win or level == current_max_distance:
            return self.heuristic(board)
        # opponent
        if level % 2 == 1:
            ordering = []
            moves = [i for i in range(self.root)]
            if path in self.transposition_table[level].keys():
                ordering = sorted(self.transposition_table[level][path].items(), key=lambda kv: kv[1])
            self.transposition_table[level][path] = {}
            for (x, val) in ordering:
                moves.remove(x)
                new_board = Connect4.Board(board.size_x, board.size_y, copy.deepcopy(board.board))
                added = new_board.add_symbol(x, self.opponent_symbol)
                if added:
                    new_path = list(path)
                    new_path.append(x)
                    new_path = tuple(new_path)
                    new_beta = self.alpha_beta_pruning(new_board, level + 1, old_alpha, old_beta, current_max_distance,
                                                       new_path)
                    beta = min(beta, new_beta)

                    self.transposition_table[level][path][x] = new_beta
                    if alpha >= beta:
                        return beta
            for x in moves:
                new_board = Connect4.Board(board.size_x, board.size_y, copy.deepcopy(board.board))
                added = new_board.add_symbol(x, self.opponent_symbol)
                if added:
                    new_path = list(path)
                    new_path.append(x)
                    new_path = tuple(new_path)
                    new_beta = self.alpha_beta_pruning(new_board, level + 1, old_alpha, old_beta, current_max_distance,
                                                       new_path)
                    beta = min(beta, new_beta)
                    self.transposition_table[level][path][x] = new_beta
                    if alpha >= beta:
                        return beta

            return beta
        # player
        else:
            ordering = []
            moves = [i for i in range(self.root)]
            if path in self.transposition_table[level].keys():
                ordering = sorted(self.transposition_table[level][path].items(), key=lambda kv: kv[1],
                                  reverse=True)
            self.transposition_table[level][path] = {}
            for (x, val) in ordering:
                moves.remove(x)
                new_board = Connect4.Board(board.size_x, board.size_y, copy.deepcopy(board.board))
                added = new_board.add_symbol(x, self.symbol)
                if added:
                    new_path = list(path)
                    new_path.append(x)
                    new_path = tuple(new_path)
                    new_alpha = self.alpha_beta_pruning(new_board, level + 1, old_alpha, old_beta, current_max_distance,
                                                        new_path)

                    alpha = max(alpha, new_alpha)
                    self.transposition_table[level][path][x] = new_alpha
                    if alpha >= beta:
                        return alpha
            for x in moves:
                new_board = Connect4.Board(board.size_x, board.size_y, copy.deepcopy(board.board))
                added = new_board.add_symbol(x, self.symbol)
                if added:
                    new_path = list(path)
                    new_path.append(x)
                    new_path = tuple(new_path)
                    new_alpha = self.alpha_beta_pruning(new_board, level + 1, old_alpha, old_beta, current_max_distance,
                                                        new_path)

                    alpha = max(alpha, new_alpha)
                    self.transposition_table[level][path][x] = new_alpha
                    if alpha >= beta:
                        return alpha
            return alpha

    def iterative_deepening(self):
        # [level] [(path)] {to : val }
        self.transposition_table = [{} for _ in range(self.max_distance)]
        try:
            for i in range(1, self.max_distance):
                self.alpha_beta_pruning(Connect4.Board(self.board.size_x, self.board.size_y,
                                                              copy.deepcopy(self.board.board)), 0, minusInfinity,
                                               infinity,
                                               current_max_distance=i, path=(self.root,))
            signal.alarm(0)
        except TimeOutException:
            return

    ''' 
    Returns value of the board for given symbol S.
    Line with k S symbols (k >= 3), that are consecutive or divided by blank space, 
    is worth k * 10 points.
    '''
    def heuristic_for_player(self, board, symbol):
        limit = 2
        (end, who) = board.end_game()
        if end:
            if who == symbol:
                return infinity
            return minusInfinity
        board = board.board
        result = 0
        for a in board:
            counter = 0
            empty_counter = 0
            for i in range(0, len(a)):
                if a[i] == symbol:
                    counter += 1
                elif a[i] == ' ':
                    empty_counter += 1
                else:
                    if counter > limit and counter + empty_counter >= 4:
                        result += (counter * 10)
                    counter = 0
                    empty_counter = 0
            if counter > limit and counter + empty_counter >= 4:
                result += (counter * 10)

        for i in range(0, len(board[0])):
            counter = 0
            empty_counter = 0
            for j in range(0, len(board)):
                if board[j][i] == symbol:
                    counter += 1
                elif board[j][i] != ' ':
                    if counter > limit and empty_counter + counter >= 4:
                        result += (counter * 10)
                    counter = 0
                    empty_counter = 0
                else:
                    empty_counter += 1
            if counter > limit and counter + empty_counter >= 4:
                result += (counter * 10)

        for i in range(1, len(board) - 3):
            counter = 0
            empty_counter = 0
            for k in range(0, len(board)):
                if i + k >= len(board):
                    break
                if board[i + k][k] == symbol:
                    counter += 1
                elif board[i + k][k] != ' ':
                    if counter > limit and counter + empty_counter >= 4:
                        result += (counter * 10)
                    counter = 0
                    empty_counter = 0
                else:
                    empty_counter += 1
            if counter > limit and counter + empty_counter >= 4:
                result += (counter * 10)

        for i in range(1, len(board[0]) - 3):
            counter = 0
            empty_counter = 0
            for k in range(len(board)):
                if i + k >= len(board):
                    break
                if board[k][k + i] == symbol:
                    counter += 1
                elif board[k][k + i] != ' ':
                    if counter > limit and counter + empty_counter >= 4:
                        result += (counter * 10)
                    counter = 0
                    empty_counter = 0
                else:
                    empty_counter += 1
            if counter > limit and counter + empty_counter >= 4:
                result += (counter * 10)

        for i in range(1, len(board) - 3):
            counter = 0
            empty_counter = 0
            for k in range(0, len(board)):
                if i + k >= len(board):
                    break
                if board[i + k][len(board[0]) - 1 - k] == symbol:
                    counter += 1
                elif board[i + k][len(board[0]) - 1 - k] != ' ':
                    if counter > limit and counter + empty_counter >= 4:
                        result += (counter * 10)
                    counter = 0
                    empty_counter = 0
                else:
                    empty_counter = 0
            if counter > limit and counter + empty_counter >= 4:
                result += (counter * 10)

        for i in range(3, len(board[0])):
            counter = 0
            empty_counter = 0
            for k in range(len(board)):
                if i - k < 0:
                    break
                if board[k][i - k] == symbol:
                    counter += 1
                elif board[k][i - k] != ' ':
                    if counter > limit and counter + empty_counter >= 4:
                        result += (counter * 10)
                    counter = 0
                    empty_counter = 0
                else:
                    empty_counter += 1
            if counter > limit and counter + empty_counter >= 4:
                result += (counter * 10)

        return result

    def heuristic(self, board):
        result = -1 * self.heuristic_for_player(board, self.opponent_symbol)
        result += self.heuristic_for_player(board, self.symbol)
        return result

    def make_move(self):
        self.root = len(self.board.board[0])
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(self.time)

        self.iterative_deepening()
        if (self.root,) in self.transposition_table[0].keys():
            ordering = sorted(self.transposition_table[0][(self.root,)].items(), key=lambda kv: kv[1], reverse=True)
            if self.debug:
                print(self.transposition_table[0][(self.root,)].items())
            if len(ordering) == 0:
                return random.randint(0, len(self.board[0]) - 1)
            move, val = ordering[0]
            moves = [move]
            for (m, v) in ordering:
                if v == val:
                    moves.append(m)
            random.shuffle(moves)
            move = moves[0]
        else:
            move = random.randint(0, len(self.board[0]) - 1)
        if self.debug:
            print("MOVE", move)
        return move
