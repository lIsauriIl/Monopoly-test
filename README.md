# Waterloo Monopoly
Note: This project is in progress.

This is a simplified version of Monopoly but with a twist! Instead of property tiles being places in the UK, they are buildings in the University of Waterloo. The purpose of the game is to provide a fun way for incoming first years to learn about the different buildings and places in UWaterloo.

# Installation and setup
First, install the latest stable python version from here:

https://www.python.org/downloads/

and make sure that you install tkinter during the python installation. This is important as the start menu will not come up without it. Also, make sure that Git is installed. If not installed, install it from the following link:

https://git-scm.com/downloads.

Then, either navigate to your preferred directory in your terminal of choice (Command Line, Terminal, Powershell or Git Bash), and run the following command:
```git clone https://github.com/lIsauriIl/Waterloo-Monopoly```

OPTIONAL but RECOMMENDED: in your code editor/IDE of choice, set up a virtual environment. Different editors have different ways of doing it, so search how to do it with your preferred one. It is recommended as it prevents dependency conflicts that this project might have with other projects you might have on your system.

Afterwards, run this in your terminal of choice:
```pip install -r requirements.txt```

# Running the game
After setup is complete, run Monopoly.py either on the terminal via
```python Monopoly.py```
or via the GUI interface on your editor.

# Features and playing the game
This game is a simplified version of Monopoly, so there are some features removed. The main one is the lack of houses that you can place on owned property. Property tiles are also not colour coded, meaning that you can't achieve a "monopoly", so to speak.

HOWEVER! There is something different to this compared to the original Monopoly. When you click on tiles, a popup appears on the screen, that contains an image of the property as well as information about the property, consisting of a description and rent price. The rolling dice mechanism, property buying, and rent stay the same. Selling is removed for this game, however it might be added in the future.

2 players play at a time. Each player has 2 metrics: Amount and Net Worth. Amount is the liquid cash that each player owns, and controls how much money you have to spend. Net Worth is the Amount in addition to the total value of all properties that the player has bought. The value of a property is equal to its selling price. 

# Win conditions
There are several win conditions. A player wins if:

1. The properties on the board are all owned and they have a higher Net Worth.
2. The other player's Amount goes below 0.

Players can tie if all the properties on the board are owned and both players have an equal Net Worth.

Happy playing!
