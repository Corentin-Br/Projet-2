import requests
from bs4 import BeautifulSoup
from P2_scraping_une_page import fatal, page_scraping
from os import mkdir

all_categories = {'travel': 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html',
                  'mystery': 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
                  'historical fiction': 'http://books.toscrape.com/catalogue/category/books/historical-fiction_4'
                                        '/index.html',
                  'sequential art': 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html',
                  'classics': 'http://books.toscrape.com/catalogue/category/books/classics_6/index.html',
                  'philosophy': 'http://books.toscrape.com/catalogue/category/books/philosophy_7/index.html',
                  'romance': 'http://books.toscrape.com/catalogue/category/books/romance_8/index.html',
                  'womens fiction': 'http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html',
                  'fiction': 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html',
                  'childrens': 'http://books.toscrape.com/catalogue/category/books/childrens_11/index.html',
                  'religion': 'http://books.toscrape.com/catalogue/category/books/religion_12/index.html',
                  'nonfiction': 'http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html',
                  'music': 'http://books.toscrape.com/catalogue/category/books/music_14/index.html',
                  'default': 'http://books.toscrape.com/catalogue/category/books/default_15/index.html',
                  'science fiction': 'http://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html',
                  'sports and games': 'http://books.toscrape.com/catalogue/category/books/sports-and-games_17/index'
                                      '.html',
                  'add a comment': 'http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html',
                  'fantasy': 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html',
                  'new adult': 'http://books.toscrape.com/catalogue/category/books/new-adult_20/index.html',
                  'young adult': 'http://books.toscrape.com/catalogue/category/books/young-adult_21/index.html',
                  'science': 'http://books.toscrape.com/catalogue/category/books/science_22/index.html',
                  'poetry': 'http://books.toscrape.com/catalogue/category/books/poetry_23/index.html',
                  'paranormal': 'http://books.toscrape.com/catalogue/category/books/paranormal_24/index.html',
                  'art': 'http://books.toscrape.com/catalogue/category/books/art_25/index.html',
                  'psychology': 'http://books.toscrape.com/catalogue/category/books/psychology_26/index.html',
                  'autobiography': 'http://books.toscrape.com/catalogue/category/books/autobiography_27/index.html',
                  'parenting': 'http://books.toscrape.com/catalogue/category/books/parenting_28/index.html',
                  'adult fiction': 'http://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html',
                  'humor': 'http://books.toscrape.com/catalogue/category/books/humor_30/index.html',
                  'horror': 'http://books.toscrape.com/catalogue/category/books/horror_31/index.html',
                  'history': 'http://books.toscrape.com/catalogue/category/books/history_32/index.html',
                  'food and drink': 'http://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html',
                  'christian fiction': 'http://books.toscrape.com/catalogue/category/books/christian-fiction_34/index'
                                       '.html',
                  'business': 'http://books.toscrape.com/catalogue/category/books/business_35/index.html',
                  'biography': 'http://books.toscrape.com/catalogue/category/books/biography_36/index.html',
                  'thriller': 'http://books.toscrape.com/catalogue/category/books/thriller_37/index.html',
                  'contemporary': 'http://books.toscrape.com/catalogue/category/books/contemporary_38/index.html',
                  'spirituality': 'http://books.toscrape.com/catalogue/category/books/spirituality_39/index.html',
                  'academic': 'http://books.toscrape.com/catalogue/category/books/academic_40/index.html',
                  'self help': 'http://books.toscrape.com/catalogue/category/books/self-help_41/index.html',
                  'historical': 'http://books.toscrape.com/catalogue/category/books/historical_42/index.html',
                  'christian': 'http://books.toscrape.com/catalogue/category/books/christian_43/index.html',
                  'suspense': 'http://books.toscrape.com/catalogue/category/books/suspense_44/index.html',
                  'short stories': 'http://books.toscrape.com/catalogue/category/books/short-stories_45/index.html',
                  'novels': 'http://books.toscrape.com/catalogue/category/books/novels_46/index.html',
                  'health': 'http://books.toscrape.com/catalogue/category/books/health_47/index.html',
                  'politics': 'http://books.toscrape.com/catalogue/category/books/politics_48/index.html',
                  'cultural': 'http://books.toscrape.com/catalogue/category/books/cultural_49/index.html',
                  'erotica': 'http://books.toscrape.com/catalogue/category/books/erotica_50/index.html',
                  'crime': 'http://books.toscrape.com/catalogue/category/books/crime_51/index.html',
                  }


