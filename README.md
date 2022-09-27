# Fantasy-Land
This is a turn based, text based, rpg battle engine implemented using Object Oriented Programming using Python. It is themed around generic fantasy.
You should run the rpg.py file to start the game.

<h1> New Features </h1>

- Added comments
- Changed Hobbit class to Hibbot
- Fixed NameError in gui.py where sys was not imported
- Changed startup message in rpg.py.
- Switched unnecessary try/except statements into if statements
- Fixed the defense stat making the game faster paced.
- Added map feature
- Added a customisable settings file that allows the game to be personalised a little bit,
- Moved methods in rpg.py to gameMethods.py
- Added structures.py which contains the structures referenced in mapClasses.py
- Added new <b>Evil</b> sorcerer class
- Added a save and load feature allowing progress to be made and saved
    - If people feel like it they are able to change the stats in the gameSettings file, but that's up to them
- Added a gold and <i>backpack</i> (sorta) feature
    - Backpack is stat changes and potions which can be purchased in the store
- Speed attribute allows for characters to attack in order of speed
- Changed the health, mana, damage, defence, magic and resist stats on characters to make the game more balanced
- Created new <i>magic</i> ability for hobbits, healing them entirely in place of their turn
    - Also added to their a.i. to use instead of a potion
