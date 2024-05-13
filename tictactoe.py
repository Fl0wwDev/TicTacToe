import tkinter as tk
import random
from tkinter import messagebox

# Fonction pour vérifier s'il y a un gagnant ou non
def check_winner(board):
    # Retourne 'X' si le joueur X a gagné, 'O' si le joueur O a gagné, ou 'tie' pour une égalité
    # Retourne None si le jeu n'est pas terminé
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != ' ':
            return row[0]

    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    if all([cell != ' ' for row in board for cell in row]):
        return 'tie'

    return None

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.game_mode = None  # 'pvp' for player vs player, 'pvc' for player vs computer
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.main_menu()

    def main_menu(self):
        # Détruire tous les widgets de la fenêtre actuelle
        for widget in self.root.winfo_children():
            widget.destroy()

        # Créer le menu principal
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)

        tk.Label(menu_frame, text="Tic-Tac-Toe", font=('Helvetica', 24)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(menu_frame, text="Joueur vs Joueur", font=('Helvetica', 14), command=self.start_pvp_game).grid(row=1, column=0, pady=5)
        tk.Button(menu_frame, text="Joueur vs Ordinateur", font=('Helvetica', 14), command=self.start_pvc_game).grid(row=2, column=0, pady=5)
        tk.Button(menu_frame, text="Règles", font=('Helvetica', 14), command=self.show_rules).grid(row=3, column=0, pady=5)


    def start_pvp_game(self):
        self.game_mode = 'pvp'
        self.setup_game()

    def start_pvc_game(self):
        self.game_mode = 'pvc'
        self.setup_game()

    def setup_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=' ', font=('Helvetica', 24), width=5, height=2,
                                                command=lambda row=i, col=j: self.button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.message_label = tk.Label(self.root, text="", font=('Helvetica', 18))
        self.message_label.grid(row=3, columnspan=3)

        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        if self.game_mode == 'pvc' and self.current_player == 'O':
            self.ai_move()
        else:
            self.message_label.config(text=f"Au tour de {self.current_player}")

    def show_rules(self):
        rules_text = ("Tic-Tac-Toe est un jeu pour deux joueurs, X et O, qui s'affrontent sur une grille de 3x3.\n\n"
                      "Le premier joueur à aligner trois de ses symboles horizontalement, verticalement ou en diagonale gagne la partie.\n\n"
                      "Si la grille est remplie sans qu'un joueur n'ait aligné trois symboles, la partie est déclarée nulle.")
        messagebox.showinfo("Règles du jeu", rules_text)

    def button_click(self, row, col):
        if self.game_mode == 'pvc' and self.current_player == 'O':
            messagebox.showerror("Tic-Tac-Toe", "Ce n'est pas votre tour.")
            return

        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            winner = check_winner(self.board)
            if winner:
                if winner == 'tie':
                    messagebox.showinfo("Tic-Tac-Toe", "Match nul !")
                else:
                    messagebox.showinfo("Tic-Tac-Toe", f"{winner} a gagné !")
                self.main_menu()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.game_mode == 'pvc' and self.current_player == 'O':
                    self.root.after(1000, self.ai_move)  # Appel de ai_move après un court délai
                    self.message_label.config(text="Tour de l'ordinateur")
                else:
                    self.message_label.config(text=f"Au tour de {self.current_player}")






    def ai_move(self):
        # Implémenter une logique d'IA pour l'ordinateur
        # Pour l'exemple, l'IA choisira une case vide au hasard
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O')
            winner = check_winner(self.board)
            if winner:
                if winner == 'tie':
                    messagebox.showinfo("Tic-Tac-Toe", "Match nul !")
                else:
                    messagebox.showinfo("Tic-Tac-Toe", f"{winner} a gagné !")
                self.main_menu()

    def play(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.play()
