import tkinter as tk

# O'yin oynasi sozlamalari
CELL_SIZE = 60
ROWS, COLS = 8, 8
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

class CheckersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Shashka o'yini")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()

        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = "X"  # O'yin navbati ("X" yoki "O")
        self.selected_piece = None
        self.valid_moves = []

        self.draw_board()
        self.place_pieces()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        """Shashka taxtasini chizadi."""
        for row in range(ROWS):
            for col in range(COLS):
                color = "white" if (row + col) % 2 == 0 else "gray"
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def place_pieces(self):
        """Donalarni boshlang'ich holatda joylashtiradi."""
        for row in range(ROWS):
            for col in range(COLS):
                if row < 3 and (row + col) % 2 != 0:
                    self.board[row][col] = "O"
                elif row > 4 and (row + col) % 2 != 0:
                    self.board[row][col] = "X"

        self.update_board()

    def update_board(self):
        """Taxtani yangilaydi va donalarni qayta chizadi."""
        self.canvas.delete("piece")
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    x1 = col * CELL_SIZE + CELL_SIZE // 2
                    y1 = row * CELL_SIZE + CELL_SIZE // 2
                    color = "red" if piece == "X" else "blue"
                    self.canvas.create_oval(
                        x1 - 20, y1 - 20, x1 + 20, y1 + 20, fill=color, tags="piece"
                    )

    def handle_click(self, event):
        """O'yinchi bosgan joyni qayta ishlaydi."""
        col, row = event.x // CELL_SIZE, event.y // CELL_SIZE
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, (row, col))
                self.switch_turn()
            self.selected_piece = None
            self.valid_moves = []
            self.update_board()
        elif self.board[row][col] == self.turn:
            self.selected_piece = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            self.highlight_moves()

    def move_piece(self, from_pos, to_pos):
        """Dona yurishini amalga oshiradi."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None

        # Agar raqib donasi ustidan sakrasa, uni o'chiradi
        if abs(to_row - from_row) == 2:
            middle_row = (from_row + to_row) // 2
            middle_col = (from_col + to_col) // 2
            self.board[middle_row][middle_col] = None

    def get_valid_moves(self, row, col):
        """Donaning yurishi mumkin bo'lgan joylarni qaytaradi."""
        moves = []
        direction = -1 if self.board[row][col] == "X" else 1
        for dr, dc in [(direction, -1), (direction, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and not self.board[new_row][new_col]:
                moves.append((new_row, new_col))
            elif (
                0 <= new_row + dr < ROWS
                and 0 <= new_col + dc < COLS
                and self.board[new_row][new_col] not in (None, self.turn)
                and not self.board[new_row + dr][new_col + dc]
            ):
                moves.append((new_row + dr, new_col + dc))
        return moves

    def highlight_moves(self):
        """Donaning yurishi mumkin bo'lgan joylarni ta'kidlaydi."""
        self.canvas.delete("highlight")
        for row, col in self.valid_moves:
            x1 = col * CELL_SIZE + CELL_SIZE // 2
            y1 = row * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_oval(
                x1 - 10, y1 - 10, x1 + 10, y1 + 10, outline="yellow", width=2, tags="highlight"
            )

    def switch_turn(self):
        """O'yin navbatini almashtiradi."""
        self.turn = "O" if self.turn == "X" else "X"


if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()
