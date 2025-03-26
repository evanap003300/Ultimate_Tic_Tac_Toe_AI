'''
  ultimate-tick-alpha.py
  Author: Evan Phillips, Dao Bui, Paul Talaga
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
def getAIMove(state):
  # As an example pick the first available spot to play
  depth = 4
  maximizing = True
  options = generateSuccessors(state, 1)
  best_move, score = minimax(state, depth, maximizing)

  return best_move
  
# AI aspect: Insert your AI functions below

#for i in grid:
  #if(board(i) == " "):
    
# - and + scores 
def evaluate_mini_board(state):
  (big, box) = state
  mini_board = getMiniBoard(big, box)
  points_of_each_pos = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2] #weights
  sum = 0

  for i in range(9):
    if mini_board[i] == 'X':
        sum += points_of_each_pos[i]
    elif mini_board[i] == 'O':
        sum -= points_of_each_pos[i]

  
  # if(1 == X and 2 == x) # This is showing if two rows have x then smth happens

  # Block win - check row for 2, check column for 2, check diagonal for 2.
  # Take win - simulate a move and check if it wins 
  print("SUM SKIBIDI:", sum)

  return sum

def block_win(mini_board):
  pass

def winMiniBoard(mini_board):
  pass

def evaluate_macro_board(state):
  # loop through each mini board and check
  (big, box) = state
  sum = 0
  for i in range(9):
    mini_board = getMiniBoard(big, i)
    if miniScorePlayer(mini_board, 'X') == 1:
      sum += 10
    if miniScorePlayer(mini_board, 'O') == 1:
      sum -= 10

  for i in range(9):
    new_state = (big, i)
    sum += evaluate_mini_board(new_state)

  print("SUM RIZZIDIYYY:", sum)
  return sum

def minimax(state, depth, maximizing):
  # Base case terminal state reached or depth reached
  (big, box) = state
  mini_board = getMiniBoard(big, box)
  best_move = None

  if miniScorePlayer(mini_board, 'X') == 1 or miniScorePlayer(mini_board, 'O') == 1 or isBigFull(state):
    return None, evaluate_macro_board(state)

  if depth == 0:
    return best_move, evaluate_macro_board(state)
  
  evaluation_score = 0
  
  if maximizing:
      max_evaluation = float('-inf')
      print("nibidi")
      for move in generateSuccessors(state, 'X'):  
        new_state = move[1] # Update board with move
        _, evaluation_score = minimax(new_state, depth - 1, False)
        if evaluation_score > max_evaluation:
          max_evaluation = evaluation_score
          best_move = move[0]
      print(best_move, "maxwell corwin", max_evaluation)
      return best_move, max_evaluation
  
  else:
    min_evaluation = float('inf')
    for move in generateSuccessors(state, 'O'):
      new_state = move[1]
      _, evaluation_score = minimax(new_state, depth - 1, True)
      if evaluation_score < min_evaluation:
        min_evaluation = evaluation_score
        best_move = move[0]
    print(best_move, "minwell corwin", min_evaluation)
    return best_move, min_evaluation


#  -------------- Run the Game! -------------------

state = ([" "] * 81, 0)
play = True
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

  move = getAIMove(state)
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
