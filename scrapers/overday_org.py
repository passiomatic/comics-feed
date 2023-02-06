def scrape(soup):
    items_soup = soup.find_all(class_="short-item")
    items = []
    for item_soup in items_soup: 
        title_soup = item_soup.find(class_="short-link")
        image_soup = item_soup.find(class_="short-img")
        item = {
            'title': title_soup.string,
            'link': title_soup["href"],
            'cover': image_soup.img["src"]
        }
        items.append(item)
    return items