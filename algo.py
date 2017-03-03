"""
	update board_status 
	for each block in board
		if block is won by 'x'
			fill the entire block by 'x'
		elif block is won by 'o'
			fill the entire block by 'o'
		else
			do not change anything

	minimax

	keep range of valid cells
	xl to xr
	yl to yr

	if present block is already filled
	xl = 0 xr = 15 yl = 0 yr = 15

	if there is no empty block in the range (xl,yl) to (xr,yr)
		return board heuristic
	--------------------------------------------------------------------------------
	HEURISTIC FUNCTION

	board heuristic
	if entire board is won by 'x'
		heuristic = 100000
	else
		heuristic = -100000

	If random value chosen in the range(0,9) is less than 3
		H = 
			3 2 2 3
		    2 3 3 2
		    2 3 3 2
		    3 2 2 3

		cell heuristic
			if cell is filled
				value[cell] = H[cell]
			else
				value[cell] = 0.5
				
		row/column heuristic in a block 
			if there is atleast one 'x' and atleast one 'o'
				row/column/diagonal heuristic = 0
			else 
				
				if there is atleast one x
					row/column/diagonal heuristic = value[cell]*value[cell+1]*value[cell+2]*value[cell+3] (here value[cell] is cell heuristic)
				else
					row/column/diagonal heuristic = -1*value[cell]*value[cell+1]*value[cell+2]*value[cell+3]
		
		block heuristic
			sum of heuristics of all rows and all columns and all diagonals	

		block_status heuristic
			It is block heuristic of block_status
		
		board heuristic
			sum of heuristics of all blocks + 5 * heuristic of block_status
	

	If random value chosen in the range(0,9) is greater than 3

		block heuristic
			if block is won by 'x'
				block heuristic = 20
			elif block is won by 'o' 
				block heuristic = -20

		row/column/diagonal heuristic
			if a row/column/diagonal has two 'x' s 
				row/column/diagonal heuristic = 2
			elif a row/column/diagonal has three 'x' s 
				row/column/diagonal heuristic = 5
			else
				row/column/diagonal heuristic = 0

		block heuristic
			sum of all row heuristics and column heuristics and diagonal heuristics

		board heuristic
			sum of all block heuristics and block_status heuristic calculated in above fashion
	---------------------------------------------------------------------------------
	
	In minimax while using board.update function if that block can be won by update then fill all cells in that block
	
"""