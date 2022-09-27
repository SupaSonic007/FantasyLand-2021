import random,json,battle,time
import mapClasses
import character as characterType
#from map import TownMap

class Structure:
    '''
    Base Structure class that is built
    off of for all other structure classes
    '''
    def __init__(self, app):

        # Icon shown on map in greyscale
        self.icon = "⨀"
        # Name for interaction with structure
        self.name = "Structure"
        # Pay to enter?
        self.entryCost = 0
        # How many enemies spawn when you enter
        self.numberOfEnemies = 0
        # Can you buy things here
        self.shop = False
        # Is this a dungeon
        self.dungeon = False
        # The app this is associated with
        self.app = app
        # Player speed when in this area
        # out of 1
        self.playerSpeed = 1
        # For loading save, to load back into the right classes
        self.clss = self.__class__.__name__
        
    # Does the user want to interact with the structure?
    def askInteract(self, player, Map):
        self.app.write("Would you like to interact with %s (y/n)?" % self.__class__.__name__)
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        choice = self.app.inputVariable.get()
        if choice in ['y','n']:
            if choice == 'y':
                self.interact(player, Map)

    # Interact with the structure!
    def interact(self, player, Map):
        self.app.write("You interacted with %s!" % self.__class__.__name__)

    def createEnemy(self, mode):
        '''
        Create and return the enemy
        that will be fought against
        '''
        with open("./gameSettings.json","r") as f:
            settings = json.load(f)
            # Custom names/random names
            # gameSettings.json allows player to use custom names
            if mode == 1:
                evilEnemies = settings["Evil Enemies"]
                # Random race
                enemy = random.choice([
                    characterType.Goblin(random.choice(evilEnemies["Goblin Names"]),self.app), 
                    characterType.Orc(random.choice(evilEnemies["Orc Names"]),self.app), 
                    characterType.Sorcerer(random.choice(evilEnemies["Sorcerer Names"]),self.app), 
                    characterType.Uruk(random.choice(evilEnemies["Uruk Names"]),self.app), 
                    characterType.Wizard(random.choice(evilEnemies["Evil Wizard Names"]),self.app)
                    ])
            else:
                goodEnemies = settings["Good Enemies"]
                # Random race
                enemy = random.choice([
                    characterType.Dwarf(random.choice(goodEnemies["Dwarf Names"]), self.app), 
                    characterType.Elf(random.choice(goodEnemies["Elf Names"]), self.app), 
                    characterType.Hibbot(random.choice(goodEnemies["Hibbot Names"]), self.app), 
                    characterType.Human(random.choice(goodEnemies["Human Names"]), self.app), 
                    characterType.Wizard(random.choice(goodEnemies["Good Wizard Names"]), self.app)
                ])

        return enemy

class Enemy(Structure):
    '''
    Enemy structure that will start a battle when interacted with
    '''

    def __init__(self, app):
        super().__init__(app)

        self.icon = '😈'
        self.name = "Enemy"
        # Number of enemies to spawn
        self.numberOfEnemies = random.randint(1,3)
        self.enabled = True
        self.lossMod = 0

    def askInteract(self, player, Map):
        # Wanna interact with them?
        if self.enabled:
            self.app.write("Would you like to interact with %s? (y/n)" % self.__class__.__name__)
            self.app.write("")
            self.app.wait_variable(self.app.inputVariable)
            choice = self.app.inputVariable.get()
            if choice in ['y','n']:
                if choice == 'y':
                    self.interact(player, Map)
        else:
            # Can't fight dead enemies
            self.app.write("You have already defeated these enemies..")
    
    def interact(self, player, Map):
        enemies = []
        # Create enemy objects for number of enemies in the structure
        for i in range(self.numberOfEnemies):
            enemy = self.createEnemy(player.mode)
            enemy.max_health = (enemy.max_health-100 + (player.difficulty*18))-(self.lossMod*50)
            enemy.health = enemy.max_health
            enemy.attack = (abs(enemy.attack - 2) + (player.difficulty))-self.lossMod
            enemy.magic = (abs(enemy.attack - 2) + (player.difficulty))-self.lossMod
            enemy.defense = (abs(enemy.defense - 2) + (player.difficulty))-self.lossMod
            enemy.resistance = (abs(enemy.defense - 2) + (player.difficulty))-self.lossMod
            if enemy.attack <= 2:
                enemy.attack = 3
            if enemy.defense <= 2:
                enemy.defense = 3
            enemies.append(enemy)
        # Battle
        bttl = battle.Battle(player, enemies, self.app)
        wins, kills = bttl.play()
        if wins and kills:
            # Make sure if you lose it isn't counted as a win
            if player.wins < (player.wins + wins):
                player.wins += wins
                self.enabled = False
            else:
                self.lossMod += 1
            player.kills += kills
        # Check for cleared chunk
        cleared = True
        # Loop through chunks, and the structures in each chunk
        for i in range(len(Map.chunkList)):
            for j in range(len(Map.chunkList[i])):
                for k in range(len(Map.chunkList[i][j])):
                    for l in range(len(Map.chunkList[i][j][k])):
                        if not isinstance(Map.chunkList[i][j][k][l], str):
                            if Map.chunkList[i][j][k][l].clss == 'Enemy':
                                if Map.chunkList[i][j][k][l].enabled == True:
                                    cleared = False
                                else:
                                    Map.chunkList[i][j][k][l].icon = '💀'
        if cleared == True:
            xy = ['y']
            # x more likely to be picked when there are more y chunks
            for i in range(len(Map.chunkList)*2):
                xy.append('x')
            xOrY = random.choice(xy)
            if xOrY == 'x':
                lowest = 0
                for i in range(len(Map.chunkList)):
                    if len(Map.chunkList[i])-1 < lowest:
                        lowest = i
                # Place in y level where there are less chunks
                if lowest == 0:
                    Map.newChunkX(1)
                else:
                    Map.newChunkX(lowest+1)
            else:
                Map.newChunkY()


