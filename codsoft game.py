import tkinter as tk
import random
from tkinter import messagebox

class RockPaperScissorsGame:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")
        master.geometry("500x450") 
        master.resizable(False, False) 
        master.config(bg="#f0f0f0") 

        self.user_score = 0
        self.computer_score = 0

        
        self.title_label = tk.Label(master, text="Rock, Paper, Scissors!", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333333")
        self.title_label.pack(pady=20)

        
        self.score_frame = tk.Frame(master, bg="#f0f0f0")
        self.score_frame.pack(pady=10)

        self.user_score_label = tk.Label(self.score_frame, text=f"Your Score: {self.user_score}", font=("Arial", 14), bg="#f0f0f0", fg="#007bff")
        self.user_score_label.grid(row=0, column=0, padx=20)

        self.computer_score_label = tk.Label(self.score_frame, text=f"Computer Score: {self.computer_score}", font=("Arial", 14), bg="#f0f0f0", fg="#dc3545")
        self.computer_score_label.grid(row=0, column=1, padx=20)

        
        self.message_label = tk.Label(master, text="Make your move!", font=("Arial", 16, "italic"), bg="#f0f0f0", fg="#555555")
        self.message_label.pack(pady=20)

        
        self.button_frame = tk.Frame(master, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        self.rock_button = tk.Button(self.button_frame, text="Rock", font=("Arial", 14, "bold"), width=10, height=2,
                                     bg="#28a745", fg="white", activebackground="#218838", command=lambda: self.play("rock"))
        self.rock_button.grid(row=0, column=0, padx=10)

        self.paper_button = tk.Button(self.button_frame, text="Paper", font=("Arial", 14, "bold"), width=10, height=2,
                                      bg="#ffc107", fg="black", activebackground="#e0a800", command=lambda: self.play("paper"))
        self.paper_button.grid(row=0, column=1, padx=10)

        self.scissors_button = tk.Button(self.button_frame, text="Scissors", font=("Arial", 14, "bold"), width=10, height=2,
                                        bg="#007bff", fg="white", activebackground="#0056b3", command=lambda: self.play("scissors"))
        self.scissors_button.grid(row=0, column=2, padx=10)

        
        self.reset_button = tk.Button(master, text="Reset Game", font=("Arial", 12),
                                     bg="#6c757d", fg="white", activebackground="#545b62", command=self.reset_game)
        self.reset_button.pack(pady=15)

    def play(self, user_choice):
        """
        Determines the game outcome based on user and computer choices.
        Updates scores and displays messages.
        """
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)

        result_message = ""
        winner = None 

        if user_choice == computer_choice:
            result_message = f"It's a tie! Both chose {user_choice}."
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            self.user_score += 1
            result_message = f"You win! {user_choice.capitalize()} beats {computer_choice}."
            winner = 'user'
        else:
            self.computer_score += 1
            result_message = f"You lose! {computer_choice.capitalize()} beats {user_choice}."
            winner = 'computer'

        self.update_scores()
        self.message_label.config(text=result_message, fg=self.get_message_color(winner))

    def update_scores(self):
        """Updates the score labels on the GUI."""
        self.user_score_label.config(text=f"Your Score: {self.user_score}")
        self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")

    def get_message_color(self, winner):
        """Returns color based on winner."""
        if winner == 'user':
            return "#28a745" 
        elif winner == 'computer':
            return "#dc3545" 
        else:
            return "#555555" 

    def reset_game(self):
        """Resets scores and game messages."""
        self.user_score = 0
        self.computer_score = 0
        self.update_scores()
        self.message_label.config(text="Game Reset! Make your move!", fg="#555555")
        messagebox.showinfo("Game Reset", "The game has been reset!")


if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
