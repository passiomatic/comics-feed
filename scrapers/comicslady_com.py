def scrape(soup):
    # Locate "list-now" section and subsequent articles
    header_soup = soup.body.find("div", class_="list-now").parent
    items_soup = header_soup.find_next_sibling().find_all("article")
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