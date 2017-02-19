import time
class Player21:

	def __init__(self):
		"""This is This """

	def minmax(self, old_move, valid_cells, board, depth, player):

		if len(valid_cells) == 0:
			return (-2, -1, -1)
		
		Block_Status = board.block_status

		x = 0
		y = 0

		for cell in valid_cells:
			i = cell[0]
			j = cell[1]
			
			board.update(old_move,(i,j),player)			

			if board.block_status[i/4][j/4] == 'd':
				board.board_status[i][j] = '-'
				board.block_status = Block_Status
				return (0, i, j)


			if player == 'x':

				state = board.find_terminal_state()

				# if board is won
				if state[1] == 'WON':
					if state[0] == 'x':
						board.board_status[i][j] = '-'
						board.block_status = Block_Status
						return (16,i,j)

				#if block is won
				if board.block_status[i/4][j/4] == 'x':
					board.board_status[i][j] = '-'
					board.block_status = Block_Status
					return (1, i, j)

				value = self.minmax((i, j), board.find_valid_move_cells((i, j)), board, depth+1, 'o')
				
				if value[0] > score:
					x = i
					y = j
				score = value[0]
			else:
				state = board.find_terminal_state()

				if state[1] == 'WON':
					if state[0] == 'o':
						board.board_status[i][j] = '-'
						board.block_status = Block_Status
						return (-16,i,j)

				if board.block_status[i/4][j/4] == 'o':
					board.board_status[i][j] = '-'
					board.block_status = Block_Status
					return (-1, i, j)

				value = self.minmax( (i, j), board.find_valid_move_cells((i, j)), board, depth+1, 'x')
				if value[0] < score :
					x = i
					y = j
				score = value[0]

			board.board_status[i][j] = '-'
			board.block_status = Block_Status
	
		return (score,x,y)

	def move(self, board, old_move, flag):
		time.sleep(5)
		valid_cells = board.find_valid_move_cells(old_move)
		tuplex = self.minmax(old_move, valid_cells, board, 0, flag)
		return (tuplex[0],tuplex[1])
