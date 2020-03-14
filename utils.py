# Some utilities for better offers filtering

import re

# Checks if given word is in the blacklist
def checkForBlacklist(blacklist, word):
    for badword in blacklist:
        if badword in word:
            print("Bad word found: " + badword)
            return True
    return False

# Gets the first number found in string. Used for getting number
# of floors from offer bullet points.
def getfloornumberfromstring(string):
    res = re.findall(r'\d+', string)
    if len(res) > 0:
        return res[0]
    return -1