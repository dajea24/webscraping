import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import pandas as pd


def url_to_html(url: str):
    """
    Extraire de la page de l'URL
    :param url: url de la page web
    :return: page au format HTML
    """
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    response = requests.get(url, headers=headers)
    html = response.text
    return html


def html_to_soup(html: str):
    """
    Convertir une page au format HTML en objet bs4
    :param html: page au format HTML
    :return: objet bs4
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup


def html_str_to_int(x: str):
    """
    Convertir un nombre en caractère HTML en nombre entier
    :param x: Nombre format HTML
    :return y: Nombre entier
    """
    y = int("".join(x.split()))
    return y


def file_csv(myList: list, filename: str):
    """
    Créer un fichier de sortie au format CSV
    :param myList: Séquence de listes pour créer le fichier .csv
    :param filename: Nom du fichier .csv
    :return: filename.csv
    """
    with open(filename, 'a', newline='') as myFile:
        wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)
        [wr.writerow(myList[k]) for k in range(0, len(myList))]

def db_covid_canada(data):
    """
    Stocker dans une base de données
    :param data:
    :return:
    """
    try:

        # ouverture de connexion
        conn = sqlite3.connect("../../Desktop/Web_Scraping/covid_canada.dbf")

        # obtenir le curseur
        curseur = conn.cursor()

        # Création de la table DDL
        cde = """ 
        create table if not exists covid( id integer primary key autoincrement unique,
        Jour TEXT, Heure TEXT,
        Testees REAL, Totaux REAL,
        Guerisons REAL, Actifs REAL,
        Deces REAL
        )"""

        # Executer la commande
        curseur.execute(cde)

        # requete/commande parametrée
        cde = """insert into covid(Jour, Heure, Testees, Totaux, Guerisons, Actifs, Deces)values(?,?,?,?,?,?,?) """
        curseur.execute(cde, data)  # Executer la commande
        conn.commit()  # Valider la commande

    except sqlite3.OperationalError as e:
        print(e)  # Gestion de l'erreur

    finally:
        # Fermeture de la connexion
        conn.close()


def SQLite_to_DF_covid(db):
    """
    Importer les résultats d'une requête SQLite dans un DataFrame
    :param db: nom de la base de données (string)
    :return:
    """
    con = sqlite3.connect(db)
    df = pd.read_sql_query("SELECT * from covid", con)

    return df
