import csv
from prettytable import PrettyTable
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from datetime import date, datetime, timedelta
from typing import Tuple

#Funktio 1. kesto_kustannuspaikoille
def kesto_kustannuspaikoille(
    kp1_total: float,
    kp2_total: float,
    kp3_total: float,
    kp1_kpl_taskissa: float,
    kp2_kpl_taskissa: float,
    kp3_kpl_taskissa: float,
    kp1_aika1_kustannus: float,
    kp2_aika1_kustannus: float,
    kp3_aika1_kustannus: float,
    aika1_kesto: int) -> Tuple[float, float, float, float, float, float]:
    
    """Funktio keston, tässä työpäivien määrän laskemiseksi kullekin
    kustannuspaikalle =kp tässä resurssille: konetyölle (kp1), 
    miestyölle (kp2) ja kuljetukselle (kp3). 
    Parametrit: kustannuspaikkojen kokonaiskustannus / tehtävä,
    kustannuspaikkojen tuntikustannus ja työpäivän pituus tunteina. 
    Laskee keston tuntikustannus * työpäivän kesto / resurssien määrä.
    Palauttaa tuplet: kunkin kustannuspaikkan kesto ja kustannus.
    """
    kp1_kesto = (
        kp1_total / (kp1_aika1_kustannus * aika1_kesto) / kp1_kpl_taskissa
    )
    kp2_kesto = (
        kp2_total / (kp2_aika1_kustannus * aika1_kesto) / kp2_kpl_taskissa
    )
    kp3_kesto = (
        kp3_total / (kp3_aika1_kustannus * aika1_kesto) / kp3_kpl_taskissa
    )                          
    return (kp1_kesto, kp1_total, kp2_kesto, kp2_total, kp3_kesto, kp3_total)

#Funktio 2. luo_taskit_lista 
def luo_taskit_lista(task: str,
                     pilkotun_taskin_nro,
                     kp1_kesto: float,
                     kp1_total: float,
                     kp2_kesto: float,
                     kp2_total: float,
                     kp3_kesto: float,
                     kp3_total: float,
                     kokonaiskustannus: float,
                     jaetun_taskin_kesto: int,
                     aloitus_päivä: datetime
                    ) -> list:
    """Funktion parapetrit task, pilkotun_taskin_nro,kp1_kesto,
    kp1_total, kokonaiskustannus, jaetun_taskin_kesto, aloitus_päivä.
    Jos kp1 kesto > lähtöarvojen jaetun tehtävän pituus jakaa tehtävän
    tämän mukaisiin osiin.
    Palauttaa listan, jossa tehtävät (taskit) jaettu annetun
    (jaetun_taskin_kesto) päivien määrän mittaisiin osiin.
    Osatehtävät on listassa sanakirja tietorakenteena.
    """
    
    pilkotut_taskit = []
    
    if kp1_kesto > jaetun_taskin_kesto:
        uusia_taskeja = int(kp1_kesto / jaetun_taskin_kesto)
        kp1_kesto_per_task = kp1_kesto / uusia_taskeja
        kp1_total_per_task = kp1_total / uusia_taskeja
        kp2_kesto_per_task = kp2_kesto / uusia_taskeja
        kp2_total_per_task = kp2_total / uusia_taskeja
        kp3_kesto_per_task = kp3_kesto / uusia_taskeja
        kp3_total_per_task = kp3_total / uusia_taskeja
        total_per_task = \
            kokonaiskustannus / uusia_taskeja
    else:
        uusia_taskeja = 1
        kp1_kesto_per_task = kp1_kesto / uusia_taskeja
        kp1_total_per_task = kp1_total / uusia_taskeja
        kp2_kesto_per_task = kp2_kesto / uusia_taskeja
        kp2_total_per_task = kp2_total / uusia_taskeja
        kp3_kesto_per_task = kp3_kesto / uusia_taskeja
        kp3_total_per_task = kp3_total / uusia_taskeja
        total_per_task = \
            kokonaiskustannus / uusia_taskeja

    pilkotun_taskin_nro = 1
    alku_pvm = aloitus_päivä
    for task_nro in range(uusia_taskeja):
        taskin_nimi = f"{task} osa {task_nro + 1}"
        
        pilkotut_taskit.append({
            0: taskin_nimi,
            1: round(kp1_kesto_per_task, 0),
            2: round(kp2_kesto_per_task, 0),
            3: round(kp3_kesto_per_task, 0),
            4: round(total_per_task, -2),
            5: round(kp1_total_per_task, -2),
            6: round(kp2_total_per_task, -2),
            7: round(kp3_total_per_task, -2),
            8: alku_pvm.strftime("%d.%m.%Y"),
            9: pilkotun_taskin_nro,
            
        })
        alku_pvm += timedelta(days=kp1_kesto_per_task)
        pilkotun_taskin_nro += 1
    
    return pilkotut_taskit    

#Funktio 3. kelpo_luku
def kelpo_luku(prompt, minimi=None, maksimi=None):
    """Tarkistetaan while silmukassa onko syöte luku raja-arvojen, 
    minimi ja maksimi välillä, niin kauan kunnnes saadaan "oikea" syöte. 
    Parametrit syöte, minimi ja maksimi. Palauttaa käyttäjän syötteen, 
    jos on luku ja raja-arvojen välillä, palauttaa virheilmoituksen, jos ei.
    """
    while True:
        try:
            käyttäjän_syöte = float(input(prompt))

            if (minimi is None or käyttäjän_syöte >= minimi) and \
                (maksimi is None or käyttäjän_syöte < maksimi):
                return käyttäjän_syöte
            else:
                print(f"Oltava suurempi tai yhtäsuuri kuin {minimi} ja \
pienempi kuin {maksimi}. Yritä uudelleen.")
        except ValueError as e:
            käyttäjän_syöte = e.args[0].split(":")[-1].strip() if e.args else ""
            print(f'Ei kelpaa. {käyttäjän_syöte} ei ole luku. \
Desimaalierotus piste. Yritä uudelleen.')

