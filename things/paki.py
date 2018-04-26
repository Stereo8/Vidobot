from bs4 import BeautifulSoup
import requests
import lxml


def pakijev_subcount():
    PAKI_URL = 'https://www.youtube.com/channel/UCKi1_NnE9jcTVX_k6oYO-sA'
    SELECTOR = 'span.yt-subscription-button-subscriber-count-branded-horizontal.subscribed.yt-uix-tooltip'
    req = requests.get(PAKI_URL)
    paki_soup = BeautifulSoup(req.text, 'lxml')
    paki_subcount = paki_soup.select(SELECTOR)[0].text.strip()

    return paki_subcount
