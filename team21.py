
class Player21:

	def __init__(self):


	def move (self, board, old_move, flag):

		(x,y) = self.get_optimal_move(old_move[0]%4 * 4, old_move[1]%4 *4, board)


	def minmax (x, y, score, board, depth, player):

		if is_win(x, y, board):
			if player == 'x':
				return 10 
			else if player == 'o':
				return -10
			else
				return 0

		if is_full(x, y, board):
			return 0

		for i in range(x, x + 4):
			for j in range(y, y + 4):
				if board[i][j] == '-':
					board[i][j] = player
					if player == 'x':
						value = minmax(i, j, score, board, depth+1, 'o')
						score = max(score, value)
					else:
						value = minmax(i, j, score, board, depth+1, 'x')
						score = min(score,value)
		print score
		return score