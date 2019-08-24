from connect4 import *
import math
import copy
import random
import signal

infinity = 1000000
minusInfinity = infinity * -1


class MCTSPlayer(Connect4.Player):
    def __init__(self, symbol, time, debug):
        Connect4.Player.__init__(self, symbol, debug)
        self.time = time
        self.nodes_values = {}
        self.expanded = dict()

    def ucb(self, node_path):
        w, n = self.nodes_values[node_path]
        parent_path = node_path[:-1]
        _, N = self.nodes_values[parent_path]
        if n == 0:
            return infinity
        return w + 2 * math.sqrt(2 * math.log(N) / n)

    def simulation(self, path):
        board = self.board.get_copy()
        my_turn = True
        for a in path[1:]:
            symbol_to_add = self.symbol
            if not my_turn:
                symbol_to_add = self.opponent_symbol
            board.add_symbol(a, symbol_to_add)
            e, s = board.end_game()
            if e:
                if s == self.symbol:
                    return 1
                if s == self.opponent_symbol:
                    return -1
                return 0
            my_turn = not my_turn

        while True:
            while True:
                a = random.randint(0, self.len - 1)
                symbol = self.symbol
                if not my_turn:
                    symbol = self.opponent_symbol
                if board.add_symbol(a, symbol):
                    break
            e, s = board.end_game()
            if e:
                if s == self.symbol:
                    return 1
                if s == self.opponent_symbol:
                    return -1
                return 0
            my_turn = not my_turn

    def expansion(self, node_path):
        path = (self.len,)
        board = self.board.get_copy()
        my_turn = True
        for a in node_path[1:]:
            path = path + (a,)
            symbol_to_add = self.symbol
            if not my_turn:
                symbol_to_add = self.opponent_symbol
            board.add_symbol(a, symbol_to_add)
            e, s = board.end_game()
            if e:
                return path
            my_turn = not my_turn
        possible_nodes = []
        for i in range(self.len):
            new_path = path + (i, )
            if board.can_add(i):
                self.nodes_values[new_path] = (0, 0)
                self.expanded[new_path] = False
                possible_nodes.append(i)

        self.expanded[node_path] = True
        random.shuffle(possible_nodes)
        return path + (possible_nodes[0],)

    def selection(self, path):
        if not self.expanded[path]:
            return path
        max_ucb = minusInfinity
        max_node_path = (self.len,)
        for i in range(self.len):
            new_path = path + (i,)
            if new_path in self.nodes_values.keys():
                new_ucb = self.ucb(new_path)
                if new_ucb > max_ucb:
                    max_ucb = new_ucb
                    max_node_path = new_path
        return self.selection(max_node_path)

    def backpropagation(self, path, value):
        if len(path) == 0:
            return
        w, n = self.nodes_values[path]
        new_value = value
        if len(path) % 2 == 1:
            new_value *= -1
        self.nodes_values[path] = (w + new_value, n + 1)
        return self.backpropagation(path[:-1], value)

    def evaluate(self):
        try:
            self.nodes_values = dict()
            self.expanded = dict()
            init_node = (self.len,)
            self.nodes_values[init_node] = (0, 0)
            self.expanded[init_node] = False
            while True:
                path = self.selection(init_node)
                path = self.expansion(path)
                value = self.simulation(path)
                self.backpropagation(path, value)
        except TimeOutException:
            return

    def make_move(self):
        self.len = len(self.board.board[0])
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(self.time)
        self.evaluate()
        max_nodes = []
        max_n = 0
        p = []
        for i in range(self.len):
            if (self.len, i) in self.nodes_values.keys():
                w, n = self.nodes_values[(self.len, i)]
                p.append((w, n))
                if n == max_n:
                    max_nodes.append(i)
                if n > max_n:
                    max_nodes = [i]
                    max_n = n
        if self.debug:
            print(p)
        random.shuffle(max_nodes)
        return max_nodes[0]
