import copy
import time

class Player21:

	def __init__(self):
		"""This is This """	

	def cell_heuristic(self, i, j, status):
		H = [
				[3,2,2,3],
				[2,3,3,2],
				[2,3,3,2],
				[3,2,2,3]
			]
		
		if status[i][j] == 'x':
			return H[i-4*(i/4)][j-4*(j/4)]
		elif status[i][j] == 'o':
			return -H[i-4*(i/4)][j-4*(j/4)]
		else:
			return 0.5

	def row_heuristic(self, block, row_number, board_status):
		x = block[0]
		y = block[1]
		score = 1

		for i in range(0,4):
			score *= self.cell_heuristic(4*x+row_number, 4*y+i, board_status)

		return score	

	def column_heuristic(self, block, column_number, board_status):
		x = block[0]
		y = block[1]
		score = 1
		for i in range(0,4):
			score *= self.cell_heuristic(4*x+i, 4*y+column_number, board_status)
		return score

	def diagonals_heuristic(self, block, board_status):
		x = block[0]
		y = block[1]
		score = 1

		for i in range(0, 4):
			score *= self.cell_heuristic(4*x+i, 4*y+i, board_status)

		for i in range(3, -1, -1):
			score *= self.cell_heuristic(4*x+i, 4*y+i, board_status)

		return score

	def block_heuristic(self, block, board_status):
		score = 0

		for i in range(0, 4):
			score += self.row_heuristic(block, i, board_status)
			score += self.column_heuristic(block, i, board_status)

		score += self.diagonals_heuristic(block, board_status)

		return score

	def board_heuristic(self, board):
		state = board.find_terminal_state()
		if state[1] == 'WON':
			if state[0] == 'x':
				return (100000, old_move)
			if state[0] == 'o':
				return (-100000, old_move)

		score = 0

		for i in range(0, 4):
			for j in range(0, 4):
				score += self.block_heuristic((i,j), board.board_status)

		#block_status heuristic
		temp_score = 1
		for i in range(0,4):
			for j in range(0, 4):
				temp_score *= self.cell_heuristic(i, j, board.block_status) #block_status row
				temp_score *= self.cell_heuristic(j, i, board.block_status) #block_status column

		for i in range(0,4):
			temp_score *= self.cell_heuristic(i, i, board.block_status) #block_status row

		for i in range(3, -1, -1):
			temp_score *= self.cell_heuristic(i, i, board.block_status) #block_status row

		score += 5*temp_score

		return score	

	def minmax(self, old_move, board, depth, player, alpha, beta):
		
		valid_cells = board.find_valid_move_cells(old_move)

		if depth == 8 or time.time()-self.start_time >= 14:
			x = self.board_heuristic(board)
			return (x, old_move)

		# present block is won/made draw
		if len(valid_cells) == 0:
			for i in range(0, 16):
				for j in range(0, 16):
					if board.board_status[i][j] == '-':
						valid_cells.append((i,j))
		
		# all cells present in board are filled
		if len(valid_cells) == 0:
			state = board.find_terminal_state()
			if state[1] == 'WON':
				if state[0] == 'x':
					return (100000,old_move)
				else:
					return (-100000,old_move)
			return (0,old_move) #either board is won or is draw

		temp_block_status = copy.deepcopy(board.block_status)
		temp_board_status = copy.deepcopy(board.board_status)

		move = (0, 0)

		score = 0
		for cell in valid_cells:
			i = cell[0]
			j = cell[1]
			
			board.update(old_move,(i,j),player)
			
			#board is won by 'x' or 'o'
			state = board.find_terminal_state()
			if state[1] == 'WON':
				if state[0] == 'x':
					return (100000,(i,j))
				else:
					return (-100000,(i,j))

			#board is won by 'x' or 'o'
			if board.block_status[i/4][j/4] != '-':
				for c in valid_cells:
					i1 = cell[0]
					j1 = cell[1]
					board.board_status[i][j] = board.block_status[i/4][j/4] # fill all cell in that block with winning player
				board.block_status = temp_block_status
				board.board_status = temp_board_status
				return (self.board_heuristic(board),(i,j))
				# valid_cells = []

				# for i in range(0, 16):
				# 	for j in range(0, 16):
				# 		if board.board_status[i][j] == '-':
				# 			valid_cells.append((i,j))
				# continue

			if player == 'x':
				state = board.find_terminal_state()
				score = -1e15
				value = self.minmax((i, j), board, depth+1, 'o', alpha, beta)
				alpha = max(value[0],alpha)

				if value[0] > score:
					move = copy.deepcopy((i,j))
					score = value[0]
			
				if alpha > beta:
					break
			else:
				state = board.find_terminal_state()
				score = 1e15
				value = self.minmax( (i, j), board, depth+1, 'x', alpha, beta)
				beta = min(value[0], beta)
				
				if value[0] < score :
					move = copy.deepcopy((i,j))
					score = value[0]
				
				if alpha > beta:
					break

			board.block_status = temp_block_status
			board.board_status = temp_board_status
		return (score,move)

	def move(self, board, old_move, flag):
		player = flag
		if player == 'x':
			opponent_player = 'o'
		else:
			opponent_player = 'x'

		self.start_time = time.time()
		
		if board.board_status == [['-' for j in range(16)]for i in range(16)]:
			return(0, 0)

		board = copy.deepcopy(board)
		
   		for i in range(0,16):
   			for j in range(0,16):
   				if board.block_status[i/4][j/4] == player:
   					board.board_status[i][j] = player
   				elif board.block_status[i/4][j/4] == opponent_player:
   					board.board_status[i][j] = opponent_player
		
		
		new_move = self.minmax(old_move, board, 0, flag, -1e15, 1e15)
		print "NEW MOVE",new_move
		return (new_move[1][0],new_move[1][1])