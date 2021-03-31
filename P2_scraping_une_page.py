import requests
from bs4 import BeautifulSoup

def fatal(url, raison) :
    print("Une erreur est survenue lors de l'obtention de {chose}. Vérifiez que vous scrapez bien la page d'un livre. L'URL fautive est {url}".format(url = url, chose = raison))

def page_scraping(url = str()) :
    if not url.startswith ("http://books.toscrape.com") :
        return("L'URL donnée n'est pas valide. Le script ne peut scraper que sur http://books.toscrape.com .")
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
                            

        content = soup.findAll('tr') ##Trouve les quatres tags de tags_to_search.
        for tr in content :
            th = tr.find("th")
            if th.text in tags_to_search :
                td = tr.find("td")
                tags_to_search[th.text] = td.text

        number_available = str() ##Obtient et rend propre le nombre de livres disponibles.
        for char in tags_to_search["Availability"] :
            if char.isnumeric() :
                number_available += char

        content = soup.findAll('li')  ##Obtient la catégorie et le titre.
        try : 
            category = content[2].find("a").text
            title = content[3].text
        except (IndexError, AttributeError) :
            fatal(url, "catégorie/titre")
            return
            
        try :
            description = soup.find("meta", {"name" : "description"}).get("content") ##Obtient la description. Il y a un peu de travail car il y a des espaces en trop au début
        except AttributeError :
            fatal(url , "description")
            return

        starting_index = 0
        for k in range(len(description)) :
            if description[k] != " " and description[k] != "\n" :
                starting_index = k
                break;
        description = description[starting_index:]
        description = "\'" + description  + "\'" #L'ajout des apostrophes permet à Libre Office de l'ouvrir correctement (avec les bons paramètres). Il y a peut-être moyen de faire mieux.


        try :
            classes = soup.find("p", {"class" : "star-rating"}).get("class") ##Obtient la note. Normalement la note du livre est toujours la première (celle des autres livres est à la fin)
        except AttributeError :
            fatal(url, "rating")
            return
            
        for thing in classes :
            if thing in possible_ratings :
                rating = possible_ratings[thing]
        try : 
            if tags_to_search["Price (incl. tax)"][0] != "£" :
                tags_to_search["Price (incl. tax)"] = tags_to_search["Price (incl. tax)"][1:]
            if tags_to_search["Price (excl. tax)"][0] != "£" :
                tags_to_search["Price (excl. tax)"] = tags_to_search["Price (excl. tax)"][1:] ##Résout le problème d'encodage apparent s'il est présent. On verra pour trouver mieux.
        except IndexError:
            fatal(url , "prix")
            return
        
        try :
            image = soup.find("img")["src"].replace("../..", "books.toscrape.com")
        except :
            fatal(url, "image")
            return

        all_data = [url, tags_to_search["UPC"], title, tags_to_search["Price (incl. tax)"], tags_to_search["Price (excl. tax)"], number_available, description, category, rating, image]
        if str() in all_data :
            return("Certaines valeurs sont incorrectes ou ienxistantes. Vérifiez que vous scrapez bien la page d'un livre. L'URL fautive est {url}".format(url = url))
            
        
        with open("{cat}.csv".format(cat = category), "w") as file :
            file.write("""product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url \n""")
            
            file.write(", ".join(all_data)) 
            file.write("\n")


    else :
        return("An error has occured and the page could not be reached.")

while True :
    url= input("What page do you want to scrape?")
    page_scraping(url)
        
