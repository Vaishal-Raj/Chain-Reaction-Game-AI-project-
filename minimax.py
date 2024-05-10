from structure import *

def bestn(board,n=10):
	conf = {}
	for pos in [(x,y) for x in range(board.m) for y in range(board.n)]:
		if board.new_move == sgn(board[pos]) or 0 == sgn(board[pos]): 
			conf[pos] = score(move(board,pos),board.new_move)
			#Return just the winning position in case you find one
			if conf[pos]==10000:
				return [pos]
	return sorted(conf, key=conf.get, reverse=True)[:n]

def minimax(board,depth=3,breadth=3):
	best_moves = bestn(board,n=breadth)
	best_pos, best_val = (best_moves[0], score(move(board,best_moves[0]),board.new_move))
	if depth == 1:
		return best_pos, best_val
	for b_new_pos in bestn(board):
		b_new = move(board,b_new_pos)
		val = minimax(b_new, depth=depth-1)[1]
		if val > best_val:
			best_val = val
			best_pos = b_new_pos
	return best_pos, best_val

def minmax(board, depth=3, breadth=5):
    is_maximizing = True if depth % 2 == 0 else False

    if depth == 0:
        return None, score(board, board.new_move)

    best_moves = bestn(board, n=breadth)
    best_score = float('-inf') if is_maximizing else float('inf')
    best_pos = None

    for b_new_pos in best_moves:
        b_new = move(board, b_new_pos)
        _, score_val = minimax(b_new, depth=depth-1)
        
        if (is_maximizing and score_val > best_score) or (not is_maximizing and score_val < best_score):
            best_score = score_val
            best_pos = b_new_pos

    return best_pos, best_score

def alpha_beta(board, depth=3, alpha=float('-inf'), beta=float('inf')):
    def max_value(board, depth, alpha, beta):
        if depth == 0:
            return score(board, board.new_move)

        value = float('-inf')
        for mv in valid_moves(board):
            new_board = move(board, mv)
            value = max(value, min_value(new_board, depth-1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return value

    def min_value(board, depth, alpha, beta):
        if depth == 0:
            return score(board, board.new_move)

        value = float('inf')
        for mv in valid_moves(board):
            new_board = move(board, mv)
            value = min(value, max_value(new_board, depth-1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff
        return value

    best_move = None
    best_val = float('-inf')
    for mv in valid_moves(board):
        new_board = move(board, mv)
        value = min_value(new_board, depth-1, alpha, beta)
        if value > best_val:
            best_val = value
            best_move = mv
        alpha = max(alpha, value)
        if alpha >= beta:
            break  # Beta cutoff

    return best_move, best_val

def valid_moves(board):
    return [(x, y) for x in range(board.m) for y in range(board.n)
            if board.new_move == sgn(board[(x, y)]) or 0 == sgn(board[(x, y)])]

