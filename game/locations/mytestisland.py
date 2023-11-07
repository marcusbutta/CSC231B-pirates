import random

from game import location
import game.config as config
from game.display import announce
import random as r


class MyTestIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "My Test Island"
        self.symbol = "(●__●)"
        self.visitable = True
        self.starting_location = BeachWithShip(self)
        self.locations = {}
        self.locations["south beach"] = self.starting_location
        self.locations["shrine"] = Shrine(self)

    def enter(self, ship):
        announce("You arrive at an island")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class BeachWithShip(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "south beach"
        self.verbs["north"] = self
        self.verbs["south"] = self

    def enter(self):
        announce("You arrive at a nice beach.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["shrine"]
        if verb == "south":
            announce("You return to the ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False


class Shrine(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "shrine"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["investigate"] = self

        self.shrineUsed = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["south beach"]
        if verb == "investigate":
            self.HandleShrine()

    def HandleShrine(self):
        if not self.shrineUsed:
            announce("You investigate the shrine and hear a strange voice.")
            announce("I am the ghost of this shrine please answer a riddle.")
            choice = input("Do you wish to answer the riddles?")
            if "yes" in choice.lower():
                self.HandleRiddles()
            else:
                announce("You walk away from the shrine.")
        else:
            announce("The shrine has been used.")

    def HandleRiddles(self):
        riddle = self.GetRiddleAndAnswer()
        guesses = 3
        while guesses > 0:
            print(riddle[0])
            plural = ""
            if guesses > 1:
                plural = "s"
            print(f"You have {guesses}{plural} remaining.")
            choice = input("What is your guess?: ")
            announce(choice)

    def GetRiddleAndAnswer(self):
        riddleList = [("Riddle Question", "Riddle Answer")]
        return random.choice(riddleList)
