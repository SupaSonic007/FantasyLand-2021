#!/usr/local/bin/python3
"""
Character.py - Class definition for RPG Characters

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin
"""

# import required Python modules
import time
import random

######
### Define the attributes and methods available to all characters in the Character
### Superclass. All characters will be able to access these abilities.
### Note: All classes should inherit the 'object' class.
######

class Character:
  """ Defines the attributes and methods of the base Character class """
  
  def __init__(self, char_name=None, app=None, dictVals=None):
    """ Parent constructor - called before child constructors """
    self.name = char_name
    self.app = app
    if dictVals != None:
      self.__dict__.update(dictVals)
      self.__dict__[app].__dict__.update(dictVals[app])
    self.attack_mod = 1.0
    self.defense_mod = 1.0
    self.shield = 0
    self.max_shield = 50
    self.wins = 0
    self.kills = 0
    self.battles = 0
    self.pos = [0,0]
    self.gold = 500
    self.mode = 0
    self.difficulty = 1
    self.manaPotions = 1

  def __str__(self):
    """ string representation of character """
    return str("You are " + self.name + " the " + self.__class__.__name__)

  def move(self):
    """
    Defines any actions that will be attempted before individual
    character AI kicks in - applies to all children
    """
    move_complete = False
    if self.health < 50 and self.potions > 0:
      self.set_stance('d')
      if not self.__class__.__name__ == "Hibbot":
        self.use_potion(1)
      else:
        self.cast_feast()
      move_complete = True
    return move_complete

#### Character Attacking Actions ####
  def flee(self):
    self.app.write("You have fled the battle!")
    self.app.write("")

  def set_stance(self, stance_choice):
    """ sets the fighting stance based on given parameter """
    
    if stance_choice == "a":
      self.attack_mod = 1.3
      self.defense_mod = 0.6
      self.app.write(self.name + " chose aggressive stance.")

    elif stance_choice == "d":
      self.attack_mod = 0.6
      self.defense_mod = 1.3
      self.app.write(self.name + " chose defensive stance.")

    else:
      self.attack_mod = 1.0
      self.defense_mod = 1.0
      self.app.write(self.name + " chose balanced stance.")
    self.app.write("")

  def attack_enemy(self, target):
    ''' Attacks the targeted enemy. Accepts a Character object as the parameter (enemy
    to be targeted). Returns True if target killed, False if still alive.'''

    roll = random.randint(1,20)
    hit = int(roll * self.attack_mod * self.attack)
    
    self.app.write("%s attacks %s." % (self.name, target.name))

    time.sleep(0.6)

    self.app.write("%s rolled a %s, with an attack mod of %s." %(self.name, roll, self.attack_mod))

    time.sleep(0.6)

    crit_roll = random.randint(1, 10)
    if crit_roll == 10:
      hit = hit*2
      self.app.write("%s scores a critical hit! Double damage inflicted!!" %(self.name))
      
      time.sleep(0.6)

    self.app.write("%s dealt %s damage!" %(self.name, hit))

    kill = target.defend_attack(hit, self)
    time.sleep(0.6)

    if kill:
      self.app.write("%s has killed %s." %(self.name, target.name))
      time.sleep(0.6)
      self.app.write("")
      time.sleep(0.6)
      return True      
    else:
      return False

  def defend_attack(self, att_damage, attacker):
    ''' Defends an attack from the enemy. Accepts the "hit" score of the attacking enemy as
    a parameter. Returns True is character dies, False if still alive.'''
    
    # defend roll
    roll = random.randint(1, 20)
    # How much damage is blocked
    block = int((roll * self.defense_mod * self.defense)/3)
        
    # Roll for counter attack - must roll a 20 (5% chance)
    counter_roll = random.randint(1,20)
    if counter_roll == 20:
      self.app.write("%s successfully counter attacks, reflecting 1/2 the damage back onto %s, \nand taking the remaining 1/2 as they rolled a %s for their counter attack roll" %(self.name,attacker.name,counter_roll))
      time.sleep(0.6)
      attacker.health = attacker.health - (att_damage/2)
      self.app.write("")
      self.app.write("%s has %s health remaining" %(attacker.name, attacker.health))
      damage = att_damage/2
      
    else:
      self.app.write("%s rolls a %s for their counter attack roll" %(self.name,counter_roll))
    # Roll for block - must roll a 10 (10% chance)
      block_roll = random.randint(1, 10)
      if block_roll == 10:
        self.app.write("%s successfully blocks the attack, rolling a 10 for their block roll!" %(self.name))
        block = att_damage
        time.sleep(0.6)
      else:
        self.app.write("%s rolls a %s, with a defence modifier of %s" %(self.name, roll, self.defense_mod))
        time.sleep(0.6)
        self.app.write("%s blocks %s damage." %(self.name, block))

      # Calculate damage from attack
      damage = att_damage - block
      if damage < 0:
        damage = 0

      # If character has a shield, shield is depleted, not health
      if self.shield > 0:
        # Shield absorbs all damage if shield is greater than damage
        if damage <= self.shield:
          self.app.write("%s's shield absorbs %s damage." %(self.name, damage))
          time.sleep(0.6)
          self.shield = self.shield - damage
          damage = 0
        # Otherwise some damage will be sustained and shield will be depleted
        elif damage != 0:
          self.app.write("%s's shield absorbs 50 damage." %(self.name))
          time.sleep(0.6)
          damage = damage - self.shield
          self.shield = 0
        
      # Reduce health
    self.app.write("%s suffers %s damage!" %(self.name, damage))
    self.health = self.health - damage
    time.sleep(0.6)
      
    # Check to see if dead or not
    if self.health <= 0:
      self.health = 0
      self.app.write("%s is dead!" %(self.name))
      time.sleep(0.6)
      self.app.write("")
      time.sleep(0.6)
      return True
    else:
      self.app.write("%s has %s hit points left" %(self.name, self.health))
      time.sleep(0.6)
      self.app.write("")
      time.sleep(0.6)
      return False