class Town(Structure):

    def __init__(self, app):
        super().__init__(app)
        
        self.icon = '🏘'
        self.name = "Town"
    
    def interact(self, player, Map):
        # Pick a location
        self.app.write("Where would you like to go?")
        self.app.write("")
        self.app.write("1. Shop")
        self.app.write("2. Back")
        self.app.write("<Other places will be coming soon>")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        choice = self.app.inputVariable.get()
        # Validate Location
        if choice in ['1','2']:
            if choice == '1':
                self.store(player)
            elif choice == '2':
                pass
        else:
            self.app.write("Please Enter A Valid Choice!")
            self.app.write("")
            self.interact(player, Map)
    
    def store(self, player):
        # Location: Store
        shopping = True
        # Items to be sold
        items = ["Health Potion - 500","Mana Potion - 500","Attack Charm - 1000","Defence Charm - 1000","Death Charm - 1000", "Speed Charm - 800","Restore my health and mana! - 0"]
        self.app.write("Store Owner: Hello, welcome to my store!")
        time.sleep(0.6)
        self.app.write("Store Owner: Let me show you what I have to offer!")
        time.sleep(0.6)
        self.app.write("")
        # List out items
        while shopping:
            for i in range(len(items)):
                self.app.write("%s. %s"%(i, items[i]))
                num = i
            self.app.write("%s. Back"%str(int(num)+1))
            self.app.write("You have %s gold" % player.gold)
            self.app.write("")
            self.app.wait_variable(self.app.inputVariable)
            choice = self.app.inputVariable.get()
            # Validate choice
            if choice.isdigit():
                if int(choice) < len(items):
                    item, price = items[int(choice)].split('-')
                    item = item.strip()
                    price = price.strip()
                    # Confirmation
                    self.app.write("Would you like to purchase %s for %s gold? (y/n)" %(item, price))
                    time.sleep(0.6)
                    self.app.write("")
                    time.sleep(0.6)
                    self.app.wait_variable(self.app.inputVariable)
                    choice = self.app.inputVariable.get()
                    if choice in ['y','n']:
                        if choice == 'y':
                            if ("%s - %s" %(item, price)) in items:
                                if player.gold >= int(price):
                                    player.gold -= int(price)
                                    # Buy the item
                                    if items.index(("%s - %s" %(item, price))) == 0:
                                        player.potions += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 1:
                                        player.manaPotions += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 2:
                                        player.attack += 1
                                        player.magic += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 3:
                                        player.defence += 1
                                        player.resistance += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 4:
                                        player.health = 0
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 5:
                                        player.speed += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    else:
                                        # Free so refills health and mana without taking money
                                        player.health = player.max_health
                                        player.mana = player.max_mana
                                        self.app.write("Store Owner: <Healing Majik> ")
                                        time.sleep(0.6)
                                        self.app.write("")
                                # Making sure they have enough gold
                                else:
                                    self.app.write("You can't afford that!")
                                    time.sleep(0.6)
                                    self.app.write("")
                # On Leave
                elif int(choice) == len(items):
                    self.app.write("Store Owner: Thank You, Come Again!")
                    time.sleep(0.6)
                    shopping = False
                

