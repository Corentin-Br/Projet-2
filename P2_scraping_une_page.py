import requests
from bs4 import BeautifulSoup
from os import mkdir
import time


def cleaning(string):  # #Try to make sure the name will be valid for a file name
    forbidden_characters = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    for char in forbidden_characters:
        if char in string:
            string = " ".join(string.split(char))
    return string


def fatal(url_probleme, raison):
    print("Une erreur est survenue lors de l'obtention de {chose}. Vérifiez que vous scrapez bien la page appropriée"
          " (la page d'un livre ou d'une catégorie selon le script utilisé). "
          "L'URL fautive est {url}".format(url=url_probleme, chose=raison))


def page_scraping(url_page=str(), getpic=False):
    if not url_page.startswith("http://books.toscrape.com"):
        return "L'URL donnée n'est pas valide. Le script ne peut scraper que sur http://books.toscrape.com ."
    response = requests.get(url_page)
    response.encoding = "utf-8"
    if response.ok:
        soup = BeautifulSoup(response.text, features="lxml")

        tags_to_search = {"UPC": str(),
                          "Price (excl. tax)": str(),
                          "Price (incl. tax)": str(),
                          "Availability": str()}

        possible_ratings = {"One": "1",
                            "Two": "2",
                            "Three": "3",
                            "Four": "4",
                            "Five": "5"}

        content = soup.findAll('tr')  # #Trouve les quatres tags de tags_to_search.
        for tr in content:
            th = tr.find("th")
            if th.text in tags_to_search:
                td = tr.find("td")
                tags_to_search[th.text] = td.text

        number_available = str()  # #Obtient et rend propre le nombre de livres disponibles.
        for char in tags_to_search["Availability"]:
            if char.isnumeric():
                number_available += char

        content = soup.findAll('li')  # #Obtient la catégorie et le titre.
        try:
            category = content[2].find("a").text
            title = "\"" + content[3].text.replace("\"", "❞") + "\""  # #certains noms contiennent une virgule.
            # Les apostrophes vont permettre de gérer ça pour Libre Office
        except (IndexError, AttributeError):
            fatal(url_page, "catégorie/titre")
            return
            
        try:
            description = soup.find("meta", {"name": "description"}).get("content")  # #Obtient la description.
            # Il y a un peu de travail car il y a des espaces en trop au début.
        except AttributeError:
            fatal(url_page, "description")
            return

        description = description.replace("\n", "")
        description = description.strip()
        description.replace("\"", "❞")
        description = "\"" + description + "\""  # #L'ajout des guillemets permet à Libre Office
        # de l'ouvrir correctement (avec les bons paramètres). Il y a peut-être moyen de faire mieux.

        try:
            classes = soup.find("p", {"class": "star-rating"}).get("class")  # #Obtient la note. Normalement la note
            # du livre est toujours la première (celle des autres livres est à la fin)
        except AttributeError:
            fatal(url_page, "rating")
            return
        rating = "inconnu"  # #Rating devrait toujours être initialisé par la boucle suivante, mais par précaution.
        for thing in classes:
            if thing in possible_ratings:
                rating = possible_ratings[thing]
        
        try:
            image = soup.find("img")["src"].replace("../..", "http://books.toscrape.com")
        except(AttributeError, TypeError):
            fatal(url_page, "l'image")
            return
        if getpic:
            try:
                reponse = requests.get(image)
            except requests.exceptions.ConnectionError:  # #Sans ralentissement, il semble que des erreurs se
                # produisent lors de l'utilisation de plusieurs threads. On les détecte, et on force le thread
                # à patienter
                time.sleep(1)
                reponse = requests.get(image)

            try:
                with open("{cat}\\{name}.jpg".format(cat=category, name=cleaning(title)), "wb") as file_image:
                    file_image.write(reponse.content)
            except FileNotFoundError:
                mkdir(category)
                with open("{cat}\\{name}.jpg".format(cat=category, name=cleaning(title)), "wb") as file_image:
                    file_image.write(reponse.content)
        return [url_page, tags_to_search["UPC"], title, tags_to_search["Price (incl. tax)"],
                tags_to_search["Price (excl. tax)"], number_available, description, category, rating, image]
    else:
        return "Une erreur est survenue et la page {url} n'a pas pu être atteinte.".format(url=url_page)


if __name__ == "__main__":  # #Permet au script d'être utilisé en standalone pour scraper une page précise,
    # tout en permettant son import
    while True:
        url = input("Quelle page voulez-vous scraper?")
        data = page_scraping(url)
        if type(data) == list:
            with open("{name}.csv".format(name=cleaning(data[2])), "w") as file:
                file.write("product_page_url, universal_product_code (upc), title, price_including_tax,"
                           + " price_excluding_tax, number_available, product_description, category, review_rating,"
                           + " image_url \n")
                file.write(", ".join(data))
                file.write("\n")
        else:
            print(data)