#### Character Magic Actions ####

  def valid_spell(self, choice):
    ''' Checks to see if the spell being cast is a valid spell i.e. can be cast by
    that race and the character has enough mana '''

    valid = False

    # Determine this character's race
    # This is a built-in property we can use to work out the
    # class name of the object (i.e. their race)
    race = self.__class__.__name__
    
    if choice == 1:
      if (race == "Wizard" or race == "Sorcerer") and self.mana >= 10:
        valid = True
    elif choice == 2 and self.mana >= 20:
      valid = True
    elif choice == 3:
      if (race == "Wizard" or race == "Sorcerer"):
        valid = True
    elif choice == 4:
      if (race == "Hibbot"):
        valid - True
        
    return valid

  def cast_spell(self, choice, target=False):
    ''' Casts the spell chosen by the character. Requires 2 parameters - the spell
    being cast and the target of the spell. '''

    kill = False;

    if choice == 1:
      kill = self.cast_fireball(target)
    elif choice == 2:
      self.cast_shield()
    elif choice == 3:
      self.cast_mana_drain(target)
    elif choice == 4:
      self.cast_feast()
    else:
      self.app.write("Invalid spell choice. Spell failed!")
      self.app.write("")

    return kill

  def cast_fireball(self, target):
    self.mana -= 10
    self.app.write(self.name + " casts Fireball on " + target.name + "!")
    time.sleep(0.6)
      
    roll = random.randint(1, 10)
    defense_roll = random.randint(1, 10)
    damage = int(roll * self.magic) - int(defense_roll * target.resistance)
    if damage < 0:
      damage = 0
      
    if target.shield > 0:
      if damage <= target.shield:
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(0.6)
        target.shield = target.shield - damage
        damage = 0
      elif damage != 0:
        self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
        time.sleep(0.6)
        damage = damage - target.shield
        target.shield = 0
                        
    self.app.write(target.name + " takes " + str(damage) + " damage.")
    self.app.write("")
    time.sleep(0.6)
    target.health = target.health - damage
      
    if target.health <= 0:
      target.health = 0
      self.app.write(target.name + " is dead!")
      self.app.write("")
      time.sleep(0.6)
      return True

    else:
      self.app.write(target.name + " has " + str(target.health) + " hit points left")
      self.app.write("")
      time.sleep(0.6)
      return False

  def cast_shield(self):
    self.mana -= 20
    self.app.write(self.name + " casts Shield!")
    time.sleep(0.6)
    if self.shield <= self.max_shield:
      self.shield = self.max_shield
    self.app.write(self.name + " is shielded from the next " + str(self.shield) + " damage.")
    self.app.write("")
    time.sleep(0.6)

  def cast_mana_drain(self, target):
    self.app.write(self.name + " casts Mana Drain on " + target.name + "!")
    time.sleep(0.6)

    if target.mana >= 20:
      drain = 20
    else:
      drain = target.mana
    self.app.write(self.name + " drains " + str(drain) + " mana from "+ target.name + ".")
    time.sleep(0.6)
      
    target.mana -= drain
    self.mana += drain
    if target.mana <= 0:
      target.mana = 0
      self.app.write(target.name + "'s mana has been exhausted!")
    else:
      self.app.write(target.name + " has " + str(target.mana) + " mana left")
    self.app.write("")

  def cast_feast(self):
     self.app.write("%s pulls an entire feast out of their back pocket!" % self.name)
     self.app.write("%s sits down to eat!" % self.name)
     self.app.write("%s is healed back to full HP!" % self.name)
     self.health = self.max_health
     

