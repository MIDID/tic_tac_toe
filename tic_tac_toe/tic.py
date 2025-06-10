class UltimateTicTacToe:
    def __init__(self):
        # Initialize the main board and sub-boards
        self.main_board = [[' ' for _ in range(3)] for _ in range(3)]
        self.sub_boards = [[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.last_move = None  # Tracks the last move to determine the next sub-board

    def print_board(self):
        """Print the entire Ultimate Tic-Tac-Toe board."""
        for i in range(3):
            for k in range(3):
                row = []
                for j in range(3):
                    row.append('|'.join(self.sub_boards[i][j][k * 3:(k + 1) * 3]))
                print(' || '.join(row))
            if i < 2:
                print('=' * 29)

    def is_sub_board_won(self, sub_board):
        """Check if a sub-board is won by a player."""
        # Check rows
        for row in sub_board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        # Check columns
        for col in range(3):
            if sub_board[0][col] == sub_board[1][col] == sub_board[2][col] != ' ':
                return sub_board[0][col]
        # Check diagonals
        if sub_board[0][0] == sub_board[1][1] == sub_board[2][2] != ' ':
            return sub_board[0][0]
        if sub_board[0][2] == sub_board[1][1] == sub_board[2][0] != ' ':
            return sub_board[0][2]
        return None

    def is_main_board_won(self):
        """Check if the main board is won by a player."""
        return self.is_sub_board_won(self.main_board)

    def is_sub_board_full(self, sub_board):
        """Check if a sub-board is full."""
        for row in sub_board:
            if ' ' in row:
                return False
        return True

    def is_game_over(self):
        """Check if the game is over (either won or drawn)."""
        if self.is_main_board_won():
            return True
        for i in range(3):
            for j in range(3):
                if not self.is_sub_board_won(self.sub_boards[i][j]) and not self.is_sub_board_full(self.sub_boards[i][j]):
                    return False
        return True

    def make_move(self, main_row, main_col, sub_row, sub_col):
        """Make a move on the board."""
        if self.main_board[main_row][main_col] != ' ':
            print("This sub-board is already won. Choose another.")
            return False
        if self.sub_boards[main_row][main_col][sub_row][sub_col] != ' ':
            print("This cell is already occupied. Choose another.")
            return False
        if self.last_move and (main_row != self.last_move[0] or main_col != self.last_move[1]):
            print(f"You must play in sub-board ({self.last_move[0]}, {self.last_move[1]}).")
            return False

        # Make the move
        self.sub_boards[main_row][main_col][sub_row][sub_col] = self.current_player

        # Check if the sub-board is won
        if self.is_sub_board_won(self.sub_boards[main_row][main_col]):
            self.main_board[main_row][main_col] = self.current_player

        # Update the last move
        self.last_move = (sub_row, sub_col)

        # Switch players
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def play(self):
        """Main game loop."""
        while not self.is_game_over():
            self.print_board()
            print(f"Player {self.current_player}'s turn.")

            # Get input for main board and sub-board
            try:
                main_row, main_col = map(int, input("Enter main board row and column (0-2): ").split())
                sub_row, sub_col = map(int, input("Enter sub-board row and column (0-2): ").split())
            except ValueError:
                print("Invalid input. Please enter numbers between 0 and 2.")
                continue

            # Validate and make the move
            if not (0 <= main_row <= 2 and 0 <= main_col <= 2 and 0 <= sub_row <= 2 and 0 <= sub_col <= 2):
                print("Invalid input. Numbers must be between 0 and 2.")
                continue
            if not self.make_move(main_row, main_col, sub_row, sub_col):
                continue

        # Game over
        self.print_board()
        winner = self.is_main_board_won()
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a draw!")


# Run the game
if __name__ == "__main__":
    game = UltimateTicTacToe()
    game.play()