import game.event as event
import random
import game.combat as combat
import game.crewmate as crew
from game.display import announce

class FinalFight (event.Event):

    def __init__ (self):
        self.name = "skeleton"

    def process (self, world):
        result = {}
        skeleton = ()
        announce("A horde of skeletons comes from underground and charge the crew")
        #combat.Combat([skeleton]).combat()
        announce("Some of the skeletons were killed")
        result["newevents"] = []
        result["message"] = ""
        
        
        return result
