import math
'''
  ultimate-tick-alpha.py
  Author: Paul Talaga
  Date: Nov 8, 2018
  Description: Implements the Ultimate Tic Tac Toe game, but no AI is implemented.
               See the getAIMove to add an AI player.
  Works with Python 2.X and 3.X
''' 


'''A board state is an array of 81 strings, where each string is either X, O, or a space.
   The inBox, getMiniBoard, getHighBoard, and minToBig functions allow this big state to
   be analyzed as a normal 3x3 board.'''

def inBox(box, x, y):
  #boxes are labeled 0 1 2    3 4 5    6 7 8
  return int(x / 3) == int(box % 3) and int(y / 3) == int(box / 3)
  
def getMiniBoard(big, box):
  (x,y) = (box%3, int(box / 3) )
  indexes = []
  indexes += map(lambda a: x*3 + a + y *27,range(3))
  indexes += map(lambda a: x*3 + a + y *27 + 9,range(3))
  indexes += map(lambda a: x*3 + a + y *27 + 18,range(3))
  # make subboard
  subboard = []
  for i in indexes:
    subboard.append(big[i])
  return subboard
  
  
def getHighBoard(big):
  ret = []
  for box in range(9):
    (x,y) = (box%3, int(box / 3) )
    indexes = []
    indexes += map(lambda a: x*3 + a + y *27, range(3))
    indexes += map(lambda a: x*3 + a + y *27 + 9, range(3))
    indexes += map(lambda a: x*3 + a + y *27 + 18, range(3))
    # make subboard
    subboard = []
    for i in indexes:
      subboard.append(big[i])
    if miniScorePlayer(subboard,'X') == 1: # If X won this miniboard, fill all with Xs
      ret.append('X')
    elif miniScorePlayer(subboard,'O') == 1:# If O won this miniboard, fill with all Os
      ret.append('O')
    elif isFull(subboard):  # No win, but a Tie
      ret.append('T')
    else:
      ret.append(' ')
  return ret
    
def minToBig(index, box):
  (x,y) = (box%3, int(box / 3) )
  return x*3 + (index % 3) + y *27 + int(index/3) * 9

def printState(state):
  (big, box) = state
  # Print the large board
  print("Large board state.  You must play on the . locations.")
  print("Box: %d" % box)
  for y in range(9):
    line = ""
    for x in range(9):
      if big[x + y * 9] == " " and inBox(box,x,y):
         line += "."
      else:
        line += big[x + y * 9]
      if (x + 1) % 3 == 0 and x != 8:
        line += "|"
    print( line)
    if (y+1) % 3 == 0 and y != 8:
      print("-" * 11)
  print("")
  print("Who is winning each small board:")
  mini = getHighBoard(big)
  for y in range(3):
    line = ""
    for x in range(3):
      line += mini[x + y * 3] 
      if x < 2:
        line += "|"
    print( line)
    if y < 2:
      print("-----")
  print("Score for O: " + str(score(state)))
  print("")
  
def printNumberHelp():
  state = list("0123456789")
  print("Index Helper:")
  for y in range(3):
    line = ""
    for x in range(3):
      line += state[x + y * 3] 
      if x < 2:
        line += "|"
    print( line )
    if y < 2:
      print("-----")
  print("\n")


def miniScorePlayer(mini, c):
  # horizontal
  for y in range(3):
    r = y * 3
    if mini[r] == c and mini[r+1] == c and mini[r+2] == c:
      return 1
  # vertical
  for x in range(3):
    if mini[x] == c and mini[x+3] == c and mini[x+6] == c:
      return 1
  # diag down to right
  if mini[0] == c and mini[4] == c and mini[8] == c:
    return 1
  # diag down to left
  if mini[2] == c and mini[4] == c and mini[6] == c:
    return 1
  return 0
  
def validMove(state, pos):
  (big, box) = state
  miniboard = getMiniBoard(big, box)
  high = getHighBoard(big)
  if high[box] in ['X', 'O', 'T']:
    return False
  return 0 <= pos <= 8 and miniboard[pos] == " "

  
def score(state):
  (big, box) = state
  mini = getHighBoard(big)
  x = miniScorePlayer(mini,'X')
  o = miniScorePlayer(mini,'O')
  if x == o:
    return 0
  if x > o:
    return 1
  if x < o:
    return -1
    
def isFull(minBoard):
  return not " " in minBoard
  
def isBigFull(state):
  (big, box) = state
  return isFull(getHighBoard(big))
  
