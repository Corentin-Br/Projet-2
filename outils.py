import requests
from bs4 import BeautifulSoup

response = requests.get("http://books.toscrape.com/index.html")
response.encoding = "utf-8"
if response.ok:
    dic = dict()
    soup = BeautifulSoup(response.text, features="lxml")
    content = soup.find("ul", {"class": "nav"}).find("ul").findAll("a")
    for a in content:
        key = a.text.replace("\n", "").replace("  ", "")
        if key.startswith(" "):
            key = key[1:]
        if key.endswith(" "):
            key = key[:-2]
        key = key.lower()
        value = a.get("href")
        value = "http://books.toscrape.com/" + value
        dic[key] = value
    print("{")
    for key in dic:
        print("'" + key + "':  '" + dic[key] + "',")
    print("}")
