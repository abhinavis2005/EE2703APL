
def check_row_column(grid):
    invalid_blocks = 0
    for row in grid:
        numbers = {number for number in row} #making a set
        if len(numbers) != 9:
            invalid_blocks +=1
    transpose_grid = [list(row) for row in zip(*sblk)]
    for row in transpose_grid:
        numbers = {number for number in row} #making a set
        if len(numbers) != 9:
            invalid_blocks +=1
    return invalid_blocks
def check_sub_grid(sub_grid):
    numbers = set()
    for row in sub_grid:
        numbers.update(num for num in row)
    if len(numbers) != 9:
        return 1
    else:
        return 0
def sudoku_check(grid):
    invalid_blocks = check_row_column(grid)
    

    for i in range(0,9, 3):
       for j in range(0,9,3):
            sub_grid = [subrow[j:j+3] for subrow in grid[i:i+3]]
            invalid_blocks += check_sub_grid(sub_grid)
    
    return invalid_blocks 

sblk = [
 [1, 2, 3, 4, 5, 6, 7, 8, 9],
 [4, 5, 6, 7, 8, 9, 1, 2, 3],
 [7, 8, 9, 1, 2, 3, 4, 5, 6],
 [2, 3, 4, 5, 6, 7, 8, 9, 1],
 [5, 6, 7, 8, 9, 1, 2, 3, 4],
 [8, 9, 1, 2, 3, 4, 5, 6, 7],
 [3, 4, 5, 6, 7, 8, 9, 1, 2],
 [6, 7, 8, 9, 1, 2, 3, 4, 5],
 [9, 1, 2, 3, 4, 5, 6, 7, 8]
]
print(sudoku_check(sblk)) 