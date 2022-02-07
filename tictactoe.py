def printBoard(board):
    print('  a   b   c')
    print(*(f'{i+1} ' + ' | '.join(board[i*3:(i+1)*3]) for i in range(3)), sep='\n -----------\n')
    print()

def makeMove(i, j, turn, history):
    tmp = history[-1].copy()
    if turn:
        tmp[i*3 + j] = 'X'
    else:
        tmp[i*3 + j] = 'O'
    history.append(tmp)

def unmakeMove(history):
    history.pop()

def checkWin(history):
    triplets = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    board = history[-1]
    for triple in triplets:
        if [board[i] for i in triple] in (['X','X','X'], ['O','O','O']):
            return True


def minimax(depth, min_depth, maximizing, history, best_move, tTable):
    if checkWin(history):
        return -1 if maximizing else 1

    if depth == 0:
        return 0

    current = history[-1]
    board_str = str(current)
    if depth < min_depth and board_str in tTable:
        return tTable[board_str]

    score = -1 if maximizing else 1

    for i in range(9):
        if current[i] == '·':
            makeMove(i // 3, i % 3, maximizing, history)
            candidate =  minimax(depth-1, min_depth, not maximizing, history, best_move, tTable)
            if maximizing:
                if score < candidate:
                    score = candidate
                    if depth == min_depth:
                        best_move[0] = (i // 3, i % 3) 
            else:
                if score > candidate:
                    score = candidate
                    if depth == min_depth:
                        best_move[0] = (i // 3, i % 3)
            unmakeMove(history)
            
            if maximizing and score == 1:
                break
            elif not maximizing and score == -1:
                break

    tTable[board_str] = score

    return score

def main(player1=True, player2=True):
    transposition = {}
    turns = 0
    history = [['·'] * 9]
    best_move = [0]
    xTurn = True
    printBoard(history[-1])
    while turns < 9:
        if (xTurn and player1) or (not xTurn and player2):
            player_input = input('Your move: ')
            i = int(player_input[1]) - 1
            j = ord(player_input[0]) - 97
            idx = i*3 + j
            if idx < 0 or idx > 8 or history[-1][idx] != '·':
                print('Invalid move!')
                continue
        else:
            minimax(9-turns,9-turns,xTurn,history,best_move,transposition)
            i, j = best_move[0]
            print('My move:', f'{chr(j+97)}{i+1}')

        makeMove(i, j, xTurn, history)
        printBoard(history[-1])
        if checkWin(history):
            if xTurn:
                print('X wins')
            else:
                print('O wins')
            break
        xTurn = not xTurn
        turns += 1
        if turns >= 9:
            print('Draw')

if __name__ == '__main__':
    main(player1=False, player2=False)