import requests
import json
from bs4 import BeautifulSoup

URL = 'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-1-par_page-20-tri-aleatoire.html?print'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "cookie": "infosoins=23ge5g0sp0rbsn0lr56g63gjo4; AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; TS01b76c1f=0139dce0d2a3b638ba19c52ae26379023b42a68c3f90fb3c5b475c43fafb36242d73f7a3107bc9607f745a2e940673d954276bd403"
}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

tmps = soup.find_all('div', class_="item-professionnel")


for e in tmps:
    print()
    print(e.prettify())
    print()

# print(soup.prettify())
#print(results)


# fetch("http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-1-par_page-20-tri-aleatoire.html", {
#     "headers": {
#       "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#       "accept-language": "en-US,en;q=0.9,fr;q=0.8",
#       "cache-control": "max-age=0",
#       "upgrade-insecure-requests": "1",
#       "cookie": "infosoins=23ge5g0sp0rbsn0lr56g63gjo4; AmeliDirectPersist=745595191.36895.0000; cookieconsent_dismissed=yes; TS01b76c1f=0139dce0d2a3b638ba19c52ae26379023b42a68c3f90fb3c5b475c43fafb36242d73f7a3107bc9607f745a2e940673d954276bd403"
#       },
#     "referrer": "http://annuairesante.ameli.fr/nouvelle-recherche/professionnels-de-sante.html",
#     "referrerPolicy": "strict-origin-when-cross-origin",
#     "body": null,
#     "method": "GET",
#     "mode": "cors"
# })