def generateSuccessors(state, player):
  player_character = 'O' if player == 1 else 'X'
  ret = []
  (big, box) = state

  if isFull(getMiniBoard(big, box)) or miniScorePlayer(getMiniBoard(big, box), 'O') or miniScorePlayer(getMiniBoard(big, box), 'X'):
    box = -1
    for i in range(9):
      if not isFull(getMiniBoard(big, i)) and not miniScorePlayer(getMiniBoard(big, i), 'O') and not miniScorePlayer(getMiniBoard(big, i), 'X'):
        box = i
        break

  state = (big, box)
  for i in range(9):
    if validMove(state, i):
      newBig = big[:]
      newBig[minToBig(i, box)] = player_character
      ret.append((i, (newBig, i)))

  if len(ret) == 0:
    print("no options!")
  return ret
  
'''This is called in the game play.  Substitute your own function to change the AI method.
   This needs to return a move, which is an index to place their character.'''
def getAIMove(state, depth):
    # It isn't taking free wins of boards 
    score, move = minimax(state, depth, -float('inf'), float('inf'), True)
    return move
  
# AI aspect: Insert your AI functions below

# Evals a single local board
def evaluate_square(mini_board, is_ai_move):
    evaluation = 0
    points = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]
    
    # Apply positional weights
    for bw in range(len(mini_board)):
        if mini_board[bw] == 'X':  # AI is 'X'
          evaluation += points[bw]
        elif mini_board[bw] == 'O':  # Human is 'O'
          evaluation -= points[bw]
    
    # Check for potential wins (AI)
    ai_temp_board = mini_board.copy()
    for i in range(9):
        if ai_temp_board[i] == 0:  # Empty space
            ai_temp_board[i] = 1  # Simulate AI move
            pair_value = check_for_pair(ai_temp_board, i)
            win_value = check_for_win(ai_temp_board)
            if win_value > 0:
                evaluation -= 7  # AI win potential
            elif pair_value > 0:
                evaluation -= 6  # AI pair potential
            ai_temp_board[i] = 0  # Reset
    
    # Check for blocking opportunities (Human)
    human_temp_board = mini_board.copy()
    for i in range(9):
        if human_temp_board[i] == 0:  # Empty space
            block_value = check_for_block(human_temp_board, i)
            if block_value > 0:
                evaluation += 9  # Value for blocking opponent
    
    return evaluation


# Evals a potential move (might not need)
def evaluate_position(state, square):
    evaluation = 0

    (big, box) = state
    mini_board = getMiniBoard(big, box)
    position_weights = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]

    evaluation += position_weights[square]

    ai_char = 'X'  # AI plays as X
    human_char = 'O'  # Human plays as O
    
    # Simulate making the move
    temp_board = mini_board.copy()
    temp_board[square] = ai_char

    pair_value = check_for_pair(temp_board, square)
    block_value = check_for_block(mini_board, square)  # Pass original board to check blocking
    win_value = check_for_win(temp_board)

    # Creating a pair
    evaluation += pair_value

    # Blocking a win
    evaluation += block_value

    # Winning the box
    evaluation += win_value

    return evaluation

