#Scraping du site Books.toscrape

##Installation :

Créez l'environnement virtuel et installez les prérequis présents dans requirements.txt .
Assurez-vous d'avoir un accès à internet.
	
##Utilisation :
	
Double-cliquez sur P2_scraping_une_page.py pour obtenir les informations d'un livre à partir de l'URL de celui-ci. 
Il produira un fichier .csv avec le nom du livre* et les informations requises.
	
Double-cliquez sur P2_scraping_une_catégorie.py pour obtenir les informations de tous les livres d'une catégorie à partir du nom ou de l'URL de celle-ci.
Il produira un dossier avec le nom de la catégorie dans lequel se trouvera un fichier .csv avec le nom de la catégorie aussi, qui contiendra les informations requises.
	
Pour exécuter le scraping du site entier, utilisez le terminal pour vous placer dans le dossier où se trouve P2_scraping_site.py, puis exécutez la commande 'python P2_scraping_site.py'.
Il produira un dossier par catégorie dans lequel se trouvera l'ensemble des images des couvertures des livres de la catégorie ainsi qu'un fichier .csv qui contiendra les informations requises de la catégorie.

	
* : Certains caractères (\\, /, :, \*, ?, ", <, >, et |) sont retirés du nom du livre pour s'assurer autant que possible que le nom du fichier soit valide.

