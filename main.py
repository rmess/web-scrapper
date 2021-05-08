import xmltodict
import json
import requests
from bs4 import BeautifulSoup

URL = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-1-par_page-20-tri-aleatoire.html?print'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "cookie": "AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; infosoins=fltdpsc21lg64n4g880lpj3785; TS01b76c1f=0139dce0d28ca24912917a29a07354e23e583ea3bd2aeb0a9a00d850dc64b079afbc3b282195e55e83746cd7c4ab0b90d1acbfc74c"
  }
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup)
tmps = soup.find_all('div', class_="item-professionnel")


for e in tmps:
    print('---------------------------')
    # e.div = ['index', 'content']
    print(json.dumps(xmltodict.parse(str(e))))
    # print(json.dumps(xmltodict.parse(e)))
    print("============")
    print(type(e))
    print('--------------------------')

# print(soup.prettify())
#print(results)


