import xmltodict
import json
import requests
from bs4 import BeautifulSoup

# URL='http://annuairesante.ameli.fr/nouvelle-recherche/professionnels-de-sante.html'

URL = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-1-par_page-20-tri-aleatoire.html'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "cookie": "AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; infosoins=hlriun5n0sg1rq21kc98ou9rr2; TS019773cb=0139dce0d238030ad3d8d9c68ee752e1daeab05c9da6976349f19016fee53ea0c99917087c964e342a05a35ba298953d01bbb33c06; TS01b76c1f=0139dce0d276caa80197dd09bd328ea275584f5e3f88870d64ab09fd44062cf695a1d0528f92c025dccfd1895639d3979be798fda0"
  }

page = requests.get(URL, headers=headers)
# page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

print(soup)
tmps = soup.find_all('div', class_="item-professionnel")


for e in tmps:
    print('---------------------------')
    e.div.unwrap()
    mystr = json.dumps(xmltodict.parse(str(e)))
    res = json.loads(mystr)
    # tata = res.items()
    # nom + prenom = res.get('div').get('div')[0].get('h2')
    nom = res.get('div').get('div')[0].get('h2').get('a').get('strong')
    prenom = res.get('div').get('div')[0].get('h2').get('a').get('#text')
    print(res.get('div').get('div')[2])
    # print(res)
    # print(e)
    print("============")
    # print(type(tata))
    print('--------------------------')

# print(soup.prettify())
#print(results)
