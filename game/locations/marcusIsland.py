# imports needed for all islands
from game import location
import game.config as config
from game.display import announce
# island specific imports
import random as r
import game.items as items
# enemies
from game.events import drowned_pirates

# Items:
class Dagger(items.Item):
    def __init__(self):
        super().__init__("dagger", 50)
        self.damage = (5, 50)
        self.skill = "swords"
        self.verb = "stab"
        self.verb2 = "stabs"

class Key(items.Item):
    def __init__(self):
        super().__init__("Key", 200)

class Rusted_Locket(items.Item):
    def __init__(self):
        super().__init__("Rusted Locket", 500)
class Fire_Prod(items.Item):
    def __init__(self):
        super().__init__("Fire Prod", 50)
        self.damage = (5, 20)
        self.skill = "melee"
        self.verb = "poke"
        self.verbs = "pokes"
# Global Funcs
def take_item(name, item):
    while True:
        userInput = input("Do you wish to take it?: ")
        if 'yes' in userInput.lower():
            print(f"You take the {name}.")
            config.the_player.add_to_inventory([item])
            break
        if 'no' in userInput.lower():
            print(f"You leave the {name}.")
            break
        else:
            print("Invalid option please try again")
def nav_obstacle(obstacle, compass):
    if obstacle == "cliff":
        announce(f"You attempt to go {compass}, but stumble on a cliff.")
    if obstacle == "ocean":
        announce(f"You attempt to go {compass}, but stumble into open ocean.")


# Locations:

class island(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "Foggy Island"
        self.symbol = "~"
        self.visitable = True
        self.starting_location = NorthBeach(self)
        self.locations = {}
        self.locations["North Shore"] = NorthBeach(self)
        self.locations["Dark Forest"] = DarkForest(self)
        self.locations["Church"] = Church(self)
        self.locations["Graveyard"] = Graveyard(self)
        self.locations["Wood Cabin"] = Wood_Cabin(self)
        self.locations["Field"] = Field(self)
        self.locations["Lighthouse"] = Lighthouse(self)
        self.cultists_triggered = False
    def enter(self, ship):
        announce("You arrive at an island.\nYou find it hard to see.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class NorthBeach(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "North Beach"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["investigate"] = self

    def enter(self):
        announce("You arrive at a beach.\nAt least you think it is a beach, you cannot see the sand.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            announce("You return to the ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["Dark Forest"]
        if verb == "investigate":
            possibilities = ["notice sand", "find locket", "find key", "find skeleton", "flint lock"]
            chance = r.choice(possibilities)
            if chance == "notice sand":
                announce("You notice that there is white sand under the deep fog.")
            elif chance == "find skeleton":
                announce("You find a skeleton, almost clean.\nYou feel the hair on your arms stick up.")
            # item based:
            elif chance == "find locket":
                announce("You find a rusted but none the less fancy locket.")
                take_item("Rusted Locket", Rusted_Locket())
            elif chance == "find key":
                announce("You find a key.\nThere is no sign as to what it is for.")
                take_item("Key", Key())
            elif chance == "flint lock":
                announce("You find a flint lock pistol")
                take_item("Flint Lock", Dagger())
            
class DarkForest(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "The Dark Forest"
        self.event_chance = 0
        self.events.append(drowned_pirates.DrownedPirates())
        # verbs
        self.verbs["investigate"] = self
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self

    def enter(self):
        announce("You step foot in a strangely dense forest\nYou sense that you are not alone.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "investigate":
            announce("You see nothing but trees and moss.")
        elif verb == "north":
            announce("You go back to the North Shore")
            config.the_player.next_loc = self.main_location.locations["North Shore"]
        elif verb == "south":
            announce("You attempt to go south but quickly arrive at a cliff.\nYou will have to find another way.")
        elif verb == "west":
            announce("You head west.")
            config.the_player.next_loc = self.main_location.locations["Church"]
        elif verb == "east":
            announce("You head east.")
            config.the_player.next_loc = self.main_location.locations["Wood Cabin"]

class Church(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Church"
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
    def enter(self):
        announce("You enter a seemingly abandoned church, the door creeks as you open it.")
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            nav_obstacle("ocean", "north")
        if verb == "south":
            announce("You head south.")
            config.the_player.next_loc = self.main_location.locations["Field"]
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["Graveyard"]
        if verb == "east":
            announce("You head east.")
            config.the_player.next_loc = self.main_location.locations["Dark Forest"]

class Graveyard(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Graveyard"
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
    def enter(self):
        announce("You enter a graveyard.")
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["Church"]
        if verb == "north":
            nav_obstacle("ocean", "north")
        if verb == "south":
            nav_obstacle("ocean", "south")
        if verb == "west":
            nav_obstacle("ocean", "west")

class Wood_Cabin(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Wood Cabin"
        self.floors = ["ground", "upstairs", "basement"]
        self.floor = self.floors[0]
        # in cabin nav
        self.verbs["upstairs"] = self
        self.verbs["downstairs"] = self
        # actions
        self.verbs["investigate"] = self
        # global nav
        self.verbs["south"] = self
    def enter(self):
        announce("You find and enter a cabin that appears to be abandoned.\nYou notice the cabin has multiple floors.")
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "upstairs":
            if self.floor == "upstairs":
                announce("You are already on the top floor.")
            else:
                announce("You go upstairs.")
                if self.floor == "ground":
                    self.floor = self.floors[1]
                elif self.floor == "basement":
                    self.floor = self.floors[0]
        if verb == "downstairs":
            if self.floor == "basement":
                announce("You can't go any further down.")
            else:
                announce("You go downstairs")
                if self.floor == "ground":
                    self.floor = self.floors[-1]
                elif self.floor == "upstairs":
                    self.floor = self.floors[0]
        if verb == "investigate":
            if self.floor == "ground":
                announce("The room you are in is warm and comfy, you see embers in the fireplace.")
                announce("You spot a fire prod and mostly burnt piece of paper.")
                announce("You take a closer look at the fire prod.")
                take_item("Fire Prod", Fire_Prod())
                announce("You take a closer look at the piece of paper.")
                userInput = input("Do you wish to attempt to read it?")
                if "yes" in userInput.lower() or "sure" in userInput.lower():
                    announce("You cannot see much but you notice it appears to have been written in a hurry.")
                    announce("It seems to imply something paranormal.")
                else:
                    announce("You leave the paper alone.")
        # global nav
        if verb == "south":
            announce("You head south.")
            config.the_player.next_loc = self.main_location.locations["Lighthouse"]

class Field(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Field"
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
    def enter(self):
        announce("You enter a field with an obelisk in the middle.")
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            announce("You head north.")
            config.the_player.next_loc = self.main_location.locations["Church"]
        if verb == "south":
            nav_obstacle("cliff", "south")
        if verb == "west":
            nav_obstacle("cliff", "west")
        if verb == "east":
            nav_obstacle("cliff", "east")

class Lighthouse(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Lighthouse"
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
    def enter(self):
        announce("You enter a deteriorating lighthouse.")
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            announce("You head north.")
            config.the_player.next_loc = self.main_location.locations["Wood Cabin"]
        if verb == "west":
            announce("You attempt to go west but run into a massive chasm, you turn around.")
        if verb == "east":
            announce("You attempt to go west but there is nothing but ocean.")
        if verb == "south":
            announce("You attempt to go south but there is nothing but ocean.")
