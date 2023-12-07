class Island(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Beach(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["lake"] = Lake(self)
        self.locations["hill"] = Hill(self)
