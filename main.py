def create_board():
    """Create the initial 8x8 checkers board."""
    board = []
    for row in range(8):
        board.append([])
        for col in range(8):
            if (row + col) % 2 == 1:
                if row < 3:
                    board[row].append('X')  # Player X's pieces
                elif row > 4:
                    board[row].append('O')  # Player O's pieces
                else:
                    board[row].append('-')  # Empty space
            else:
                board[row].append(' ')  # Unplayable space
    return board

def print_board(board):
    """Display the board."""
    print("  0 1 2 3 4 5 6 7")
    for idx, row in enumerate(board):
        print(idx, ' '.join(row))

def is_valid_move(board, player, start, end):
    """Check if a move is valid."""
    sr, sc = start
    er, ec = end

    if not (0 <= sr < 8 and 0 <= sc < 8 and 0 <= er < 8 and 0 <= ec < 8):
        return False  # Out of bounds

    if board[sr][sc] != player or board[er][ec] != '-':
        return False  # Invalid piece or destination

    if abs(er - sr) == 1 and abs(ec - sc) == 1:  # Simple move
        return True

    if abs(er - sr) == 2 and abs(ec - sc) == 2:  # Capture move
        mid_r, mid_c = (sr + er) // 2, (sc + ec) // 2
        opponent = 'O' if player == 'X' else 'X'
        if board[mid_r][mid_c] == opponent:
            return True

    return False

def make_move(board, player, start, end):
    """Make a move on the board."""
    sr, sc = start
    er, ec = end
    board[sr][sc] = '-'
    board[er][ec] = player

    # Capture move
    if abs(er - sr) == 2:
        mid_r, mid_c = (sr + er) // 2, (sc + ec) // 2
        board[mid_r][mid_c] = '-'

def main():
    board = create_board()
    current_player = 'X'

    while True:
        print_board(board)
        print(f"{current_player}'s turn.")
        try:
            start = tuple(map(int, input("Enter the piece position to move (row col): ").split()))
            end = tuple(map(int, input("Enter the position to move to (row col): ").split()))

            if is_valid_move(board, current_player, start, end):
                make_move(board, current_player, start, end)
                current_player = 'O' if current_player == 'X' else 'X'
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Use row and column numbers.")

if __name__ == "__main__":
    main()
