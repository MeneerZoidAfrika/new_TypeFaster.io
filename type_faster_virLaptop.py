import tkinter as tk
import ctypes
import time
import random
from RandomWordsGenerator import RandomWordsGenerator

FONT = ("Helvetica", 18)
TITLE_FONT = ("Helvetica", 50, "bold")
LARGER_FONT = ("Helvetica", 50)

total_correct_words = 0
user_accuracy = 0


def center_window(window, width, height):
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def start_timer():
    global timer_is_running, starting_time

    submit_button.config(text="Submit")

    input_entry.delete(0, "end")
    input_entry.config(fg="black")
    timer_is_running = True
    starting_time = time.time()


def stop_timer():
    global timer_is_running, total_correct_words
    timer_is_running = False

    total_words_typed = len(input_entry.get().split())

    user_wpm = (total_words_typed / 60) * 100
    user_accuracy = (total_correct_words / total_words_typed) * 100

    timer_label.config(text=f"Time's up! You type at {user_wpm:.0f} WPM with {user_accuracy:.0f}% accuracy!",
                       font=FONT)


def update_timer():
    """Updates the timer after 100ms"""

    if timer_is_running:
        time_left = 60 - (time.time() - starting_time)
        timer_label.config(text=f"Time Left: {time_left:.0f}")

        if time_left <= 0:
            stop_timer()

    # Schedule after 100ms
    root.after(100, update_timer)


def submit():
    """Calculates the Words Per Minute that the user types if the user doesn't want to type for 1 minute"""
    global total_correct_words, timer_is_running, starting_time

    # Keeps the variables from updating after the user has submitted
    if not timer_is_running:
        return

    total_words_typed = len(input_entry.get().split())
    timer_is_running = False

    submit_time = time.time()
    time_elapsed = submit_time - starting_time

    approximate_wpm = (total_words_typed / time_elapsed) * 60
    approximate_accuracy = (total_correct_words / total_words_typed) * 100

    print(f"Total words typed: {total_words_typed}")
    timer_label.config(text=f"Time's up! You type at approximately {approximate_wpm:.0f} WPM with {approximate_accuracy:.0f}% accuracy!",
                       font=FONT)


    submit_button.config(text="Start typing to start again!")


def on_entry_click(event):
    input_entry.delete(0, "end")


def read_keyboard(event):
    """Constantly reads what the user is typing"""
    global total_correct_words

    user_input = input_entry.get()  # Get text from the widget

    if not timer_is_running:
        start_timer()
    if timer_is_running:
        update_timer()

    for tag in random_words_text.tag_names():
        random_words_text.tag_remove(tag, "1.0", tk.END)

    # Looping through the text to find which words to turn Green
    for word in user_input.split():
        if word in random_words:
            start_index = "1.0"
            while True:
                start_index = random_words_text.search(word, start_index, tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                random_words_text.tag_add(word, start_index, end_index)
                start_index = end_index

    # Changing the correct word to green
    for word in random_words:
        random_words_text.tag_config(word, foreground="green")

    correct_words = []
    for word in user_input.split():
        if word in random_words and word not in correct_words:
            correct_words.append(word)
            print(correct_words)
            total_correct_words = len(correct_words)


# Getting the random words
rwg = RandomWordsGenerator()
random_words = rwg.get_random_words()


# Initializing GUI
root = tk.Tk()
root.title("TypeFaster.io")

window_width = 1105
window_height = 900
root.geometry(f"{window_width}x{window_height}")


# Labels
title_label = tk.Label(root, text="TypeFaster.io", font=TITLE_FONT)
title_label.grid(row=0, column=1, columnspan=3, padx=20, pady=40)

# Random Words Textbox
random_words_text = tk.Text(root, font=FONT, wrap=tk.WORD, highlightcolor="#242424", height=10)
random_words_text.grid(row=1, column=1, columnspan=3, padx=30, pady=5, sticky="ew")

for word in random_words:
    random_words_text.insert(tk.END, word + " ")


# Timer
timer_is_running = False
starting_time = 0

timer_label = tk.Label(root, font=LARGER_FONT)
timer_label.grid(column=1, row=5, columnspan=3)


# Entry Widget
input_entry = tk.Entry(root, font=LARGER_FONT)
input_entry.insert(0, "Click to start")
input_entry.config(fg="gray")
input_entry.grid(row=2, column=1, columnspan=3, padx=20, pady=20, rowspan=1, )
input_entry.bind("<KeyPress>", read_keyboard)

# Removing text after user has clicked on Entry Bar
input_entry.bind("<FocusIn>", on_entry_click)

# Buttons
submit_button = tk.Button(root, text="Submit", command=submit, height=5, width=5, bg="lightblue")
submit_button.grid(row=3, column=2, columnspan=1, padx=20, pady=40, sticky="nsew")


if __name__ == "__main__":
    center_window(root, window_width, window_height)
    root.mainloop()

