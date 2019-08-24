import enum
import copy


class TimeOutException(Exception):
    pass


class GameState(enum.Enum):
    UNRESOLVED = 0
    RESOLVED_WIN = 1
    RESOLVED_DRAW = 2


def signal_handler(signum, frame):
    raise TimeOutException("Timed out!")


class Connect4:

    def new_game(self, playerO, playerX, sizeX, sizeY):
        return Connect4.Game(playerO, playerX, sizeX, sizeY)

    class Board:
        def __init__(self, size_x, size_y, board=None):
            self.size_x = size_x
            self.size_y = size_y
            if board is None:
                self.set_clear_board()
            else:
                self.board = board

        def get_copy(self):
            return Connect4.Board(self.size_x, self.size_y, copy.deepcopy(self.board))

        def set_clear_board(self):
            self.board = list()
            for i in range(self.size_y):
                a = list()
                for _ in range(self.size_x):
                    a.append(' ')
                self.board.append(a)

        def print(self):
            for i in range(len(self.board) - 1, -1, -1):
                a = self.board[i]
                print('', *a, '', sep='|')
            a = [i for i in range(len(self.board[0]))]
            print('', *a, '', sep='|')
            print()

        def add_symbol(self, x, symbol):
            for a in self.board:
                if a[x] == ' ':
                    a[x] = symbol
                    return True
            return False

        def can_add(self, x):
            for a in self.board:
                if a[x] == ' ':
                    return True
            return False

        def end_game(self):
            flag = True
            for a in self.board:
                for b in a:
                    if b == ' ':
                        flag = False
                        break
                if not flag:
                    break
            if flag:
                return True, 0
            for a in self.board:
                counter = 1
                for i in range(1, len(a)):
                    if a[i] == a[i - 1] and a[i] != ' ':
                        counter += 1
                        if counter == 4:
                            return True, a[i]
                    else:
                        counter = 1

            for j in range(self.size_x):
                counter = 1
                for i in range(1, self.size_y):
                    if self.board[i][j] == self.board[i - 1][j] and self.board[i][j] != ' ':
                        counter += 1
                        if counter == 4:
                            return True, self.board[i][j]
                    else:
                        counter = 1

            for i in range(0, self.size_y - 3):
                for j in range(0, self.size_x - 3):
                    if self.board[i][j] != ' ':
                        flag = True
                        for k in range(1, 4):
                            if self.board[i + k][j + k] != self.board[i][j]:
                                flag = False
                                break
                        if flag:
                            return True, self.board[i][j]
            for i in range(3, self.size_y - 1):
                for j in range(0, self.size_x - 3):
                    if self.board[i][j] != ' ':
                        flag = True
                        for k in range(1, 4):
                            if self.board[i - k][j + k] != self.board[i][j]:
                                flag = False
                                break
                        if flag:
                            return True, self.board[i][j]
            return False, -1

    class Player:
        def __init__(self, symbol, debug):
            self.debug = debug
            self.board = None
            self.symbol = symbol

        def set_board(self, board):
            self.board = board

        def make_move(self):
            pass

        def set_opponent_symbol(self, symbol):
            self.opponent_symbol = symbol

    class Game:
        def __init__(self, player_o, player_x, size_x, size_y):
            self.playerO = player_o
            self.playerX = player_x
            self.board = Connect4.Board(size_x, size_y)

        def add_symbol(self, x, symbol):
            return self.board.add_symbol(x, symbol)

        def end_game(self):
            return self.board.end_game()

        def play(self, print):
            self.playerO.set_board(self.board)
            self.playerX.set_board(self.board)
            self.playerO.set_opponent_symbol(self.playerX.symbol)
            self.playerX.set_opponent_symbol(self.playerO.symbol)
            if print:
                self.board.print()
            while True:
                while True:
                    column = self.playerO.make_move()
                    if self.add_symbol(column, self.playerO.symbol):
                        if print:
                            self.board.print()
                        (c, w) = self.end_game()
                        if c:
                            return w
                        break
                while True:
                    column = self.playerX.make_move()
                    if self.add_symbol(column, self.playerX.symbol):
                        if print:
                            self.board.print()
                        (c, w) = self.end_game()
                        if c:
                            return w
                        break
