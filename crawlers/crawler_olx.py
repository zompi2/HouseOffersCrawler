from crawlers.crawler import Crawler
import soupmaker

class CrawlerOlx(Crawler):
    pass

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

    def makesoup(self):

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
        url += "search%5Border%5D=created_at%3Adesc"

        return soupmaker.makesoup(url)
    
    def getlinks(self):
        soup = self.makesoup()

        table = soup.find('table', {'summary': 'Ogłoszenia'})
        links = table.find_all('a', {'class' : 'detailsLink'})

        uniquelinks = set()

        for link in links:
            if link['href'] not in uniquelinks:
                uniquelinks.add(link['href'])
        
        return uniquelinks