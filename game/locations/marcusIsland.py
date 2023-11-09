# imports needed for all islands
from game import location
import game.config as config
from game.display import announce
# island specific imports
import random as r

class island(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "Foggy Island"
        self.symbol = "~"
        self.visitable = True
        self.starting_location = NorthBeach(self)
        self.locations = {}
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
        if verb == "investigate":
            possibilities = ["notice sand", "find locket", "find key", "find skeleton"]
            chance = r.choice(possibilities)
            if chance == "notice sand":
                announce("You notice that there is white sand under the deep fog.")
            elif chance == "find locket":
                announce("You find a rusted but none the less fancy locket.")
            elif chance == "find key":
                announce("You find a key.\nThere is no sign as to what it is for.")
            elif chance == "find skeleton":
                announce("You find a skeleton, almost clean.\nYou feel the hair on your arms stick up.")

class DarkForest(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "The Dark Forest"

    def enter(self):
        announce("You step foot in a strangely dense forest\nYou sense that you are not alone.")
