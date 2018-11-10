import argparse
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

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

###
# gets an HTML header from 'html' who's content contains at least one of 'keywords'
# and optionally has sub-elements in the 'validifiers' list
###
def get_section_header(html, keywords, validifiers):
    return get_section(headings, html, keywords, validifiers)

###
# gets an HTML tag from 'html' who's content contains at least one of 'keywords'
# and optionally has sub-elements in the 'validifiers' list
###
def get_section(types, html, keywords, validifiers):
    for _type in types:
        for tag in html.find_all(_type):
            for string in tag.stripped_strings:
                if any(x in string.lower() for x in keywords):
                    if (validifiers == None or contains(tag.parent, validifiers)):
                        return tag

### gets the name of the recipe
def get_name(url, html):
    return get_section_header(html, get_name_segments(url), None)

### gets all keywords of the recipe title
def get_name_segments(url):
    segmented_url = url.split('/')
    for segment in segmented_url:
        sub_segments = segment.split('-')
        if (len(sub_segments) > 1):
            return sub_segments

### gets the list of ingredients 
def get_ingredients(html):
    return None

### gets the set of instructions to follow
def get_instructions(html):
    tags = ['ul', 'ol']
    section = get_section_header(html, ['ingredients', 'steps'], tags)
    return get_list_with_sub(section.parent, tags, 'li')

### returns true if 'html' is a parent to any of 'tags'
def contains(html, tags):
    for tag in tags:
        for _ in html.find_all(tag):
            return True
    return False

### given 'section', returns a list of strings of type 'sub_tag' that live beneath one of 'tags'
def get_list_with_sub(section, tags, sub_tag):
    if section:
        _list=[]
        i=1
        for tag in tags:
            for t in section.find_all(tag):
                if (sub_tag == None):
                    _list.append(t.string)
                    return _list
                for elt in t.find_all(sub_tag):
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
        name = get_name(url, html)
        print("Recipe Name: " + name.string)
        instructions = get_instructions(html)
        print("Instructions")
        for x in instructions:
            print('\t' + x)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape some recipes')
    parser.add_argument('url', type=str)
    args = parser.parse_args()

    print("Downloading webpage at '" + args.url)
    parse_recipe(args.url)
