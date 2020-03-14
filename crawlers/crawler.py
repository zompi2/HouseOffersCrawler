# Base class of a crawler which contains all required data for working crawler.

class Blacklist:
    keywords = []
    locations = []
    nolastfloor = False

    # Checks if there are any blacklist data to check. 
    # Prevents from making request for offer which can't be rejected.
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
 