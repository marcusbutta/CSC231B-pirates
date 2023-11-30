from game import location
import game.config as config
from game.display import announce
import random
from game.events import *

class IbrasIsland(location.Location):

    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "IbrasIsland"
        self.symbol = 'X'
        self.visitable = True
        self.starting_location = Beach(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["lake"] = Lake(self)
        self.locations["hill"] = Hill(self)
        self.locations["shrine"] = Shrine(self)
        self.locations["well"] = well(self)

    #Make the island walkable 

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach (location.SubLocation):
    def __init__(self, island):
        super().__init__(island)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.visitable = True
        self.description = "You are on a beach."

    def enter (self):
        announce ("You are at the beach, go explore!")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You are back to the ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["lake"]
        elif (verb == "east" or verb == "west"):
            if random.randint(0, 1) == 0:
                announce("You got lost and wandered around for hours. You end up back at the beach.")
            
class Lake (location.SubLocation):
    def __init__(self, island):
        super().__init__(island)
        self.name = "lake"
        self.verbs['south'] = self
        self.visitable = True
        self.description = "You are at a lake."
        self.locations = {}
        self.event_chance = 100
        self.events.append(You_found_a_fish.YouFoundAFish())

    def enter (self):
        announce ("A lake captain!")

        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        elif (verb == "east" or verb == "west"):
            announce ("You can't go this way")

class Hill (location.SubLocation):
    def __init__(self, island):
        super().__init__(island)
        self.name = "hill"
        self.verbs['east'] = self
        self.visitable = True
        self.description = "You are on a hill."
        self.locations = {}
        self.event_chance = 100
        self.events.append(Carnivore_flower.CarnivoreFlower())

    def enter (self):
        announce ("Look, a hill")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["lake"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["shrine"]
        elif (verb == "east" or verb == "west"):
            announce ("You can't go this way")

class Shrine (location.SubLocation):
    def __init__(self, island):
        super().__init__(island)
        self.name = "shrine"
        self.verbs['west'] = self
        self.visitable = True
        self.description = "You are at a shrine."
        self.locations = {}
        #self.event_chance = 10
        #self.events.append(Event("You found a gem", self.event_chance))

    def enter (self):
        announce ("Ha! the shrine is here")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["well"]
        elif (verb == "south" or verb == "west"):
            announce ("You can't go this way")

class well (location.SubLocation):
    def __init__(self, island):
        super().__init__(island)
        self.name = "well"
        self.verbs['north'] = self
        self.visitable = True
        self.description = "You are at the well."
        self.locations = {}
        #self.event_chance = 5
        #self.events.append(Event("You found the treasure", self.event_chance))

    def enter (self):
        announce ("Finally, the well")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["shrine"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations[""]
        elif (verb == "south" or verb == "west"):
            announce ("You can't go this way")
