import requests
from bs4 import BeautifulSoup
from P2_scraping_une_catégorie import category_page_scraping
from multiprocessing import Pool


def site_scraping():
    response = requests.get("http://books.toscrape.com/index.html")
    response.encoding = "utf-8"
    if response.ok:
        liste_categories = list()
        soup = BeautifulSoup(response.text, features="lxml")
        content = soup.find("ul", {"class": "nav"}).find("ul").find_all("a")
        for a in content:
            value = a.get("href")
            value = "http://books.toscrape.com/" + value
            liste_categories.append((value, True, True))
        with Pool() as pool:
            pool.starmap(category_page_scraping, liste_categories)
            pool.close()
            pool.join()
    else:
        return"Une erreur est survenue et le site n'a pas pu être contacté."


if __name__ == "__main__":
    print("Le scraping est en cours, patientez quelques minutes.")
    site_scraping()
    print("scraping terminé!")
