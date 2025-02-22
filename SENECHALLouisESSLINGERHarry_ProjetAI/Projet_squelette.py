import tkinter as tk
import numpy as np
from tkinter import ttk
from threading import Thread
from queue import Queue
from alphabeta import alpha_beta_decision, winner_value, draw_value
from alphabeta_basic import alpha_beta_decision_basic

disk_color = ['white', 'red', 'orange']
disks = list()

player_type = ['human']
for level in range(42):
    player_type.append('AI: alpha-beta level '+str(level+1))

for level in range(42):
    player_type.append('AI: alpha-beta mock lvl '+str(level+1))

class Board:
    grid = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

    def eval(self, player):
        if self.check_victory():
            return winner_value
        return self.calculate_threats(player)

    def mock_eval(self, player):
        if self.check_victory():
            return winner_value
        return draw_value

    def calculate_threats(self, player):
        threat_score = 0

        # Vérification des alignements horizontaux possibles
        for row in range(6):
            for col in range(4):  # Vérifier les fenêtres de 4 colonnes
                window = self.grid[col:col + 4, row]
                if self.is_alignment_possible(window, player):
                    threat_score += self.evaluate_window(window, player)

        # Vérification des alignements verticaux possibles
        for col in range(7):
            for row in range(3):  # Vérifier les fenêtres de 4 lignes
                window = self.grid[col, row:row + 4]
                if self.is_alignment_possible(window, player):
                    threat_score += self.evaluate_window(window, player)

        # Vérification des alignements diagonaux possibles (de gauche à droite)
        for col in range(4):
            for row in range(3):
                window = [self.grid[col + i][row + i] for i in range(4)]
                if self.is_alignment_possible(window, player):
                    threat_score += self.evaluate_window(window, player)

        # Vérification des alignements diagonaux possibles (de droite à gauche)
        for col in range(4):
            for row in range(3, 6):
                window = [self.grid[col + i][row - i] for i in range(4)]
                if self.is_alignment_possible(window, player):
                    threat_score += self.evaluate_window(window, player)

        return threat_score

    def evaluate_window(self, window, player):
        score = 0
        opponent = (player % 2) + 1

        player_count = np.count_nonzero(window == player)
        empty_count = np.count_nonzero(window == 0)

        if player_count == 3 and empty_count == 1:
            score += 250
        elif player_count == 2 and empty_count == 2:
            score += 50

        return score

    def is_alignment_possible(self, window, player):
        opponent_count = np.count_nonzero(window == (player % 2) + 1)  # Jetons adverses

        # Un alignement est possible si :
        # - Il y a au maximum 1 jeton adverse.
        # - Les cases vides dans la fenêtre sont accessibles.
        if opponent_count > 1:
            return False

        for idx, cell in enumerate(window):
            if cell == 0:  # Vérifier la gravité pour les cases vides
                # Trouver la position (colonne et ligne) dans la grille
                col = idx
                row = np.where(window == cell)[0][0]
                # Si une case vide n'est pas en bas ou supportée, ce n'est pas un alignement possible
                if row > 0 and self.grid[col][row - 1] == 0:
                    return False

        return True

    def copy(self):
        new_board = Board()
        new_board.grid = np.array(self.grid, copy=True)
        return new_board

    def reinit(self):
        self.grid.fill(0)
        for i in range(7):
            for j in range(6):
                canvas1.itemconfig(disks[i][j], fill=disk_color[0])


    def get_possible_moves(self):
        possible_moves = list()
        if self.grid[3][5] == 0:
            possible_moves.append(3)
        for shift_from_center in range(1, 4):
            if self.grid[3 + shift_from_center][5] == 0:
                possible_moves.append(3 + shift_from_center)
            if self.grid[3 - shift_from_center][5] == 0:
                possible_moves.append(3 - shift_from_center)
        return possible_moves

    def add_disk(self, column, player, update_display=True):
        for j in range(6):
            if self.grid[column][j] == 0:
                break
        self.grid[column][j] = player
        if update_display:
            canvas1.itemconfig(disks[column][j], fill=disk_color[player])

    def column_filled(self, column):
        return self.grid[column][5] != 0

    def check_victory(self):
        # Horizontal alignment check
        for line in range(6):
            for horizontal_shift in range(4):
                if self.grid[horizontal_shift][line] == self.grid[horizontal_shift + 1][line] == self.grid[horizontal_shift + 2][line] == self.grid[horizontal_shift + 3][line] != 0:
                    return True
        # Vertical alignment check
        for column in range(7):
            for vertical_shift in range(3):
                if self.grid[column][vertical_shift] == self.grid[column][vertical_shift + 1] == \
                        self.grid[column][vertical_shift + 2] == self.grid[column][vertical_shift + 3] != 0:
                    return True
        # Diagonal alignment check
        for horizontal_shift in range(4):
            for vertical_shift in range(3):
                if self.grid[horizontal_shift][vertical_shift] == self.grid[horizontal_shift + 1][vertical_shift + 1] ==\
                        self.grid[horizontal_shift + 2][vertical_shift + 2] == self.grid[horizontal_shift + 3][vertical_shift + 3] != 0:
                    return True
                elif self.grid[horizontal_shift][5 - vertical_shift] == self.grid[horizontal_shift + 1][4 - vertical_shift] ==\
                        self.grid[horizontal_shift + 2][3 - vertical_shift] == self.grid[horizontal_shift + 3][2 - vertical_shift] != 0:
                    return True
        return False


