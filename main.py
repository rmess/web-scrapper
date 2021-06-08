# import sys
# import requests
# import xmltodict
# import json
# from requests import Request, Session, utils
# import csv
# from bs4 import BeautifulSoup

# # print(sys.argv[1] or "No args")

# oldDoctorList = []
# newDoctorList = []
# # doctorList.append(["Nom", "Prénom", "Addresse", "Téléphone"])
# fieldNames= ["Nom", "Prénom", "Addresse", "Téléphone"]
# with open('doctorDb.csv' or sys.argv[1],'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         # print(row)
#         oldDoctorList.append(row)
# # print("/////////////////")
# # print(oldDoctorList)
# # print("///////////////")



# URL = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-1-par_page-20-tri-aleatoire.html'
# URL2 = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-2-par_page-20-tri-aleatoire.html'
# headers = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-language": "en-US,en;q=0.9,fr;q=0.8",
#     "cache-control": "max-age=0",
#     "upgrade-insecure-requests": "1",
#   }


# # urlPost = "http://annuairesante.ameli.fr/recherche.html"  



# s = Session()
# page = s.get(URL, headers=headers, cookies={"cookie": "infosoins=mmgubk55qeqoi8m0f6hr6bddt0; AmeliDirectPersist=745595191.36895.0000; TS01b76c1f=0139dce0d2a69f22a456ef2ccde09be9f88ec109ce70fb779c6b2be5edf97100cb100bdd41ca28d238976a14b4cbe2e095e3c2a190"})
# print(s.cookies)
# print(utils.dict_from_cookiejar(s.cookies))
# print('&&&&&&&&&&&&&&&&&&&&')
# print(page.cookies)
# print(utils.dict_from_cookiejar(page.cookies))

# # print(type(json.dump(page.headers.get('Set-Cookie'))))

# page2 = s.get(URL2)

# print(s.get(URL2).status_code)

# # print((BeautifulSoup(page.content, 'html.parser')))

# # page2 = s.get(URL2)
# # prepped.body = postBody

# # resp = s.send()
# # print(resp.text)
# # print(BeautifulSoup(page.content, 'html.parser'))

# # page = session.get(URL2)
# print('//////////////////')
# print('//////////////////')
# print('//////////////////')
# print('//////////////////')
# print('//////////////////')
# print('//////////////////')
# # print(page2.cookies)
# print('//////////////////')
# print('//////////////////')
# print('//////////////////')
# print('//////////////////')
# print('//////////////////')
# # print(session.cookies)
# print(BeautifulSoup(page2.content, 'html.parser'))
# # print(page.cookies)
# # print(page.headers)


# # i = 0
# # while i < 2:
# #     i += 1
# #     URL = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-' + str(i) +'-par_page-20-tri-aleatoire.html'
# #     print(URL)
# #     page = session.get(URL)
# #     # print(page.cookies)
# #     print('------------------')
# #     print('------------------')
# #     soup = BeautifulSoup(page.content, 'html.parser')
# #     print(soup)
# #     # print(page.headers)

# # soup = BeautifulSoup(page.content, 'html.parser')

# # print(soup)
# # nameAddress = soup.find_all('div', class_="item-professionnel")



# # print("debut")
# # print(doctorList)

# # with open('doctorDb.csv', 'a+') as file:
# #     writer = csv.writer(file)
# #     for e in nameAddress:
# #         print('=============')
# #         e.div.unwrap()
# #         mystr = json.dumps(xmltodict.parse(str(e)))
# #         res = json.loads(mystr)
# #         firstName = res.get('div').get('div')[0].get('h2').get('a').get('strong') or "Null"
# #         lastName = res.get('div').get('div')[0].get('h2').get('a').get('#text') or "Null"
# #         address = res.get('div').get('div')[2].get('div').pop(6).get('#text') or "Null"
# #         phone = res.get('div').get('div')[2].get('div').pop(3).get('#text') or "Null"
# #         currentRow = [firstName, lastName, address, phone]
# #         # print(currentRow)
# #         # print(oldDoctorList.count(currentRow))
# #         if (currentRow in oldDoctorList):
# #             newDoctorList.append(currentRow)
# #         # print(firstName)
# #         # print(lastName)
# #         # print(address)
# #         # print(phone)
# #         # print('=============')
# #     # writer.writerows(oldDoctorList)
# #     writer.writerows(newDoctorList)

# # print(newDoctorList)


# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:29:48 2015

@author: FL232714
"""

import requests
import re
from bs4 import BeautifulSoup
import math

AMELI_URL = 'http://annuairesante.ameli.fr'

def extract_information(block):
    """
    returns name, address, phone, prices and convention from
    a doctor html block
    """
    name = block.find('h2')
    address = block.find("div", attrs={'class':"item left adresse"})
    phone = block.find("div", attrs={'class':"item left tel"})
    prices = block.find("div", attrs={'class':"item right type_honoraires"})
    convention = block.find("div", attrs={'class':"item right convention"})
    return [item.get_text(' ') if item is not None else '' for item in [name, address, phone, prices, convention]]

def extract_number_of_doctors(soup):
    """
    returns the number of doctors found in the query page
    returns 0 if no doctors are found in the query
    """
    p = re.compile(u"(\d+) résultat[s]* correspond[ent]* à votre recherche")

    tags = soup.find_all(name="h1")
    for tag in tags:
        if tag.string is not None:
            res = p.findall(tag.string)
            if len(res) > 0:
                return int(p.findall(tag.string)[0])
    return 0

def make_multiple_query(specialty, locations):
    """
    queries Ameli for a given specialty of doctors in locations, which is a list
    of postcodes
    """
    dfs = []
    for location in locations:
        df = make_single_query(specialty, location)
        if df is not None:
            dfs.append(df)
        
    return True

def make_single_query(specialty, location):
    """queries Ameli for a given specialty of doctors in a given location
    returns a pandas dataframe or None if no doctors have been found"""
    
    # create new session and open the connection to get cookies
    s = requests.Session()
    r = s.get(AMELI_URL)
    
    # extract the page towards which we make our first request
    p = re.compile('<form action="([\w\d/.-]+)" method="post">')
    suburl = p.findall(r.text)[0]
    

    # make the request
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"}
    payload = {"type":"ps",
        "ps_profession":specialty,
        "ps_localisation":location}
    r = s.post(AMELI_URL + suburl, params=payload,
          headers=headers)

    # extract information
    soup = BeautifulSoup(r.text, 'html.parser')
    number_of_doctors = 1000
    if number_of_doctors == 0:
        return None
    # loop over needed pages
    dfs = []
    for pagenumber in range(1, int(math.ceil(number_of_doctors / 20.)) + 1):
        r2 = s.post(r.url.replace("liste-resultats-page-1-par_page-20-tri-aleatoire", 
                                  "liste-resultats-page-{}-par_page-20-tri-aleatoire").format(pagenumber))
        soup = BeautifulSoup(r2.text, 'html.parser')
        doctors = soup.findAll('div', attrs={"class":"item-professionnel"})
        # dfs.append(pd.DataFrame([extract_information(doc) for doc in doctors], 
        #          columns=['Nom', u'Adresse', u"Téléphone", u"Honoraires", "Convention"]))
        print([extract_information(doc) for doc in doctors])
    # df = pd.concat(dfs, ignore_index=True)
    # df.insert(0, u'Specialité', specialty)
    # df.insert(1, 'Commune', pd.Series([location] * df.shape[0], index=df.index))
    print("je suis en vie")
    # write data in csv
    return 

if __name__ == "__main__":
    make_multiple_query('médecin généraliste',["34000"])