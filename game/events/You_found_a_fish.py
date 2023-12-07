from game import event
from game.display import announce
import game.config as config
from game.items import Item
import time

class YouFoundAFish (event.Event):
    '''Once at the Lake, the pirates will start fishing to feed themselves'''

    def __init__ (self):
        self.name = "YouFoundAFish"

    def process (self, world):
        result = {}
        print("Fishing in progress...")
        time.sleep(2)
        result["message"] = "Youhou! Fish for dinner"
        result["newevents"] = [ self ]
        
        announce("You've caught something!")
        #config.the_player.add_to_inventory([Fishbone()])
        
        return result