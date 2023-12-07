from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Pray (Context, event.Event):
    '''The pirates reached the shrine and can either meditate to get more health or skip and keep exploring the island'''
    def __init__ (self):
        super().__init__()
        self.name = "Shrine exploration!"
        self.verbs['meditate'] = self
        self.verbs['skip'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "meditate"):
            self.go = True
            self.result["message"] = "Your crew just acquired the holy protection"
            #Increase the health of all the pirates by 10
            for lucky_pirate in config.the_player.get_pirates():
                    lucky_pirate.health += 10
        elif (verb == "skip"):
            self.go = True
            #config.the_player.next_loc = self.main_location.locations["well"]
            #self.result["newevents"] = [GoNorth()]
        else:
            print ("Enter meditate or skip")
            self.go = False

    def process (self, world):
        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "The crew will skip the prayer"

        while (self.go == False):
            print (str (self.name) + " Do you want to meditate or skip?")
            Player.get_interaction ([self])

        return self.result