import argparse
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def get_webpage(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def get_print_urls(html):
    possible_urls = []
    for a in html.select('a'):
        for string in a.stripped_strings:
            if 'print' in string.lower():
                possible_urls.append(a.get('href'))
    return possible_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape some recipes')
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    
    print("Downloading webpage at '" + args.url)
    raw_html = get_webpage(args.url)
    print("Extracting HTML")
    html = BeautifulSoup(raw_html, 'html.parser')
    print("Searching for printable version")
    urls = get_print_urls(html)
    if (len(urls) > 0):
        print("Printable version found, extracting HTML")
    
        for url in get_print_urls(html):
            print(get_webpage(url))

