import requests
from bs4 import BeautifulSoup
from P2_scraping_une_page import fatal
from P2_scraping_une_page import page_scraping

def category_page_scraping(url, first_pass = True) :
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
                                                                
