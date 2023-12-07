# imports needed for all islands
import random

from game import location
import game.config as config
from game.display import announce
# island specific imports
import random as r
import game.items as items
# for cultists
import game.event as event
import game.combat as combat

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
class Token(items.Item):
    def __init__(self):
        super().__init__("Token", 1000)
class Treasure(items.Item):
    def __init__(self):
        super().__init__("Treasure", 1000)
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
# enemies
class Cultists(event.Event):
    def __init__(self):
        self.name = "Cultists attack!"
        super().__init__()
    def process(self, world):
        result = {}
        result["message"] = "The cultists are defeated!"
        cultist_encounter(3, 5)
        return result

def cultist_encounter(minimum, upperLimit):
    monsters = []
    enemyCount = r.randrange(minimum, upperLimit)
    enemyCounter = 1
    letters = "äåæɐĕęïøġɦħɧɮʫşšʨʎ"
    while enemyCounter <= enemyCount:
        name = ""
        clock = 1
        while clock <= r.randrange(3, 8):
            name += r.choice(letters)
            clock += 1
        monsters.append(Cultist(name))
        enemyCounter += 1
    announce("You are being attacked by cultists!")
    combat.Combat(monsters).combat()
            
class Cultist(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["stab"] = ["stabs", random.randrange(50, 60), (10, 15)]
        attacks["screech"] = ["screeches", random.randrange(20, 50), (3, 7)]
        super().__init__(name, r.randrange(10, 25), attacks, 80 + r.randrange(-10, 10))


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
        self.event_chance = 30
        self.events.append(Cultists())
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
        # local nav
        self.areas = ["basement", "back", "main"]
        self.area = self.areas[2]
        self.verbs["move"] = self
        self.verbs["downstairs"] = self
        self.verbs["upstairs"] = self
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        # actions
        self.verbs["investigate"] = self
        # token
        self.token_taken = False
    def enter(self):
        announce("You enter a seemingly abandoned church, the door creeks as you open it.")
        announce("You notice there are multiple rooms and floors.")
    def process_verb(self, verb, cmd_list, nouns):
        # global nav
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
        # local nav
        if verb == "move":
            if self.area == "main":
                announce("You go into the back of the church.")
                self.area = self.areas[1]
            elif self.area == "back":
                announce("You go back to the main room.")
                self.area = self.areas[2]
            else:
                announce("There is only one room on this floor.")
        if verb == "downstairs":
            if self.area == "back":
                announce("You go downstairs.")
                self.area = self.areas[0]
            elif self.area == "main":
                announce("You don't see any means to go downstairs.")
            elif self.area == "basement":
                announce("You are already on the lowest floor")
        if verb == "upstairs":
            if self.area == "basement":
                announce("You go upstairs.")
                self.area = self.areas[1]
            else:
                announce("You are already on the highest floor.")
        # actions
        if verb == "investigate":
            self.investigate_area(area=self.area)
    def investigate_area(self, area):
        if area == "main":
            announce("Most things of value appear to have been taken.")
            announce("The church appears to have a fairly standard layout.")
            announce("You notice there is a room in the back.")
        elif area == "back":
            announce("The room is fairly empty but there appears to be some communion wafers that were not taken by raiders.")
            userInput = input("Do you wish to take it?")
            if "yes" in userInput.lower():
                announce("You take the communion wafers.")
                config.the_player.ship.food += 10
            if "no" in userInput.lower():
                announce("You leave the communion wafers.")
        elif area == "basement":
            announce("The basement appears mostly empty except for a chest in the corner.")
            announce("Upon closer inspection you realize there are some swords surrounding the chest.")
            announce("Do you wish to take them?")
            sword = random.choice([items.Cutlass(), Dagger()])
            amount = 0
            while amount < 3:
                take_item("Sword", sword)
                amount += 1
            if self.token_taken is False:
                announce("You open the chest and find what appears to be a token of some sort.")
                take_item("Token", Token())
                self.token_taken = True
            else:
                announce("You already looked through the chest.")

class Graveyard(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Graveyard"
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        # interactions
        self.verbs["investigate"] = self
        # token
        self.token_taken = False
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
        if verb == "investigate":
            if self.token_taken is False:
                announce("You see a hand reaching out of one of the graves.")
                announce("It appears to be holding something.")
                announce("When you inspect closer you see it seems to be a token of some sort.")
                take_item("Token", Token())
                self.token_taken = True
            else:
                announce("There is nothing more to investigate.")

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
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["north"] = self
        self.verbs["south"] = self
        # items
        self.token_taken = False
        self.treasure_taken = False
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
            self.investigate_area(area=self.floor)
        # global nav
        if verb == "west":
            announce("You head west.")
            config.the_player.next_loc = self.main_location.locations["Dark Forest"]
        if verb == "south":
            announce("You head south.")
            config.the_player.next_loc = self.main_location.locations["Lighthouse"]
        if verb == "north":
            nav_obstacle("ocean", "north")
        if verb == "east":
            nav_obstacle("cliff", "east")
    def investigate_area(self, area):
        if area == "ground":
            announce("The room you are in is warm and comfy, you see embers in the fireplace.")
            announce("You spot a fire prod and mostly burnt piece of paper.")
            announce("You take a closer look at the fire prod.")
            take_item("Fire Prod", Fire_Prod())
            announce("You take a closer look at the piece of paper.")
            userInput = input("Do you wish to attempt to read it?: ")
            if "yes" in userInput.lower() or "sure" in userInput.lower():
                announce("You cannot see much but you notice it appears to have been written in a hurry.")
                announce("It seems to imply something paranormal.")
            else:
                announce("You leave the paper alone.")
        if area == "upstairs":
            if self.token_taken is False:
                announce("The upstairs appears to be mostly empty, except for the corpse of an old man in a chair.")
                announce("He appears to have a token in his hand.")
                take_item("Token", Token())
                self.token_taken = True
            else:
                announce("There is nothing more to investigate.")
        if area == "basement":
            if self.treasure_taken is False:
                announce("As you go downstairs your jaw drops.")
                announce("You see the most treasure you have ever seen in one room.")
                announce("A creaky voice suddenly permeates through the room.")
                announce('"YOU MAY ONLY TAKE 3"')
                userInput = input("Do you wish to listen to the voice?: ")
                if "yes" in userInput.lower():
                    announce("You take 3 treasures.")
                    amount = 0
                    while amount < 3:
                        config.the_player.add_to_inventory([Treasure()])
                        amount += 1
                    self.treasure_taken = True
                elif "no" in userInput.lower():
                    announce("You take all the treasure.")
                    amount = 0
                    while amount < 10:
                        config.the_player.add_to_inventory([Treasure()])
                        amount += 1
                    self.treasure_taken = True
                    cultist_encounter(5, 15)
            else:
                announce("You have already taken all the treasure.")
                announce("There is nothing else to investigate.")

class Field(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Field"
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self
        self.game = Monolith()
    def enter(self):
        announce("You enter a field with an monolith in the middle.")
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            announce("You head north.")
            config.the_player.next_loc = self.main_location.locations["Church"]
        elif verb == "south":
            nav_obstacle("cliff", "south")
        elif verb == "west":
            nav_obstacle("cliff", "west")
        elif verb == "east":
            nav_obstacle("cliff", "east")
        elif verb == "investigate":
            announce("You approach the monolith.")
            self.game.play()


class Lighthouse(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Lighthouse"
        # global nav
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        # interactions
        self.verbs["investigate"] = self
        # token
        self.token_taken = False
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
        if verb == "investigate":
            if self.token_taken is False:
                announce("On the bottom of the ladder you notice a strange locket looking item.")
                announce("Upon closer inspection it appears to be a token turned into a necklace.")
                take_item("Token", Token())
                self.token_taken = True
            else:
                announce("There is nothing else to investigate.")

# puzzle
class Monolith:
    def __init__(self):
        self.slots = 3
        self.completed = False
    def word_search(self):
        words = ["treasure", "island", "pirates", "ship", "crewmate", "jolly"]
        alphabet = "qwertyuiopasdfghjklzxcvbnm"
        word = words[r.randrange(0, 6)]
        lines = []
        letter_index = 0
        for letter in word:
            line = []
            for x in range(len(word)):
                line += r.choice(alphabet)
            line.pop(letter_index)
            line.insert(letter_index, letter)
            line = "".join(line)
            lines.append(line)
            letter_index += 1
        r.shuffle(lines)
        print("---------------")
        for line in lines:
            print(line)
        print("---------------")
        announce("There is a word hidden in the above text.")
        announce("It is read left to right.")
        announce("You have three guesses.")
        guesses = 3
        while guesses > 0:
            userInput = input("What is your guess?: ")
            if userInput == word:
                self.treasure()
                break
            else:
                announce(f"Incorrect guess, you have {guesses} remaining.")
    def treasure(self):
        if self.completed is False:
            for x in range(20):
                config.the_player.add_to_inventory([Treasure()])
            announce("Congrats on finishing the puzzle.")
            announce("You have been gained 20 treasure.")
            announce("Have safe travels!")
            self.completed = True
            self.leave()
        else:
            announce("You have completed this puzzle before.")
            announce("You can only get the treasure once.")
            self.leave()
    def inv_check(self):
        clock = 0
        token_status = False
        for x in config.the_player.inventory:
            x = str(x)
            if "token" in x.lower():
                token_status = True
                token_index = clock
            clock += 1
        if token_status is True:
            config.the_player.inventory.pop(token_index)
            self.slots -= 1
            announce("You insert a token into one of the slots.")
            announce(f"You have {self.slots} remaining.")
            return True
        else:
            announce("You do not have a token to insert.")
            announce(f"You have {self.slots} slots remaining.")
            return False

    def leave(self):
        announce("You leave the monolith alone for now.")

    def play(self):
        announce("There appears to be three circular indents in the Monolith.")
        announce("Maybe you could place something in them?")
        while True:
            if self.slots == 0:
                announce("All slot have tokens.")
                userInput = input("Do you wish to play a puzzle?: ")
                if "yes" in userInput.lower():
                    self.word_search()
                else:
                    self.leave()
            userInput = input("Do you wish to do anything?: ")
            if 'token' in userInput.lower():
                status = self.inv_check()
                if status is False:
                    self.leave()
                    break
            elif 'no' in userInput.lower():
                self.leave()
                break
