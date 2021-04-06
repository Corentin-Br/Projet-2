#Scraping du site Books.toscrape

##Installation :

Créez l'environnement virtuel et installez les prérequis présents dans requirements.txt .
Assurez-vous d'avoir un accès à internet.
	
##Utilisation :

Pour utiliser n'importe lequel des trois scripts, utilisez le terminal pour vous placer dans le dossier où se trouve le script et exécutez le script via 'python nom_du_script.py' (e.g : 'python P2_scraping_site.py')

	
P2_scraping_une_page.py demandera une URL de livre à scrapper et produira un fichier .csv avec le nom du livre* et les informations requises.
	
P2_scraping_une_catégorie.py demandera une URL de catégorie ou son nom. Il demandera aussi si vous voulez récupérer les images.
Il produira un dossier avec le nom de la catégorie dans lequel se trouvera un fichier .csv avec le nom de la catégorie aussi, qui contiendra les informations requises.
	
P2_scraping_site.py produira un dossier par catégorie dans lequel se trouvera l'ensemble des images des couvertures des livres de la catégorie ainsi qu'un fichier .csv qui contiendra les informations requises de la catégorie.
Tous les dossiers se situeront dans un dossier appelé Books_to_scrape.
	
* : Certains caractères (\\, /, :, \*, ?, ", <, >, et |) sont retirés du nom du livre pour s'assurer autant que possible que le nom du fichier soit valide.

