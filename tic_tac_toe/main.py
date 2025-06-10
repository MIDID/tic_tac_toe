import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.core.audio import SoundLoader  # Import SoundLoader for sound effects

# Set window size
Window.size = (400, 600)


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Title Label
        title_label = Label(
            text="Tic Tac Toe",
            font_size=40,
            color=(1, 0.5, 0, 1),  # Orange
            bold=True
        )
        self.layout.add_widget(title_label)

        # Spinner for mode selection
        self.spinner = Spinner(
            text="Select Mode",
            values=("Easy", "Normal", "Hard", "2 Player"),
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 1, 1),  # Light blue
            color=(1, 1, 1, 1)  # White text
        )
        self.layout.add_widget(self.spinner)

        # Start Game Button
        start_button = Button(
            text="Start Game",
            size_hint=(1, 0.2),
            background_color=(0, 0.7, 0, 1),  # Green
            color=(1, 1, 1, 1)  # White text
        )
        start_button.bind(on_press=self.start_game)
        self.layout.add_widget(start_button)

        self.add_widget(self.layout)

    def start_game(self, instance):
        self.manager.current = 'game'
        self.manager.get_screen('game').initialize_game(self.spinner.text)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Status Label
        self.status_label = Label(
            text="Game in Progress",
            font_size=30,
            color=(0, 0, 0, 1),  # Black
            bold=True
        )
        self.layout.add_widget(self.status_label)

        # Game Board
        self.game_board = TicTacToeGame()
        self.layout.add_widget(self.game_board)

        # Reset Button
        reset_button = Button(
            text="Reset Game",
            size_hint=(1, 0.2),
            background_color=(0.8, 0, 0, 1),  # Red
            color=(1, 1, 1, 1)  # White text
        )
        reset_button.bind(on_press=self.reset_game)
        self.layout.add_widget(reset_button)

        # Back Button
        back_button = Button(
            text="Back to Start",
            size_hint=(1, 0.2),
            background_color=(0.5, 0.5, 0.5, 1),  # Gray
            color=(1, 1, 1, 1)  # White text
        )
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def initialize_game(self, mode):
        self.game_board.clear_widgets()
        self.game_board.__init__(mode=mode)
        self.layout.clear_widgets()
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.game_board)
        reset_button = Button(
            text="Reset Game",
            size_hint=(1, 0.2),
            background_color=(0.8, 0, 0, 1),  # Red
            color=(1, 1, 1, 1)  # White text
        )
        reset_button.bind(on_press=self.reset_game)
        self.layout.add_widget(reset_button)

        # Add Back Button again after reset
        back_button = Button(
            text="Back to Start",
            size_hint=(1, 0.2),
            background_color=(0.5, 0.5, 0.5, 1),  # Gray
            color=(1, 1, 1, 1)  # White text
        )
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

    def reset_game(self, instance):
        self.game_board.clear_widgets()
        self.game_board.__init__(mode=self.game_board.mode)

    def go_back(self, instance):
        """ Switch back to the Start Screen """
        self.manager.current = 'start'