#Funktio 4. kelpo_kokonaisluku
def kelpo_kokonaisluku(prompt, minimi=None, maksimi=None):
    """Tarkistetaan while silmukassa onko syöte kokonaisluku raja-arvojen, 
    minimi ja maksimi välillä, niin kauan kunnes saadaan "oikea" syöte. 
    Parametrit syöte, minimi ja maksimi. Palauttaa käyttäjän syötteen,
    jos on kokonaisluku ja raja-arvojen välillä ja virheilmoituksen, jos ei.
    """
    while True:
        try:
            käyttäjän_syöte = int(input(prompt))

            if (minimi is None or käyttäjän_syöte >= minimi) and \
                (maksimi is None or käyttäjän_syöte < maksimi):
                return käyttäjän_syöte
            else:
                print(f"Oltava suurempi tai yhtäsuuri kuin {minimi} ja \
pienempi kuin {maksimi}. Yritä uudelleen.")
        except ValueError as e:
            käyttäjän_syöte = e.args[0].split(":")[-1].strip() if e.args else ""
            print(f'Ei kelpaa. {käyttäjän_syöte} \
ei ole kokonaisluku. Yritä uudelleen.')

#Funktio 5. kelpo_luku_tiedostosta
def kelpo_luku_tiedostosta(value, minimi=None, maksimi=None):
    """Tarkistaa onko (tiedostossa oleva) luku raja-arvojen, minimi ja maksimi 
    välillä. Parametrit luku, minimi ja maksimi. Palauttaa luvun, jos on luku 
    ja raja-arvojen välillä ja virheilmoituksen, jos ei.
    """
    try:
        luku_tiedostosta = float(value)

        if (minimi is None or luku_tiedostosta >= minimi) and \
            (maksimi is None or luku_tiedostosta < maksimi):
            return luku_tiedostosta
        else:
            raise ValueError(f'Oltava suurempi tai yhtäsuuri kuin {minimi} ja \
pienempi kuin {maksimi}.')
    except ValueError as e:
        luku_tiedostosta = e.args[0].split(":")[-1].strip() if e.args else ""
        raise ValueError(f'Ei kelpaa. {luku_tiedostosta} ei ole luku.')

#Funktio 6. kelpo_kokonaisluku_tiedostosta 
def kelpo_kokonaisluku_tiedostosta(value, minimi=None, maksimi=None):
    """Tarkistaa onko (tiedostossa oleva) kokonaisluku raja-arvojen, 
    minimi ja maksimi välillä. Parametrit luku, minimi ja maksimi. 
    Palauttaa luvun, jos on kokonaisluku ja raja-arvojen välillä ja
    virheilmoituksen, jos ei.
    """
    try:
        luku_tiedostosta = int(value)

        if (minimi is None or luku_tiedostosta >= minimi) and \
            (maksimi is None or luku_tiedostosta < maksimi):
            return luku_tiedostosta
        else:
            raise ValueError(f'Oltava suurempi tai yhtäsuuri kuin {minimi} ja\
pienempi kuin {maksimi}.')
    except ValueError as e:
        luku_tiedostosta = e.args[0].split(":")[-1].strip() if e.args else ""
        raise ValueError(f'Ei kelpaa. {luku_tiedostosta} ei ole kokonaisluku.')
    
#Funktio 7. kelpo_päivämäärä
def kelpo_päivämäärä(prompt, pvm_muoto="%d.%m.%Y"):
    while True:
        try:
            pvm_syöte = input(prompt)
            parsed_pvm = datetime.strptime(pvm_syöte, pvm_muoto)
            return parsed_pvm
        except ValueError:
            print(f'Ei kelpaa. "{pvm_syöte}" ei ole päivämäärä tai oikea muoto\
{pvm_muoto}. Yritä uudelleen.')

#Arkipyhät 2024
arkipyhät = [
    date(2024, 1, 1),  # Uudenvuodenpäivä
    date(2024, 3, 29),  # Pitkäperjantai
    date(2024, 4, 1),  # Toinen pääsiäispäivä
    date(2024, 5, 1),  # Vappupäivä
    date(2024, 5, 9),  # Helatorstai
    date(2024, 12, 6),  # Itsenäisyyspäivä
    date(2024, 12, 24),  # Jouluaatto
    date(2024, 12, 25)  # Joulupäivä
]

#Funktio 8. työpäivät
def työpäivät(aloitus: datetime, kesto: int, arkipyhät=[])-> datetime:
    """Poistaa viikonloput 'laskuista' parametrit aloitus, kesto ja 
    arkipyhät lista.
    Palauttaa valmis päivämäärän. Määritelty silmukka while > 0 jossa
    käydään aloituspäivästä alkaen läpi päivät yksi kerrallaan niin 
    kauan kunnes kesto = 0. Jos päivän nro < 5 (ma-pe/0-4) vähentää 
    kestoa yhdellä, jos 5 tai 6 eli la/su ei vähennä kestoa. Jos päivä
    osuu arkipyhille ei myöskään vähennä.
    """
    valmis = aloitus
    while kesto > 0:
        valmis += timedelta(days=1)
        if valmis.weekday() < 5 and valmis.date() not in arkipyhät: 
            kesto -= 1
    return valmis

tänään = date.today()
pvm_muoto="%d.%m.%Y"
tänään_muodossa = date.strftime(tänään, pvm_muoto)

