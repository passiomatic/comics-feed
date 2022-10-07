# A configurable comic sites scraper

Comics Feed is a little Python 3 script that scrapes given web site URL's and produces a RSS feed, ready to be consumed by your feed reader of choice.

![Screenshot](./screenshot.jpg)

_The RSS feed as seen in Reeder app on iOS_

## Install 

```
pip3 install -r requirements.txt
```

## Run

There are two ways to use it:

```
python3 scrape.py http://example.com/ http://example2.com/
python3 scrape.py -i sources.txt
```

In the second line Comics Feed will look into `sources.txt` and fetch one URL per line.

## Add more scrapers

The `scrapers` folder contains a Python module for each web site to scrape, named after its domain name. As an example see the `scrapers/comicslady_com.py` module, which scrapes the ComicsLady.com web site.

Each scraper function receives a [BeautifulSoup object][1] as argument, ready to be navigated, and returns a list of found feed items, using these Python dictionary keys:

```python
{
    'title': "Lorem ipsum"                   # Comic title 
    'link': "http://example.com/..."         # URL for the download or detail page
    'cover': "http://example.com/cover.jpg"  # URL for the cover image, set '' if there's no cover available
}
```

[1]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup