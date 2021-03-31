import requests
from bs4 import BeautifulSoup
from P2_scraping_une_page import fatal
from P2_scraping_une_page import page_scraping

all_categories = {'Travel': 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html',
                  'Mystery': 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
                  'Historical Fiction': 'http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html',
                  'Sequential Art': 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html',
                  'Classics': 'http://books.toscrape.com/catalogue/category/books/classics_6/index.html',
                  'Philosophy': 'http://books.toscrape.com/catalogue/category/books/philosophy_7/index.html',
                  'Romance': 'http://books.toscrape.com/catalogue/category/books/romance_8/index.html',
                  'Womens Fiction': 'http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html',
                  'Fiction': 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html',
                  'Childrens': 'http://books.toscrape.com/catalogue/category/books/childrens_11/index.html',
                  'Religion': 'http://books.toscrape.com/catalogue/category/books/religion_12/index.html',
                  'Nonfiction': 'http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html',
                  'Music': 'http://books.toscrape.com/catalogue/category/books/music_14/index.html',
                  'Default': 'http://books.toscrape.com/catalogue/category/books/default_15/index.html',
                  'Science Fiction': 'http://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html',
                  'Sports and Games': 'http://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html',
                  'Add a comment': 'http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html',
                  'Fantasy': 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html',
                  'New Adult': 'http://books.toscrape.com/catalogue/category/books/new-adult_20/index.html',
                  'Young Adult': 'http://books.toscrape.com/catalogue/category/books/young-adult_21/index.html',
                  'Science': 'http://books.toscrape.com/catalogue/category/books/science_22/index.html',
                  'Poetry': 'http://books.toscrape.com/catalogue/category/books/poetry_23/index.html',
                  'Paranormal': 'http://books.toscrape.com/catalogue/category/books/paranormal_24/index.html',
                  'Art': 'http://books.toscrape.com/catalogue/category/books/art_25/index.html',
                  'Psychology': 'http://books.toscrape.com/catalogue/category/books/psychology_26/index.html',
                  'Autobiography': 'http://books.toscrape.com/catalogue/category/books/autobiography_27/index.html',
                  'Parenting': 'http://books.toscrape.com/catalogue/category/books/parenting_28/index.html',
                  'Adult Fiction': 'http://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html',
                  'Humor': 'http://books.toscrape.com/catalogue/category/books/humor_30/index.html',
                  'Horror': 'http://books.toscrape.com/catalogue/category/books/horror_31/index.html',
                  'History': 'http://books.toscrape.com/catalogue/category/books/history_32/index.html',
                  'Food and Drink': 'http://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html',
                  'Christian Fiction': 'http://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html',
                  'Business': 'http://books.toscrape.com/catalogue/category/books/business_35/index.html',
                  'Biography': 'http://books.toscrape.com/catalogue/category/books/biography_36/index.html',
                  'Thriller': 'http://books.toscrape.com/catalogue/category/books/thriller_37/index.html',
                  'Contemporary': 'http://books.toscrape.com/catalogue/category/books/contemporary_38/index.html',
                  'Spirituality': 'http://books.toscrape.com/catalogue/category/books/spirituality_39/index.html',
                  'Academic': 'http://books.toscrape.com/catalogue/category/books/academic_40/index.html',
                  'Self Help': 'http://books.toscrape.com/catalogue/category/books/self-help_41/index.html',
                  'Historical': 'http://books.toscrape.com/catalogue/category/books/historical_42/index.html',
                  'Christian': 'http://books.toscrape.com/catalogue/category/books/christian_43/index.html',
                  'Suspense': 'http://books.toscrape.com/catalogue/category/books/suspense_44/index.html',
                  'Short Stories': 'http://books.toscrape.com/catalogue/category/books/short-stories_45/index.html',
                  'Novels': 'http://books.toscrape.com/catalogue/category/books/novels_46/index.html',
                  'Health': 'http://books.toscrape.com/catalogue/category/books/health_47/index.html',
                  'Politics': 'http://books.toscrape.com/catalogue/category/books/politics_48/index.html',
                  'Cultural': 'http://books.toscrape.com/catalogue/category/books/cultural_49/index.html',
                  'Erotica': 'http://books.toscrape.com/catalogue/category/books/erotica_50/index.html',
                  'Crime': 'http://books.toscrape.com/catalogue/category/books/crime_51/index.html'}

def category_page_scraping(url, first_pass = True) :
    global all_categories
    if url in all_categories :
        url = all_categories[url]
    response = requests.get(url)
    response.encoding = "utf-8"
    if response.ok :
        soup = BeautifulSoup(response.text, features="lxml")
        
        if first_pass : ##créer un fichier au début
            try :
                category = soup.find("div", {"class" : "page-header"}).find("h1").text
                with open("{cat}.csv".format (cat = category), "w") as file :
                        file.write("""product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url \n""")
            except AttributeError :
                fatal(url, "catégorie, trouver la catégorie")
                return
            
        all_books_on_the_page = soup.findAll("li", {"class" : "col-xs-6"})
        
        for li in all_books_on_the_page : ##scrape chaque page de livre
            try :
                book_link = li.find("h3").find("a").get("href").replace("../../..", "http://books.toscrape.com/catalogue")
                data = page_scraping(book_link)
            except AttributeError :
                fatal(url, "catégorie, trouver les livres")
                return
            
            if type(data) == list : ##la fonction page_scraping ne renvoye pas une liste si elle a eu une erreur
                with open("{cat}.csv".format(cat=data[-3]), "a") as file :
                        file.write(", ".join(data)) 
                        file.write("\n")
            else :
                return("Il y a eu une erreur : {error}".format(error = data))

            next_button = soup.find("li", {"class" : "next"})
            
        if next_button != None : ##permet de passer à la page suivante de la catégorie si elle existe.
            url = url.split("/")
            url[-1] = next_button.find("a").get("href")
            url = "/".join(url)
            category_page_scraping(url, first_pass = False)
    else :
        return("Une erreur est survenue et la page {url} n'a pas pu être atteinte.".format(url = url))


if __name__ == "__main__" : ##Permet au script d'être utilisé en standalone pour scraper une catégorie précise, tout en permettant son import
    while True :
        url= input("Quelle catégorie voulez-vous scraper?")
        data = category_page_scraping(url)
                                                                
