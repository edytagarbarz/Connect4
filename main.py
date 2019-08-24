import inputPlayer
import connect4
import miniMaxPlayer
import mcts
import argparse
import sys

DEBUG = False
PRINT = False

parser = argparse.ArgumentParser(description="Connect4")
parser.add_argument('-p1', '--player1', type=str, help='type of the player1. One of: "input", "minimax", "mcts"')
parser.add_argument('-p2', '--player2', type=str, help='type of the player2. One of: "input", "minimax", "mcts"')
parser.add_argument('--depth', type=int, default=4, help='maximal depth search for MiniMax Player')
parser.add_argument('-t1', '--time1', type=int, default=6, help='number of seconds for a simple move decision')
parser.add_argument('-t2', '--time2', type=int, default=6, help='number of seconds for a simple move decision')
parser.add_argument('-d', '--debug', help='show debug info', action='store_true')
parser.add_argument('-p', '--print', help='print board', action='store_true')
parser.add_argument('-g', '--games', help='number of games', type=int, default=1)



def run_program():
    args = parser.parse_args()

    if args.debug:
        global DEBUG
        DEBUG = True

    if args.print:
        global PRINT
        PRINT = True

    if args.player1 == "input":
        p1 = inputPlayer.InputPlayer('O', DEBUG)
    elif args.player1 == "minimax":
        p1 = miniMaxPlayer.MiniMaxPlayer('O', args.depth, args.time1, DEBUG)
    elif args.player1 == "mcts":
        p1 = mcts.MCTSPlayer('O', args.time1, DEBUG)
    else:
        print("tu 1")
        parser.print_help()
        sys.exit()

    if args.player2 == "input":
        p2 = inputPlayer.InputPlayer('X', DEBUG)
    elif args.player2 == "minimax":
        p2 = miniMaxPlayer.MiniMaxPlayer('X', args.depth, args.time2, DEBUG)
    elif args.player2 == "mcts":
        p2 = mcts.MCTSPlayer('X', args.time2, DEBUG)
    else:
        print("tu 2", args.player2)
        parser.print_help()
        sys.exit()
    c = connect4.Connect4()

    p1w = 0
    p2w = 0
    for i in range(args.games):
        game = c.new_game(p1, p2, 7, 6)
        symbol = game.play(PRINT)
        if symbol == p1.symbol:
            p1w += 1
        elif symbol == p2.symbol:
            p2w += 1
        print("Won Player", symbol)

    print("P1:", p1.symbol, p1w)
    print("P2:", p2.symbol, p2w)


if __name__ == "__main__":
    run_program()
