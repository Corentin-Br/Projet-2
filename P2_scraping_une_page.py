import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'

response = requests.get(url)

if response.ok :
    soup = BeautifulSoup(response.text, features="html.parser")
    tags_to_search = {"UPC" : str(),
                      "Price (excl. tax)" : str(),
                      "Price (incl. tax)" :str() ,
                      "Availability" : str()}
    possible_ratings = {"One" : "1",
                        "Two" : "2" ,
                        "Three" : "3",
                        "Four" : "4",
                        "Five" : "5"}
    

    rating_found = False
                        

    content = soup.findAll('tr')
    for tr in content :
        th = tr.find("th")
        if th.text in tags_to_search :
            td = tr.find("td")
            tags_to_search[th.text] = td.text

    number_available = str()
    for char in tags_to_search["Availability"] :
        if char.isnumeric :
            number_available += char

    content = soup.findAll('li')
    category = content[2].find("a").text
    title = content[3].text

    

    content = soup.findAll("p")
    for p in content :
        if p.text.startswith("\"") :
            description = "\'" + p.text + "\'" ##L'ajout des apostrophes permet à Libre Office de l'ouvrir correctement (avec les bons paramètres). Il y a peut-être moyen de faire mieux.
        if not rating_found :
            for cl in p.get("class",list()) :
                if cl in possible_ratings :
                    rating = possible_ratings[cl]
                    rating_found = True

    if tags_to_search["Price (incl. tax)"][1] != "£" :
        tags_to_search["Price (incl. tax)"] = tags_to_search["Price (incl. tax)"][1:]
    if tags_to_search["Price (excl. tax)"][1] != "£" :
        tags_to_search["Price (excl. tax)"] = tags_to_search["Price (excl. tax)"][1:] ##Résoud le problème d'encodage apparent s'il est présent. On verra pour trouver mieux.
                    
    image = soup.find("img")["src"].replace("../..", "books.toscrape.com")
    
    with open("category.csv", "w") as file :
        file.write("""product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url \n""")
        
        file.write(", ".join([url, tags_to_search["UPC"], title, tags_to_search["Price (incl. tax)"], tags_to_search["Price (excl. tax)"], number_available, description, category, rating, image])) 
        file.write("\n")

    with open("category.csv", "r") as file :
        for row in file :
            print(row)

        
