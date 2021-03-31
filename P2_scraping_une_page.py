import requests
from bs4 import BeautifulSoup

def fatal(url, raison) :
    print("Une erreur est survenue lors de l'obtention de {chose}. Vérifiez que vous scrapez bien la page appropriée (la page d'un livre ou d'une catégorie selon le script utilisé). L'URL fautive est {url}".format(url = url, chose = raison))

def page_scraping(url = str()) :
    if not url.startswith ("http://books.toscrape.com") :
        return("L'URL donnée n'est pas valide. Le script ne peut scraper que sur http://books.toscrape.com .")
    response = requests.get(url)
    response.encoding = "utf-8"
    if response.ok :
        soup = BeautifulSoup(response.text, features="lxml")        
        
        
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
            title = "\"" + content[3].text.replace("\"", "❞") + "\""  ##certains noms contiennent une virgule. Les apostrophes vont permettre de gérer ça pour Libre Office
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
        description.replace("\"", "❞")
        description = "\"" + description  + "\"" #L'ajout des guillemets permet à Libre Office de l'ouvrir correctement (avec les bons paramètres). Il y a peut-être moyen de faire mieux.


        try :
            classes = soup.find("p", {"class" : "star-rating"}).get("class") ##Obtient la note. Normalement la note du livre est toujours la première (celle des autres livres est à la fin)
        except AttributeError :
            fatal(url, "rating")
            return
            
        for thing in classes :
            if thing in possible_ratings :
                rating = possible_ratings[thing]
        
        try :
            image = soup.find("img")["src"].replace("../..", "books.toscrape.com")
        except :
            fatal(url, "image")
            return

        return([url, tags_to_search["UPC"], title, tags_to_search["Price (incl. tax)"], tags_to_search["Price (excl. tax)"], number_available, description, category, rating, image])



    else :
        return("Une erreur est survenue et la page {url} n'a pas pu être atteinte.".format(url = url))

if __name__ == "__main__" : ##Permet au script d'être utilisé en standalone pour scraper une page précise, tout en permettant son import
    while True :
        url= input("What page do you want to scrape?")
        data = page_scraping(url)
        if type(data) == list :
            with open("{name}.csv".format (name = data[1]), "w") as file :
                    file.write("""product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url \n""")
                    file.write(", ".join(data)) 
                    file.write("\n")
        else :
            print(data)
        