class Connect4:

    def __init__(self):
        self.board = Board()
        self.human_turn = False
        self.turn = 1
        self.players = (0, 0)
        self.ai_move = Queue()

    def current_player(self):
        return 2 - (self.turn % 2)

    def launch(self):
        print("\nNew game :\n")
        self.board.reinit()
        self.turn = 0
        information['fg'] = 'black'
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        self.human_turn = False
        self.players = (combobox_player1.current(), combobox_player2.current())
        self.handle_turn()

    def move(self, column):
        if not self.board.column_filled(column):
            self.board.add_disk(column, self.current_player())
            self.handle_turn()

    def click(self, event):
        if self.human_turn:
            column = event.x // row_width
            self.move(column)

    def ai_turn(self, ai_level):
        Thread(target=alpha_beta_decision, args=(self.board, self.turn, ai_level, self.ai_move, self.current_player(),)).start()
        self.ai_wait_for_move()

    def ai_turn_basic(self, ai_level):
        Thread(target=alpha_beta_decision_basic, args=(self.board, self.turn, ai_level, self.ai_move, self.current_player(),)).start()
        self.ai_wait_for_move()

    def ai_wait_for_move(self):
        if not self.ai_move.empty():
            self.move(self.ai_move.get())
        else:
            window.after(100, self.ai_wait_for_move)

    def handle_turn(self):
        self.human_turn = False
        if self.board.check_victory():
            information['fg'] = 'red'
            information['text'] = "Player " + str(self.current_player()) + " wins !"
            return
        elif self.turn >= 42:
            information['fg'] = 'red'
            information['text'] = "This a draw !"
            return
        self.turn = self.turn + 1
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        if self.players[self.current_player() - 1] != 0:
            self.human_turn = False
            if self.players[self.current_player() - 1] < 43:
                self.ai_turn(self.players[self.current_player() - 1])
            else :
                self.ai_turn_basic(self.players[self.current_player() - 1] - 42)

        else:
            self.human_turn = True


game = Connect4()

# Graphical settings
width = 700
row_width = width // 7
row_height = row_width
height = row_width * 6
row_margin = row_height // 10

window = tk.Tk()
window.title("Connect 4")
canvas1 = tk.Canvas(window, bg="blue", width=width, height=height)

# Drawing the grid
for x in range(7):
    disks.append(list())
    for y in range(5, -1, -1):
        disks[x].append(canvas1.create_oval(row_margin + x * row_width, row_margin + y * row_height, (x + 1) * row_width - row_margin,
                            (y + 1) * row_height - row_margin, fill='white'))


canvas1.grid(row=0, column=0, columnspan=2)

information = tk.Label(window, text="")
information.grid(row=1, column=0, columnspan=2)

label_player1 = tk.Label(window, text="Player 1: ")
label_player1.grid(row=2, column=0)
combobox_player1 = ttk.Combobox(window, state='readonly', width = 30)
combobox_player1.grid(row=2, column=1)

label_player2 = tk.Label(window, text="Player 2: ")
label_player2.grid(row=3, column=0)
combobox_player2 = ttk.Combobox(window, state='readonly', width = 30)
combobox_player2.grid(row=3, column=1)

combobox_player1['values'] = player_type
combobox_player1.current(0)
combobox_player2['values'] = player_type
combobox_player2.current(6)

button2 = tk.Button(window, text='New game', command=game.launch)
button2.grid(row=4, column=0)

button = tk.Button(window, text='Quit', command=window.destroy)
button.grid(row=4, column=1)

# Mouse handling
canvas1.bind('<Button-1>', game.click)

window.mainloop()
