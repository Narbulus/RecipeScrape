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

def get_section(html, keywords, validifiers):
    try:
        for header in html.find_all('h2'):
            for string in header.stripped_strings:
                if any(x in string.lower() for x in keywords):
                    if (contains(header.parent, validifiers)):
                        return header.parent
    except e:
        print("Error " + e)

def get_name(html):
    return None

def get_ingredients(html):
    return None

def get_instructions(html):
    tags = ['ul', 'ol']
    section = get_section(html, ['ingredients', 'steps'], tags)
    return get_list_with_sub(section, tags, 'li')

def contains(html, tags):
    for tag in tags:
        for _ in html.find_all(tag):
            return True
    return False

def get_list_with_sub(section, tags, sub_tag):
    if section:
        _list=[]
        i=1
        for tag in tags:
            for t in section.find_all(tag):
                for elt in t.find_all(sub_tag):
                    if elt.string:
                        _list.append("step " + str(i) + " : " + elt.string)
                        i += 1
                return _list

def parse_recipe(url):
    raw_html = get_webpage(url)
    if raw_html:
        html = BeautifulSoup(raw_html, 'html.parser')
        urls = get_print_urls(html)
        if (len(urls) > 0):
            raw_html_print = get_webpage(urls[0])
            html = BeautifulSoup(raw_html_print, 'html.parser')
        instructions = get_instructions(html)
        if instructions:
            for x in instructions:
                print(x)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape some recipes')
    parser.add_argument('url', type=str)
    args = parser.parse_args()

    print("Downloading webpage at '" + args.url)
    parse_recipe(args.url)

