import tkinter as tk
from tkinter import ttk, messagebox
from src.color import Color
from src.master_mind import select_colors, play
from src.game_enums import EXACT, PARTIAL, NO_MATCH, WON, LOST
import time

MAX_COLORS = 6
MAX_ATTEMPTS = 20 
ROW_HEIGHT = 25   

def mastermind_game():
    selected_colors = select_colors(seed=int(time.time()))  
    guess_vars = ['' for _ in range(MAX_COLORS)]  
    result_strips = []  
    attempts = 0  
    game_finished = False  

    def run():
        root = tk.Tk()
        root.title("Mastermind Game")

        total_rows_height = ROW_HEIGHT * MAX_ATTEMPTS
        window_height = min(total_rows_height + 1200, 1500)  
        window_width = max(1800, 1400)
        root.geometry(f"{window_width}x{window_height}")
        root.configure(bg="darkslategray")

        style = ttk.Style()
        style.theme_use('clam')  

        canvas = tk.Canvas(root, bg="darkslategray")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        scrollable_frame = tk.Frame(canvas, bg="darkslategray")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        root.bind_all("<MouseWheel>", lambda event: _on_mousewheel(event, canvas))

        feedback_label, guess_frame_inner, win_message_label, loss_message_frame = setup_ui(scrollable_frame, guess_vars, style)

        root.mainloop()
    
    def create_color_buttons(root, color_frame, guess_vars, guess_frame_inner, style):
        color_buttons = []
        for color in Color:
             style.configure(f"{color.name}.TButton", background=color.value, foreground="black")
             button = ttk.Button(color_frame, text=color.name, style=f"{color.name}.TButton",
                                 command=lambda c=color: set_guess_color(c, guess_vars, guess_frame_inner))
             button.pack(side=tk.LEFT, padx=2, pady=2)
             color_buttons.append(button)
        return color_buttons

    def set_guess_color(color, guess_vars, guess_frame_inner):
        if game_finished:
            return  
        for i in range(MAX_COLORS):
            if guess_vars[i] == '':
                guess_vars[i] = color
                break
        display_guess_color(guess_vars, guess_frame_inner)

    def display_guess_color(guess_vars, guess_frame_inner):
        for widget in guess_frame_inner.winfo_children():
            widget.destroy()

        for i in range(MAX_COLORS):
            color_label = tk.Label(guess_frame_inner, width=10, height=1, relief="solid")
            if guess_vars[i] == '':
                color_label.config(bg="white")
            else:
                color_label.config(bg=guess_vars[i].value)
            color_label.grid(row=0, column=i, padx=2, pady=2)

            clear_button = tk.Button(guess_frame_inner, text="X", command=lambda i=i: clear_guess(i, guess_vars, guess_frame_inner))
            clear_button.grid(row=1, column=i, padx=2, pady=2)

    def clear_guess(index, guess_vars, guess_frame_inner):
        if game_finished:
            return  
        guess_vars[index] = ''
        display_guess_color(guess_vars, guess_frame_inner)

    def setup_ui(root, guess_vars, style):
        create_title_label(root)

        button_frame = tk.Frame(root, bg="darkslategray")
        button_frame.pack(pady=5)

        color_frame = tk.Frame(root, bg="darkslategray")
        color_frame.pack(pady=5, anchor="center") 

        guess_frame = tk.Frame(root, bg="darkslategray")
        guess_frame.pack(pady=5)
        guess_frame_inner = tk.Frame(guess_frame, bg="darkslategray")
        guess_frame_inner.pack()

        feedback_label = create_feedback_label(root)

        win_message_label = tk.Label(root, text="", font=("Arial", 14), fg="green", bg="darkslategray")
        win_message_label.pack(pady=5)

        loss_message_frame = tk.Frame(root, bg="darkslategray")
        loss_message_frame.pack(pady=5)

        color_buttons = create_color_buttons(root, color_frame, guess_vars, guess_frame_inner, style)
        create_top_buttons(root, feedback_label, guess_vars, selected_colors, result_strips, guess_frame_inner, win_message_label, loss_message_frame, color_buttons)

        create_attempt_rows(root, result_strips)
        display_guess_color(guess_vars, guess_frame_inner)

        return feedback_label, guess_frame_inner, win_message_label, loss_message_frame

    def create_title_label(root):
        title_label = tk.Label(root, text="Mastermind Game", font=("Arial", 14), fg="white", bg="darkslategray")
        title_label.pack(pady=10)

    def create_feedback_label(root):
        feedback_label = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="darkslategray")
        feedback_label.pack(pady=5)
        return feedback_label

    def create_attempt_rows(root, result_strips):
        attempts_frame = tk.Frame(root, bg="darkslategray")
        attempts_frame.pack(pady=5)

        for _ in range(MAX_ATTEMPTS):
            attempt_row = tk.Frame(attempts_frame, bg="darkslategray")
            attempt_row.pack(pady=1)

            row_strips = []

            for _ in range(MAX_COLORS):
                label = tk.Label(attempt_row, bg="white", width=4, height=1, relief="solid", bd=2)
                label.pack(side=tk.LEFT, padx=1)
                row_strips.append(label)

            spacer = tk.Label(attempt_row, width=2, bg="darkslategray")
            spacer.pack(side=tk.LEFT, padx=10)

            for _ in range(MAX_COLORS):
                label = tk.Label(attempt_row, bg="white", width=4, height=1, relief="solid", bd=2)
                label.pack(side=tk.LEFT, padx=1)
                row_strips.append(label)

            result_strips.append(row_strips)

    def create_top_buttons(root, feedback_label, guess_vars, selected_colors, result_strips, guess_frame_inner, win_message_label, loss_message_frame, color_buttons):
        button_frame = tk.Frame(root, bg="darkslategray")
        button_frame.pack(pady=10)

        submit_button = tk.Button(button_frame, text="Submit Guess",
                                  command=lambda: update_attempts(feedback_label, guess_vars, selected_colors, result_strips, guess_frame_inner, win_message_label, loss_message_frame, color_buttons))
        submit_button.pack(side=tk.LEFT, padx=10)

        restart_button = tk.Button(button_frame, text="Restart Game",
                                   command=lambda: restart_game(feedback_label, guess_vars, result_strips, guess_frame_inner, win_message_label, loss_message_frame, color_buttons))
        restart_button.pack(side=tk.LEFT, padx=10)

        give_up_button = tk.Button(button_frame, text="Give Up", command=lambda: give_up(feedback_label, guess_vars, result_strips, guess_frame_inner, loss_message_frame, color_buttons))
        give_up_button.pack(side=tk.LEFT, padx=10)

    def update_attempts(feedback_label, guess_vars, selected_colors, result_strips, guess_frame_inner, win_message_label, loss_message_frame, color_buttons):
        nonlocal attempts, game_finished
        if '' in guess_vars:
            messagebox.showwarning("Input Error", "Please select all colors before submitting.")
            return

        if attempts >= MAX_ATTEMPTS:
            display_loss(feedback_label, selected_colors, loss_message_frame, color_buttons)
            return

        guess = collect_user_guess(guess_vars)
        result, updated_attempts, status = play(selected_colors, guess, attempts)
        attempts += 1
        update_ui_feedback(feedback_label, result)
        update_result_strips(guess, result, selected_colors, result_strips, attempts)

        if status == WON:
            display_win_message(win_message_label)
            game_finished = True
            disable_color_buttons(color_buttons)
        elif status == LOST:
            display_loss(feedback_label, selected_colors, loss_message_frame, color_buttons)
            game_finished = True
            disable_color_buttons(color_buttons)

        for i in range(MAX_COLORS):
            guess_vars[i] = ''  

        display_guess_color(guess_vars, guess_frame_inner)

    def disable_color_buttons(color_buttons):
        for button in color_buttons:
            button.config(state="disabled")

    def display_win_message(win_message_label):
        win_message_label.config(text="Congratulations! You've won the game!", font=("Arial", 20, "bold"), fg="green")

    def display_loss(feedback_label, selected_colors, loss_message_frame, color_buttons):

        for widget in loss_message_frame.winfo_children():  
            widget.destroy()

        loss_label = tk.Label(loss_message_frame, text="You Lost!", font=("Arial", 12, "bold"), fg="red", bg="darkslategray")
        loss_label.pack(pady=1)  

        actual_colors_label = tk.Label(loss_message_frame, text="Actual Colors:", font=("Arial", 10, "bold"), fg="white", bg="darkslategray")
        actual_colors_label.pack(pady=2)  

        color_frame = tk.Frame(loss_message_frame, bg="darkslategray")
        color_frame.pack(pady=2) 


        for color in selected_colors: 
            color_label = tk.Label(color_frame, bg=color.value, width=6, height=1, relief="solid")
            color_label.pack(side=tk.LEFT, padx=3)  

 
        disable_color_buttons(color_buttons)

    def collect_user_guess(guess_vars):
        return guess_vars

    def update_ui_feedback(feedback_label, result):
        feedback_label.config(text="")

    def update_result_strips(guess, result, selected_colors, result_strips, attempts):
        row = result_strips[attempts - 1]

        exact_matches = result[EXACT]
        partial_matches = result[PARTIAL]
        no_matches = result[NO_MATCH]

        for i, color in enumerate(guess):
            row[i].config(bg=color.value)

        feedback_index = MAX_COLORS
        for _ in range(exact_matches):
            row[feedback_index].config(bg="black")
            feedback_index += 1

        for _ in range(partial_matches):
            row[feedback_index].config(bg="silver")
            feedback_index += 1

        for _ in range(no_matches):
            row[feedback_index].config(bg="gray")
            feedback_index += 1

    def give_up(feedback_label, guess_vars, result_strips, guess_frame_inner, loss_message_frame, color_buttons):
        display_loss(feedback_label, selected_colors, loss_message_frame, color_buttons)

    def restart_game(feedback_label, guess_vars, result_strips, guess_frame_inner, win_message_label, loss_message_frame, color_buttons):
        nonlocal attempts, selected_colors, game_finished
        attempts = 0
        game_finished = False  
        selected_colors = select_colors(seed=int(time.time()))  
        feedback_label.config(text="")
        win_message_label.config(text="")  

        for widget in loss_message_frame.winfo_children():
            widget.destroy()

        for i in range(MAX_COLORS):
            guess_vars[i] = ''

        display_guess_color(guess_vars, guess_frame_inner)

        for row in result_strips:
            for label in row:
                label.config(bg="white") 

        enable_color_buttons(color_buttons)

    def enable_color_buttons(color_buttons):
        for button in color_buttons:
            button.config(state="normal")

    return run

def _on_mousewheel(event, canvas):
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")

if __name__ == "__main__":
    game = mastermind_game()
    game()
