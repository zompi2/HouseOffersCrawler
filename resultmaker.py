import os
import time
import globs

def makeResult(offerslist, providername):
    currenttime = time.strftime("%d.%m.%Y %H:%M:%S")    
    filename = "result-%s-%s.html" % (providername, currenttime)
    filepath = os.path.join(globs.resultdir, filename)
    file = open(filepath, "w")
    
    file.write('<h1>Offers from <b>%s</b> for <b>%s</b></h1>' % (providername, currenttime))
    for offer in offerslist:
        file.write('<p><a href="%s">%s</a></p>\n' % (offer, offer))
    file.close()