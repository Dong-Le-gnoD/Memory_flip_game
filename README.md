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

![image](https://github.com/Gronderg/Memory_flip_game/assets/117520761/c980cc44-21b8-4d11-b4b8-9b4ca4f8e144)

For starting a new game, firstly user needs to choose which mode and which theme to play, the class
Mode_Theme checks the selection from user and pass the data based on that to the class GamePlay.

![image](https://github.com/Gronderg/Memory_flip_game/assets/117520761/4097fd78-7059-4745-aacc-7fc5f8d21c14)

Inside GamePlay, it handles generate cards randomly from sample cards, display on the screen and 
algorithm to check cards, hide cards, inform time, moves, and inform victory. Every click/move
from user is added to the counter below and timer also runs, only stop when user finish the game.

![image](https://github.com/Gronderg/Memory_flip_game/assets/117520761/3c33a49a-c9c5-4fa2-a9db-37dcdf96d685)

For checking rules, there is a function to popup message box.

![image](https://github.com/Gronderg/Memory_flip_game/assets/117520761/97161942-bf7f-489e-b45e-0085b8462585)

For checking gallery, a class Galley was made to display sameple picture from two themes. The beauty
of the gallery is that user only click forward from beginning and click backward at the end. 

![image](https://github.com/Gronderg/Memory_flip_game/assets/117520761/8460c292-785c-452f-9ebd-f04f09cb0b6d)

![image](https://github.com/Gronderg/Memory_flip_game/assets/117520761/9ddb918b-c302-486c-bbfe-16194388d603)

Except from options on the screen, user also have some options from menu bar, for example: during the
gameplay, user can choose to restart the game from beginning, restart the game with different mode and
theme, back to the main screen, or checking the rules.
