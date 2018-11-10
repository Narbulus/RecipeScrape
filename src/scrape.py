import requests
import argparse
from BeautifulSoup import BeautifulSoup


parser = argparse.ArgumentParser(description="Give me reci's to NOM on")
parser.add_argument('URL', metavar='url', type=str, nargs='+', help='URL to parse')
args = parser.parse_args()

url = args.URL
response = requests.get(url[0])
html = response.content

soup = BeautifulSoup(html)
for link in soup.findAll('a'):
    print link.prettify()