import argparse
import pprint
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

HEADINGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
LIST_TAGS = ['ul', 'ol']
LIST_ITEM = 'li'
IMG = 'img'

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

def get_list_with_sub(section):
    """given 'section', returns a list (unordered or ordered)"""
    return get_section_with_sub(section, LIST_TAGS, LIST_ITEM)

def get_section_header_with_list(html, keywords):
    """gets an HTML header from 'html' who's content contains at least one of 'keywords' """
    """and optionally has sub-elements in the 'validifiers' list"""
    return get_section_header(html, keywords, LIST_TAGS)

def get_section_header(html, keywords, validifiers):
    """gets an HTML header from 'html' who's content contains at least one of 'keywords'"""
    """and optionally has sub-elements in the 'validifiers' list"""
    return get_section(HEADINGS, html, keywords, validifiers)

def get_section_with_sub(section, tags, sub_tag):
    """given 'section', returns a list of strings of type 'sub_tag' that live beneath one of 'tags'"""
    if section:
        _list=[]
        i=1
        for tag in tags:
            for t in section.find_all(tag):
                if not sub_tag:
                    _list.append(t.string)
                    return _list
                for elt in t.find_all(sub_tag):
                    if elt.stripped_strings:
                        _list.append(''.join(elt.stripped_strings))
                        i += 1
                return _list

def get_section(types, html, keywords, validifiers):
    """Gets an HTML tag from 'html' who's content contains at least one of 'keywords'
    and optionally has sub-elements in the 'validifiers' list
    """
    if not keywords:
        return None
    for _type in types:
        for tag in html.find_all(_type):
            for string in tag.stripped_strings:
                if any(x in string.lower() for x in keywords):
                    if (not validifiers or contains(tag.parent, validifiers)):
                        return tag

def contains(html, tags):
    """returns true if 'html' is a parent to any of 'tags'"""
    for tag in tags:
        for _ in html.find_all(tag):
            return True
    return False

def get_name(url, html):
    """gets the name of the recipe"""
    name_segments = get_name_segments(url)
    if not name_segments:
        return None
    return get_section_header(html, name_segments, None)

def get_name_segments(url):
    """gets all keywords of the recipe title"""
    segmented_url = url.split('/')
    for segment in segmented_url:
        sub_segments = segment.split('-')
        if (len(sub_segments) > 1):
            return sub_segments

def get_ingredients(html):
    section = get_section_header_with_list(html, ['ingredients', 'materials'])
    if section:
        return get_list_with_sub(section.parent)
    return None

def get_instructions(html):
    section = get_section_header_with_list(html, ['directions', 'instructions', 'steps'])
    if section:
        return get_list_with_sub(section.parent)

def get_image_url(url, html):
    name_segments = get_name_segments(url)
    if not name_segments:
        return None

    _best_score = 0
    _best_img = None
    for img in html.find_all('img'):
        _local_score = get_image_score(img, name_segments)
        if _local_score > _best_score:
            _best_img = img.get('src')
    return _best_img

def get_image_score(img, name_segments):
    _local_score = 0
    description = img.get('title')
    if description is None:
        description = img.get('alt')
    if description is None:
        return _local_score

    description = description.lower()
    for word in name_segments:
        if word in description:
            _local_score += 1
    return _local_score

def parse_recipe(url, debug):
    raw_html = get_webpage(url)
    if raw_html:
        html = BeautifulSoup(raw_html, 'html.parser')
        name = get_name(url, html)
        instructions = get_instructions(html)
        ingredients = get_ingredients(html)
        image_url = get_image_url(url, html)
        if not name or not instructions or not ingredients:
            return None
        return  {
            'name': name.string, 
            'instructions': instructions, 
            'ingredients': ingredients, 
            'image_url': image_url
        }

def pprinty(recipe):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(recipe)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape some recipes')
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    recipe = parse_recipe(args.url)
    if recipe:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(recipe)
