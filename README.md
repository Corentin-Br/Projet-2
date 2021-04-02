#Scraping du site Books.toscrape

##Installation :

Créer l'environnement virtuel et installer les prérequis présents dans requirements.txt
	
##Utilisation :
	
Double-cliquer sur P2_scraping_une_page.py permet d'obtenir les informations d'un livre à partir de l'URL de celui-ci. 
Il produira un fichier .csv avec le nom du livre* et les informations requises.
	
	
Double-cliquer sur P2_scraping_une_catégorie.py permet d'obtenir les informations de tous les livres d'une catégorie à partir du nom ou de l'URL de celle-ci.
Il produira un dossier avec le nom de la catégorie dans lequel se trouvera un fichier .csv avec le nom de la catégorie aussi, qui contiendra les informations requises.
	
Double-cliquer sur P2_scraping_site.py lancera le scraping du site entier.
Il produira un dossier par catégorie dans lequel se trouvera l'ensemble des images des couvertures des livres de la catégorie ainsi qu'un fichier .csv qui contiendra les informations requises de la catégorie.
	
	
* : Certains caractères (\\, /, :, \*, ?, ", <, >, et |) sont retirés du nom du livre pour s'assurer autant que possible que le nom du fichier soit valide.

