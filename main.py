from crawlers.crawler_olx import CrawlerOlx

print("Hello Home Scanner!")

crawler = CrawlerOlx()

crawler.buildtypes = ['blok', 'apartamentowiec']
crawler.topprice = 380000
crawler.fromsize = 56
crawler.floors = [1,2,3,4,5,6]
crawler.rooms = [3,4]

links = crawler.getlinks()

file = open("testfile.html", "w")
file.write(str(links))
file.close()

print("Scan complete")
