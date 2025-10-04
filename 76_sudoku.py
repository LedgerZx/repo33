import random

def generate_sudoku():
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
            if board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                return False
        return True

    def solve_sudoku(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    board = [[0] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            num = random.randint(1, 9)
            while not is_valid(board, i, j, num):
                num = random.randint(1, 9)
            board[i][j] = num

    solve_sudoku(board)
    return board

def print_sudoku(board):
    for row in board:
        print(" ".join(str(num) for num in row))

def main():
    puzzle = generate_sudoku()
    print("Generated Sudoku Puzzle:")
    print_sudoku(puzzle)
    print("\nSolving the Puzzle:")
    solve_sudoku(puzzle)
    print_sudoku(puzzle)

if __name__ == "__main__":
    main()
