# Crawle for OLX

from crawlers.crawler import Crawler
import os
import utils
import soupmaker
import globs

class CrawlerOlx(Crawler):
    pass

    numofpages = -1
    lastoffer = ""
    cachefile = os.path.join(globs.cachedir, "olxcache")

    # parse int value to floor id
    def tofloor(self, intvalue):
        return 'floor_' + str(intvalue)


    # parse in value to room id
    def toroom(self, intvalue):
        switcher = {
            1:'one',
            2:'two',
            3:'three',
            4:'four',
            5:'five',
            6:'six'
        }
        return switcher.get(intvalue)


    # constructs a proper https request for specific filters and page and creates a beautiful soup
    # which we will read soon.
    def makesoup(self, page):

        print("Reading page nr " + str(page))

        url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/bydgoszcz?"
 
        #types:
        i = 0
        for buildtype in self.buildtypes:
            url += "search%5Bfilter_enum_builttype%5D%5B"+str(i)+"%5D="+buildtype+"&"
            i+=1

        #price:
        url += "search%5Bfilter_float_price%3Ato%5D="+str(self.topprice)+"&"

        #size:
        url += "search%5Bfilter_float_m%3Afrom%5D="+str(self.fromsize)+"&"

        #floors:
        i = 0
        for floor in self.floors:
            url += "search%5Bfilter_enum_floor_select%5D%5B"+str(i)+"%5D="+self.tofloor(floor)+"&"
            i+=1

        #rooms:
        i = 0
        for room in self.rooms:
            url += "search%5Bfilter_enum_rooms%5D%5B"+str(i)+"%5D="+self.toroom(room)+"&"
            i+=1

        # sort by the newest
        url += "search%5Border%5D=created_at%3Adesc&"

        # select page
        url += "page=" + str(page)

        print("Reading URL: " + url)

        return soupmaker.makesoup(url)
    

    # get links from the page
    def getlinks(self):

        uniquelinks = []

        currentpage = 1

        while currentpage <= self.numofpages or self.numofpages == -1: 
            soup = self.makesoup(currentpage)
            if self.numofpages == -1:
                self.numofpages = len(soup.findAll('span', {'class' : 'item fleft'}))

            table = soup.find('table', {'summary': 'Ogłoszenia'})
            links = table.find_all('a', {'class' : 'detailsLink'})

            for link in links:
                href = link['href']
                if href == self.lastoffer:
                    return uniquelinks
                if href not in uniquelinks:
                    uniquelinks.append(href)

            currentpage = currentpage + 1
        
        return uniquelinks
    
    # filter if the location contains a blacklisted word
    def checkForLocations(self, soup):
        map = soup.find('a', {'href' : '#map'}) #otodom map
        if map:
            for content in map.contents:
                if utils.checkForBlacklist(self.blacklist.locations, content):
                    return True
        return False

    # filter if description contains a blacklisted word
    def checkForKeywords(self, soup):
        title = soup.find('div', {'class' : 'offer-titlebox'})
        if title:
            if utils.checkForBlacklist(self.blacklist.keywords, title.text):
                return True

        desc = soup.find('section', {'class' : 'section-description'}) #otodom description
        if desc:
            ps = desc.findAll('p')
            for p in ps:
                if utils.checkForBlacklist(self.blacklist.keywords, p.text):
                    return True
                        
        desc2 = soup.find('div', {'id' : 'textContent'}) #olx description
        if desc2:
            if utils.checkForBlacklist(self.blacklist.keywords, desc2.text):
                return True

    # filter all offers that are on the last floor
    def checkforfloor(self, soup):
        overview = soup.find('section', {'class' : 'section-overview'})
        if overview:
            points = overview.findAll('li')
            floor = -1
            allfloors = -1
            for point in points:
                if "Piętro" in point.text:
                    floor = utils.getfloornumberfromstring(point.text)
                if "Liczba pięter" in point.text:
                    allfloors = utils.getfloornumberfromstring(point.text)
            if floor == allfloors:
                print("Last floor Found")
                return True
        return False

    # filter all offers
    def filteroffers(self, offers):

        if self.blacklist.shouldcheck() == False:
            return offers

        filteredoffers = []

        idx = 1
        for offer in offers:
            print("checking offer %i / %i" % (idx, len(offers)))
            idx = idx+1
            soup = soupmaker.makesoup(offer)

            # check for blacklisted locations
            if self.checkForLocations(soup) :
                continue     

            # check for blacklisted keywords
            if self.checkForKeywords(soup) :
                continue   

            # check for last floor
            if self.checkforfloor(soup) :
                continue

            filteredoffers.append(offer)         

        return filteredoffers

    # get offers for this provider
    def getoffers(self, onlynew):

        print("Getting offers from OLX")

        cachedoffers = []

        if onlynew:
            try:
                file = open(self.cachefile, "r")
                cachedoffers = file.readlines()
                if len(cachedoffers) > 0 :
                    print("Last found offer was: " + cachedoffers[0])
                    self.lastoffer = cachedoffers[0][:-1]
                    file.close()
            except:
                print("There is no Last offer found")
        else:
            print("Getting all offers")
        
        alloffers = self.getlinks()

        file = open(self.cachefile, "w")
        
        for offer in alloffers:
            file.write('%s\n' % offer)
        for offer in cachedoffers:
             file.write(offer)
        file.close()

        return self.filteroffers(alloffers)
