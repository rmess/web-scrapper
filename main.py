import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import math
from tkinter import *

AMELI_URL = 'http://annuairesante.ameli.fr'

def extract_information(block):
    """
    returns name, address, phone, prices and convention from
    a doctor html block
    """
    result = []
    name = block.find('h2')
    address = block.find("div", attrs={'class':"item left adresse"})
    phone = block.find("div", attrs={'class':"item left tel"})
 
    for item in [name, address, phone or None]:
        if phone is not None:
            result.append(item.get_text())
    
    if(len(result) > 0):
        return result
    return None


def extract_number_of_doctors(soup):
    """
    returns the number of doctors found in the query page
    returns 0 if no doctors are found in the query
    """
    p = re.compile(u"(\d+) résultat[s]* correspond[ent]* à votre recherche")

    tags = soup.find_all(name="p")
    for tag in tags:
        if tag.string is not None:
            res = p.findall(tag.string)
            if len(res) > 0:
                return int(p.findall(tag.string)[0])
    return 0

def make_multiple_query(specialty, locations, sexe, localisation_category):
    """
    queries Ameli for a given specialty of doctors in locations, which is a list
    of postcodes
    """
    dfs = []
    for location in locations:
        df = make_single_query(specialty, location, sexe, localisation_category)
        if df is not None:
            dfs.append(df)
        
    return True

def make_single_query(specialty, location, sexe, localisation_category):
    """queries Ameli for a given specialty of doctors in a given location
    returns a pandas dataframe or None if no doctors have been found"""
    
    # create new session and open the connection to get cookies
    s = requests.Session()
    r = s.get(AMELI_URL)
    
    # extract the page towards which we make our first request
    p = re.compile('<form action="([\w\d/.-]+)" method="post">')
    suburl = p.findall(r.text)[0]
    

    # make the request
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
        }

    # sexe should be an argument of the function 0=male 1=female 2=undifined
    # localisation can be "villes" or "departements"
    # ps_proximite: on
    payload = {
        "type":"ps",
        "ps_profession": specialty,
        "ps_localisation": location,
        "ps_sexe": sexe,
        "localisation_category": localisation_category
        }
    r = s.post(AMELI_URL + suburl, params=payload,
          headers=headers)

    # extract information
    soup = BeautifulSoup(r.text, 'html.parser')
    number_of_doctors = extract_number_of_doctors(soup)
    print(number_of_doctors)
    if number_of_doctors == 0:
        return None
    # loop over needed pages
    dfs = []

    for pagenumber in range(1, int(math.ceil(number_of_doctors / 20.)) + 1):
        r2 = s.post(r.url.replace("liste-resultats-page-1-par_page-20-tri-aleatoire", 
                                  "liste-resultats-page-{}-par_page-20-tri-aleatoire").format(pagenumber))
        soup = BeautifulSoup(r2.text, 'html.parser')
        doctors = soup.findAll('div', attrs={"class":"item-professionnel"})
        for doc in doctors:
            if extract_information(doc) is not None:
                dfs.append(pd.DataFrame([extract_information(doc)], columns=['Nom', u'Adresse', u"Téléphone"]))
    

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv('doctors.csv', mode='w+', header=True, encoding='utf_16')
    # df.to_csv('doctors.csv', mode='a', header=False, encoding='utf_16')
    return df


def read_csv(file):
    df = pd.read_csv(file)
    return df

def write_csv(data):
    return

if __name__ == "__main__":
    root = Tk()

    areaLbl = Label(root, text="Sexe")
    areaLbl.pack()
    genderValue = StringVar() 
    maleBtn = Radiobutton(root, text="Homme", variable=genderValue, value=0)
    femaleBtn = Radiobutton(root, text="Femme", variable=genderValue, value=1)
    undefgenderValue = Radiobutton(root, text="Indiférent", variable=genderValue, value=2)
    maleBtn.pack()
    femaleBtn.pack()
    undefgenderValue.pack()

    def recupere():
        gender = int(genderValue.get())
        areaInput = adressInput.get()
        area = areaValue.get()
        speciality = specialityValue.get()
        print(areaInput)
        print(area)
        print(gender)
        print(speciality)
        #1st select the doctor's speciality setted to généraliste for now
        # sexe should be an argument of the function 0=male 1=female 2=undifined
        # localisation can be "villes" or "departements"
        # make_single_query(specialty, location, sexe, localisation_category):
        make_multiple_query(speciality,[areaInput], gender, area)
        root.destroy()



    areaLbl = Label(root, text="Zone")
    areaLbl.pack()
    areaValue = StringVar()
    cityBtn = Radiobutton(root, text="Villes", variable=areaValue, value="villes")
    areaBtn = Radiobutton(root, text="Départements", variable=areaValue, value="departements")
    cityBtn.pack()
    areaBtn.pack()

    areaLbl = Label(root, text="Profession")
    areaLbl.pack()
    specialityValue = StringVar() 
    specialityValue.set("34")
    specialityInput = Entry(root, textvariable=specialityValue, width=30)
    specialityInput.pack()


    areaLbl = Label(root, text="Adresse")
    areaLbl.pack()
    adressValue = StringVar() 
    adressValue.set("HERAULT (34)")
    adressInput = Entry(root, textvariable=adressValue, width=30)
    adressInput.pack()

    bouton = Button(root, text="Valider", command=recupere)
    bouton.pack()


    root.mainloop()