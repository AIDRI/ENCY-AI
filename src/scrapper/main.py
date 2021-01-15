import sys
import requests
from bs4 import BeautifulSoup


def get_scrapped_content(url):
    result = requests.get(url)
    if result.status_code != 200:
        return {"error": "This website does not allow scraping"}

    html_page = result.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return {"output": output}