import sys
import xmltodict
import json
import requests
import csv
from bs4 import BeautifulSoup

# print(sys.argv.pop(1) or "No args")


# URL = "http://annuairesante.ameli.fr/recherche.html" 

# headers = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-language": "en-US,en;q=0.9,fr;q=0.8",
#     "cache-control": "max-age=0",
#     "content-type": "application/x-www-form-urlencoded",
#     "upgrade-insecure-requests": "1",
#     "cookie": "AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; TS019773cb=0139dce0d2e34598358fe3872eb734fa3ed9c1b4cf520cc0b9b7263eb0fe0ded4c2a38a12f68e1456680a8a73f64bd99f449ec1415; infosoins=esj13defiifr4fu6bonpaj0cc4; TS01b76c1f=0139dce0d25f6d11f74d20692cee589005a0eecfa875b8a957a55b3dc87d2ad71ab998d9144a2ec1bf46e2875bdd479ac1604cc6a9"
#     }

# payload = {
# "type=ps&ps_nom=&ps_profession=34&ps_profession_label=M%C3%A9decin+g%C3%A9n%C3%A9raliste&ps_acte=&ps_acte_label=&ps_type_honoraire=indifferent&ps_carte_vitale=2&ps_sexe=2&es_nom=&es_specialite=&es_specialite_label=&es_actes_maladies=&es_actes_maladies_label=&es_type=3&ps_localisation=HERAULT+%2834%29&ps_proximite=on&localisation_category=departements&submit_final=Rechercher"
# }

# body = "type=ps&ps_nom=&ps_profession=34&ps_profession_label=M%C3%A9decin+g%C3%A9n%C3%A9raliste&ps_acte=&ps_acte_label=&ps_type_honoraire=indifferent&ps_carte_vitale=2&ps_sexe=2&es_nom=&es_specialite=&es_specialite_label=&es_actes_maladies=&es_actes_maladies_label=&es_type=3&ps_localisation=HERAULT+%2834%29&ps_proximite=on&localisation_category=departements&submit_final=Rechercher"
  
# homePage = requests.post(URL,headers=headers, data=payload)



URL = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-1-par_page-20-tri-aleatoire.html'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "cookie": "AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; TS019773cb=0139dce0d2aa179b962257124d8696a2b3ee6e0e2174961d6ce5647208ede018c7b93d8e66fcdf76da1360eff6be1ba526e1f637fb; infosoins=h33vqdrpmob21d1o8h4hcrphr5; TS01b76c1f=0139dce0d2f4ab9d9a9cf3300857b1024c0ebd87c1360e5db2b2ee485a08360e2ba7197770180b7035d25d6c405cab5008802f2687"
  }
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup)
nameAddress = soup.find_all('div', class_="item-professionnel")
oldDoctorList = []
newDoctorList = []
# doctorList.append(["Nom", "Prénom", "Addresse", "Téléphone"])


# print("debut")
# print(doctorList)
with open('doctorDb.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # print(row)
        oldDoctorList.append(row)
print("/////////////////")
print(oldDoctorList)
print("///////////////")

with open('doctorDb.csv', 'a+') as file:
    writer = csv.writer(file)
    for e in nameAddress:
        print('=============')
        e.div.unwrap()
        mystr = json.dumps(xmltodict.parse(str(e)))
        res = json.loads(mystr)
        firstName = res.get('div').get('div')[0].get('h2').get('a').get('strong') or "Null"
        lastName = res.get('div').get('div')[0].get('h2').get('a').get('#text') or "Null"
        address = res.get('div').get('div')[2].get('div').pop(6).get('#text') or "Null"
        phone = res.get('div').get('div')[2].get('div').pop(3).get('#text') or "Null"
        currentRow = [firstName, lastName, address, phone]
        # print(currentRow)
        # print(oldDoctorList.count(currentRow))
        if (currentRow in oldDoctorList):
            newDoctorList.append(currentRow)
        # print(firstName)
        # print(lastName)
        # print(address)
        # print(phone)
        # print('=============')
    # writer.writerows(oldDoctorList)
    writer.writerows(newDoctorList)

# print(newDoctorList)