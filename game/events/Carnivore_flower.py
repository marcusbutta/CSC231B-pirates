from game import event
from game.player import Player
from game.context import Context

import game.config as config


class CarnivoreFlower (Context, event.Event):
    '''A carnivore plant will attack the pirates if they get too close. Have to use swords to cut them'''
    def __init__ (self):
        super().__init__()
        self.name = "YouFoundAFlower"
        self.Flower = 1
        self.verbs['cut'] = self
        self.verbs['freeze'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "cut"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "The Carnivore plant is defeated"
                if (self.carnivoreflower > 1):
                    self.carnivoreflower = self.carnivoreflower - 1

        elif (verb == "freeze"):
            self.carnivoreflower = self.carnivoreflower + 1
            self.result["newevents"].append (CarnivoreFlower())
            self.result["message"] = "The carnivore flower swallowed one of your crew member"
            self.go = True
        else:
            announce ("Enter 'cut' or 'freeze'")
            self.go = False

    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            announce ("Watch out, there is a carnivore flower")
            Player.get_interaction ([self])

        return self.result
