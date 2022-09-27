#!/usr/local/bin/python3
"""
Battle.py - The battle class manages the events of the battle

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin
"""

# import modules
import sys
import time

class Battle:

  def __init__(self, player, enemies, app):
    """
    Instantiates a battle object between the players and enemies specified,
    sending output to the given gui instance
    """
    self.player = player
    self.enemies = enemies
    self.app = app
    self.turn = 1
    self.wins = 0
    self.kills = 0
    self.player_won = False
    self.player_lost = False
    self.flee = False
  
  def play(self):
    """
    Begins and controls the battle
    returns tuple of (win [1 or 0], no. kills)
    """
    self.player.battles += 1
    while not self.player_won and not self.player_lost:
      
      self.app.write("Turn "+str(self.turn))
      self.app.write("")
      time.sleep(1)
      listOfEntities = [self.player]
      for enemy in self.enemies:
        listOfEntities.append(enemy)
      # Sort by speed
      listOfEntities.sort(key=lambda x: x.speed, reverse=True)
      # This is where the bulk of the battle takes place
      for entity in listOfEntities:
        if not self.flee:
          if not entity in self.enemies:
            self.do_player_actions()
          if not self.flee:
            self.do_enemy_actions(entity)
      if self.flee:
        self.flee = False
        break
          
      
      # advance turn counter
      self.turn += 1
      
    return (self.wins, self.kills)

  def get_action(self):
    """ Gets the player's chosen action for their turn """
    self.app.write(self.player.name + "'s Turn:")
    self.app.write("1. Attack Enemies")
    self.app.write("2. Cast Magic")
    self.app.write("3. Use Potion")
    self.app.write("")
    self.app.wait_variable(self.app.inputVariable)
    player_action = self.app.inputVariable.get()

    if player_action == 'quit':
      self.app.quit()

    if player_action.isdigit():
      player_action = int(player_action)
    else:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      player_action = self.get_action()  

    if player_action not in range(1,4):
      self.app.write("You must enter a valid choice")
      self.app.write("")
      player_action = self.get_action()      

    return player_action

  def choose_potion(self):
    """ Gets the player's chosen potion for their turn """
    self.app.write("Choose your potion:")
    self.app.write("1. Health Potion")
    self.app.write("2. Mana Potion")
    self.app.write("")
    self.app.wait_variable(self.app.inputVariable)
    potion = self.app.inputVariable.get()

    # They might want to quit
    if potion == 'quit':
      self.app.quit()

    # Makes sure choice is valid
    if potion.isdigit():
      potion = int(potion)
    else:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      potion = self.choose_potion()  
    # Makes sure choice is valid
    if potion not in range(1,3):
      self.app.write("You must enter a valid choice")
      self.app.write("")
      potion = self.choose_potion()      

    return potion

  def select_spell(self):
    """ Selects the spell the player would like to cast """
    player_race = self.player.__class__.__name__
    # Wizard and Sorcerer have all options of spells, other classes don't
    self.app.write("Select your spell:")
    if (player_race == "Wizard" or player_race == "Sorcerer") and self.player.mana >= 10:
      self.app.write("1. Fireball (10 mp)")
    if self.player.mana >= 20:
      self.app.write("2. Shield (20 mp)")
    if (player_race == "Wizard" or player_race == "Sorcerer"):
      self.app.write("3. Mana Drain (no mp cost)")
    if (player_race == "Hibbot"):
      self.app.write("4. Feast (no mp cost)")
    self.app.write("0. Cancel Spell")
    self.app.write("")
    self.app.wait_variable(self.app.inputVariable)
    spell_choice = self.app.inputVariable.get()

    # Make sure valid option
    if spell_choice == 'quit':
      self.app.quit()
    if spell_choice.isdigit():
      spell_choice = int(spell_choice)
    else:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      spell_choice = self.select_spell()
      
    if spell_choice == 0:
      return False
    valid_spell = self.player.valid_spell(spell_choice)
    if not valid_spell:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      spell_choice = self.select_spell()
    
    return spell_choice

  def choose_target(self):
    """ Selects the target of the player's action """
    try:
      self.app.write("Choose your target:")
      # use j to give a number option
      j = 0
      # Run through each enemy, write them out and a number that they can be targeted with
      while j < len(self.enemies):
        if self.enemies[j].health > 0:
          self.app.write(str(j) + ". " + self.enemies[j].name)
        j += 1
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      target = self.app.inputVariable.get()

      if target == 'quit':
        self.app.quit()

      # Make sure it's valid
      target = int(target)
      if not (target < len(self.enemies) and target >= 0) or self.enemies[target].health <= 0:
        raise ValueError
    except ValueError:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      target = self.choose_target()

    return target

  def choose_stance(self):
    # Change stats based on stance
    try:
      self.app.write("Choose your stance:")
      self.app.write("a - Aggressive")
      self.app.write("d - Defensive")
      self.app.write("b - Balanced")
      self.app.write("f - Flee Battle")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      stance_choice = self.app.inputVariable.get()

      if stance_choice == 'quit':
        self.app.quit()

      # Use a valid choice
      if stance_choice not in ['a','d','b','f'] or stance_choice == '':
        raise ValueError

    except ValueError:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      stance_choice = self.choose_stance()
    
    return stance_choice

  def do_player_actions(self):
    """ Performs the player's actions """
  
    turn_over = False

    # Keep running through until turn over
    while not self.player_won and not turn_over:

      self.player.print_status()
      # Choose a stance
      stance_choice = self.choose_stance()
      if stance_choice == "f":
        self.player.flee()
        self.flee = True
        break
      else:
        self.player.set_stance(stance_choice)
      
      # Do something!
      player_action = self.get_action()

      has_attacked = False
      # Use a potion
      if player_action == 3:
        
        potion = self.choose_potion()

        has_attacked = self.player.use_potion(potion)
      # Use magic
      elif player_action == 2:
        spell_choice = self.select_spell()

        if spell_choice != 0:
          has_attacked = True
          if spell_choice == 1 or spell_choice == 3:
            target = self.choose_target()
            if self.player.cast_spell(spell_choice, self.enemies[target]):
              self.kills += 1
          else:
            self.player.cast_spell(spell_choice)
      
      # FOR JOSH'S IT ASSIGNMENT!!!!

      else:
        target = self.choose_target()
        has_attacked = True
        # Check for a kill
        if self.player.attack_enemy(self.enemies[target]):
          self.kills += 1
          self.player.kills += 1
          # Kills award gold, and player stat of kills +1
          self.app.write("Enemy Defeated!")
          time.sleep(0.6)
          self.app.write("+%s Gold!" %(int(int(self.player.difficulty)*50)))
          self.player.gold += int(int(self.player.difficulty)*50)
    
      turn_over = True
      if not has_attacked:
        turn_over = False
      else:      
        self.player_won = True
        # Check if won is false, otherwise it stays true
        for enemy in self.enemies:
          if enemy.health > 0:
            self.player_won = False
            break

        if self.player_won == True:
          self.app.write("Your enemies have been vanquished!!")
          # Gold increases by difficulty
          self.app.write("+%s Gold!" %(int(int(self.player.difficulty)*250)))
          self.player.gold += int(int(self.player.difficulty)*250)
          self.app.write("")
          time.sleep(1)
          self.wins += 1
          self.player.wins += 1

  def do_enemy_actions(self, enemy):
    """ Performs the enemies' actions """

    turn_over = False
    # Make sure game's not over
    if not self.player_won:
    
      if enemy.health > 0 and not self.player_lost:
        # Use A.I. to fight back
        if not self.player_lost:
          self.app.write("%s's Turn:" %enemy.name)
          self.app.write("")
          time.sleep(1)
          self.player_lost = enemy.move(self.player)
      # Don't lose...
      if self.player_lost == True:
        self.app.write("You have been killed by your enemies.")
        self.app.write("")
        time.sleep(1)