class LargeTown(Structure):
    
    def __init__(self, app):
        super().__init__(app)

        self.icon = '🏰'
        self.name = "Large Town"
    
    def interact(self, player, Map):
        # Pick a location
        self.app.write("Where would you like to go?")
        self.app.write("")
        self.app.write("1. Shop")
        self.app.write("2. Back")
        self.app.write("<Other places will be coming soon>")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        choice = self.app.inputVariable.get()
        # Validate Location
        if choice in ['1','2']:
            if choice == '1':
                self.store(player)
            elif choice == '2':
                pass
        else:
            self.app.write("Please Enter A Valid Choice!")
            self.app.write("")
            self.interact(player, Map)
    
    def store(self, player):
        # Location: Store
        shopping = True
        # Items to be sold
        items = ["Health Potion - 500","Mana Potion - 500","Attack Charm - 1000","Defence Charm - 1000","Death Charm - 1000", "Speed Charm - 800","Restore my health and mana! - 0"]
        self.app.write("Store Owner: Hello, welcome to my store!")
        time.sleep(0.6)
        self.app.write("Store Owner: Let me show you what I have to offer!")
        time.sleep(0.6)
        self.app.write("")
        # List out items
        while shopping:
            for i in range(len(items)):
                self.app.write("%s. %s"%(i, items[i]))
                num = i
            self.app.write("%s. Back"%str(int(num)+1))
            self.app.write("You have %s gold" % player.gold)
            self.app.write("")
            self.app.wait_variable(self.app.inputVariable)
            choice = self.app.inputVariable.get()
            # Validate choice
            if choice.isdigit():
                if int(choice) < len(items):
                    item, price = items[int(choice)].split('-')
                    item = item.strip()
                    price = price.strip()
                    # Confirmation
                    self.app.write("Would you like to purchase %s for %s gold? (y/n)" %(item, price))
                    time.sleep(0.6)
                    self.app.write("")
                    time.sleep(0.6)
                    self.app.wait_variable(self.app.inputVariable)
                    choice = self.app.inputVariable.get()
                    if choice in ['y','n']:
                        if choice == 'y':
                            if ("%s - %s" %(item, price)) in items:
                                if player.gold >= int(price):
                                    player.gold -= int(price)
                                    # Buy the item
                                    if items.index(("%s - %s" %(item, price))) == 0:
                                        player.potions += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 1:
                                        player.manaPotions += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 2:
                                        player.attack += 1
                                        player.magic += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 3:
                                        player.defence += 1
                                        player.resistance += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 4:
                                        player.health = 0
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    elif items.index(("%s - %s" %(item, price))) == 5:
                                        player.speed += 1
                                        self.app.write("You bought a %s!" % item)
                                        time.sleep(0.6)
                                        self.app.write("")
                                    else:
                                        # Free so refills health and mana without taking money
                                        player.health = player.max_health
                                        player.mana = player.max_mana
                                        self.app.write("Store Owner: <Healing Majik> ")
                                        time.sleep(0.6)
                                        self.app.write("")
                                # Making sure they have enough gold
                                else:
                                    self.app.write("You can't afford that!")
                                    time.sleep(0.6)
                                    self.app.write("")
                # On Leave
                elif int(choice) == len(items):
                    self.app.write("Store Owner: Thank You, Come Again!")
                    time.sleep(0.6)
                    shopping = False

class Dungeon(Structure):

    def __init__(self, app):
        super().__init__(app)

        self.icon = "🗺"
        self.name = "Dungeon"
    # No way of actually unlocking the dungeon
    # Dungeons will not be in the assignment version of this game
    # Cannot unlock it...
    def interact(self, player, Map):
        self.app.write("The dungeon appears to be locked...")

class Mountain(Structure):
    # Mountains do nothing when interacted with
    def __init__(self, app):
        super().__init__(app)

        self.icon = '🏔'
        self.name = "Mountain"
        self.playerSpeed = 0.6