print(f'___________________________________________________________________\n'
      f'\n'
      f'TKO_2111 Ohjelmoinnin harjoitustyö 2023\n'
      f'MÄÄRÄ- JA YKSIKKÖHINTALUETTELOON PERUSTUVA AIKATAULUOHJELMA\n'
      f'OSA 1 LÄHTÖARVOT {tänään_muodossa}\n'
      f'\n'
      f'PIKAOHJE\n'
      f'\n'
      f'- Lähtöarvoksi tarvitaan vähintään kaksi csv-tiedostoa,\n'
      f'  määrä- ja yksikköhintaluettelo, jota tässä kutsutaan laskenta-\n'
      f'  tiedostoksi ja jossa on seuraavat 16 saraketta:\n'
      f'  Id,Littera,Rakennusosa,Paikka,Materiaali,Määrä,Yksikkö,KL,\n'
      f'  €/yks. mat.,€/yks. alih.,€/yks. kulj.,€/yks. konetyö,\n'
      f'  €yhteensa konetyö,€/yks. miestyö,€/yks,€/yks sis.kate,€yht\n'
      f'  Sekä resurssit.csv, jossa resursseja yhdellä rivillä.\n'
      f'\n'
      f'- Loput lähtöarvot voidaan antaa manuaalisesti tai tiedostosta.\n'
      f'  Jos annetaan tiedostosta tarvitaan csv-tiedosto, jossa seuraavat\n'
      f'  11 saraketta: konetyö_tuntihinta,kone_tehtävä,miestyö_tuntihinta,\n'
      f'  mies_tehtävä,kuljetus_tuntihinta,auto_tehtävä,työpäivän_pituus_h,\n'
      f'  jaetun_tehtävän_pituus,Aloituspäivämäärä,csv_laskenta-\n'
      f'  tiedoston_nimi, csv_tulosteen_nimi\n'
      f'\n'
      f'- Lähtöarvotiedostossa toisella rivillä on arvot ja laskenta-\n'
      f'  tiedoston nimi ja tulostiedoston nimi, johon ohjelman \n'
      f'  tulos tallennetaan.\n'
      f'\n'
      f'- Näillä tiedoilla ohjelma tulostaa tehtävät, jotka on jaettu osiin\n'
      f'  ja niillä aloitus ja valmis päivämäärät.\n'
      f'\n'
      f'- Ohjelma siirtyy osaan 2, jossa kysytään tehtävien riippuvuuksia,\n'
      f'  yksittäisten tehtävien aloituspäivämääriä ja resursseja. Näin voidaan\n'
      f'  tehtävien järjestystä muuttaa ja useampaa tehtävää voidaan\n'
      f'  tehdä samanaikaisesti. Kyselyissä nollalla pääsee seuraavaan\n'
      f'__________________________________________________________________\n')


"""Lähtöarvojen asetus manuaalisesti tai tiedostosta, kysytään käyttäjältä 
annetaanko lähtöarvot manuaalisesti vai käytetäänkö tiedostoa. While
silmukassa kysyy m tai t niin kauan kunnes syöte joko m tai t. Eli while
syöte ei ole m eikä t jatkaa kysymistä.
"""
tiedosto_vai_manuaali = input("Haluatko antaa lähtöarvot manuaalisesti (m) \
vai tiedostosta (t) ")

while tiedosto_vai_manuaali != "m" and tiedosto_vai_manuaali != "t":
    tiedosto_vai_manuaali = input("Ei kelpaa. Lähtöarvot manuaalisesti (m) \
vai tiedostosta (t)? Anna joko m tai t ")

konetyö_tuntihinta = None
kone_tehtävä = None
miestyö_tuntihinta = None
mies_tehtävä = None
kuljetus_tuntihinta = None
auto_tehtävä = None
työpäivän_pituus_h = None
jaetun_tehtävän_pituus = None
nimen_max_pituus = 50

#Kutsutaan funktioita 3. kelpo_luku, 4. kelpo_kokonaisluku, 
#7. kelpo_päivämäärä mikäli käyttäjä valitsee m
if tiedosto_vai_manuaali == "m":
    
    while True:
        kohteen_nimi = input("Anna kohteen nimi (max 50 merkkiä): ")

        if kohteen_nimi and len(kohteen_nimi) <= nimen_max_pituus:
            break
        else:
            print(f"Virhe: Kohteen nimi ei voi olla tyhjä ja nimen pituus saa \
olla enintään {nimen_max_pituus} merkkiä. Yritä uudelleen.")

    
    konetyö_tuntihinta = kelpo_luku("Konetyön tuntikustannus (50...200): ", \
    minimi=50, maksimi=200)

    kone_tehtävä = kelpo_luku("Koneita tehtävissä oletusarvo (1...10): ", \
    minimi=1, maksimi=10)

    miestyö_tuntihinta = kelpo_luku("Miestyön tuntikustannus (25...100): ", \
    minimi=25, maksimi=100)

    mies_tehtävä = kelpo_luku("Miehiä tehtävissä oletusarvo (1...10): ", \
    minimi=1, maksimi=10)

    kuljetus_tuntihinta = \
    kelpo_luku("Kuljetuksen tuntikustannus (50...200): ",minimi=50, maksimi=200)

    auto_tehtävä = kelpo_luku("Autoja tehtävissä oletusarvo (1...10): ", \
    minimi=1, maksimi=10)

    työpäivän_pituus_h = kelpo_kokonaisluku("Mikä on työpäivän pituus (1...12)? ", \
    minimi=1, maksimi=12)

    jaetun_tehtävän_pituus = kelpo_kokonaisluku \
    ("Kuinka monen päivän kestoisiksi tehtvät jaetaan (1...20)? ", \
    minimi=1, maksimi=20)

    aloitus_päivämäärä = kelpo_päivämäärä("Aloituspäivämäärä? \
(esim. 30.12.2023): ")
    
    while True:
        csv_laskentatiedoston_nimi = input("Laskentatiedoston nimi \
(muista pääte: .csv): ")

        try:
            with open(csv_laskentatiedoston_nimi, 'r') as csvfile:
                reader = csv.reader(csvfile)
                
                header = next(reader)
                sarakkeita_laskentatiedostossa = 17
                
                if len(header) != sarakkeita_laskentatiedostossa:
                    raise \
                ValueError(f'Tiedoston otsikot eivät sisällä tarkalleen \
{sarakkeita_laskentatiedostossa} saraketta.')   
            break 

        except FileNotFoundError:
            print(f'Laskentatiedostoa "{csv_laskentatiedoston_nimi}" ei löydy. \
Tarkista tiedostonimi ja yritä uudelleen.')
        except ValueError as ve:
            print(f'Virhe tiedoston käsittelyssä: {ve}')
        except Exception as e:
            print(f'Muun tyyppinen virhe tiedoston käsittelyssä: {e}')
        
    csv_tulosteen_nimi = input("Tulostetiedosten nimi, johon tulos \
tallennetaan (muista pääte: .csv): ")

