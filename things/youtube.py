from bs4 import BeautifulSoup
import urllib
import requests
import lxml

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36s'


def link(search_term):
    if "youtube.com/watch?v=" in search_term:
        return search_term

    search_term = ' '.join(search_term)
    query = urllib.parse.quote(search_term)
    url = "https://www.youtube.com/results?search_query=" + query
    response = requests.get(url)
    # response = requests.get(url, headers={'User Agent': USER_AGENT})
    soup = BeautifulSoup(response.text, 'lxml')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if '/user/' not in vid['href'] and '?list=' not in vid['href'] and not vid['href'].startswith(
                "https://googleads.g.doubleclick.net/"):
            return 'https://www.youtube.com' + vid['href']
    else:
        raise Exception


def links(search_term):
    """Gets 5 first search results from given terms"""
    c = 0
    search_term = ' '.join(search_term)
    songs = []
    query = urllib.parse.quote(search_term)
    url = "https://www.youtube.com/results?search_query=" + query
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if '?list=' not in vid['href'] and '/user/' not in vid['href'] and not vid['href'].startswith(
                "https://googleads.g.doubleclick.net/"):
            songs.append(['https://www.youtube.com' + vid['href'], vid.contents[-1]])
            c = c + 1
        if c == 5:
            return songs
