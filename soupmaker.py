# Request a page from url and create a proper soup.
# It must pass proper user_agent, otherwise no server will
# trust us.

import urllib.request
from bs4 import BeautifulSoup

def makesoup(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    headers = {'User-Agent':user_agent}

    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)

    data = response.read()
    
    return BeautifulSoup(data, features="html.parser")