elif tiedosto_vai_manuaali == "t":

    while True:
        csv_lähtöarvotiedoston_nimi = input("Lähtöarvotiedoston nimi \
(muista pääte: .csv): ")

        try:
            with open(csv_lähtöarvotiedoston_nimi, 'r', encoding='utf-8') \
                as lähtöarvot:
                reader = csv.DictReader(lähtöarvot)
                
                lähtöarvotiedoston_sarakkeet = [
                                    'kohteen_nimi',
                                    'konetyö_tuntihinta',
                                    'kone_tehtävä',
                                    'miestyö_tuntihinta',
                                    'mies_tehtävä',
                                    'kuljetus_tuntihinta',
                                    'auto_tehtävä',
                                    'työpäivän_pituus_h',
                                    'jaetun_tehtävän_pituus',
                                    'Aloituspäivämäärä',
                                    'csv_laskentatiedoston_nimi',
                                    'csv_tulosteen_nimi']

                file_found = False
                
#Kutsutaan funktioita 5. kelpo_luku_tiedostosta, 
#6. kelpo_kokonaisluku_tiedostosta kun käyttäjä on valinnut 't'
                for row in reader:
                    if all(column in row for column in \
                        lähtöarvotiedoston_sarakkeet) and \
                        len(row) == len(lähtöarvotiedoston_sarakkeet):
                        
                        kohteen_nimi = row['kohteen_nimi']
                        
                        konetyö_tuntihinta = kelpo_luku_tiedostosta \
                        (row['konetyö_tuntihinta'], minimi=50, maksimi=200)
                        
                        kone_tehtävä = kelpo_luku_tiedostosta \
                        (row['kone_tehtävä'], minimi=1, maksimi=10)
                        
                        miestyö_tuntihinta = kelpo_luku_tiedostosta \
                        (row['miestyö_tuntihinta'], minimi=25, maksimi=100)
                        
                        mies_tehtävä = kelpo_luku_tiedostosta \
                        (row['mies_tehtävä'], minimi=1, maksimi=10)
                        
                        kuljetus_tuntihinta = kelpo_luku_tiedostosta \
                        (row['kuljetus_tuntihinta'], minimi=50, maksimi=200)
                        
                        auto_tehtävä = kelpo_luku_tiedostosta \
                        (row['auto_tehtävä'], minimi=1, maksimi=10)
                        
                        työpäivän_pituus_h = kelpo_kokonaisluku_tiedostosta \
                        (row['työpäivän_pituus_h'], minimi=1, maksimi=12)
                        
                        jaetun_tehtävän_pituus = kelpo_kokonaisluku_tiedostosta \
                        (row['jaetun_tehtävän_pituus'], minimi=1, maksimi=20)
                        
                        date_input = row['Aloituspäivämäärä']
                        
                        aloitus_päivämäärä = \
                        datetime.strptime(date_input, "%d.%m.%Y")
                        csv_laskentatiedoston_nimi = \
                        row['csv_laskentatiedoston_nimi']
                        csv_tulosteen_nimi = row['csv_tulosteen_nimi']

                        try: 
                            with open(csv_laskentatiedoston_nimi, 'r', \
                                      encoding='utf-8') as csv_2:
                                csv_2 = csv.DictReader(csv_2) 
                            file_found = True
                            break
                        
                        except FileNotFoundError:
                            print(f'Lähtöarvotiedostossa \
"{csv_lähtöarvotiedoston_nimi}" viitattua laskentatiedostoa \
"{csv_laskentatiedoston_nimi}" ei löydy. Tarkista tiedostonimi \
ja yritä uudelleen.')
                            continue
                    else:
                        print(f'Tiedostossa "{csv_lähtöarvotiedoston_nimi}" \
ei oikeita sarakeotsikoita. Tiedostossa pitää olla nämä sarakeotsikot: \
{lähtöarvotiedoston_sarakkeet}')
                        break

                if file_found:
                    break

        except FileNotFoundError:
            print(f'Lähtöarvotiedostoa "{csv_lähtöarvotiedoston_nimi}" \
ei löydy. Tarkista tiedostonimi ja yritä uudelleen.')
        except IndexError as i:
            print(f'Virhe tiedoston käsittelyssä: {i}')
        except ValueError as ve:
            print(f'Virhe tiedoston käsittelyssä: {ve}')
        except Exception as e:
            print(f'Yleinen virhe tiedoston käsittelyssä: {e}')

"""Käyttäjän valitseman laskentatiedoston (tässä määrä- 
ja yksikköhintaluettelo) käsittely ja tehtävät 'sanakirjan' luonti.
"""
with open(csv_laskentatiedoston_nimi) as tehtävät_file:
    rivit = tehtävät_file.read().splitlines()[1:]
    
tehtävät = {}

jaetut_tehtävät = []

tehtävä_nro = 1