#### Character Item Actions ####

  def use_potion(self, potion):
    """
    Uses a health potion if the player has one. Returns True if has potion,
    false if hasn't
    """
    if potion == 1:
      if self.potions >= 1:
        self.potions -= 1
        self.health += 250
        if self.health > self.max_health:
          self.health = self.max_health
        self.app.write(self.name + " uses a health potion!")
        time.sleep(0.6)
        self.app.write(self.name + " has " + str(self.health) + " hit points.")
        self.app.write("")
        time.sleep(0.6)
        return True
      else:
        self.app.write("You have no health potions left!")
        self.app.write("")
        return False
    elif potion == 2:
      if self.manaPotions >= 1:
        self.manaPotions -= 1
        self.mana += 50
        if self.mana > self.max_mana:
          self.mana = self.max_mana
        self.app.write("%s uses a mana potion!" % self.name)
        time.sleep(0.6)
        self.app.write("%s had %s mana" %(self.name, self.mana))
        self.app.write("")
        time.sleep(0.6)
        return True
      else:
        self.app.write("You have no mana potions left!")
        self.app.write("")
        return False
    else:
      self.app.write("Please enter a valid choice!")
      self.app.write("")
      return False

#### Miscellaneous Character Actions ####

  def reset(self):
    ''' Resets the character to its initial state '''
    
    self.health = self.max_health;
    self.mana = self.max_mana;
    #self.potions = self.starting_potions;
    #self.shield = 0
    
  def print_status(self):
    ''' Prints the current status of the character '''
    self.app.write(self.name + "'s Status:")
    time.sleep(0.5)
    
    health_bar = "Health: "
    health_bar += "|"
    i = 0
    while i <= self.max_health:
      if i <= self.health:
        health_bar += "#"
      else:
        health_bar += " "
      i += 25
    health_bar += "| " + str(self.health) + " hp (" + str(int(self.health*100/self.max_health)) +"%)"
    self.app.write(health_bar)
    time.sleep(0.5)
        
    if self.max_mana > 0:
      mana_bar = "Mana: "
      mana_bar += "|"
      i = 0
      while i <= self.max_mana:
        if i <= self.mana:
          mana_bar += "*"
        else:
          mana_bar += " "
        i += 10
      mana_bar += "| " + str(self.mana) + " mp (" + str(int(self.mana*100/self.max_mana)) +"%)"
      self.app.write(mana_bar)
      time.sleep(0.5)
   
    if self.shield > 0:
      shield_bar = "Shield: "
      shield_bar += "|"
      i = 0
      while i <= 100:
        if i <= self.shield:
          shield_bar += "o"
        else:
          shield_bar += " "
        i += 10
      shield_bar += "| " + str(self.shield) + " sp (" + str(int(self.shield*100/self.max_shield)) +"%)"
      self.app.write(shield_bar)
      time.sleep(0.5)   

    self.app.write("Health Potions remaining: %s" %str(self.potions))
    self.app.write("Mana Potions remaining: %s" %str(self.manaPotions))
    self.app.write("")
    time.sleep(0.5)

######
### Define the attributes specific to each of the Character Subclasses.
### This identifies the differences between each race.
######

