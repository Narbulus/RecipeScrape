from bs4 import BeautifulSoup, NavigableString

HEADING_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
LIST_TAGS = ['ul', 'ol']
LIST_ITEM = 'li'
IMG = 'img'

class BaseParser:
    def __init__(self, tags=None, keywords=None):
        self.tags = tags
        self.keywords = keywords

    def parse(self, html):
        results = self.find(html)
        return self.process_results(results)

    def find(self, html):
        tags = []
        if self.tags:
            tags = html.find_all(self.tags)
        else:
            tags = html.find_all(string=True)
        if self.keywords:
            tags = self.find_keywords(tags)
        return tags

    def process_results(self, results):
        if results:
            return [''.join(tag.stripped_strings) for tag in results]

    def contains(self, haystack, needles):
        return any(n in haystack.lower() for n in needles)

    def find_keywords(self, tags):
        matching_tags = []
        for tag in tags:
            if any(self.contains(s, self.keywords) for s in tag.stripped_strings):
                matching_tags.append(tag)
        return matching_tags

class TitledSectionParser(BaseParser):
    def __init__(self, titles, depth=10):
        super().__init__(tags=HEADING_TAGS, keywords=titles)
        self.titles = titles
        self.depth = depth

    def find(self, html):
        title_tags = super().find(html)
        print("------------------")
        print(title_tags)
        print("------------------")
        for tag in title_tags:
            i = self.depth
            cur = tag
            while i > 0 and cur:
                for sibling in cur.next_siblings:
                    if not isinstance(sibling, NavigableString):
                        print(sibling.prettify())
                        section = self.find_section(sibling)
                        if section:
                            return section
                cur = cur.parent
                i -= 1
                
    def find_section(self, tag):
        pass

class TitledListSectionParser(TitledSectionParser):
    def find_section(self, tag):
        return self.find_section_by_repetition(tag)

    def find_section_by_repetition(self, tag):
        seen = []
        multiples = 0
        print(tag)
        print('///////')
        for child in tag.children:
            print(child)
            print('////child/////')
            if not isinstance(child, NavigableString):
                name = child.get("name")
                if name:
                    if name in seen:
                        multiples += 1
                    else:
                        seen.append(name)
        print('Multiples: ' + str(multiples))
        return []

        
    def find_section_by_tags(self, tag):
        lists = tag.find_all(LIST_TAGS)
        lists.append(tag)
        for list_tag in lists:
            items = list_tag.find_all(LIST_ITEM)
            if len(items) > 0:
                return items

