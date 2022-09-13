def scrape(soup):
    items_soup = soup.find_all("article")
    items = []
    for item_soup in items_soup: 
        title_soup = item_soup.find(class_="entry-title")
        image_soup = item_soup.find("img")
        item = {
            'title': title_soup.string,
            'link': title_soup.a["href"],
            'cover': image_soup['src']
        }
        items.append(item)
    return items