for rivi in rivit:
    rivi = rivi.split(",")
    tehtävä = rivi[3]
    määrä = float(rivi[5])
    konetyö = rivi[11].strip()
    miestyö = rivi[13].strip()
    kuljetus = rivi[10].strip()
    yhteensä_eur = rivi[-1].strip()
    
    if konetyö and konetyö.replace('.', '', 1).isdigit():
        konetyö_eur = float(konetyö)
    else:
        konetyö_eur = 0.0
    
    if miestyö and miestyö.replace('.', '', 1).isdigit():
        miestyö_eur = float(miestyö)
    else:
        miestyö_eur = 0.0

    if kuljetus and kuljetus.replace('.', '', 1).isdigit():
        kuljetus_eur = float(kuljetus)
    else:
        kuljetus_eur = 0.0
    if yhteensä_eur and yhteensä_eur.replace('.', '', 1).isdigit():
        yhteensä_eur = float(yhteensä_eur)
    else:
        yhteensä_eur = 0.0
        

    """Tehtävien kokonaiskustannusten laskenta kustannuspaikoittain ja 
    kokonaiskustannus jokaisen tehtävän riveiltä kustannuspaikan kustannus 
    lisääntyy
    """
    if tehtävä in tehtävät:
        tehtävät[tehtävä]["Konetyö"] += määrä * konetyö_eur
        tehtävät[tehtävä]["Miestyö"] += määrä * miestyö_eur
        tehtävät[tehtävä]["Kuljetus"] += määrä * kuljetus_eur
        tehtävät[tehtävä]["Yhteensä"] += yhteensä_eur
    else:
        tehtävät[tehtävä] = {"Konetyö": määrä * konetyö_eur,
                             "Miestyö": määrä * miestyö_eur,
                             "Kuljetus": määrä * kuljetus_eur,
                             "Yhteensä": yhteensä_eur}
        
aloitus_pvm = aloitus_päivämäärä

for tehtävä, summa in tehtävät.items():
    konetyö_yhteensä_eur = summa['Konetyö']
    miestyö_yhteensä_eur = summa['Miestyö']
    kuljetus_yhteensä_eur = summa['Kuljetus']
    yhteensä_total_eur = summa['Yhteensä']
    #tehtävä_nro += 1

#Kutsutaan funktiota 1. kesto_kustannuspaikoille
    konetyö_päivät, konetyö_yhteensä_eur, \
    miestyö_päivät, miestyö_yhteensä_eur, \
    kuljetus_päivät, miestyö_yhteensä_eur = kesto_kustannuspaikoille(
        konetyö_yhteensä_eur,
        miestyö_yhteensä_eur,
        kuljetus_yhteensä_eur,
        kone_tehtävä,
        mies_tehtävä,
        auto_tehtävä,
        konetyö_tuntihinta,
        miestyö_tuntihinta,
        kuljetus_tuntihinta,
        työpäivän_pituus_h
    )

#Kutsutaan funktiota 2. luo_taskit_lista    
    jaetut_tehtävät.extend(luo_taskit_lista(
        tehtävä,
        tehtävä_nro,
        konetyö_päivät,
        konetyö_yhteensä_eur,
        miestyö_päivät,
        miestyö_yhteensä_eur,
        kuljetus_päivät,
        kuljetus_yhteensä_eur,
        yhteensä_total_eur,
        jaetun_tehtävän_pituus,
        aloitus_pvm,
    ))

csv_sarakkeet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

fieldnames = ['Nro'] + [str(i) for i in csv_sarakkeet] + \
             ['Koneita / tehtävä'] + ['Miehiä / tehtävä'] + \
             ['Autoja / tehtävä'] + ['Päätehtävä nro'] + \
             ['Aloitus_2'] + ['Resurssi']

csv_tulosteen_nimi_1 = 'output1.csv'