def creer_dossier(nom):
    try:
        mkdir(nom)
    except FileExistsError:
        pass


def category_page_scraping(url_category, first_pass=True, getpic=False):
    global all_categories
    if url_category.lower() in all_categories:
        url_category = all_categories[url_category.lower()]
    if not url_category.startswith("http://books.toscrape.com"):
        print("L'URL donnée n'est pas valide, ou la catégorie n'existe pas."
              " Le script ne peut scraper que sur http://books.toscrape.com .")
        return
    response = requests.get(url_category)
    response.encoding = "utf-8"
    if response.ok:
        soup = BeautifulSoup(response.text, features="lxml")

        if first_pass:  # #créer un fichier au début
            try:
                category = soup.find("div", {"class": "page-header"}).find("h1").text
                creer_dossier(category)
                with open("{cat}\\{cat}.csv".format(cat=category), "w") as file:
                    file.write("product_page_url, universal_product_code (upc), title, price_including_tax,"
                               + " price_excluding_tax, number_available, product_description, category, review_rating,"
                               + " image_url, nom_exact_image \n")
            except AttributeError:
                fatal(url_category, "catégorie, trouver la catégorie")
                return

        all_books_on_the_page = soup.find_all("li", {"class": "col-xs-6"})
        next_button = None  # #Normalement next_button est toujours initialisé par la boucle for juste après. Mais juste
        # au cas où

        for li in all_books_on_the_page:  # #scrape chaque page de livre
            try:
                book_link = li.find("h3").find("a").get("href").replace("../../..",
                                                                        "http://books.toscrape.com/catalogue")
                data_from_a_book = page_scraping(book_link, getpic=getpic)
            except AttributeError:
                fatal(url_category, "catégorie, trouver les livres")
                return

            if type(data_from_a_book) == list:  # #la fonction page_scraping ne renvoie pas une liste si elle a eu une
                # erreur
                with open("{cat}\\{cat}.csv".format(cat=data_from_a_book[-4]), "a") as file:
                    file.write(", ".join(data_from_a_book))
                    file.write("\n")
            else:
                return "Il y a eu une erreur : {error}".format(error=data_from_a_book)

            next_button = soup.find("li", {"class": "next"})

        if next_button is not None:  # #permet de passer à la page suivante de la catégorie si elle existe.
            url_category = url_category.split("/")
            url_category[-1] = next_button.find("a").get("href")
            url_category = "/".join(url_category)
            category_page_scraping(url_category, first_pass=False, getpic=getpic)
    else:
        return "Une erreur est survenue et la page {url} n'a pas pu être atteinte.".format(url=url_category)


if __name__ == "__main__":  # #Permet au script d'être utilisé en standalone pour scraper une catégorie précise,
    # tout en permettant son import
    continuer = "y"
    while continuer == "y":
        url = input("Quelle catégorie voulez-vous scraper?")
        pic = input("Voulez-vous récupérer toutes les images des livres de cette catégorie? (y/n)")
        if pic == "y":
            pic = True
        elif pic != "n":
            print("Votre réponse n'est pas valide. Les images ne seront pas récupérées.")
            pic = False
        else:
            pic = False
        category_page_scraping(url, getpic=pic)
        continuer = input("Voulez-vous scraper un autre catégorie? (y/n)")
        if continuer not in ("y", "n"):
            print("Votre réponse n'est pas valide, le script va s'arrêter")
