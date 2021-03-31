import requests
from bs4 import BeautifulSoup
from P2_scraping_une_page import fatal
from P2_scraping_une_page import page_scraping

def category_page_scraping(url, first_pass = True) :
    response = requests.get(url)
    response.encoding = "utf-8"
    if response.ok :
        soup = BeautifulSoup(response.text, features="lxml")
    if first_pass :
        category = soup.find("div", {"class" : "page-header"}).find("h1").text
        with open("{cat}.csv".format (cat = category), "w") as file :
                file.write("""product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url \n""")
    all_books_on_the_page = soup.findAll("li", {"class" : "col-xs-6"})
    for li in all_books_on_the_page :
        book_link = li.find("h3").find("a").get("href").replace("../../..", "http://books.toscrape.com/catalogue")
        data = page_scraping(book_link)
        with open("{cat}.csv".format(cat=data[-3]), "a") as file :
                file.write(", ".join(data)) 
                file.write("\n")
        
    next_button = soup.find("li", {"class" : "next"})
    if next_button != None :
        url = url.split("/")
        url[-1] = next_button.find("a").get("href")
        url = "/".join(url)
        category_page_scraping(url, first_pass = False)
                                                                
