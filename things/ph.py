import requests
from bs4 import BeautifulSoup
import lxml
import random


def comment():
    comments = []
    while True:
        page = requests.get('http://www.pornhub.com/random')
        page_soup = BeautifulSoup(page.text, 'lxml')
        try:
            for comment in page_soup.find_all('div', attrs={'class': 'commentMessage'}):
                the_comment = comment.span.text.strip()
                if the_comment == '[[commentMessage]]':
                    continue
                comments.append(the_comment)
            random.seed()
            return comments[random.randint(0, len(comments))] + '\n' + page.url

        except Exception:
            continue

