import xmltodict
import json
import requests
import csv
from bs4 import BeautifulSoup

# URL='http://annuairesante.ameli.fr/nouvelle-recherche/professionnels-de-sante.html'


URL = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-1-par_page-20-tri-aleatoire.html'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "cookie": "AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; TS019773cb=0139dce0d20abd0c297c427f93a8238ba06038cf99093204157e70d976db3c56fd5a56cd0874555fe3b2d6036fc9cfd6b8dd759384; infosoins=cj7rg26rn0km82fpfn5g6si6s3; TS01b76c1f=0139dce0d2cf3acd5382075954c130d548abf39e49027262b53a9b7b4380a3fdd5b36fc87e6d4e953a6cfd158165a30e6a27321a4d"
  }

page = requests.get(URL, headers=headers)
# page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup)
nameAddress = soup.find_all('div', class_="item-professionnel")
# doctorList = []

with open('doctorDb.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for e in nameAddress:
        print('=============')
        print('=============')
        e.div.unwrap()
        mystr = json.dumps(xmltodict.parse(str(e)))
        res = json.loads(mystr)
        firstName = res.get('div').get('div')[0].get('h2').get('a').get('strong') or "Null"
        lastName = res.get('div').get('div')[0].get('h2').get('a').get('#text') or "Null"
        address = res.get('div').get('div')[2].get('div').pop(6).get('#text') or "Null"
        phone = res.get('div').get('div')[2].get('div').pop(3).get('#text') or "Null"
        writer.writerow([firstName, lastName, address, phone])
        print(firstName)
        print(lastName)
        print(address)
        print(phone)
        print('=============')
