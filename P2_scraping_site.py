import requests
from bs4 import BeautifulSoup
from P2_scraping_une_catégorie import category_page_scraping


def site_scraping():
    response = requests.get("http://books.toscrape.com/index.html")
    response.encoding = "utf-8"
    if response.ok:
        dic = dict()
        soup = BeautifulSoup(response.text, features="lxml")
        content = soup.find("ul", {"class": "nav"}).find("ul").findAll("a")
        for a in content:
            key = a.text.replace("\n", "").replace("  ", "")
            if key.startswith(" "):
                key = key[1:]
            if key.endswith(" "):
                key = key[:-2]
            value = a.get("href")
            value = "http://books.toscrape.com/" + value
            dic[key] = value
        for key in dic:
            print("Je suis en train de m'occuper de {catégorie}".format(catégorie=key))
            category_page_scraping(dic[key], getpic=True)
    else:
        return"Une erreur est survenue et le site n'a pas pu être contacté."


if __name__ == "__main__":
    site_scraping()
