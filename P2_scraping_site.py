import requests
from bs4 import BeautifulSoup
from P2_scraping_une_catégorie import category_page_scraping
import threading
import time


def site_scraping():
    response = requests.get("http://books.toscrape.com/index.html")
    response.encoding = "utf-8"
    if response.ok:
        dic = dict()
        soup = BeautifulSoup(response.text, features="lxml")
        content = soup.find("ul", {"class": "nav"}).find("ul").findAll("a")
        for a in content:
            key = a.text.replace("\n", "").strip()
            value = a.get("href")
            value = "http://books.toscrape.com/" + value
            dic[key] = threading.Thread(None, category_page_scraping, None, (value, True, True))
        for key in dic:
            dic[key].start()
        for key in dic:
            dic[key].join()
            print(str(key)+" est terminé")
    else:
        return"Une erreur est survenue et le site n'a pas pu être contacté."


if __name__ == "__main__":
    ping = time.time()
    site_scraping()
    pong = time.time()
    print(pong - ping)
