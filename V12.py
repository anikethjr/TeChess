import chess

def eval_state(board):
	position_points = {}
	position_points['P'] = [0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5,  5, 10, 25, 25, 10,  5,  5, 0,  0,  0, 20, 20,  0,  0,  0, 5, -5,-10,  0,  0,-10, -5,  5, 5, 10, 10,-20,-20, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0]
	position_points['N'] = [-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,  0,  0,  0,  0,-20,-40,-30,  0, 10, 15, 15, 10,  0,-30,-30,  5, 15, 20, 20, 15,  5,-30,-30,  0, 15, 20, 20, 15,  0,-30,-30,  5, 10, 15, 15, 10,  5,-30,-40,-20,  0,  5,  5,  0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50]
	position_points['B'] = [-20,-10,-10,-10,-10,-10,-10,-20,-10,  0,  0,  0,  0,  0,  0,-10,-10,  0,  5, 10, 10,  5,  0,-10,-10,  5,  5, 10, 10,  5,  5,-10,-10,  0, 10, 10, 10, 10,  0,-10,-10, 10, 10, 10, 10, 10, 10,-10,-10,  5,  0,  0,  0,  0,  5,-10,-20,-10,-10,-10,-10,-10,-10,-20]
	position_points['R'] = [0,  0,  0,  0,  0,  0,  0,  0,  5, 10, 10, 10, 10, 10, 10,  5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5,  0,  0,  0,  5,  5,  0,  0,  0]
  	position_points['Q'] = [-20,-10,-10, -5, -5,-10,-10,-20,-10,  0,  0,  0,  0,  0,  0,-10,-10,  0,  5,  5,  5,  5,  0,-10, -5,  0,  5,  5,  5,  5,  0, -5,  0,  0,  5,  5,  5,  5,  0, -5,-10,  5,  5,  5,  5,  5,  0,-10,-10,  0,  5,  0,  0,  0,  0,-10,-20,-10,-10, -5, -5,-10,-10,-20]
	position_points['K'] = [-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10, 20, 20,  0,  0,  0,  0, 20, 20, 20, 30, 10,  0,  0, 10, 30, 20]
	points = {}
	points['P'] = 100
	points['N'] = 320
	points['B'] = 330
	points['R'] = 500
	points['Q'] = 900
	points['K'] = 20000
	white = 0
	black = 0
	board = str(board)
	count = 0
	for piece in board.strip():
		if piece.isupper():
			temp = position_points[piece]
			white = white + points[piece] + temp[count]
			count = count + 1
		elif piece.islower():
			temp = position_points[piece.upper()]
			black = black + points[piece.upper()] - position_points[piece.upper()][count]
			count = count + 1
		elif piece == '.':
			count = count + 1
	return (white,black)

def best_move(board, alpha, beta, depth):
	if board.is_game_over():
		result = board.result()
		if (board.turn and result == '1-0') or ((not board.turn) and result == '0-1'):
			return (25000,0)
		elif (board.turn and result == '0-1') or ((not board.turn) and result == '1-0'):
			return (-25000,0)
		else:
			return 0
	if depth == 0:
		vals = eval_state(board)
		if board.turn:
			return (vals[0],0)
		else:
			return (vals[1],0)
	v = -float('inf')
	best = ""
	for move in board.legal_moves:
		board.push(move)
		v = max(v,worst_move(board,alpha,beta,depth-1)[0])
		if v >= beta:
			best = move
			board.pop()
			return (v,best)
		if alpha < v:
			best = move
			alpha = v
		board.pop()

	return (v,best)

def worst_move(board, alpha, beta, depth):
	if board.is_game_over():
		result = board.result()
		if (board.turn and result == '1-0') or ((not board.turn) and result == '0-1'):
			return (-25000,0)
		elif (board.turn and result == '0-1') or ((not board.turn) and result == '1-0'):
			return (25000,0)
		else:
			return 0
	if depth == 0:
		vals = eval_state(board)
		if board.turn:
			return (-vals[0],0)
		else:
			return (-vals[1],0)
	v = float('inf')
	best = ""
	for move in board.legal_moves:
		board.push(move)
		v = min(v,best_move(board,alpha,beta,depth-1)[0])
		if v <= alpha:
			best = move
			board.pop()
			return (v,best)
		if beta > v:
			best = move
			beta = v
		board.pop()
	return (v,best)


print "------------------ TeChess v0.1 ------------------"
print "What do you choose - Black or White?"
player = raw_input()
if player == 'Black' or player == 'White':
	print 'Welcome....Waking up TeChess'
else:
	print 'Invalid option - Enter either Black or White'
	exit()
board = chess.Board()
print board
while(board.is_game_over() is False):
	if (board.turn == True and player == 'White') or (board.turn == False and player == 'Black'):
		print "Enter your move in UCI format"
		pmove = raw_input()
		if not chess.Move.from_uci(pmove) in set(board.legal_moves):
			print "Invalid move. Enter again"
		else:
			board.push(chess.Move.from_uci(pmove))
	else:
		alpha = -float("inf")
		beta = float("inf")
		board.push(best_move(board,alpha,beta,5)[1])	
	print str(board) + '\n'
	if board.is_game_over() and ((board.turn == True and player == 'White') or (board.turn == False and player == 'Black')):
		print "You lose.... :("
	elif board.is_game_over():
		print "Yayyy you win :)"
