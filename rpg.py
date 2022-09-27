#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin
"""

import gui
import mapClasses as map
import structure
import os
import gameMethods as gm

app = gui.simpleapp_tk(None)
app.title('RPG Battle')
# Fixed spacing between words
# Start the game by creating the app, and writing in big letters 'Welcome'...
# Welcome message retrieved from https://patorjk.com/software/taag/
app.write('''

▄▄▌ ▐ ▄▌▄▄▄ .▄▄▌   ▄▄·       • ▌ ▄ ·. ▄▄▄ .    ▄▄▄▄▄      
██· █▌▐█▀▄.▀·██•  ▐█ ▌▪▪     ·██ ▐███▪▀▄.▀·    •██  ▪     
██▪▐█▐▐▌▐▀▀▪▄██▪  ██ ▄▄ ▄█▀▄ ▐█ ▌▐▌▐█·▐▀▀▪▄     ▐█.▪ ▄█▀▄ 
▐█▌██▐█▌▐█▄▄▌▐█▌▐▌▐███▌▐█▌.▐▌██ ██▌▐█▌▐█▄▄▌     ▐█▌·▐█▌.▐▌
 ▀▀▀▀ ▀▪ ▀▀▀ .▀▀▀ ·▀▀▀  ▀█▄▀▪▀▀  █▪▀▀▀ ▀▀▀      ▀▀▀  ▀█▄▀▪
▄▄▄   ▄▄▄· ▄▄ •     ▄▄▄▄·  ▄▄▄· ▄▄▄▄▄▄▄▄▄▄▄▄▌  ▄▄▄ .▄▄    
▀▄ █·▐█ ▄█▐█ ▀ ▪    ▐█ ▀█▪▐█ ▀█ •██  •██  ██•  ▀▄.▀·██▌   
▐▀▀▄  ██▀·▄█ ▀█▄    ▐█▀▀█▄▄█▀▀█  ▐█.▪ ▐█.▪██▪  ▐▀▀▪▄▐█·   
▐█•█▌▐█▪·•▐█▄▪▐█    ██▄▪▐█▐█ ▪▐▌ ▐█▌· ▐█▌·▐█▌▐▌▐█▄▄▌.▀    
.▀  ▀.▀   ·▀▀▀▀     ·▀▀▀▀  ▀  ▀  ▀▀▀  ▀▀▀ .▀▀▀  ▀▀▀  ▀    

''')
app.write("You can exit the game at any time by typing in 'quit'")
app.write("")

# Methods moved to gameMethods.py and used through gm.Game (gameMethods imported as gm) object
methods = gm.Game(app)

# Check if saves exist, if so ask to load, else create a new character
if os.path.exists("./save.json"):
    player, Map = methods.askLoad()
    if player == 'n':
        mode = methods.set_mode()
        race = methods.set_race(mode)
        char_name = methods.set_name()
        player = methods.create_player(mode, race, char_name)
        player.mode = mode
        Map = map.Map(app)
        app.write(player)
        app.write("")
        difficulty = methods.set_difficulty()
        battles = player.battles
        wins = player.wins
        kills = player.kills
    else:
        pass
else:
    battles = 0
    wins = 0
    kills = 0

    mode = methods.set_mode()
    race = methods.set_race(mode)
    char_name = methods.set_name()
    player = methods.create_player(mode, race, char_name)
    Map = map.Map(app)
    Map.newChunkY()
    Map.newChunkX(1)
    app.write(player)
    app.write("")
    player.difficulty = methods.set_difficulty()
    player.mode = mode
methods.play(player, Map)
