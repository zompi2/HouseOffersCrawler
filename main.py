import os
import json
import crawlerconstructor
import resultmaker
import globs
from resultmaker import ResultMaker

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

# construct a result maker which will compose and write results to a nice file
rm = ResultMaker()

# for every provider defined in the config
for provider in config["providers"]:

    # create a crawler for a provider
    crawler = crawlerconstructor.ConstructCrawler(provider)

    if crawler:
        # fill the crawler with the filters we want to use
        crawler.buildtypes = config["buildtypes"]
        crawler.topprice = config["topprice"]
        crawler.fromsize = config["fromsize"]
        crawler.floors = config["floors"]
        crawler.rooms = config["rooms"]

        # fill the crawler with blacklist words so it will remove all undesired offers
        crawler.blacklist.keywords = config["blacklist"]["keywords"]
        crawler.blacklist.locations = config["blacklist"]["locations"]
        crawler.blacklist.nolastfloor = config["blacklist"]["nolastfloor"]

        # indicates if we want only new offers or all of them
        readOnlyNewOffers = config["onlynew"]

        # get offers from crawler
        offers = crawler.getoffers(readOnlyNewOffers)
        
        # add offers to a result maker
        rm.addResult(offers, provider)

# create a result
rm.makeResult()

# if there are results
if rm.hasAnyResult() :
    # save a result to file
    rm.saveResultToFile()

    # send to mail if any address is specified
    sendmail = config["sendmail"]
    if len(sendmail) > 0:
        rm.sendResultToMail(sendmail)

print("Scan complete")
