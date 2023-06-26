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

The program starts at class Main_Screen, which has a purpose to display the main screen of the game.
On the main screen, there are four options to choose: starting a new game, checking rules, cheking
gallery and exit the game. Each option is a button to other class.

For starting a new game, firstly user needs to choose which mode and which theme to play, the class
Mode_Theme checks the selection from user and pass the data based on that to the class GamePlay.
Inside GamePlay, it handles generate cards randomly from sample cards, display on the screen and 
algorithm to check cards, hide cards, inform time, moves, and inform victory. Every click/move
from user is added to the counter below and timer also runs, only stop when user finish the game.

For checking rules, there is a function to popup message box.

For checking gallery, a class Galley was made to display sameple picture from two themes. The beauty
of the gallery is that user only click forward from beginning and click backward at the end. 

Except from options on the screen, user also have some options from menu bar, for example: during the
gameplay, user can choose to restart the game from beginning, restart the game with different mode and
theme, back to the main screen, or checking the rules.
"""

from tkinter import *
from tkinter import messagebox
import time
import random

SAMPLE_PIC = 20
MODE_DICT = {"Easy": "3x4",
            "Medium": "4x6",
            "Hard": "5x8"}
THEME_DICT = {"Pokemon": "images/pokemon/",
              "League of Legends": "images/lol/"}
IMAGE_BG = ["images/tuni.png","images/pokemon.png","images/lol.png"]

class Gallery:
    """
    This class handles gallery view
    """
    def __init__(self):
        # Creating the window and the components
        self.__gallery_window = Tk()
        self.__gallery_window.geometry("+100+20")
        self.__gallery_window.resizable(0, 0)
        self.__gallery_window.title("Gallery View")

        # Create a menu bar
        my_menu = Menu(self.__gallery_window)
        self.__gallery_window.config(menu=my_menu)

        # In the file of menubar, there are 3 options:
        # Main: to the main
        # New Game: to the selection of theme and mode to start a new game
        # Exit: to exit the gallery and turn off the program
        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Main...", 
                            command=lambda: to_main(self.__gallery_window))
        file_menu.add_command(label="New Game...", 
                            command=lambda: to_mode_theme(self.__gallery_window))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command= self.__gallery_window.destroy)

        # Adding two theme images and labels for user to choose
        # First one is pokemon
        self.__pkm_intro = Label(self.__gallery_window, 
                        text = list(THEME_DICT.keys())[0], font=('Arial',10))
        image_pkm = PhotoImage(file=IMAGE_BG[1])

        self.__pkm_view = Button(self.__gallery_window, image=image_pkm,
                        command=lambda route=THEME_DICT["Pokemon"]:
                        self.clicked(route))
        self.__pkm_view.image = image_pkm

        # Second one is league of legends
        self.__lol_intro = Label(self.__gallery_window, 
                        text = list(THEME_DICT.keys())[1], font=('Arial',10))
        image_lol = PhotoImage(file=IMAGE_BG[2])
        
        self.__lol_view = Button(self.__gallery_window, image=image_lol,
                        command=lambda route=THEME_DICT["League of Legends"]:
                        self.clicked(route))
        self.__lol_view.image = image_lol

        # Adding a back button to return to main screen
        self.__button_back = Button(self.__gallery_window, text= "Back",
                        command= lambda: to_main(self.__gallery_window))

        self.__pkm_intro.grid(column=1, row=0)
        self.__lol_intro.grid(column=0,row=0)
        self.__lol_view.grid(column=0,row=1)
        self.__pkm_view.grid(column=1,row=1)
        self.__button_back.grid(row=3,column=0, columnspan= 3)
        self.__gallery_window.mainloop()
    
    def clicked(self, route):
        """
        After user choose which theme to view the gallery, a parameter
        route was pass to the method to display the theme images

        :param route: str, the address to the theme's folder
        """
        # delete all info on the screen, to replace them with the new
        # keep the back button to return to the selection screen
        self.__lol_intro.destroy()
        self.__pkm_intro.destroy()
        self.__lol_view.destroy()
        self.__pkm_view.destroy()

        # display the first image and zoom 2x to better view (but noise)
        image_file = PhotoImage(file=route + "0.png")
        larger_image = image_file.zoom(2, 2)
        self.__my_label= Label(self.__gallery_window, image=larger_image)
        self.__my_label.image = larger_image

        # Add forward and backward button to see next/back images
        # this is the first images so the backward button is disable
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
        """
        After user choose forward button, a new image was shown

        :param route: str, the address to the theme's folder
        :pram num: int, the index of the next image
        """
        # delete the last image
        self.__my_label.destroy()

        # display the next image and zoom 2x to better view (but noise)
        image_file = PhotoImage(file= route + str(num) + ".png")
        larger_image = image_file.zoom(2, 2)
        self.__my_label = Label(self.__gallery_window,image=larger_image)
        self.__my_label.image = larger_image

        # changing the forward button to index the next image
        self.__button_forward.config(command=lambda: self.forward(route,num+1))
        # this is not the first image so backward button is active
        self.__button_backward = Button(self.__gallery_window, text= "<<",
                            command=lambda: self.backward(route, num-1))
        
        # if this is the last image, then the forward button is disable
        if num == SAMPLE_PIC-1:
            self.__button_forward.config(state=DISABLED)

        self.__my_label.grid(row=0, column=0, columnspan=3)
        self.__button_backward.grid(row=1,column=0)

    def backward(self, route,num):
        """
        After user choose backward button, the last image was shown

        :param route: str, the address to the theme's folder
        :pram num: int, the index of the last image
        """
        # delete the current image
        self.__my_label.destroy()

        # display the last image and zoom 2x to better view (but noise)
        image_file = PhotoImage(file= route + str(num) + ".png")
        larger_image = image_file.zoom(2, 2)
        self.__my_label = Label(self.__gallery_window,image=larger_image)
        self.__my_label.image = larger_image

        # changing forward and backward buttons to indicate the next images
        self.__button_forward = Button(self.__gallery_window, text= ">>", 
                            command=lambda: self.forward(route,num+1))
        self.__button_backward.config(command=lambda: self.backward(route,num-1))

        # if this is the first image, then disable the backward button
        if num == 0:
            self.__button_backward.config(state=DISABLED)

        self.__my_label.grid(row=0, column=0, columnspan=3)
        self.__button_forward.grid(row=1,column=2)
            

class GamePlay:
    """
    This class represent the gameplay, algorithm for the game,
    count moves, timer, display info, inform winner
    """
    def __init__(self, ROW_SIZE, COL_SIZE, theme):
        """
        :param ROW_SIZE: int, how many row for the game cards
        :param COL_SIZE: int, how many collumn for the game cards
        :param theme: str, the address to the theme's folder
        """
        # Creating the window and the components
        self.__game_window = Tk()
        self.__game_window.geometry("+100+20")
        self.__game_window.resizable(0, 0)
        self.__game_window.title("Game Play")

        # save parameter to class's variable
        self.__col = COL_SIZE
        self.__row = ROW_SIZE
        self.__theme = theme
        
        # using library time to start timer
        self.__start_time = time.time()

        # count moves from user
        self.__move_counter = 0

        # two cards reveal, so this variable to save the row, collumn
        # parameter for the first card
        # then to compare with second card
        self.__save_pic = []

        # how many cards needed, if user choose number of collumn and row
        self.__cards_needed = self.__col * self.__row // 2

        # how many match does user finish
        self.__finish_matched = 0

        # Create a menu bar
        my_menu = Menu(self.__game_window)
        self.__game_window.config(menu=my_menu)

        # In the file of menubar, there are 3 options:
        # Main: to the main
        # New Game: to the selection of theme and mode to start a new game
        # Restart: restart the game with the same selection of theme and mode
        #          also restart the timer and move count
        # Exit: to exit the gallery and turn off the program
        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Main...", 
                            command= lambda: to_main(self.__game_window))
        file_menu.add_command(label="New Game...", 
                            command= lambda:to_mode_theme(self.__game_window))
        file_menu.add_command(label="Restart...", command= self.restart)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command= self.__game_window.destroy)

        # In the option of menubar, there are 2 options:
        # Gallery: to the gallery view
        # Rules: checking the rules, but timer still run
        opt_menu = Menu(my_menu)
        my_menu.add_cascade(label="Option", menu=opt_menu)
        opt_menu.add_command(label="Gallery...",
                            command= lambda: to_gallery((self.__game_window)))
        opt_menu.add_command(label="Rules...", command= pop_up_rule)

        self.gameboard()
        self.update_time()
        self.__game_window.mainloop()
    
    def update_time(self):
        """
        update timer
        """
        if not self.game_clear():
            # if the game is not finished, then timer still run and update every 1sec
            time_passed = int(time.time() - self.__start_time)
            self.__time_display.config(text="Time: " + str(time_passed) + " sec")
            self.__game_window.after(1000, self.update_time)
        else:
            self.pop_up_ques()

    def gameboard(self):
        """
        Display cards as button on the game board
        """
        # a 2D array of cards is stored
        cards = self.generate_cards()

        # setup background image
        self.__background_image = PhotoImage(file=IMAGE_BG[0])
        # a list of buttons(aka cards)
        buttons = []
        for row in range(self.__row):
            for col in range(self.__col):
                button = Button(self.__game_window, image=self.__background_image,
                                command=lambda row=row, column=col:
                                self.reveal(buttons, row, column, cards))
               
                buttons.append(button)
                button.grid(row=row, column=col)
        # sort from list to 2D list
        buttons = self.list_2_matrix(buttons)

        # Display timer and move counter
        self.__time_display = Label(self.__game_window,
                                    text="Time: 0 sec", font=('Arial',12))
        self.__move_display = Label(self.__game_window,
                                    text="Moved: 0",font=('Arial',12))
        
        self.__time_display.grid(row=self.__row+1,column=0,columnspan=self.__col+1)
        self.__move_display.grid(row=self.__row+2,column=0,columnspan=self.__col+1)


    def list_2_matrix(self, raw_list):
        """
        Change from 1D to 2D list base on the number of collum in each row

        :param raw_list: list, a list of cards or buttons that need to change to 2D list
        """
        set_list = []
        for i in range(0, len(raw_list), self.__col):
            set_list.append(raw_list[i:i + self.__col])
        return set_list


    def generate_cards(self):
        """
        Generate cards randomly from SAMPLE_PIC
        """
        cards = []
        # random index number is stored to a list randomcards
        randomcards = random.sample(list(range(0, SAMPLE_PIC)), k=self.__cards_needed)
        
        # for each index number in randomcards, add images to the list cards
        for i in range(len(randomcards)):
            route = self.__theme + str(randomcards[i]) + '.png'
            image = PhotoImage(file=route)
            cards.append(image)
            cards.append(image)
        
        # random shuffle the order of list
        random.shuffle(cards)

        # change from 1D to 2D list
        cards_generated = self.list_2_matrix(cards)
        return cards_generated
    
    def reveal(self, buttons, row, col, cards):
        """
        After user choose a card to reveal, the method handles display the card
        and compare two cards, if mismatch then hide them again, or remain 
        display if matched

        :param buttons: list, a list of buttons
        :param row: int, index of row
        :param col: int, index of collumn
        :param cards: list, a list of cards
        """

        # move counter is increased and display on the screen
        self.__move_counter +=1
        self.__move_display.config(text="Moved: " + str(self.__move_counter))

        # reveal/change the button image with the actual card image
        buttons[row][col].config(image=cards[row][col])

        # if move counter is even, it means this is the second reveal
        if self.__move_counter % 2 == 0:
            # get the data from save_pic list
            x = self.__save_pic[0]
            y = self.__save_pic[1]

            # compare the first one to the second one
            if cards[row][col] == cards[x][y]:
                # if match, increase the finish_matched
                self.__finish_matched += 1
                # disable two buttons
                buttons[row][col].config(state=DISABLED)
                buttons[x][y].config(state=DISABLED)
            else:
                # if mismatch, then hide the buttons again after 0.5sec
                buttons[row][col].after(500, self.hide_buttons, buttons, row, col, x, y)
            self.__save_pic.clear()
        else:
            # the move counter is odd, this is the first reveal
            # save the parameter of the first image to the save_pic list
            self.__save_pic.append(row)
            self.__save_pic.append(col)


    def hide_buttons(self, buttons, row, col, x, y):
        """
        Hide the card image after mismatch, set them to background image

        :param buttons: list, a list of buttons
        :param row: int, index of row for second card
        :param col: int, index of collumn for second card
        :param x: int, index of row for first card
        :param y: int, index of collumn for first card
        """
        buttons[row][col].config(image=self.__background_image)
        buttons[x][y].config(image=self.__background_image)


    def game_clear(self):
        # check if the finish match is equal to cards needed
        return self.__finish_matched == self.__cards_needed

    def pop_up_ques(self):
        # after game is finished, check if user want to play more
        ask = messagebox.askyesno(title="Success!", 
                    message="Congratulation, you won!\n\nDo you want to play again?")
        if ask == 1:
            # if yes, go back to theme and mode selection
            to_mode_theme(self.__game_window)
        else:
            # if no, go back to main window
            to_main(self.__game_window)

    def restart(self):
        # from menu bar, if user choose restart, then delete everything
        # run the GamePlay class again with the same parameter as the old one
        # in this case, cards are different, timer is reset, move counter is reset
        self.__game_window.destroy()
        GamePlay(self.__row, self.__col, self.__theme)



class Main_Screen:
    """
    The main screen class handle the first screen of the game
    """
    def __init__(self):
        # Creating the window and the components
        self.__main_window = Tk()
        self.__main_window.geometry("+100+20")
        self.__main_window.resizable(0, 0)
        self.__main_window.title("Memory Game")

        # Welcome label to the game
        self.__intro = Label(self.__main_window, text="Welcome to Memory Game",
                        bg="#A2A2CD",fg="#E6E6E6", font=('Arial',21))
        
        # Four buttons for new game, checking rules, checking gallery, and exit
        self.__newgame = Button(self.__main_window, text="New Game",
                        bg="#A2A2CD",fg="#E6E6E6",
                        command= lambda: to_mode_theme(self.__main_window))

        self.__rule = Button(self.__main_window, text="Rules",
                        bg="#A2A2CD",fg="#E6E6E6",command=pop_up_rule)
        
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
        

class Mode_Theme:
    """
    The class handle the user selection of mode and theme
    """
    def __init__(self):
        # Creating the window and the components
        self.__mt_window = Tk()
        self.__mt_window.geometry("+100+20")
        self.__mt_window.resizable(0, 0)
        self.__mt_window.title("New Game")

        # Intro to user
        self.__intro = Label(self.__mt_window, text="Choose mode and theme")
        # back button to return to main window
        self.__button_quit = Button(text= "Back",
                            command= lambda: to_main(self.__mt_window))

        # setup two option menu for mode and theme
        self.__clicked1 = StringVar()
        # set the default option of mode is the first key of dictionary MODE_DICT
        # which is easy mode
        self.__clicked1.set(next(iter(MODE_DICT)))
        intro1 = Label(self.__mt_window, text="Mode")
        choice1 = OptionMenu(self.__mt_window, self.__clicked1, *MODE_DICT)

        
        self.__clicked2 = StringVar()
        # set the default option of theme is the first key of dictionary THEME_DICT
        # which is pokemon theme
        self.__clicked2.set(next(iter(THEME_DICT)))
        intro2 = Label(self.__mt_window, text="Theme")
        choice2 = OptionMenu(self.__mt_window, self.__clicked2, *THEME_DICT)

        # button to start the game
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
        # delete the window to start a new window in GamePlay class
        self.__mt_window.destroy()
        # loop through the THEME_DICT
        for i in THEME_DICT:
            # if user choose any theme that the same as key of the theme
            # dictionary, then the theme is the value of that key
            if self.__clicked2.get() == i:
                theme = THEME_DICT[i]
        
        # loop through the MODE_DICT
        for j in MODE_DICT:
            # if user choose any mode that the same as key of the mode
            # dictionary, then the parameter row and collumn are the
            # first value and last value in integer
            if self.__clicked1.get() == j:
                row = int(MODE_DICT[j][0])
                col = int(MODE_DICT[j][-1])
                # pass the data to GamePlay class
                GamePlay(row, col,theme)

def pop_up_rule():
    # function display rules of the game in a message box
    text = "Click on the cards to see what symbol they uncover and try to find the matching symbol underneath the other cards.\n\n"
    text1 = "Uncover two matching symbols at once to eliminate them.\n\n" 
    text2 = "If two cards are mismatch, they flip over to hide their symbols.\n\n" 
    text3 = "Eliminate all cards as fast as you can to win the game."

    messagebox.showinfo("Rules",text+text1+text2+text3)

def to_main(window):
    # Delete everything in the current window, and start at the Main_Screen class
    window.destroy()
    Main_Screen()

def to_mode_theme(window):
    # Delete everything in the current window, and start at the Mode_Theme class
    window.destroy()
    Mode_Theme()

def to_gallery(window):
    # Delete everything in the current window, and start at the Gallery class
    window.destroy()
    Gallery()       

def main():
    Main_Screen()


if __name__ == "__main__":
    main()
