import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

base_url = "https://quotes.toscrape.com"
NAMES_AUTHORS = set()
QUANTITY_PAGES = 10


def get_urls():
    page_urls = []
    for p in range(1, QUANTITY_PAGES+1):
        url = base_url + "/page/" + str(p) + "/"
        page_urls.append(url)
    return page_urls


def about_author(url):
    data = {}
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    date = soup.find('span', attrs={"class": "author-born-date"}).text
    # try:
    #     date = datetime.strptime(date, "%B %d, %Y").isoformat()
    # except ValueError:
    #     print("Error date")
    #     pass
    description = soup.find('div', attrs={"class": "author-description"}).text
    description = description.strip("\n").strip()
    born_location = soup.find('span', attrs={"class": "author-born-location"}).text
    data.update({"born_date": date, "born_location": born_location, "description":  description})
    return data


def get_data(urls):
    quotes = []
    authors = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes_div = soup.find_all('div', {"class": "quote"})
        for q in quotes_div:
            quote = q.find('span', attrs={"class": "text"}).string
            name_author = q.find('small', attrs={"class": "author"}).string
            tags_for_quote = [t.text for t in q.find_all('a', attrs={"tag"})]
            quotes.append({
                'quote': quote,
                'author': name_author,
                'tags': tags_for_quote})
            if name_author not in NAMES_AUTHORS:
                author = {}
                NAMES_AUTHORS.add(name_author)
                # author["fullname"] = name_author
                author_url = q.find('a')["href"]
                result = about_author(author_url)
                # author['born_date'] = result['born_date']
                # author['description'] = result['description']
                # authors.append(author)
                authors.append({
                    'fullname': name_author,
                    'born_date': result['born_date'],
                    'born_location': result['born_location'],
                    'description': result['description']
                })
            # quotes.append(quote)
    return quotes, authors


if __name__ == '__main__':
    urls_for_page = get_urls()
    quotes, authors = get_data(urls_for_page)
    for q in quotes:
        print(q)

    with open('quotes.json', 'w', encoding='utf-8') as file:
        json.dump(quotes, file, ensure_ascii=False)
    with open('authors.json', 'w', encoding='utf-8') as file:
        json.dump(authors, file, ensure_ascii=False)

    # spider(urls_for_parsing)


    # print(soup.prettify())
    # print(soup.title.name)   # title
    # print(soup.title.string)   # те, що всередині title - назва Quotes to Scrape
    # print(soup.find_all('span')) # аргумент - назва тегу, який ми шукаємо