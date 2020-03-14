import os
import json
import crawlerconstructor
import resultmaker
import globs

print("Hello Home Scanner!")

# read config file
configfile = open("config.json", "r")
if configfile:
    config = json.load(configfile)

# create a cache directory if doesn't already exist
if not os.path.exists(globs.cachedir):
    print("Creating cache directory")
    os.makedirs(globs.cachedir)

# create a result directory if doesn't already exist
if not os.path.exists(globs.resultdir):
    print("Creating result directory")
    os.makedirs(globs.resultdir)

# for every provider defined in the config
for provider in config:

    # create a crawler for a provider
    crawler = crawlerconstructor.ConstructCrawler(provider)

    if crawler:
        # fill the crawler with the filters we want to use
        crawler.buildtypes = config[provider]["buildtypes"]
        crawler.topprice = config[provider]["topprice"]
        crawler.fromsize = config[provider]["fromsize"]
        crawler.floors = config[provider]["floors"]
        crawler.rooms = config[provider]["rooms"]

        # fill the crawler with blacklist words so it will remove all undesired offers
        crawler.blacklist.keywords = config[provider]["blacklist"]["keywords"]
        crawler.blacklist.locations = config[provider]["blacklist"]["locations"]
        crawler.blacklist.nolastfloor = config[provider]["blacklist"]["nolastfloor"]

        # indicates if we want only new offers or all of them
        readOnlyNewOffers = config[provider]["onlynew"]

        # get offers from crawler
        offers = crawler.getoffers(readOnlyNewOffers)
        
        # save offers to a file
        resultmaker.makeResult(offers, provider)

print("Scan complete")
