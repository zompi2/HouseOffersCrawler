# Creates a result from given offers lists

import os
import time
import globs
import mailsender

class ResultEntry:
    providername = ""
    offerslist = []

    def __init__(self, inProviername, inOfferslist):
        self.providername = inProviername
        self.offerslist = inOfferslist

class ResultMaker:

    results = []
    textresult = ""
    timestamp = ""
    readabletime = ""
    topic = ""

    def addResult(self, offerslist, providername):
        self.results.append(ResultEntry(providername, offerslist))

    def makeResult(self):
        self.timestamp = time.strftime("%Y%m%d%H%M%S")   
        self.readabletime = time.strftime("%d.%m.%Y - %H:%M:%S")

        self.topic = "Offers from: %s" % self.readabletime
        self.textresult = '<h1>Offers in <b>%s</b></h1>\n' % self.readabletime
        for result in self.results:
            self.textresult += '<h2>%s</h2>\n' % result.providername
            for offer in result.offerslist:
                self.textresult += '<p><a href="%s">%s</a></p>\n' % (offer, offer)

    def saveResultToFile(self):
        filename = "result_%s.html" % self.timestamp
        filepath = os.path.join(globs.resultdir, filename)

        file = open(filepath, "w")
        file.write(self.textresult)
        file.close()
        
    def sendResultToMail(self, receivers):
        mailsender.sendMail(receivers, self.topic, self.textresult)
