from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Arial", 40, "italic")
FONT_WORD = ("Arial", 60, "bold")
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/hebrew_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_word, text=current_card["hebrew"], fill="black")
    canvas.itemconfig(card_title, text="Hebrew", fill="black")
    canvas.itemconfig(front_image, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(front_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["english"], fill="white")


def is_known():
    to_learn.remove(current_card)
    datadf = pandas.DataFrame(to_learn)
    datadf.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.geometry("900x720")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.maxsize(width=900, height=720)
window.minsize(width=900, height=720)

flip_timer = window.after(3000, flip_card)

# Canvas
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
front_image = canvas.create_image(402, 265, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

card_title = canvas.create_text(400, 150, text="Title", font=FONT_TITLE)
card_word = canvas.create_text(400, 263, text="word", font=FONT_WORD)

# Buttons
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, border=0, command=is_known)
known_button.grid(row=1, column=1)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, border=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()

window.mainloop()
