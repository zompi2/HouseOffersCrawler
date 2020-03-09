import os
from crawlers.crawler_olx import CrawlerOlx

print("Hello Home Scanner!")

if not os.path.exists("cache"):
    print("Creating cache directory")
    os.makedirs("cache")

crawler = CrawlerOlx()

crawler.buildtypes = ['blok', 'apartamentowiec']
crawler.topprice = 380000
crawler.fromsize = 56
crawler.floors = [1,2,3,4,5,6]
crawler.rooms = [3,4]

links = crawler.getoffers(True)

file = open("result.html", "w")
for link in links:
    file.write('<p><a href="%s">%s</a></p>\n' % (link, link))
file.close()

print("Scan complete")
