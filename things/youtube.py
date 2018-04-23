from bs4 import BeautifulSoup
import urllib
import requests
import lxml

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36s'


def link(search_term):
    search_term = ' '.join(search_term)
    query = urllib.parse.quote(search_term)
    url = "https://www.youtube.com/results?search_query=" + query
    response = requests.get(url, headers={'User Agent': USER_AGENT})
    soup = BeautifulSoup(response.text, 'lxml')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        return 'https://www.youtube.com' + vid['href']
    else:
        raise Exception