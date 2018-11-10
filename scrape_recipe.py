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

def get_section(html, keywords):
    for header in html.find_all('h2'):
        for string in header.stripped_strings:
            if any(x in string.lower() for x in keywords):
                if (is_valid(header.parent)):
                    return header.parent
    return None

def is_valid(html):
    for ul in html.find_all('ul'):
        return True
    for ul in html.find_all('ol'):
        return True

def get_ingredients(html):
    return None

def get_instructions(html):
    section = get_section(html, ['ingredients', 'steps'])
    i = 1
    for ul in section.find_all('ul'):
        for li in ul.find_all('li'):
            print("step " + str(i) + " : " + li.string)
            i += 1

def get_name(html):
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape some recipes')
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    
    print("Downloading webpage at '" + args.url)
    raw_html = get_webpage(args.url)
    print("Extracting HTML from: " + args.url)
    html = BeautifulSoup(raw_html, 'html.parser')
    print("Searching for printable version")
    urls = get_print_urls(html)
    if (len(urls) > 0):
        print("Printable version found, extracting HTML")
    
    raw_html_print = get_webpage(urls[0])
    html_print = BeautifulSoup(raw_html_print, 'html.parser')
    get_instructions(html_print)

