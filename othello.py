
import math
white = "O"
black = "X"
EDGE = [p for p in range(10)] + [q for q in range(90,100)] + [10*r for r in range(10)] + [10*s+9 for s in range(10)]  #position of edges
UP, DOWN, LEFT, RIGHT = -10,10,-1,1     
NW,NE,SW,SE = -11,-9,9,11
DIRECTIONS = [UP,DOWN,LEFT,RIGHT,NW,NE,SW,SE]  #directions to be considered
BOARD_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,               #Board weights assigned to each postion based on
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0, 			  #the score value or importance of each position
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

def make_board():           #initial game position
    array = []
    for k in range(100):
        if k in EDGE: 
            array.append("*")
        elif k == 44 or k == 55: 
            array.append(white)
        elif k == 45 or k == 54:
            array.append(black)
        else:
            array.append(".")
    return array

def Show(board):         #display board positon
    print("  1 2 3 4 5 6 7 8 ", end = "")     
    i = 1
    for s in range(len(board)):
        if board[s] == '*':
            if s == 0:
                print(" ", end = " ")
            elif s%10 == 0:
                print()
                if i != 9:
                    print(i, end = " ")
                    i+=1
            if s == 90:
                print(" ",end = " ")
        else:
            print(board[s], end = " ")
    print()

def count(board,player):     #count no of discs on board of a player
    c = 0
    for k in range(len(board)):
        if k in EDGE: continue
        if board[k] == player:
            c+=1
    return c


def emptyEntries(board):
    c = []
    for k in range(len(board)):
        if k in EDGE: continue
        if board[k] == '.':
            c.append(k)
    return c

def opponent(player):
    if player == white: return black
    else: return white

def position(m,direction,board,player):
    position = m + direction
    if board[position] == player or position in EDGE: return None
    while board[position] == opponent(player):
        position += direction
    if position in EDGE or board[position] == ".": return None
    else: return position


def valid_move(m,board,player):
    if board[m] != '.': return False 
    return any(position(m,D,board,player) for D in DIRECTIONS)


def flip(m,position,direction,board,player): #flip all squares between m and position
    current = m + direction
    while current != position:
        board[current] = player
        current += direction


def PossibleMoves(board,player): #all possible Moves
    m = []
    for k in range(len(board)):
        if k in EDGE:
            continue
        if valid_move(k,board,player):
            m.append(k)
    return m


def play(m,board,player):
    if not m: return
    if not valid_move(m,board,player):
        print("INVALID MOVE")
        if player == black:  
            return play(int(input("MOVE: ")),board,player)
    board[m] = player
    for D in DIRECTIONS:
        br = position(m,D,board,player)
        if br:
            flip(m,br,D,board,player)
    return board


def winner(board):     #max no. of discs ==> winner
    if count(board,white) > count(board,black): return white
    elif count(board,black) > count(board,white): return black
    else: return 0

def score(board,player):      #to calculate score on board
    total = 0
    for k in range(len(board)):
        if k in EDGE: continue
        if board[k] == player: total += BOARD_WEIGHTS[k]
        elif board[k] == opponent(player): total -= BOARD_WEIGHTS[k]
    return total


def alphabeta(board,depth,alpha,beta,player,maximizing_player):       #for alphabeta pruning 
    if depth == 0 or not PossibleMoves(board,player):
        return score(board,player)
    if maximizing_player:
        v = -math.inf
        for k in PossibleMoves(board,player):
            temp_board = play(k,board.copy(),player)
            v = max(v,alphabeta(temp_board,depth-1,alpha,beta,opponent(player),False))
            alpha = max(alpha,v)
            if beta<=alpha:
                break
        return v
    else:
        v = math.inf
        for k in PossibleMoves(board,player):
            temp_board = play(k,board.copy(),player)
            v = min(v,alphabeta(temp_board,depth-1,alpha,beta,opponent(player),True))
            beta = min(beta,v)
            if beta<=alpha:
                break
        return v


def best_move(board,player):
    if len(emptyEntries(board))==1: return emptyEntries(board)[0]     # if only one move remaining return that 
    depth = 4 # depth limit for search
    mov = PossibleMoves(board,player)
    if not mov: return None
    print("COMPUTER'S MOVE ",mov)
    max_points = 0
    max_index = mov[0]
    for m in mov:
        temp_board = play(m,board.copy(),player)
        points = alphabeta(temp_board,depth,-math.inf,math.inf,player,True)
        if points > max_points:
            max_points = points
            max_index = m 
    return max_index           #for getting move where max score can be achieved



def gameOver():
    return all(board[k] != '.' for k in range(len(board)))

board = make_board()
print()
print("Type a position number to play")
print()
print("START")
print()
Show(board)
print()
while not gameOver():
    print("YOUR POSSIBLE MOVES: ",PossibleMoves(board,black))
    move = int(input("YOUR MOVE: "))
    play(move,board,black)
    Show(board)
    print()
    best = best_move(board,white)
    play(best,board,white)
    print("COMPUTER'S MOVE: ", best)
    Show(board)
    print()
print("END")
Show(board)
print("winner: ",winner(board))
