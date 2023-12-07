from game import event
from game.player import Player
from game.context import Context
import game.config as config
from game.display import announce
import random

class CarnivoreFlower(Context, event.Event):
    '''A carnivore plant will attack the pirates if they get too close. Have to use swords to cut them'''
    def __init__(self):
        super().__init__()
        self.name = "YouFoundAFlower"
        self.carnivoreflower = 1
        self.verbs['cut'] = self
        self.verbs['freeze'] = self
        self.result = {}
        self.go = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "cut":
            self.go = True
            r = random.randint(1, 10)
            if r < 5:
                self.result["message"] = "The Carnivore plant is defeated"
                if self.carnivoreflower > 1:
                    self.carnivoreflower -= 1

        elif verb == "freeze":
            c = random.choice(config.the_player.get_pirates())
            self.carnivoreflower += 1
            self.result["newevents"].append(CarnivoreFlower())
            self.result["message"] = "The carnivore flower swallowed one of your crew member"
            deathcause = "test"
            c.inflict_damage(100, deathcause)
            self.go = True
        else:
            self.result["message"] = "Enter 'cut' or 'freeze'"
            self.go = False

    
    def inflict_damage (self, num, deathcause, combat=False):
        '''Injures the pirate. If needed, it will record the pirate's cause of death'''
        if combat and len(self.defenders) > 0:
            defender = random.choice (self.defenders)
            announce (f"{defender.name} blocks the attack!")
            return defender.inflict_damage ((num+1)//2, deathcause, False) #Combat should be false here to avoid possible infinite recursion.
        #else:
        self.health = self.health - num
        self.hurtToday = True
        if(self.health > 0):
            return None
        self.death_cause = deathcause
        for d in self.defendees:
            d.removeDefender(self)
        self.defendees = []
        for d in self.defenders:
            d.removeDefendee(self)
        self.defenders = []
        return self

    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "The Carnivore plant is defeated"


        while (self.go == False):
            announce ("Watch out, there is a carnivore flower")
            Player.get_interaction ([self])

        return self.result
