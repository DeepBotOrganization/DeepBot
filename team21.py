import copy
import time

class Player21:

	def __init__(self):
		"""This is This """	

	def hueristic(self, x, y, board_status):
		
		if self.player == 'x':
			# row or coloumn
			for i in range(4):
				score = 0
				for j in range(4):
					if board_status[x+i][y+j] != 'o':
						if board_status[x+i][y+j] == 'x':
							score += 1
					else:
						score += -5
				
			score *= 2

			# left diagnol
			for i in range(4):
				if board_status[x+i][y+i] != 'o':
					if board_status[x+i][y+i] == 'x':
						score += 1
				else:
					score += -5
			# right diagnol
			for i in range(3,-1,-1):
				if board_status[x+i][y+i] != 'o':
					if board_status[x+i][y+i] == 'x':
						score += 1
				else:
					score += -5

		else:
			# row coloumn
			for i in range(4):
				score = 0
				for j in range(4):
					if board_status[x+i][y+j] != 'x':
						if board_status[x+i][y+j] == 'o':
							score += 1
					else:
						score += -5
				
			score *= 2
			
			# left diagnol
			for i in range(4):
				if board_status[x+i][y+i] != 'x':
					if board_status[x+i][y+i] == 'o':
						score += 1
				else:
					score += -5
			# right diagnol
			for i in range(3,-1,-1):
				if board_status[x+i][y+i] != 'x':
					if board_status[x+i][y+i] == 'o':
						score += 1
				else:
					score += -5

		return score			

	def minmax(self, old_move, valid_cells, board, depth, player, alpha, beta):
		
		if depth == 5:
			return (self.board_hueristic(board.board_status), old_move[0], old_move[1])

		if len(valid_cells) == 0:
			return (-2, -1, -1)
		
		temp_block_status = copy.deepcopy(board.block_status)
		temp_board_status = copy.deepcopy(board.board_status)

		x = 0
		y = 0

		for cell in valid_cells:
			i = cell[0]
			j = cell[1]
			
			board.update(old_move,(i,j),player)			

			if board.block_status[i/4][j/4] == 'd':
				board.board_status[i][j] = '-'
				board.block_status = temp_block_status
				board.board_status = temp_board_status
				score = 0
				x = i;
				y = j;
				# print "player", player, "has chosen ", i,j,"which has score",score
				return (score, i, j)


			if player == 'x':

				state = board.find_terminal_state()
				score = -100000

				# if board is won
				if state[1] == 'WON':
					if state[0] == 'x':
						board.block_status = temp_block_status
						board.board_status = temp_board_status
						score = 16
						x = i;
						y = j;

						# print "player", player, "has chosen ", i,j,"which has score",score
						return (score,i,j)

				#if block is won
				if board.block_status[i/4][j/4] == 'x':
					board.block_status = temp_block_status
					board.board_status = temp_board_status
					score = 1
					x = i;
					y = j;
					
					# print "player", player, "has chosen ", i,j,"which has score",score
					return (score, i, j)

				value = self.minmax((i, j), board.find_valid_move_cells((i, j)), board, depth+1, 'o', alpha, beta)
				alpha = max(value[0],alpha)

				if value[0] > score:
					x = i;
					y = j;
					score = value[0]
			
				if alpha > beta:
					break
			else:
				state = board.find_terminal_state()
				score = 100000

				if state[1] == 'WON':
					if state[0] == 'o':
						board.block_status = temp_block_status
						board.board_status = temp_board_status
						score = -16
						x = i;
						y = j;
						# print "player", player, "has chosen ", i,j,"which has score",score
						return (score,i,j)

				if board.block_status[i/4][j/4] == 'o':
					board.block_status = temp_block_status
					board.board_status = temp_board_status
					score = -1
					x = i;
					y = j;					
					# print "player", player, "has chosen ", i,j,"which has score",score
					return (score, i, j)

				value = self.minmax( (i, j), board.find_valid_move_cells((i, j)), board, depth+1, 'x', alpha, beta)
				beta = min(value[0], beta)
				
				if value[0] < score :
					x = i;
					y = j;
					score = value[0]
				
				if alpha > beta:
					break

			board.block_status = temp_block_status
			board.board_status = temp_board_status

		# print "player", player, "has chosen ", x,y,"which has score",score
		return (score,x,y)

	def move(self, board, old_move, flag):
		# time.sleep(5)
		self.board = copy.deepcopy(board)
		self.player = flag
		valid_cells = board.find_valid_move_cells(old_move)
		tuplex = self.minmax(old_move, valid_cells, self.board, 0, flag, -100000, 100000)
		print tuplex
		return (tuplex[1],tuplex[2])

	def board_hueristic(self, board_status):

		score = 0
		# board heuristic
		for i in range(4):
			for j in range(4):
				score += self.hueristic(4*i, 4*j, board_status)


		score *= 2
		#left diagnol
		for i in range(4):
			score += self.hueristic(4*i, 4*i, board_status)
		#right diagnol
		for i in range(3,-1,-1):
			score += self.hueristic(4*i, 4*i, board_status)

		return score
