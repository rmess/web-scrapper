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
    "cookie": "AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; infosoins=tke43dsp2d8g3blq4alejqde64; TS01b76c1f=0139dce0d29a98c5a1421e367b20ad53e0e692516614e3517a8d2e2acaeed54964153dfa73c0d8b950a3528c362f0df658d90a4e7c"
  }
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup)
tmps = soup.find_all('div', class_="item-professionnel")


for e in tmps:
    print('---------------------------')
    e.div.unwrap()
    mystr = json.dumps(xmltodict.parse(str(e)))
    res = json.loads(mystr)
    tata = res.items()
    print(tata.get('h2'))
    # print(tata)
    # print(res)
    # print(e)
    print("============")
    print(type(tata))
    print('--------------------------')

# print(soup.prettify())
#print(results)
