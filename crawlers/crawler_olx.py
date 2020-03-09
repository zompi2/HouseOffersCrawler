from crawlers.crawler import Crawler
import soupmaker

class CrawlerOlx(Crawler):
    pass

    numofpages = -1
    lastoffer = ""
    cachefile = "cache/olxcache"

    def tofloor(self, intvalue):
        return 'floor_' + str(intvalue)

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

    def makesoup(self, page):

        print("Reading page nr " + str(page))

        url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/bydgoszcz?"
 
        #typy:
        i = 0
        for buildtype in self.buildtypes:
            url += "search%5Bfilter_enum_builttype%5D%5B"+str(i)+"%5D="+buildtype+"&"
            i+=1

        #cena:
        url += "search%5Bfilter_float_price%3Ato%5D="+str(self.topprice)+"&"

        #powierzchnia:
        url += "search%5Bfilter_float_m%3Afrom%5D="+str(self.fromsize)+"&"

        #poziomy:
        i = 0
        for floor in self.floors:
            url += "search%5Bfilter_enum_floor_select%5D%5B"+str(i)+"%5D="+self.tofloor(floor)+"&"
            i+=1

        #pokoje:
        i = 0
        for room in self.rooms:
            url += "search%5Bfilter_enum_rooms%5D%5B"+str(i)+"%5D="+self.toroom(room)+"&"
            i+=1

        # sortuj od najnowszych
        url += "search%5Border%5D=created_at%3Adesc&"

        # wybierz strone
        url += "page=" + str(page)

        print("Reading URL: " + url)

        return soupmaker.makesoup(url)
    
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
    
    def checkforfordon(self, soup):
        
        badwords = ["Fordon", "FORDON", "fordon", "Bajka", "BAJKA", "bajka"]
        
        map = soup.find('a', {'href' : '#map'}) #otodom map
        if map:
            for content in map.contents:
                if "Fordon" in content:
                    print("Fordon Found")
                    return True
        
        title = soup.find('div', {'class' : 'offer-titlebox'})
        if title:
            for badword in badwords:
                if badword in title.text:
                    print("Fordon Found")
                    return True

        desc = soup.find('section', {'class' : 'section-description'}) #otodom desc
        if desc:
            ps = desc.findAll('p')
            for p in ps:
                for badword in badwords:
                    if badword in p.text:
                        print("Fordon Found")
                        return True
                        
        desc2 = soup.find('div', {'id' : 'textContent'}) #olx desc
        if desc2:
            for badword in badwords:
                if badword in desc2.text:
                    print("Fordon Found")
                    return True


        return False      

    def checkforfloor(self, soup):
        overview = soup.find('section', {'class' : 'section-overview'})
        if overview:
            points = overview.findAll('li')
            floor = -1
            allfloors = -1
            for point in points:
                if "Piętro: 4" in point.text:
                    floor = 4
                if "Liczba pięter: 4" in point.text:
                    allfloors = 4
            if floor == 4 and allfloors == 4:
                print("Last four floor Found")
                return True
        return False

    def filteroffers(self, offers):
        filteredoffers = []

        idx = 1
        for offer in offers:
            print("checking offer %i / %i" % (idx, len(offers)))
            idx = idx+1
            soup = soupmaker.makesoup(offer)

            # check for Fordon
            if self.checkforfordon(soup) :
                continue     

            # check for last floor (4th)
            if self.checkforfloor(soup) :
                continue

            filteredoffers.append(offer)         

        return filteredoffers

    def getoffers(self, onlynew):

        print("Getting offers fro OLX")

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