class Dwarf(Character):
  '''Defines the attributes of a Dwarf in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Dwarf class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 300;
    self.max_mana = 30;
    self.starting_potions = 1;
    self.attack = 9;
    self.defense = 6;
    self.magic = 4;
    self.resistance = 3;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 2

  def move(self, player):
    """ Defines the AI for the Dwarf class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('a')
      return self.attack_enemy(player)
    return False
    
class Elf(Character):
  '''Defines the attributes of an Elf in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Elf class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 200;
    self.max_mana = 60;
    self.starting_potions = 1;
    self.attack = 6;
    self.defense = 5;
    self.magic = 8;
    self.resistance = 5;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 7

  def move(self, player):
    """ Defines the AI for the Elf class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('d')
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Goblin(Character):
  '''Defines the attributes of a Goblin in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Goblin class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 200;
    self.max_mana = 0;
    self.starting_potions = 3;
    self.attack = 8;
    self.defense = 4;
    self.magic = 0;
    self.resistance = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 6

  def move(self, player):
    """ Defines the AI for the Goblin class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('d')
      return self.attack_enemy(player)
    return False

class Hibbot(Character):
  '''Defines the attributes of a Hibbot (Definetely not a hobbit) in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Hibbot class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 250;
    self.max_mana = 40;
    self.starting_potions = 2;
    self.attack = 6;
    self.defense = 8;
    self.magic = 5;
    self.resistance = 5;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 4

  def move(self, player):
    """ Defines the AI for the Hibbot class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('d')
      # Hibbots shield if they don't have one
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Human(Character):
  '''Defines the attributes of a Human in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Human class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 250;
    self.max_mana = 40;
    self.starting_potions = 1;
    self.attack = 8;
    self.defense = 6;
    self.magic = 2;
    self.resistance = 4;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 6

  def move(self, player):
    """ Defines the AI for the Human class """
    move_complete = Character.move(self)
    if not move_complete:
      if self.health*100 / self.max_health > 75:
        self.set_stance('a')
      elif self.health*100 / self.max_health > 30:
        self.set_stance('b')
      else:
        self.set_stance('d')
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Orc(Character):
  '''Defines the attributes of an Orc in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Orc class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 250;
    self.max_mana = 0;
    self.starting_potions = 0;
    self.attack = 9;
    self.defense = 5;
    self.magic = 2;
    self.resistance = 4;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 2

  def move(self, player):
    """ Defines the AI for the Orc class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('b')
      return self.attack_enemy(player)
    return False

class Uruk(Character):
  '''Defines the attributes of an Uruk in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Uruk class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 300;
    self.max_mana = 20;
    self.starting_potions = 1;
    self.attack = 4;
    self.defense = 10;
    self.magic = 2;
    self.resistance = 3;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 1

  def move(self, player):
    """ Defines the AI for the Uruk class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('a')
      return self.attack_enemy(player)
    return False

class Wizard(Character):
  '''Defines the attributes of a Wizard in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Wizard class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 200;
    self.max_mana = 200;
    self.starting_potions = 2;
    self.attack = 5;
    self.defense = 6;
    self.magic = 20;
    self.resistance = 15;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.speed = 4

  def move(self, player):
    """ Defines the AI for the Wizard class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('d')
      if self.mana < 10 and player.mana > 0:
        self.cast_spell(3, player)
      elif self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      elif self.mana >= 10:
        return self.cast_spell(1, player)
      else:
        return self.attack_enemy(player)
    return False

class Sorcerer(Character):
  '''Defines the attributes of a Sorcerer in the game. Inherits the constructor and methods
  of the Character class
  The Sorcerer class is similar to the Wizard class, but takes a more aggressive stance'''
  
  # Constructor for Sorcerer class
  def __init__(self, char_name=None, app=None, dictVals=None):
    Character.__init__(self, char_name, app, dictVals)
    self.max_health = 200;
    self.max_mana = 200;
    self.starting_potions = 2;
    self.attack = 4;
    self.defense = 3;
    self.magic = 22;
    self.resistance = 15;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.speed = 5
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Sorcerer class """
    move_complete = Character.move(self)
    if not move_complete:
      self.set_stance('a')
      if self.mana >= 10 and player.mana > 0:
        self.cast_spell(1, player)
      elif self.health < 75 and self.mana >= 10:
        self.cast_spell(2, player)
      elif self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      elif self.mana >= 10:
        return self.cast_spell(1, player)
      else:
        return self.attack_enemy(player)
    return False
