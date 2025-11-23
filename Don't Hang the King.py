import tkinter.messagebox
import customtkinter
import os
import random
from tkinter import *
from PIL import Image, ImageTk
from wonderwords import RandomWord, RandomSentence, Defaults


class DontHangTheKing(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title("Don't Hang The King")

        self.frame = HomePage(self)
        self.frame.pack()

    def switch_frame(self, FRAME):
        self.frame.destroy()
        self.frame = FRAME(self)
        self.frame.pack()


class HomePage(Frame):
    def __init__(self, MASTER):  # parameter master is where the frame will be place, also, frames are stackable
        super().__init__(master=MASTER)

        # loading the background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = Image.open(current_path + "\dhtk.png")

        # creating the canvas for the frames
        self.canvas = customtkinter.CTkCanvas(self, width=1400, height=800)
        self.canvas.pack(fill="both", expand=TRUE)

        # finishing the home screen
        self.resized_image = self.bg_image.resize((1400, 800))
        self.bg_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw')

        # play customtkinter.CTkButton
        play_btn = customtkinter.CTkButton(self, text="Let's Save the King!", fg_color="#443C0F", bg_color="#443C0F",
                                           hover_color="#443C0F", text_color="#EFC74E", font=("Constantia", 30),
                                           command=lambda: MASTER.switch_frame(Game))
        self.canvas.create_window(700, 550, anchor="center", window=play_btn)


class Button(customtkinter.CTkButton):
    def __init__(self, master, command, letter, x, y):
        super().__init__(master=master, text=letter, width=50, font=("Constantia", 18), fg_color="#30271E",
                         bg_color="#30271E", hover_color="#6B0303", command=command, height=50)
        self.letter = letter
        self.x = x
        self.y = y


class Game(Frame):
    def __init__(self, MASTER):
        super().__init__(MASTER)

        current_path = os.path.dirname(os.path.realpath(__file__))

        # bg frames of dont hang the king
        frame0 = Image.open(current_path + f"\\0-lives-left.png")
        frame1 = Image.open(current_path + f"\\1-lives-left.png")
        frame2 = Image.open(current_path + f"\\2-lives-left.png")
        frame3 = Image.open(current_path + f"\\3-lives-left.png")
        frame4 = Image.open(current_path + f"\\4-lives-left.png")
        frame5 = Image.open(current_path + f"\\5-lives-left.png")
        frame6 = Image.open(current_path + f"\\6-lives-left.png")
        frame7 = Image.open(current_path + f"\\7-lives-left.png")

        # dont hang the king game variables
        self.bg_frames = [frame0, frame1, frame2, frame3, frame4, frame5, frame6, frame7]
        self.guessed_letters = []
        self.score = 0
        self.categ = ""
        self.word = ""

        # creating the canvas for the frames
        self.canvas = customtkinter.CTkCanvas(self, width=1400, height=800)
        self.canvas.pack(fill="both", expand=TRUE)

        self.start()

    def display_bg_frame(self, arr):
        current = arr[-1]
        resized_image = current.resize((1400, 800))
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def reset(self):
        self.guessed_letters.clear()
        self.canvas.delete("all")
        self.start()

    def start(self):
        word_categ = random.choice(("nouns=Defaults.NOUNS", "verbs=Defaults.VERBS", "adj=Defaults.ADJECTIVES"))
        if word_categ == "nouns=Defaults.NOUNS":
            self.categ = "NOUN"
        elif word_categ == "verbs=Defaults.VERBS":
            self.categ = "VERB"
        else:
            self.categ = "ADJECTIVE"

        to_guess = random.choice(("word_categ", "sentence"))
        if to_guess == "word_categ":
            self.word = eval(f"RandomWord({word_categ}).word().upper()")
        else:
            self.word = RandomSentence().simple_sentence().upper().rstrip(".")
            self.categ = "SENTENCE"

        frames = self.bg_frames.copy()
        lives = len(frames) - 1
        self.display_bg_frame(frames)

        # playing field | fill="#FFC821"
        text = self.word
        for char in text:
            if char != " " and char != "-":
                text = text.replace(char, "_")
        text = " ".join(list(text))
        word_label = customtkinter.CTkLabel(self, height=10, text=text, font=("Constantia", 18), fg_color="#3D260F")
        self.canvas.create_window(1010, 260, anchor="center", window=word_label)

        # displays
        selected_letters = customtkinter.CTkLabel(self, height=10, text="Selected letters go here", font=("Constantia", 15), fg_color="#3D260F")
        score_display = customtkinter.CTkLabel(self, height=10, text=str(self.score), font=("Constantia", 25),
                                                    text_color="#FFE1C4", fg_color="#5D4E3F")
        lives_display = customtkinter.CTkLabel(self, height=10, text=str(lives), font=("Constantia", 25),
                                                    text_color="#FFE1C4", fg_color="#BCA38B")
        categ_display = customtkinter.CTkLabel(self, height=10, text=self.categ, font=("Constantia", 25),
                                                    text_color="#FFE1C4", fg_color="#BCA38B")

        self.canvas.create_window(1010, 403, anchor="center", window=selected_letters)
        self.canvas.create_window(1315, 174, anchor="center", window=score_display)
        self.canvas.create_window(780, 174, anchor="center", window=lives_display)
        self.canvas.create_window(1010, 190, anchor="center", window=categ_display)

        def check_and_destroy(btn):
            btn.destroy()

            self.guessed_letters.append(btn.letter)
            selected_letters.configure(text=" ".join(self.guessed_letters))

            if btn.letter in self.word:
                word_list = []
                for letter in self.word:
                    if letter in self.guessed_letters:
                        word_list.append(letter)
                    elif letter == " " or letter == "-":
                        word_list.append(letter)

                    else:
                        word_list.append("_")
                word_label.configure(text=" ".join(word_list))

                if all(letter in self.guessed_letters for letter in self.word if letter != " " and letter != "-"):
                    tkinter.messagebox.showinfo("The King Lived", "You succeed in saving your king!")
                    self.score += 1
                    score_display.configure(text=self.score)
                    self.reset()

            else:
                frames.pop()
                lives = len(frames)-1
                lives_display.configure(text=lives)
                self.display_bg_frame(frames)

                if lives == 0:
                    tkinter.messagebox.showinfo("The King Died",
                                                f"You failed to save your king. The word is {self.word}.")
                    self.reset()

        # buttons
        btn_a = Button(self, command=lambda: check_and_destroy(btn_a), letter='A', x=735, y=500)
        btn_b = Button(self, command=lambda: check_and_destroy(btn_b), letter='B', x=815, y=500)
        btn_c = Button(self, command=lambda: check_and_destroy(btn_c), letter='C', x=895, y=500)
        btn_d = Button(self, command=lambda: check_and_destroy(btn_d), letter='D', x=975, y=500)
        btn_e = Button(self, command=lambda: check_and_destroy(btn_e), letter='E', x=1055, y=500)
        btn_f = Button(self, command=lambda: check_and_destroy(btn_f), letter='F', x=1135, y=500)
        btn_g = Button(self, command=lambda: check_and_destroy(btn_g), letter='G', x=1215, y=500)
        btn_h = Button(self, command=lambda: check_and_destroy(btn_h), letter='H', x=1295, y=500)
        btn_i = Button(self, command=lambda: check_and_destroy(btn_i), letter='I', x=735, y=575)
        btn_j = Button(self, command=lambda: check_and_destroy(btn_j), letter='J', x=815, y=575)
        btn_k = Button(self, command=lambda: check_and_destroy(btn_k), letter='K', x=895, y=575)
        btn_l = Button(self, command=lambda: check_and_destroy(btn_l), letter='L', x=975, y=575)
        btn_m = Button(self, command=lambda: check_and_destroy(btn_m), letter='M', x=1055, y=575)
        btn_n = Button(self, command=lambda: check_and_destroy(btn_n), letter='N', x=1135, y=575)
        btn_o = Button(self, command=lambda: check_and_destroy(btn_o), letter='O', x=1215, y=575)
        btn_p = Button(self, command=lambda: check_and_destroy(btn_p), letter='P', x=1295, y=575)
        btn_q = Button(self, command=lambda: check_and_destroy(btn_q), letter='Q', x=735, y=650)
        btn_r = Button(self, command=lambda: check_and_destroy(btn_r), letter='R', x=815, y=650)
        btn_s = Button(self, command=lambda: check_and_destroy(btn_s), letter='S', x=895, y=650)
        btn_t = Button(self, command=lambda: check_and_destroy(btn_t), letter='T', x=975, y=650)
        btn_u = Button(self, command=lambda: check_and_destroy(btn_u), letter='U', x=1055, y=650)
        btn_v = Button(self, command=lambda: check_and_destroy(btn_v), letter='V', x=1135, y=650)
        btn_w = Button(self, command=lambda: check_and_destroy(btn_w), letter='W', x=1215, y=650)
        btn_x = Button(self, command=lambda: check_and_destroy(btn_x), letter='X', x=1295, y=650)
        btn_y = Button(self, command=lambda: check_and_destroy(btn_y), letter='Y', x=975, y=725)
        btn_z = Button(self, command=lambda: check_and_destroy(btn_z), letter='Z', x=1055, y=725)

        buttons = [btn_a, btn_b, btn_c, btn_d, btn_e, btn_f, btn_g, btn_h, btn_i, btn_j, btn_k, btn_l, btn_m,
                   btn_n, btn_o, btn_p, btn_q, btn_r, btn_s, btn_t, btn_u, btn_v, btn_w, btn_x, btn_y, btn_z]

        for btn in buttons:
            self.canvas.create_window(btn.x, btn.y, anchor="center", window=btn)


DontHangTheKing().mainloop()