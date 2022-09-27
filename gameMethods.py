import json
import os
import math
import battle
import character
import gui
from mapClasses import Chunk, Map
from structure import *


class Game:

    def __init__(self, app):
        # Initialise the methods into an object
        self.app = app

    def set_mode(self):
        """ Select the game mode """
        # This is an error checking version of reading user input
        # This will be explained in class - pay attention!!
        # Understanding try/except cases is important for
        # verifying user input

        # No try/except needed, replaced with isdigit()

        # Choose between evil or good characters

        self.app.write("Please select a side:")
        self.app.write("1. Good")
        self.app.write("2. Evil")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        mode = self.app.inputVariable.get()

        if mode == 'quit':
            self.app.quit()

        if mode.isdigit():
            mode = int(mode)
        else:
            self.app.write("You must enter a valid choice")
            self.app.write("")
            mode = self.set_mode()

        if mode not in range(1, 3):
            self.app.write("You must enter a valid choice")
            self.app.write("")
            mode = self.set_mode()

        return mode

    def set_race(self, mode):
        """ Set the player's race """
        if mode == 2:  # Evil Mode
            self.app.write(
                "Playing as the legally distinct Forces of Not Sauron.")
            self.app.write("")

            # No need for a try/except statement

            # race selection - evil
            self.app.write("Please select your race:")
            self.app.write("1. Goblin")
            self.app.write("2. Orc")
            self.app.write("3. Uruk")
            self.app.write("4. Wizard")
            # Added 5
            self.app.write("5. Sorcerer")
            self.app.write("")
            self.app.wait_variable(self.app.inputVariable)
            race = self.app.inputVariable.get()

            if race == 'quit':
                self.app.quit()

            if race.isdigit():
                race = int(race)
            else:
                self.app.write("You must enter a valid choice")
                self.app.write("")
                race = self.set_race(mode)

            if race not in range(1, 6):
                self.app.write("You must enter a valid choice")
                self.app.write("")
                race = self.set_race(mode)

            return race

        else:  # Good Mode
            self.app.write(
                "Playing as the legally distinct Free Peoples of Just a Little Up from Middle Earth.")
            self.app.write("")

            # No need for a try/except statement

            # race selection - good
            self.app.write("Please select your race:")
            self.app.write("1. Elf")
            self.app.write("2. Dwarf")
            self.app.write("3. Human")
            self.app.write("4. Hibbot")
            self.app.write("5. Wizard")
            self.app.write("")
            self.app.wait_variable(self.app.inputVariable)
            race = self.app.inputVariable.get()

            # Quit command
            if race == 'quit':
                self.app.quit()

            if race.isdigit():
                race = int(race)
            else:
                self.app.write("You must enter a valid choice")
                self.app.write("")
                race = self.set_race(mode)

            # Value must be in list (1-5)
            if race not in range(1, 6):
                self.app.write("You must enter a valid choice")
                self.app.write("")
                race = self.set_race(mode)

            return race

    def set_name(self):
        """ Set the player's name """

        # Input name and return it, unless it's blank or 'quit'
        self.app.write("Please enter your Character Name:")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        char_name = self.app.inputVariable.get()

        if char_name == 'quit':
            self.app.quit()

        if char_name == '':
            self.app.write("")
            self.app.write("Your name cannot be blank")
            char_name = self.set_name()

        return char_name

    def create_player(self, mode, race, char_name):
        """ Create the player's character """

        # Player object is a race object with custom name,
        # It will still have same stats as a.i. of the same race

        # Evil - Mode 2
        if mode == 2:
            if race == 1:
                player = character.Goblin(char_name=char_name, app=self.app)
            elif race == 2:
                player = character.Orc(char_name=char_name, app=self.app)
            elif race == 3:
                player = character.Uruk(char_name=char_name, app=self.app)
            elif race == 4:
                player = character.Wizard(char_name=char_name, app=self.app)
            else:
                # Sorcerer is the new race
                player = character.Sorcerer(char_name=char_name, app=self.app)
        # Good - Mode 1
        else:
            if race == 1:
                player = character.Elf(char_name=char_name, app=self.app)
            elif race == 2:
                player = character.Dwarf(char_name=char_name, app=self.app)
            elif race == 3:
                player = character.Human(char_name=char_name, app=self.app)
            elif race == 4:
                player = character.Hibbot(char_name=char_name, app=self.app)
            else:
                player = character.Wizard(char_name=char_name, app=self.app)
        return player
        # New Player Object Created/Instantiated

    def set_difficulty(self):
        """ Set the difficulty of the game """

        # No try/except needed, using if statement instead
        # Give options and pull input to return difficulty level
        self.app.write("Please select a difficulty level:")
        self.app.write("1 - Easy")
        self.app.write("2 - Medium")
        self.app.write("3 - Hard")
        self.app.write("4 - Legendary")
        # Added 5, 6, 7
        self.app.write("5 - Why would you even try at this point")
        self.app.write("6 - Now you're embarrasing yourself")
        self.app.write("7 - 💀")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        difficulty = self.app.inputVariable.get()

        if difficulty == 'quit':
            self.app.quit()

        if difficulty not in ['1', '2', '3', '4', '5', '6', '7'] or difficulty == '':
            self.app.write("You must enter a valid choice")
            self.app.write("")
            difficulty = self.set_difficulty()

        return int(difficulty)

    # Create enemies method replaced and now in map.py under Structure class

    def quit_game(self, player, map):
        """ Quits the game """
        # Ask if they want to save, then quit
        self.askSave(player, map)
        self.app.quit()

    def save(self, player, map):
        '''
        Save player and map data into save.json file
        '''
        with open("save.json", "w") as f:
            # app atribute data too complex to store, and overriden when loaded anyway
            delattr(player, "app")
            delattr(map, "app")
            for i in range(len(map.chunkList)):
                for j in range(len(map.chunkList[i])):
                    for k in range(len(map.chunkList[i][j])):
                        for l in range(len(map.chunkList[i][j][k])):

                            if not isinstance(map.chunkList[i][j][k][l], str):
                                # app atribute data too complex to store, and overriden when loaded anyway
                                delattr(map.chunkList[i][j][k][l], "app")
                                # Structure attributes and data put into dict form to store in json file
                                # Done first as map.chunk.__dict__ will try putting this obj into dict but cannot serialise
                                map.chunkList[i][j][k][l] = map.chunkList[i][j][k][l].__dict__
            # Map attributes and data put into dict for to store in json file
            #map.chunkList = map.chunkList.__dict__
            # Dump data into file
            json.dump({"Player": player.__dict__, "Map": map.__dict__}, f)

    def load(self):
        '''
        Load the save from save.json
        '''

        # Create a new player and map object to put data back into obj
        player = self.create_player(1, 0, "")
        map = Map()

        with open("save.json", "r") as f:

            data = json.load(f)
            # Load the player data back into the Character object, automatically giving the right stats back
            player.__dict__.update(data["Player"])
            # Load the map data back into the Map object, automatically giving the right data back
            map.__dict__.update(data["Map"])
            map.chunkList
            # Object data written back into object

            for i in range(len(map.chunkList)):

                for j in range(len(map.chunkList[i])):

                    for k in range(len(map.chunkList[i][j])):

                        for l in range(len(map.chunkList[i][j][k])):

                            if not isinstance(map.chunkList[i][j][k][l], str):

                                # Make sure the map objects are the right class
                                clss = map.chunkList[i][j][k][l]["clss"]
                                # Reinstantiates the structures but reupdates the structure data to hold the same data as before the save
                                if clss == "Enemy":

                                    item = map.chunkList[i][j][k][l]
                                    map.chunkList[i][j][k][l] = Enemy(self.app)
                                    map.chunkList[i][j][k][l].__dict__.update(
                                        item)

                                elif clss == "Town":

                                    item = map.chunkList[i][j][k][l]
                                    map.chunkList[i][j][k][l] = Town(self.app)
                                    map.chunkList[i][j][k][l].__dict__.update(
                                        item)

                                elif clss == "LargeTown":

                                    item = map.chunkList[i][j][k][l]
                                    map.chunkList[i][j][k][l] = LargeTown(
                                        self.app)
                                    map.chunkList[i][j][k][l].__dict__.update(
                                        item)

                                elif clss == "Dungeon":

                                    item = map.chunkList[i][j][k][l]
                                    map.chunkList[i][j][k][l] = Dungeon(
                                        self.app)
                                    map.chunkList[i][j][k][l].__dict__.update(
                                        item)

                                elif clss == "Mountain":

                                    item = map.chunkList[i][j][k][l]
                                    map.chunkList[i][j][k][l] = Mountain(
                                        self.app)
                                    map.chunkList[i][j][k][l].__dict__.update(
                                        item)

                                else:

                                    item = map.chunkList[i][j][k][l]
                                    map.chunkList[i][j][k][l] = Structure(
                                        self.app)
                                    map.chunkList[i][j][k][l].__dict__.update(
                                        item)

        # Show that the player has been loaded correctly
        # Print out player stats
        player.print_status()

        return player, map

    def askLoad(self):
        '''
        Ask the user if they would like to load a save
        '''
        self.app.write("Would you like to load a save? (y/n)")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        loadChoice = self.app.inputVariable.get()

        if loadChoice in "yn":

            if loadChoice in "y":

                self.app.write("Loading save now: ")
                self.app.write("")

                return self.load()
            # If they don't want to, returns nothing
            else:

                return loadChoice, loadChoice
        # Choice not valid, rerun
        else:

            self.app.write("Please enter a valid choice")

            return self.askLoad()

    def askSave(self, player, map):
        '''
        Ask the user if they would like to save
        '''
        self.app.write("Would you like to save? (y/n)")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        saveChoice = self.app.inputVariable.get()

        if saveChoice in 'yn':

            if saveChoice == 'y':

                self.save(player, map)
        # If not a valid choice, reask
        else:

            self.askSave(player, map)

    def print_results(self):
        '''
        Print Player Stats To The App Interface
        '''
        # Print battles, wins, kill, success rate and avg. kills p.b. to the app
        self.app.write("No. Battles: {0}".format(str(self.battles)))
        self.app.write("No. Wins: {0}".format(self.wins))
        self.app.write("No. Kills: {0}".format(self.kills))
        self.app.write("Success Rate (%): {0:.2f}%".format(
            float(self.wins*100/self.battles)))
        self.app.write("Avg. kills per battle: {0:.2f}".format(
            float(self.kills)/self.battles))
        self.app.write("")

    def popMap(self, player, map, rerun=False):
        '''
        Display Map With Player Icon On Top
        '''
        item = map.chunkList[math.floor((player.pos[1])/5)][math.floor(
            player.pos[0]/5)][player.pos[1] % 5].pop((player.pos[0]) % 5)
        map.chunkList[math.floor((player.pos[1])/5)][math.floor(player.pos[0]/5)
                                                     ][player.pos[1] % 5].insert((player.pos[0]) % 5, '🕹')
        map.displayMap(self.app)
        map.chunkList[math.floor((player.pos[1])/5)][math.floor(player.pos[0]/5)
                                                     ][player.pos[1] % 5].pop((player.pos[0]) % 5)
        map.chunkList[math.floor((player.pos[1])/5)][math.floor(player.pos[0]/5)
                                                     ][player.pos[1] % 5].insert((player.pos[0]) % 5, item)

        if not isinstance(item, str) and not rerun:
            item.askInteract(player, map)
            self.popMap(player, map, True)

    def move(self, player, map):
        '''
        Move the player with w/a/s/d
        '''
        self.popMap(player, map)
        self.app.write("Where would you like to move? (w/a/s/d/q)")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        choice = self.app.inputVariable.get()
        # Make sure valid choice, else do nothing, this method is run in a while loop for the game to continue running
        if choice in ['w', 'a', 's', 'd','q']:
            if choice == 'w':
                if player.pos[1] != 0:
                    player.pos[1] -= 1

            if choice == 'a':
                if player.pos[0] != 0:
                    player.pos[0] -= 1

            if choice == 's':
                if player.pos[1] < len(map.chunkList)*5:
                    player.pos[1] += 1

            if choice == 'd':
                if player.pos[0] < len(map.chunkList[math.floor(player.pos[1]/5)]*5):
                    player.pos[0] += 1
            
            if choice == 'q':
                self.app.write("Which chunk would you like to quick travel to? ('x y')")
                self.app.write("")
                self.app.wait_variable(self.app.inputVariable)
                choice = self.app.inputVariable.get()
                choice = choice.split()
                while not choice[0].isdigit() and not choice[1].isdigit():
                    self.app.write("You must enter a valid choice...")
                    self.app.write("")
                    self.app.write("Which chunk would you like to quick travel to? ('x y')")
                    self.app.write("")
                    self.app.wait_variable(self.app.inputVariable)
                    choice = self.app.inputVariable.get()
                    choice = choice.split()
                choice[0] = int(choice[0])
                choice[1] = int(choice[1])
                player.pos = choice

        elif choice == 'quit':

            self.quit_game(player, map)

        else:

            self.app.write("Please enter a valid choice!")
            self.app.write("")

    def play(self, player, map):
        '''
        Start the game
        '''
        spawned = False

        while not spawned:
            # Random Spawnpoint unless player has a position already
            if not isinstance(map.chunkList[math.floor((player.pos[1])/5)][math.floor(player.pos[0]/5)][player.pos[1]%5][player.pos[0]%5], str):
                x = random.randrange(0, len(map.chunkList[0][0]))
                y = random.randrange(0, len(map.chunkList[0][0]))
                player.pos = [x, y]
            else:
                spawned = True
            

        playing = True
        # Play until quit
        while playing:
            self.move(player, map)
