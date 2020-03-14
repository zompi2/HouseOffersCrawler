import re

def checkForBlacklist(blacklist, word):
    for badword in blacklist:
        if badword in word:
            print("Bad word found: " + badword)
            return True
    return False

def getfloornumberfromstring(string):
    res = re.findall(r'\d+', string)
    if len(res) > 0:
        return res[0]
    return -1