from game import event

class YouFoundAFish (event.Event):
    '''Once at the Lake, the pirates will start fishing to feed themselves'''

    def __init__ (self):
        self.name = "YouFoundAFish"

    def process (self, world):
        result = {}
        result["message"] = "Youhou! Fish for dinner"
        result["newevents"] = [ self ]
        return result