# Check for creating pairs (2 in a row with an empty space)
def check_for_pair(board, square):
  pair_value = 0
  ai_char = 'X'  
  
  # Horizontal check
  row_start = (square // 3) * 3
  row = board[row_start:row_start+3]
  if row.count(ai_char) == 2 and row.count(" ") == 1:
      pair_value += 1
  
  # Vertical check
  col_start = square % 3
  column = [board[col_start], board[col_start+3], board[col_start+6]]
  if column.count(ai_char) == 2 and column.count(" ") == 1:
      pair_value += 1
  
  # Diagonal checks
  if square in [0, 4, 8]:  # Top-left to bottom-right diagonal
      diag1 = [board[0], board[4], board[8]]
      if diag1.count(ai_char) == 2 and diag1.count(" ") == 1:
          pair_value += 1.2  # Slightly higher value for diagonals
  
  if square in [2, 4, 6]:  # Top-right to bottom-left diagonal
      diag2 = [board[2], board[4], board[6]]
      if diag2.count(ai_char) == 2 and diag2.count(" ") == 1:
          pair_value += 1.2  # Slightly higher value for diagonals

  return pair_value

def check_for_block(original_board, square):
    block_value = 0
    temp_board = original_board.copy()
    human_char = 'O'
    
    # Simulate opponent's move
    temp_board[square] = human_char
    
    # Check if this blocks a win (horizontal)
    row_start = (square // 3) * 3
    row = temp_board[row_start:row_start+3]
    if row.count(human_char) == 3:
        block_value += 2
    
    # Vertical check
    col_start = square % 3
    column = [temp_board[col_start], temp_board[col_start+3], temp_board[col_start+6]]
    if column.count(human_char) == 3:
        block_value += 2
    
    # Diagonal checks
    if square in [0, 4, 8]:
        diag1 = [temp_board[0], temp_board[4], temp_board[8]]
        if diag1.count(human_char) == 3:
            block_value += 2
    
    if square in [2, 4, 6]:
        diag2 = [temp_board[2], temp_board[4], temp_board[6]]
        if diag2.count(human_char) == 3:
            block_value += 2
            
    return block_value

def check_for_win(board):
    ai_char = 'X'
    if miniScorePlayer(board, ai_char) == 1:
        return 5  # Value for winning the box
    return 0

# Evals a whole game state (Should be done)
def evaluate_game(state, is_ai_move):
  (big, box) = state
  high_board = getHighBoard(big)
  total_score = 0
  
  weights = [1.4, 1, 1.4, 1, 1.75, 1, 1.4, 1, 1.4]

  # Evaluate each mini board
  for i in range(9):
      mini_board = getMiniBoard(big, i)
      if not isFull(mini_board) and not miniScorePlayer(mini_board, 'X') and not miniScorePlayer(mini_board, 'O'):
          total_score += evaluate_square(mini_board, is_ai_move) * 1.5 * weights[i]
  
  # Check if the game is decided
  if miniScorePlayer(high_board, 'X') == 1:
      total_score = 5000  # AI wins
  if miniScorePlayer(high_board, 'O') == 1:
      total_score = -5000  # Human wins

  if not is_ai_move:
    return total_score * -1
  
  return total_score

# Minimax algo with alpha-beta pruning
def minimax(state, depth, alpha, beta, is_ai_move):
    INFINITY = 9223372036854775807
    best_move = -1

    # Terminal conditions
    (big, box) = state
    calcEval = evaluate_game(state, is_ai_move)
    if depth <= 0 or abs(calcEval) > 5000:
        return calcEval, best_move
    
    if is_ai_move:  # Maximizing player (AI)
        max_eval = -INFINITY
        # Generate all possible AI moves
        moves = generateSuccessors(state, 0)  # 0 for AI ('X')
        
        for move, new_state in moves:
            eval_score, _ = minimax(new_state, depth-1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        
        return max_eval, best_move
    
    else:  # Minimizing player (Human)
        min_eval = INFINITY
        # Generate all possible human moves
        moves = generateSuccessors(state, 1)  # 1 for Human ('O')
        
        for move, new_state in moves:
            eval_score, _ = minimax(new_state, depth-1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        
        return min_eval, best_move


#  -------------- Run the Game! -------------------

state = ([" "] * 81, 0)
play = True
count = 0
while play:
  big, box = state
  high = getHighBoard(big)
  for b in range(9):
    if high[b] in ['X', 'O', 'T']:
      (x, y) = (b % 3, b // 3)
      indexes = []
      indexes += [x*3 + a + y*27 for a in range(3)]
      indexes += [x*3 + a + y*27 + 9 for a in range(3)]
      indexes += [x*3 + a + y*27 + 18 for a in range(3)]
      for i in indexes:
        big[i] = high[b]
  state = (big, box)

  if isFull(getMiniBoard(big, box)) or miniScorePlayer(getMiniBoard(big, box), 'X') or miniScorePlayer(getMiniBoard(big, box), 'O'):
    for i in range(9):
      if not isFull(getMiniBoard(big, i)) and not miniScorePlayer(getMiniBoard(big, i), 'X') and not miniScorePlayer(getMiniBoard(big, i), 'O'):
        state = (big, i)
        break

  print("")
  printNumberHelp()
  printState(state)
  move = int(input('Enter O placement:'))
  if not validMove(state, move):
    print("That move is not valid, try again.")
    continue

  big, box = state
  big[minToBig(move, box)] = "O"
  state = (big, move)

  if score(state) == -1:
    printState(state)
    print("You Won!!!!")
    play = False
    break
  if isFull(getHighBoard(big)):
    printState(state)
    print("Tie!")
    play = False
    break

  move = getAIMove(state, 5)
  count += 1

  if count > 10:
    move = getAIMove(state, 6)
  
  if count > 20:
    move = getAIMove(state, 7)

  big, box = state
  big[minToBig(move, box)] = "X"
  state = (big, move)

  if score(state) == 1:
    printState(state)
    print("Computer Won.  ;-(")
    play = False
    break
  if isFull(getHighBoard(big)):
    printState(state)
    print("Tie!")
    play = False
    break