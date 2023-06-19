import json
import requests
# from datetime import datetime

from bs4 import BeautifulSoup

base_url = "https://quotes.toscrape.com"
NAMES_AUTHORS = set()
QUANTITY_PAGES = 10

headers = {'Accept':
'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'User-Agent':
'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}
def get_urls():
    page_urls = []
    for p in range(1, QUANTITY_PAGES+1):
        url = base_url + "/page/" + str(p) + "/"
        page_urls.append(url)
    return page_urls


def about_author(url):
    url_about = base_url + url
    with requests.Session() as session:
        response = session.get(url=url_about, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')

    data = {}
    date = soup.find('span', attrs={"class": "author-born-date"}).text
    description = soup.find('div', attrs={"class": "author-description"}).text
    description = description.strip("\n").strip()
    born_location = soup.find('span', attrs={"class": "author-born-location"}).text
    data.update({"born_date": date, "born_location": born_location, "description":  description})
    return data
    # try:
    #     date = datetime.strptime(date, "%B %d, %Y").isoformat()
    # except ValueError:
    #     print("Error date")
    #     pass

def get_data(urls):
    quotes = []
    authors = []

    with requests.Session() as session:
        for url in urls:
            response = session.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

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
                    NAMES_AUTHORS.add(name_author)
                    author_url = q.find('a')["href"]
                    result = about_author(author_url)
                    authors.append({
                        'fullname': name_author,
                        'born_date': result['born_date'],
                        'born_location': result['born_location'],
                        'description': result['description']
                    })
                # author = {}
                # author["fullname"] = name_author
                # author['born_date'] = result['born_date']
                # author['description'] = result['description']
                # authors.append(author)
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