from connect4 import *


class InputPlayer(Connect4.Player):
    def __init__(self, symbol, debug):
        Connect4.Player.__init__(self, symbol, debug)

    def make_move(self):
        while True:
            x = input("Column number: ")
            try:
                x = int(x)
                if x > 6 or x < 0:
                    raise ValueError
                return x
            except ValueError:
                print("Invalid input, try number from range [0,6]")
    
