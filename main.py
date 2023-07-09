from tkinter import *
import random
import pandas
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
word_dict = {}

# Ask user to choose language to learn
language = askstring("Language",
                     "What language do you want to learn? (Type Korean/French)")
showinfo("Welcome!", f"Let's start learning some {language} vocabularies")

# Open and read csv file
try:
    data_list = pandas.read_csv(f"data/{language}_words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv(f"data/{language}_words.csv")
    word_dict = original_data.to_dict(orient="records")
else:
    word_dict = data_list.to_dict(orient="records")


def update_card():
    """Update the next card to learn"""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_dict)
    canvas.itemconfig(language_label, text=f"{language}", fill="black")
    canvas.itemconfig(vocab_label, text=current_card[f"{language}"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """Change the back of the card for the meaning in English"""
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(language_label, text="English", fill="white")
    canvas.itemconfig(vocab_label, text=current_card["English"], fill="white")


def known_card():
    """Remove the word that user already known in the word list"""
    word_dict.remove(current_card)
    to_learn_data = pandas.DataFrame(word_dict)
    to_learn_data.to_csv(f"data/{language}_words_to_learn.csv", index=False)
    update_card()


# Create Tkinter User Interface
window = Tk()
window.title("Flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# Create canvas to add images
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

# Create text for language and word to learn
language_label = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
vocab_label = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Create right and wrong button
button_X_image = PhotoImage(file="./images/wrong.png")
button_X = Button(image=button_X_image, highlightthickness=0, command=update_card)
button_X.grid(column=0, row=1)

button_Y_image = PhotoImage(file="./images/right.png")
button_Y = Button(image=button_Y_image, highlightthickness=0, command=known_card)
button_Y.grid(column=1, row=1)

update_card()

window.mainloop()
