from bs4 import BeautifulSoup
import urllib
import requests
import lxml

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36s'


def link(search_term):
    if "youtube.com/watch?v=" in search_term:
        return search_term

    payload = {'search_query': search_term}

    request = requests.get("https://www.youtube.com/results", params=payload)
    soup = BeautifulSoup(request.text, 'lxml')
    # print(request.url)

    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if 'list' not in vid['href'] and 'radio' not in vid['href'] and 'googleads' not in vid['href']:
            return 'https://www.youtube.com' + vid['href']


def links(search_term):
    """Gets 5 first search results from given terms"""
    c = 0
    songs = []
    payload = {'search_query': search_term}
    response = requests.get("https://www.youtube.com/results", params=payload)
    soup = BeautifulSoup(response.text, 'lxml')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if 'list' not in vid['href'] and 'radio' not in vid['href'] and 'googleads' not in vid['href']:
            songs.append(['https://www.youtube.com' + vid['href'], vid.contents[-1]])
            c = c + 1
        if c == 5:
            return songs
