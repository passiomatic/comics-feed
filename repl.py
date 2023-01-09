import requests
from bs4 import BeautifulSoup
url = "https://comicslady.com"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
# Do your thing