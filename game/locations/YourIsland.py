from game import location
import game.config as config
from game.display import announce
import random

class YourIsland(location.Location):

    def __init__(self,x,y, world):
        super().__init__(x, y, world)
        self.name = "My island"
        self.symbol = "Y"
        self.visitable = True
        self.starting_location = BeachWithShip(self)
        self.locations = {}
        self.locations["southBeach"] = self.starting_location
        self.locations["shrine"] = Shrine(self)
        self.locations["well"] = Well(self)

    def enter(self,ship):
      announce("You arrive at an island.")

    def visit(self):
      config.the_player.location = self.starting_location
      self.locations["shrine"] = Shrine(self)

class BeachWithShip(location.SubLocation):
  def __init__(self, mainLocation):
    super().__init__(mainLocation)
    self.name = "southBeach"
    self.verbs["north"] = self
    self.verbs["south"] = self

  def process_verb(self,verb, cmd_list, nouns):
    if verb == "north":
      config.the_player.next_location = self.mainLocation.locations["shrine"]
    if(verb == "south"):
      announce("You return to your ship.")
      config.the_player.next_loc = config.the_player.ship
      config.the_player.visiting = False
    elif (verb == "north"):
        config.the_player.next_loc = self.main_location.locations["Srhine"]
    elif (verb == "east"):
        config.the_player.next_loc = self.main_location.locations["well"]
    elif (verb == "west"):
            announce ("Island visited")
        

class Shrine(location.SubLocation):
  def __init__(self, mainLocation):
    super().__init__(mainLocation)
    self.name = "shrine"
    self.verbs["north"] = self
    self.verbs["south"] = self
    self.verbs["west"] = self
    self.verbs["east"] = self
    self.verbs["investigate"] = self

    self.shrineUsed = False

  def enter(self):
    announce("You walk to the top of the hill. A finely crafted shrine sits before you. You walk up to the shrine and gaze at the golden statue.")

  def process_verb(self,verb, cmd_list, nouns):
    if verb == "north":
      config.the_player.next_location = self.mainLocation.locations["yourIsland"]
    if verb == "south":
      config.the_player.next_location = self.mainLocation.locations["yourIsland"]

  def handleShrine(self):
    if (not self.shrineUsed):
      announce("You investigate the shrine and hear a voice in your head")
      announce("You walk up to the shrine and gaze at the golden statue.")
      announce("The statue speaks:")

class Well(location.SubLocation):
  def __init__(self, mainLocation):
    super().__init__(mainLocation)
    self.name = "well"
    self.verbs["north"] = self
    self.verbs["south"] = self
    self.verbs["west"] = self
    self.verbs["east"] = self
    self.verbs["well"] = self

    def enter(self):
        announce("Yo-ho-ho, here is the well captain")

    def process_verb(self,verb, cmd_list, nouns):
        if verb == "west":
          config.the_player.next_location = self.mainLocation.locations["yourIsland"]
        if verb == "east":
          config.the_player.next_location = self.mainLocation.locations["yourIsland"]
        


  def GetRiddleAndAnswer(self):
        riddleList = [("Under a full moon , I throw a yellow hat into th red sea. What happens")]
        return random.choice(list)

    