class TicTacToeGame(GridLayout):
    def __init__(self, mode="2 Player", **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.mode = mode
        self.move_order = []  # Track the order of moves

        # Load sound effects
        self.click_sound = SoundLoader.load('click.wav')  # Sound for button clicks
        self.win_sound = SoundLoader.load('win.wav')  # Sound for winning
        self.tie_sound = SoundLoader.load('tie.wav')  # Sound for tie
        self.ai_sound = SoundLoader.load('ai_move.wav')  # Sound for AI move

        # Define colors for the grid and players
        self.grid_color = (0.9, 0.9, 0.9, 1)  # Light gray for grid
        self.x_color = (1, 0, 0, 1)  # Red for X
        self.o_color = (0, 0, 1, 1)  # Blue for O

        for i in range(9):
            btn = Button(
                text="",
                font_size=32,
                background_color=self.grid_color,  # Light gray for grid
                color=(0, 0, 0, 1)  # Black text (initially)
            )
            btn.bind(on_press=self.make_move)
            self.buttons.append(btn)
            self.add_widget(btn)

    def make_move(self, instance):
        index = self.buttons.index(instance)
        if self.board[index] == "":
            # Play click sound
            if self.click_sound:
                self.click_sound.play()

            # Update the board and UI
            self.board[index] = self.current_player
            instance.text = self.current_player

            # Assign colors to X and O
            if self.current_player == "X":
                instance.color = self.x_color  # Red for X
            else:
                instance.color = self.o_color  # Blue for O

            # Animate the button
            anim = Animation(background_color=(0.5, 0.5, 1, 1), duration=0.2) + \
                   Animation(background_color=self.grid_color, duration=0.2)
            anim.start(instance)

            if self.check_winner():
                self.show_winner(self.current_player)
                return

            if self.check_tie():
                self.handle_tie()
                return

            # Switch players
            self.current_player = "O" if self.current_player == "X" else "X"

            # AI should play immediately after the player's move
            if self.mode != "2 Player" and self.current_player == "O":
                Clock.schedule_once(lambda dt: self.ai_move(), 0.5)  # Slight delay for AI move

    def ai_move(self):
        """ AI makes a move based on the selected mode """
        if self.mode == "Easy":
            self.easy_ai()
        elif self.mode == "Normal":
            self.normal_ai()
        elif self.mode == "Hard":
            self.hard_ai()

        # Play AI move sound
        if self.ai_sound:
            self.ai_sound.play()

        # Check for winner or tie after AI move
        if self.check_winner():
            self.show_winner(self.current_player)
            return
        if self.check_tie():
            self.handle_tie()
            return

        # Switch back to the human player
        self.current_player = "X"

    def easy_ai(self):
        """ AI picks a random available cell """
        empty_cells = [i for i in range(9) if self.board[i] == ""]
        if empty_cells:
            index = random.choice(empty_cells)
            self.update_board(index, "O")

    def normal_ai(self):
        """ AI blocks the player or plays randomly """
        move = self.find_winning_move("O")  # Check if AI can win
        if move is not None:
            self.update_board(move, "O")
            return

        move = self.find_winning_move("X")  # Block player from winning
        if move is not None:
            self.update_board(move, "O")
            return

        self.easy_ai()  # Play randomly if no winning or blocking move

    def hard_ai(self):
        """ AI uses minimax algorithm for best move """
        best_score = -float("inf")
        best_move = None

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(False)
                self.board[i] = ""

                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.update_board(best_move, "O")

    def minimax(self, is_maximizing):
        """ Minimax algorithm to determine best AI move """
        winner = self.check_winner_return()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif "" not in self.board:
            return 0  # Draw

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    score = self.minimax(False)
                    self.board[i] = ""
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "X"
                    score = self.minimax(True)
                    self.board[i] = ""
                    best_score = min(best_score, score)
            return best_score

    def find_winning_move(self, player):
        """ Check if a player can win in the next move """
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for pattern in win_patterns:
            values = [self.board[i] for i in pattern]
            if values.count(player) == 2 and values.count("") == 1:
                return pattern[values.index("")]
        return None

    def update_board(self, index, player):
        """ Updates the board and UI """
        if self.board[index] == "":
            self.board[index] = player
            self.buttons[index].text = player

            # Assign colors to X and O
            if player == "X":
                self.buttons[index].color = self.x_color  # Red for X
            else:
                self.buttons[index].color = self.o_color  # Blue for O

            # Check for a winner immediately after move
            if self.check_winner():
                self.show_winner(player)
                return

    def check_winner(self):
        """ Check if there is a winner """
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] and self.board[pattern[0]] != "":
                return True
        return False

    def check_winner_return(self):
        """ Returns winner symbol (X or O) """
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] and self.board[pattern[0]] != "":
                return self.board[pattern[0]]
        return None

    def check_tie(self):
        """ Check if the game is in a tie state """
        return "" not in self.board and not self.check_winner()

    def handle_tie(self):
        """ Handle tie state by clearing the board and replaying moves """
        if self.tie_sound:
            self.tie_sound.play()
        self.clear_board()
        self.replay_moves()

    def clear_board(self):
        """ Clear the board and reset the buttons """
        for i in range(9):
            self.board[i] = ""
            self.buttons[i].text = ""
            self.buttons[i].color = (0, 0, 0, 1)  # Reset to black text

    def replay_moves(self):
        """ Replay the moves in the order they were made """
        # Reset the current player to the starting player
        self.current_player = "X"

        # Replay all moves
        for move in self.move_order:
            self.update_board(move, self.current_player)
            self.current_player = "O" if self.current_player == "X" else "X"

        # Clear the move order to avoid infinite loops
        self.move_order.clear()

    def show_winner(self, winner):
        """ Displays the winner with animation """
        if self.win_sound:
            self.win_sound.play()

        self.clear_widgets()
        label = Label(
            text=f"Player {winner} Jayichuuu!",
            font_size=40,
            color=(0, 1, 0, 1)  # Green
        )
        self.add_widget(label)

        # Animate the label
        anim = Animation(font_size=50, duration=0.5) + \
               Animation(font_size=40, duration=0.5)
        anim.repeat = True
        anim.start(label)


class TicTacToeApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.start_screen = StartScreen(name='start')
        self.screen_manager.add_widget(self.start_screen)

        self.game_screen = GameScreen(name='game')
        self.screen_manager.add_widget(self.game_screen)

        return self.screen_manager


if __name__ == "__main__":
    TicTacToeApp().run()