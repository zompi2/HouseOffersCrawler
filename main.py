import os
import json
import crawlerconstructor
import resultmaker
import globs

print("Hello Home Scanner!")

configfile = open("config.json", "r")
if configfile:
    config = json.load(configfile)

if not os.path.exists(globs.cachedir):
    print("Creating cache directory")
    os.makedirs(globs.cachedir)

if not os.path.exists(globs.resultdir):
    print("Creating result directory")
    os.makedirs(globs.resultdir)

for provider in config:
    crawler = crawlerconstructor.ConstructCrawler(provider)

    if crawler:
        crawler.buildtypes = config[provider]["buildtypes"]
        crawler.topprice = config[provider]["topprice"]
        crawler.fromsize = config[provider]["fromsize"]
        crawler.floors = config[provider]["floors"]
        crawler.rooms = config[provider]["rooms"]

        crawler.blacklist.keywords = config[provider]["blacklist"]["keywords"]
        crawler.blacklist.locations = config[provider]["blacklist"]["locations"]
        crawler.blacklist.nolastfloor = config[provider]["blacklist"]["nolastfloor"]

        links = crawler.getoffers(config[provider]["onlynew"])
        resultmaker.makeResult(links, provider)

print("Scan complete")
