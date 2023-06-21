"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 151057054
Name:       Dong Le
Email:      dong.le@tuni.fi

This is an advanced GUI program
The memroy flip game is about remember cards, game's rule is simple, user clicks on a card to see
what symbol it uncover and try to find the matching symbol underneath the other cards. 
Uncover two cards at once to eliminate them from the game. Eliminate all cards to win the game.

The program starts by import libraries: tkinter, time, and random. There are 3 modes for the game:
easy, medium, and hard. Each modes have different number of cards, easy mode has 3x4=12 cards/game,
medium mode has 4x6=24 cards/game, and hard mode has 5x8=40 cards/game. 

There are 2 themes for the game: pokemon and league of legends (note: all images from pokemon are
from The Pokémon Company and Nitendo, images from league of legends are from Riot Games)
All modes and themes are stored in dictionaries, MODE_DICT has values are name of mode and keys are
row * collumn, THEME_DICT has values are theme name and keys are the location of images for that
theme. There is also a list of background images: tuni logo, pokeball logo, league of legends logo.



"""

from tkinter import *
from tkinter import messagebox
import time
import random

SAMPLE_PIC = 20
# MODE = ["Easy", "Medium", "Hard"]
# THEME = ["Pokemon", "League of Legends"]

MODE_DICT = {"Easy": "3x4",
            "Medium": "4x6",
            "Hard": "5x8"}
THEME_DICT = {"Pokemon": "images/pokemon/",
              "League of Legends": "images/lol/"}
IMAGE_BG = ["images/tuni.png","images/pokemon.png","images/lol.png"]

class Gallery:
    def __init__(self):
        self.__gallery_window = Tk()
        self.__gallery_window.geometry("+100+20")
        self.__gallery_window.resizable(0, 0)
        self.__gallery_window.title("Gallery View")

        my_menu = Menu(self.__gallery_window)
        self.__gallery_window.config(menu=my_menu)

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Main...", 
                            command=lambda: to_main(self.__gallery_window))
        file_menu.add_command(label="New Game...", 
                            command=lambda: to_mode_theme(self.__gallery_window))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command= self.__gallery_window.destroy)

        self.__lol_intro = Label(self.__gallery_window, 
                        text = list(THEME_DICT.keys())[1], font=('Arial',10))
        image_lol = PhotoImage(file=IMAGE_BG[2])
        
        self.__lol_view = Button(self.__gallery_window, image=image_lol,
                        command=lambda route=THEME_DICT["League of Legends"]:
                        self.clicked(route))
        self.__lol_view.image = image_lol
        
        self.__pkm_intro = Label(self.__gallery_window, 
                        text = list(THEME_DICT.keys())[0], font=('Arial',10))
        image_pkm = PhotoImage(file=IMAGE_BG[1])

        self.__pkm_view = Button(self.__gallery_window, image=image_pkm,
                        command=lambda route=THEME_DICT["Pokemon"]:
                        self.clicked(route))
        self.__pkm_view.image = image_pkm
        
        self.__button_back = Button(self.__gallery_window, text= "Back",
                        command= lambda: to_main(self.__gallery_window))

        self.__pkm_intro.grid(column=1, row=0)
        self.__lol_intro.grid(column=0,row=0)
        self.__lol_view.grid(column=0,row=1)
        self.__pkm_view.grid(column=1,row=1)
        self.__button_back.grid(row=3,column=0, columnspan= 3)
        self.__gallery_window.mainloop()
    
    def clicked(self, route):
        self.__lol_intro.destroy()
        self.__pkm_intro.destroy()
        self.__lol_view.destroy()
        self.__pkm_view.destroy()

        image_file = PhotoImage(file=route + "0.png")
    
        self.__my_label= Label(self.__gallery_window, image=image_file)
        self.__my_label.image = image_file
        self.__button_backward = Button(self.__gallery_window, text= "<<",
                            command=lambda: self.backward(route),
                            state=DISABLED)
        self.__button_back.config(command= lambda: to_gallery(self.__gallery_window))

        self.__button_forward = Button(self.__gallery_window, text= ">>", 
                            command=lambda: self.forward(route,1))

        self.__my_label.grid(row=0, column=0, columnspan=3)
        self.__button_backward.grid(row=1,column=0)
        self.__button_forward.grid(row=1,column=2)

    def forward(self,route,num):
        self.__my_label.destroy()
        image_file = PhotoImage(file= route + str(num) + ".png")
        self.__my_label = Label(self.__gallery_window,image=image_file)
        self.__my_label.image = image_file

        self.__button_forward.config(command=lambda: self.forward(route,num+1))
        self.__button_backward = Button(self.__gallery_window, text= "<<",
                            command=lambda: self.backward(route, num-1))
        
        if num == SAMPLE_PIC-1:
            self.__button_forward.config(state=DISABLED)

        self.__my_label.grid(row=0, column=0, columnspan=3)
        self.__button_backward.grid(row=1,column=0)

    def backward(self, route,num):
        self.__my_label.destroy()
        image_file = PhotoImage(file= route + str(num) + ".png")
        self.__my_label = Label(self.__gallery_window,image=image_file)
        self.__my_label.image = image_file

        self.__button_forward = Button(self.__gallery_window, text= ">>", 
                            command=lambda: self.forward(route,num+1))
        self.__button_backward.config(command=lambda: self.backward(route,num-1))
        if num == 0:
            self.__button_backward.config(state=DISABLED)

        self.__my_label.grid(row=0, column=0, columnspan=3)
        self.__button_forward.grid(row=1,column=2)
            

class GamePlay:
    def __init__(self, ROW_SIZE, COL_SIZE, theme):
        self.__game_window = Tk()
        self.__game_window.geometry("+100+20")
        self.__game_window.resizable(0, 0)
        self.__game_window.title("Game Play")

        self.__col = COL_SIZE
        self.__row = ROW_SIZE
        self.__theme = theme
        self.__start_time = time.time()
        self.__move_counter = 0
        self.__save_pic = []
        self.__cards_needed = self.__col * self.__row // 2
        self.__finish_matched = 0

        my_menu = Menu(self.__game_window)
        self.__game_window.config(menu=my_menu)

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Main...", 
                            command= lambda: to_main(self.__game_window))
        file_menu.add_command(label="New Game...", 
                            command= lambda:to_mode_theme(self.__game_window))
        file_menu.add_command(label="Restart...", command= self.restart)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command= self.__game_window.destroy)

        opt_menu = Menu(my_menu)
        my_menu.add_cascade(label="Option", menu=opt_menu)
        opt_menu.add_command(label="Gallery...",
                            command= lambda: to_gallery((self.__game_window)))
        opt_menu.add_command(label="Hint...", command= self.hint)

        self.prepare()
        self.update_time()
        self.__game_window.mainloop()
    
    def update_time(self):
        if not self.game_clear():
            time_passed = int(time.time() - self.__start_time)
            self.__time_display.config(text="Time: " + str(time_passed) + " sec")
            self.__game_window.after(1000, self.update_time)
        else:
            self.pop_up_ques()

    def prepare(self):
        cards = self.generate_cards()
        self.__background_image = PhotoImage(file=IMAGE_BG[0])
        buttons = []
        for row in range(self.__row):
            for col in range(self.__col):
                button = Button(self.__game_window, image=self.__background_image,
                                command=lambda row=row, column=col:
                                self.change_label(buttons, row, column, cards))
               
                buttons.append(button)
                button.grid(row=row, column=col)
        buttons = self.set_on_board(buttons)
        self.__time_display = Label(self.__game_window,
                                    text="Time: 0 sec", font=('Arial',12))
        self.__move_display = Label(self.__game_window,
                                    text="Moved: 0",font=('Arial',12))
        
        self.__time_display.grid(row=self.__row+1,column=0,columnspan=self.__col+1)
        self.__move_display.grid(row=self.__row+2,column=0,columnspan=self.__col+1)


    def set_on_board(self, raw_list):
        set_list = []
        for i in range(0, len(raw_list), self.__col):
            set_list.append(raw_list[i:i + self.__col])
        return set_list


    def generate_cards(self):
        cards = []
        randomcards = random.sample(list(range(0, SAMPLE_PIC)), k=self.__cards_needed)
        
        for i in range(len(randomcards)):
            route = self.__theme + str(randomcards[i]) + '.png'
            image = PhotoImage(file=route)
            cards.append(image)
            cards.append(image)
        random.shuffle(cards)
        cards_generated = self.set_on_board(cards)
        return cards_generated
    
    def change_label(self, buttons, row, col, cards):
        self.__move_counter +=1
        self.__move_display.config(text="Moved: " + str(self.__move_counter))
        buttons[row][col].config(image=cards[row][col], bg="gray99")
        if self.__move_counter % 2 == 0:
            x = self.__save_pic[0]
            y = self.__save_pic[1]

            if cards[row][col] == cards[x][y]:
                self.__finish_matched += 1
                buttons[row][col].config(state=DISABLED, bg="white")
                buttons[x][y].config(state=DISABLED, bg="white")
            else:
                buttons[row][col].after(500, self.hide_buttons, buttons, row, col, x, y)
            self.__save_pic.clear()
        else:
            self.__save_pic.append(row)
            self.__save_pic.append(col)


    def hide_buttons(self, buttons, row, col, x, y):
        buttons[row][col].config(image=self.__background_image, bg="white")
        buttons[x][y].config(image=self.__background_image, bg="white")


    def game_clear(self):
        return self.__finish_matched == self.__cards_needed

    def pop_up_ques(self):
        ask = messagebox.askyesno(title="Success!", 
                    message="Congratulation, you won!\n\nDo you want to play again?")
        if ask == 1:
            to_mode_theme(self.__game_window)
        else:
            to_main(self.__game_window)

    def restart(self):
        self.__game_window.destroy()
        GamePlay(self.__row, self.__col, self.__theme)

    
    def hint(self):
        for row in range(self.__row):
            for col in range(self.__col):
                pass


class Main_Screen:
    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.geometry("+100+20")
        self.__main_window.resizable(0, 0)
        self.__main_window.title("Memory Game")

        self.__intro = Label(self.__main_window, text="Welcome to Memory Game",
                        bg="#A2A2CD",fg="#E6E6E6", font=('Arial',21))
        self.__newgame = Button(self.__main_window, text="New Game",
                        bg="#A2A2CD",fg="#E6E6E6",
                        command= lambda: to_mode_theme(self.__main_window))

        self.__rule = Button(self.__main_window, text="Rules",
                        bg="#A2A2CD",fg="#E6E6E6",command=self.rule)
        
        self.__gallery = Button(self.__main_window, text= "Gallery",
                        bg="#A2A2CD",fg="#E6E6E6",
                        command=lambda: to_gallery(self.__main_window))
        
        self.__quit_button = Button(self.__main_window, text="Quit",
                        bg="#54548B",fg="#E6E6E6",command=self.__main_window.destroy)
        
        self.__intro.grid(row=0,column=0, columnspan=3)
        self.__newgame.grid(row=1, column=0, columnspan=3)
        self.__rule.grid(row=2, column=0, columnspan=3)
        self.__gallery.grid(row=3, column=0, columnspan=3)
        self.__quit_button.grid(row=4, column=0, columnspan=3)
        self.__main_window.mainloop()
        
    def rule(self):
        self.__intro.destroy()
        self.__newgame.destroy()
        self.__rule.destroy()
        self.__gallery.destroy()
        self.__quit_button.destroy()
        button_quit = Button(text= "Back", 
                    command=lambda: to_main(self.__main_window))
        rule1 = Label(text= "Click on the cards to see what symbol they uncover\n and try to find the matching symbol underneath the other cards")
        rule2 = Label(text= "Uncover two matching symbols at once\n to eliminate them from the game.") 
        rule3 = Label(text= "Eliminate all cards\n as fast as you can to win the game.")


        rule1.grid(row=0,column=0)
        rule2.grid(row=1,column=0)
        rule3.grid(row=2,column=0)
        button_quit.grid(row=3,column=0)


class Mode_Theme:
    def __init__(self):
        self.__mt_window = Tk()
        self.__mt_window.geometry("+100+20")
        self.__mt_window.resizable(0, 0)
        self.__mt_window.title("New Game")

        self.__intro = Label(self.__mt_window, text="Choose mode and theme")
        self.__button_quit = Button(text= "Back",
                            command= lambda: to_main(self.__mt_window))

        
        self.__clicked1 = StringVar()
        self.__clicked1.set(next(iter(MODE_DICT)))
        intro1 = Label(self.__mt_window, text="Mode")
        choice1 = OptionMenu(self.__mt_window, self.__clicked1, *MODE_DICT)

        
        self.__clicked2 = StringVar()
        self.__clicked2.set(next(iter(THEME_DICT)))
        intro2 = Label(self.__mt_window, text="Theme")
        choice2 = OptionMenu(self.__mt_window, self.__clicked2, *THEME_DICT)

        self.__game_start = Button(self.__mt_window, text="Start Game",
                            command= self.game_start)

        self.__intro.grid(column=0,row=0,columnspan=3)
        intro1.grid(column=0,row=1)
        intro2.grid(column=1,row=1)
        choice1.grid(column=0,row=2)
        choice2.grid(column=1,row=2)
        self.__game_start.grid(column=0,row=3,columnspan=3)
        self.__button_quit.grid(row=4,column=0,columnspan=3)
        self.__mt_window.mainloop()


    def game_start(self):
        self.__mt_window.destroy()
        for i in THEME_DICT:
            if self.__clicked2.get() == i:
                theme = THEME_DICT[i]
        
        for j in MODE_DICT:
            if self.__clicked1.get() == j:
                row = int(MODE_DICT[j][0])
                col = int(MODE_DICT[j][-1])
                GamePlay(row, col,theme)

        # if self.__clicked2.get() == THEME[0]:
        #     theme ='images/pokemon/'
        # elif self.__clicked2.get() == THEME[1]:
        #     theme ='images/lol/'

        # if self.__clicked1.get() == MODE[0]:
        #     GamePlay(3, 4,theme)
        # elif self.__clicked1.get() == MODE[1]:
        #     GamePlay(4, 6,theme)
        # elif self.__clicked1.get() == MODE[2]:
        #     GamePlay(5, 8, theme)


def to_main(window):
    window.destroy()
    Main_Screen()

def to_mode_theme(window):
    window.destroy()
    Mode_Theme()

def to_gallery(window):
    window.destroy()
    Gallery()       

def main():

    Main_Screen()


if __name__ == "__main__":
    main()
