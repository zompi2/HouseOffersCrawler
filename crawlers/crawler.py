class Blacklist:
    keywords = []
    locations = []
    nolastfloor = False
    def shouldcheck(self):
        if len(self.keywords) > 0:
            return True
        if len(self.locations) > 0:
            return True
        if self.nolastfloor == True:
            return True
        return False

class Crawler:
    buildtypes = []
    topprice = 0
    fromsize = 0
    floors = []
    rooms = []
    blacklist = Blacklist()
 