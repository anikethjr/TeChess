import chess
import random
import numpy as np
from multiprocessing import Process, Value, Array
thres = 0.0000000000000000000000000001
val={}

def piece_count(board):
	board = str(board)
	count = 0
	for piece in board.strip():
		if piece.isupper() or piece.islower():
			count = count + 1
	return count

def eval_state(board):
        z=board.zobrist_hash()
        if(val.has_key(z)):
                return val[z]
        else:  
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
                count = 0
                if(board.turn == True and board.is_check()):
                        white = white-300
                elif(board.turn == False and board.is_check()):
                        black = black-300
                if(board.has_castling_rights(True)):
                        white = white+100
                elif(board.has_castling_rights(False)):
                        black = black+100
                for squares in chess.SQUARES:
                        if(str(board.piece_at(squares)).isupper()):
                                if(board.is_attacked_by(False,squares)):
                                        black = black+10
                        elif(str(board.piece_at(squares)).islower()):
                                if(board.is_attacked_by(True,squares)):
                                        white = white+10
                board = str(board)               
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
                val[z] = (white,black)
                return (white,black)

def qsearch(board,alpha,beta):
	lower_bound = eval_state(board)
	if board.turn:
		lower_bound = lower_bound[0]
	else:
		lower_bound = lower_bound[1]
	if lower_bound >= beta:
		return beta
	if alpha < lower_bound:
		alpha = lower_bound
	for move in board.legal_moves:
		init_piececount = piece_count(board)
		board.push(move)
		final_piececount = piece_count(board)
		if init_piececount > final_piececount:
			score = qsearch(board,-beta,-alpha)
			score = -score
			if score >= beta:
				board.pop()
				return beta
			if score > alpha:
				alpha = score
		board.pop()
	return alpha

def PVS(board,alpha,beta,prob,lastmove):
	if board.is_game_over():
		result = board.result()
		if (board.turn and result == '1-0') or ((not board.turn) and result == '0-1'):
			return (25000,lastmove)
		elif (board.turn and result == '0-1') or ((not board.turn) and result == '1-0'):
			return (-25000,lastmove)
		else:
			return (0,lastmove)
	if prob<=thres:
		return (qsearch(board,alpha,beta),lastmove)
	best = ""
	#using fail soft with negamax:
	first_move = 1
	for move in board.legal_moves:
		board.push(move)
		if first_move == 1:
			(bestscore,tmp) = PVS(board,-beta, -alpha, prob*prob1,move)
			bestscore = -bestscore
			board.pop()
			if bestscore > alpha:
				if bestscore >= beta:
					return (bestscore,move)
				alpha = bestscore
				best = move
			first_move = 0
		else:
			(score,tmp) = PVS(board,-alpha-1, -alpha, prob*prob1,move)
			score = -score
			if score > alpha and score < beta:
				(score,tmp) = PVS(board,-beta, -alpha, prob*prob1,move)
				score = -score
				if score > alpha:
					alpha = score
			board.pop()
			if score > bestscore:
				if score >= beta:
					return (score,move)
				bestscore = score
				best = move
	return (bestscore,best)

print "------------------ TeChess v0.1 ------------------"
print "What do you choose - Black or White?"
player = raw_input()
if player == 'Black' or player == 'White':
	print 'Welcome....Waking up TeChess'
else:
	print 'Invalid option - Enter either Black or White'
	exit()

board = chess.Board() #"7r/pppb1pkp/n7/8/4p2K/8/3p4/6r1 w KQkq - 0 4"
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
		x = PVS(board,alpha,beta,1,"")
		print x
		board.push(x[1])	
	print str(board) + '\n'
	if board.is_game_over() and ((board.turn == True and player == 'White') or (board.turn == False and player == 'Black')):
		print "You lose.... :("
	elif board.is_game_over():
		print "Yayyy you win :)"