#Kirjoitetaan pilkotut tehtävät csv tiedostoon
with open(csv_tulosteen_nimi_1, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    päätehtävä_numero = 0

    for index, tehtävä in enumerate(jaetut_tehtävät):
        row_data = {'Nro': index + 1}
        
        if int(tehtävä[csv_sarakkeet[-1]]) == 1:
            päätehtävä_numero += 1
        else:
            päätehtävä_numero = päätehtävä_numero
        
        row_data['Päätehtävä nro'] = päätehtävä_numero

        row_data.update({str(key): value for key, value in tehtävä.items()})
        row_data['Koneita / tehtävä'] = kone_tehtävä
        row_data['Miehiä / tehtävä'] = mies_tehtävä
        row_data['Autoja / tehtävä'] = auto_tehtävä
        row_data['Aloitus_2'] = 0
        row_data['Resurssi'] = 0

        writer.writerow(row_data)

#Funktio 9. aloitus_ja_valmis_päivämäärät tiedoston luku ja kirjoitus
def aloitus_ja_valmis_päivämäärät(
    luettava_tiedosto: str, kirjoitettava_tiedosto: str
    ) -> None:
    """Varsinainen aikataulu funktio, jonka parametreinä on kaksi 
    tiedostoa (tiedostopolkua eli str). Ensimmäinen luetaan ja toinen 
    kirjoitetaan. Eli ei palauta mitään arvoja vaan kirjoittaa uudet 
    arvot (aloitus ja valmis) tehtväville tiedostoon keston mukaan.
    Huomioi Aloitus_2 päivämäärän, jos sellainen osassa 2 annetaan.
    Käyttää funktiota työpäivät valmis -arvon laskentaan.
    """
    with open(luettava_tiedosto, 'r', newline='', encoding='latin-1') as infile, \
         open(kirjoitettava_tiedosto, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        header = next(reader)
        header += ['Aloitus_1', 'Valmis_1']
        writer = csv.writer(outfile)
        writer.writerow(header)
        aloitus_1 = aloitus_pvm

        for row in reader:
            kesto = float(row[2])

            valmis_1 = ""  

            if len(row) > 0 and row[15] != '0': #Aloitus_2 mikäli sellainen on
                aloitus_1 = datetime.strptime(row[15], '%d.%m.%Y')

            #Kutsutaan funktiota 8. työpäivät
            valmis_1 = työpäivät(aloitus_1, kesto, arkipyhät).strftime('%d.%m.%Y')
            row += [aloitus_1.strftime('%d.%m.%Y'), valmis_1]
            writer.writerow(row)
            aloitus_1 = datetime.strptime(valmis_1, '%d.%m.%Y') + timedelta(days=1)
            #Aloitus edellisen valmistumispäivämäärä + 1päivä???

#Kutsutaan funktiota 9. aloitus_ja_valmis_päivämäärät luo csv tiedoston
#jossa tehtävillä päivämäärät aloitus ja valmis
aloitus_ja_valmis_päivämäärät(csv_tulosteen_nimi_1, 'output.csv')

csv_tulosteen_nimi_1 = 'output.csv'

with open(csv_tulosteen_nimi_1, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

#Ohjelma osan 1. tulostaulukko
#Otetaan käyttään PrettyTable kirjasto
#Taulukkoon 1. tulostettavat sarakkeet
tulostettavat_2 = ['Nro', '0', '1', 'Päätehtävä nro', 'Aloitus_1', 'Valmis_1']

taulukko_2 = PrettyTable(tulostettavat_2)

taulukko_2.align = 'l'

for row in data:
    taulukko_2.add_row([row[column] for column in tulostettavat_2])

print(taulukko_2)

print(f'________________________________________________________________'"\n")
print(f'TKO_2111 Ohjelmoinnin harjoitustyö 2023')
print(f'MÄÄRÄ- JA YKSIKKÖHINTALUETTELOON PERUSTUVA AIKATAULUOHJELMA')
print(f'OSA 2 LAJITTELU, RIIPPUVUUDET JA RESURSSIT {tänään_muodossa}')
print(f'________________________________________________________________'"\n")

csv_tulosteen_nimi_1 = 'output.csv'

with open(csv_tulosteen_nimi_1, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

#Lasketaan tehtävien määrä, josta kyselyn max
tehtäviä_yhteensä = max(int(row['Päätehtävä nro']) for row in data)

#Luodaan riippuvuudet-, aloitus_2- ja resurssi-sanakirjat.
#Kysytään käyttäjältä
riippuvuudet_sanakirja = {}
aloitus_2_sanakirja = {}
resurssi_sanakirja = {}

#Kysytään riippuvuuksia. Ensin tehtävä, 
#jolla riippuvuus sitten tehtävä, josta riippuvainen.
while True:
    task_number = kelpo_kokonaisluku(f"Onko tehtävillä riippuvuuksia? \
Jos on anna tehtävän numero (tehtäviä yhteensä \
'{tehtäviä_yhteensä}') tai ohita = 0: ", \
minimi=0, maksimi=tehtäviä_yhteensä+1)
    if task_number == 0:
        break
    dependency_value = kelpo_kokonaisluku \
(f"Anna tehtävän numero, jonka jälkeen tehtävä nro '{task_number}' \
pitäisi alkaa: ", minimi=1, maksimi=tehtäviä_yhteensä+1)
    
    riippuvuudet_sanakirja[int(task_number)] = dependency_value

while True:
    task_number_2 = kelpo_kokonaisluku \
(f"Tietyn tehtävän aloitus. Anna tehtävän numero (tehtäviä yhteensä \
'{tehtäviä_yhteensä}') tai ohita = 0: ", \
minimi=0, maksimi=tehtäviä_yhteensä+1)
    if task_number_2 != 0:
        """aloitus_2 = kelpo_päivämäärä(f"Anna tehtävän '{task_number_2}' \
        aloituspäivämäärä: ")  ??? funktio kelpo_päivämäärä ei jostain 
        syystä toimi tässä ???
        #aloitus_2_mapping[int(task_number_2)] = aloitus_2
        """
        try:
            aloitus_2 = input(f"Anna tehtävän '{task_number_2}' \
aloituspäivämäärä (siirtää sen jälkeiset \
tehtävät tämän jälkeiseen aikaan) : ")
            datetime.strptime(aloitus_2, '%d.%m.%Y')
        
        except ValueError:
            print(f'Ei kelpaa. "{aloitus_2}" ei ole päivämäärä tai oikea \
muoto dd.mm.yyyy. Yritä uudelleen.')
            continue
        
        aloitus_2_sanakirja[int(task_number_2)] = aloitus_2
    
    else:
        break

resurssit_csv_file = 'resurssit.csv'

while True:
    task_number_3 = kelpo_kokonaisluku(f"Tehtävän resurssi? "
f"Oletuksena resurssi 1. "
f"Jos on anna tehtävän numero (tehtäviä yhteensä '{tehtäviä_yhteensä}') "
f"tai ohita = 0: ",
    minimi=0, maksimi=tehtäviä_yhteensä + 1)
    if task_number_3 == 0:
        break

    """print("Resurssivaihtoehdot: ")
    with open(resurssit_csv_file, newline='', encoding='utf-8') as resurssi_file:
        resurssi_reader = csv.reader(resurssi_file)
        resurssit = list(resurssi_reader)
        resursseja_yhteensä = len(resurssit)
    for index, team in enumerate(resurssit, start=1):
        print(f"{index}: {team[0]}")
    """
    print("Resurssivaihtoehdot: ")

    with open(resurssit_csv_file, newline='', encoding='utf-8') as resurssi_file:
        resurssi_reader = csv.reader(resurssi_file)
        resurssit = list(resurssi_reader)

        if not resurssit:
            print("No teams found in the CSV file.")
        else:
            resursseja_yhteensä = len(resurssit[0])

            for index, team in enumerate(resurssit[0], start=1):
                print(f"{index}: {team}")
        resurssi = kelpo_kokonaisluku(f"Anna resurssin numero,\
tehtävälle nro '{task_number_3}': ",
        minimi=1, maksimi=resursseja_yhteensä + 1)
        
        resurssi_sanakirja[int(task_number_3)] = resurssi

#Lajittelu riippuvuus sarakkeen mukaan
for row in data:
    task_number = int(row['Päätehtävä nro'])
    row['Riippuvuus'] = riippuvuudet_sanakirja.get(task_number, 0)

for row in data:
    row['Riippuvuus'] = row.get('Riippuvuus', 0)
   
for row in data:
    if row['Riippuvuus'] > 0:
        row['Sort_Key'] = int(row['Riippuvuus']) + 0.1
    else:
        row['Sort_Key'] = int(row['Päätehtävä nro'])

for row in data:
    task_number = int(row['Päätehtävä nro'])

    row['Resurssi'] = resurssi_sanakirja.get(task_number, 1)

    #Resurssi 2 sarakkeeseen resurssin nimi
    resurssi = resurssi_sanakirja.get(task_number)
    with open(resurssit_csv_file, newline='', encoding='utf-8') as resurssi_file:
        resurssi_reader = csv.reader(resurssi_file)
        resurssit = list(resurssi_reader)
    if resurssi is not None:
        if 0 < resurssi <= len(resurssit[0]):
            row['Resurssi 2'] = resurssit[0][resurssi - 1]
        else:
            print("Ei kelpaa:", resurssi)
            
    else:
        
        row['Resurssi 2'] = resurssit[0][0] #Oletus resurssi 1.

data = sorted(data, key=lambda x: x['Sort_Key'])
      
if isinstance(riippuvuudet_sanakirja, dict) and len(riippuvuudet_sanakirja) > 0:
    for row in data:
        if row['Riippuvuus'] == 0:
            row['Riippuvuus'] = " "

csv_tulosteen_nimi_1 = 'output.csv'

#Aloitus_2 päivämäärä sarakkeeseen
if isinstance(aloitus_2_sanakirja, dict) and len(aloitus_2_sanakirja) > 0:
    for row in data:
        task_number_2 = int(row['Päätehtävä nro'])
        row['Aloitus_2'] = aloitus_2_sanakirja.get(task_number_2, 0)
        
for row in data:
    row['Aloitus_2'] = row.get('Aloitus_2', 0)


if isinstance(aloitus_2_sanakirja, dict) and len(aloitus_2_sanakirja) > 0:
    
    päivämäärät = set()

    for row in data:
        aloitus_2_value = row['Aloitus_2']

        #Poistetaan 'duplikaatit' Aloitus_2 sarakkeesta - osatehtäviltä
        if aloitus_2_value not in päivämäärät:
            päivämäärät.add(aloitus_2_value)
        else:
            row['Aloitus_2'] = 0

for row in data:
    row['Aloitus_2'] = row.get('Aloitus_2', 0)

fieldnames = data[0].keys()

#Poistetaan ensimmäisen aloitus_ja_valmis_päivämäärät funktion
#lisäämät sarakkeet
poistettavat_sarakkeet = ['Aloitus_1', 'Valmis_1']

for row in data:
    for sarake in poistettavat_sarakkeet:
        row.pop(sarake, None)

#Kirjoitetaan data csv-tiedostoon
with open(csv_tulosteen_nimi_1, 'w', newline='', encoding='latin-1') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

csv_tulosteen_nimi_1 = 'output.csv'

#Kutsutaan funktiota 9. aloitus_ja_valmis_päivämäärät 
aloitus_ja_valmis_päivämäärät(csv_tulosteen_nimi_1, 'output_.csv')

csv_tulosteen_nimi_1 = 'output_.csv'

with open(csv_tulosteen_nimi_1, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

#Lisätään Tehtävän nro sarake juoksevalla numeroinnilla
for index, row in enumerate(data, start=1):
    row['Tehtävä nro'] = index

#Nimetään sarakkeet kuvailevilla nimillä
sarake_mapping = {
    'Tehtävä nro': 'Tehtävä nro',
    '0': 'Tehtävä',
    '1': 'Kesto konetyö',
    '4': 'Yhteensä EUR',
    '5': 'EUR konetyö',
    '6': 'EUR miestyö',
    '7': 'EUR kuljetus',
    'Päätehtävä nro': 'Päätehtävä nro',
    'Aloitus_2': 'Aloitus_2',
    'Riippuvuus': 'Riippuvuus',
    'Resurssi': 'Resurssi',
    'Resurssi 2': 'Resurssi 2',
    'Aloitus_1': 'Aloitus',
    'Valmis_1': 'Valmis'
}

päivitetty_taulukko = []
for row in data:
    new_row = {sarake_mapping.get(key, key): value 
    for key, value in row.items()}
    päivitetty_taulukko.append(new_row)

#Valitaan sarakkeet
tulostettavat_sarakkeet = ['Tehtävä nro', 'Tehtävä', 'Kesto konetyö', 
'Yhteensä EUR', 'EUR konetyö', 'EUR miestyö', 'EUR kuljetus',
'Päätehtävä nro', 'Aloitus_2', 'Riippuvuus', 'Resurssi', 'Resurssi 2',
'Aloitus', 'Valmis']

valitut_sarakkeet = [{key: row[key] for key in tulostettavat_sarakkeet} 
for row in päivitetty_taulukko]

csv_tulosteen_nimi_1 = csv_tulosteen_nimi
with open(csv_tulosteen_nimi_1, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=tulostettavat_sarakkeet)
    writer.writeheader()
    writer.writerows(valitut_sarakkeet)

csv_tulosteen_nimi_1 = csv_tulosteen_nimi

with open(csv_tulosteen_nimi_1, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

#Ohjelma osan 2. tulostaulukko
#Taulukkoon 2. tulostettavat sarakkeet
tulostettavat_2 = ['Tehtävä', 'Kesto konetyö', 'Päätehtävä nro',
'Aloitus_2', 'Riippuvuus', 'Resurssi', 'Resurssi 2', 'Aloitus', 'Valmis']

taulukko_2 = PrettyTable(tulostettavat_2)

taulukko_2.align = 'l'

for row in data:
    taulukko_2.add_row([row[column] for column in tulostettavat_2])

#Ohjelman lopullinen tuloste kirjoitetaan ja nimetään käyttäjän antamalla
#tulostiedoston nimellä ja printataan tulos ja viesti. 
print(taulukko_2)
print(f'________________________________________________________________'"\n")
print(f"Tuloste tiedostossa '{csv_tulosteen_nimi_1}'")
print(f'________________________________________________________________'"\n")

#*****************************************************************************
"""Osa 3 lainattu Datacamp tutorialista, jossa luodaan Gantt-kaavio.
https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib
"""
#*****************************************************************************
#Otetaan käyttöön Pandas kirjasto csv tiedoston käsittelyyn
#Otetaan käyttöön Matplotlib kirjasto
#Otetaan käyttöön Numpy kirjasto

teams_df = pd.read_csv('resurssit.csv') 
csv_tulosteen_nimi_1 = csv_tulosteen_nimi

df = pd.read_csv(csv_tulosteen_nimi_1)
with open('resurssit.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        resurssit = row

resurssi_dict = {i + 1: value.strip(" '") for i, value in enumerate(resurssit)}

"""Käytetään edellisen osan tulos csv:a ja luodaan tehtavat_list ja team_list,
jotka voidaan sijoittaa pd.DataFrameen (tutorialista). 
start_lista ja end_list samoin edellisen osan dataframeistä, mutta 
päivämäärämuoto muutetaan tutorialin mukaiseksi '31 Oct 2022'
Valmistumisaste (completion_frac) on tässä koravattu 1 kertomalla
tehtävät_list pituus. Ominaisuus jätetään kehitysversioon...
"""

tehtavat_list = df['Tehtävä'].tolist()

df['Resurssi'] = df['Resurssi'].replace(resurssi_dict)
team_list = df['Resurssi'].tolist()
start_list = df['Aloitus'].tolist()
start_dates = pd.to_datetime(start_list, format='%d.%m.%Y')
start_dates_str = start_dates.strftime('%d %b %Y') #päivämäärien formaattimuunnos

end_list = df['Valmis'].tolist()
end_dates = pd.to_datetime(end_list, format='%d.%m.%Y')
end_dates_str = end_dates.strftime('%d %b %Y') #päivämäärien formaattimuunnos

df_gantt = pd.DataFrame({'task': tehtavat_list,
                         'team': team_list,
                         'start': pd.to_datetime(start_dates_str),
                         'end': pd.to_datetime(end_dates_str),
                         'completion_frac': [1] * len(tehtavat_list)})


df_gantt['days_to_start'] = (df_gantt['start'] - df_gantt['start'].min()).dt.days
df_gantt['days_to_end'] = (df_gantt['end'] - df_gantt['start'].min()).dt.days
df_gantt['days_to_end'] = (df_gantt['end'] - df_gantt['start'].min()).dt.days
df_gantt['task_duration'] = df_gantt['days_to_end'] - df_gantt['days_to_start'] + 1 
df_gantt['completion_days'] = df_gantt['completion_frac'] * df_gantt['task_duration']

#matplotlib.colors
#b: blue
#g: green
#r: red
#c: cyan
#m: magenta
#y: yellow
#k: black
#w: white

matplotlib_colors = ['y','m','b','r','c']

#Luodaan resurssi_väritys sanakirja värilistan ja teams_df yhdistelmällä
resurssi_väritys = {}

for i, team in enumerate(teams_df):
    color_index = i
    if color_index >= len(matplotlib_colors): 
    #Jos värikartta loppuu kesken eli resursseja enemmän, aloitetaan alusta
        color_index = 0
    resurssi_väritys[team] = matplotlib_colors[color_index]

resurssi_väritys = {
    key.strip('\'"'): value
    for key, value in resurssi_väritys.items()
}
team_colors = resurssi_väritys

patches = []
for team in team_colors:
    patches.append(matplotlib.patches.Patch(color=team_colors[team]))

fig, ax = plt.subplots()
for index, row in df_gantt.iterrows():
    plt.barh(y=row['task'], width=row['task_duration'],
    left=row['days_to_start'] + 1, color=team_colors[row['team']], alpha=0.4)
    
    plt.barh(y=row['task'], width=row['completion_days'], 
    left=row['days_to_start'] + 1, color=team_colors[row['team']])

plt.title(f"{kohteen_nimi} yleisaikataulu {tänään_muodossa}", fontsize=15)
plt.gca().invert_yaxis()

xticks = np.arange(5, df_gantt['days_to_end'].max() + 2, 7)

xticklabels = pd.date_range(start=df_gantt['start'].min() + 
dt.timedelta(days=4), end=df_gantt['end'].max()).strftime("%d.%m.")

ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels[::7])
ax.xaxis.grid(True, alpha=0.5)

ax.legend(handles=patches, labels=team_colors.keys(), fontsize=10)

tänään_timestamp = pd.to_datetime(tänään)

nykyhetki = (tänään_timestamp - df_gantt['start'].min()).days + 1

ax.axvline(x=nykyhetki, color='b', linestyle='dashed')
ax.text(x=nykyhetki + 1, y=0, s=f"NYKYHETKI {tänään_muodossa}", color='b')

plt.show()

#print(print.__doc__)
#import pydoc

#pydoc.writedoc("aikataulu")