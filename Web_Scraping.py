# 1. Téléchargement des bibiblothèques

from modTP import url_to_html, html_to_soup, html_str_to_int, db_covid_canada, SQLite_to_DF_covid
from datetime import datetime, timedelta
from time import sleep
from modTimer import random_timestamp


def main():
    # ######################################## #
    # ## GÉNÉRATION D'UN TIMELINE ALÉATOIRE ## #
    # ######################################## #

    start_date = datetime.now()  # datetime(2020, 8, 10)
    end_date = datetime(2020, 8, 15)  # date de fin
    step = timedelta(days=1)  # le pas d'une journée pour N enregistrements
    p = 25  # nombre d'enregistrement par 24 heures

    timer_ = [datetime.timestamp(start_date)]  # Horodatage pour la date début

    # Génération d'une chronologie (timeline) temporelle aléatoire à partir des horodatages
    timer = random_timestamp(start_date, end_date, step, p)

    timer_.extend(timer)  # Ajouter à l'horodatage de début l'horodatage aléatoire

    nbr_requests = len(timer_) - 1  # le nombre total de requêtes

    # Caculer la différence de temps (en secondes) entre deux enregistrements
    elapsed_timer = [abs((timer_[k + 1]) - (timer_[k])) for k in range(len(timer_) - 1)]

    # Afficher le début de la boucle de scraping

    print("============================================")
    print(" Web Scraping en Cours - Veuillez Patientez! ")
    print("============================================")

    # ####################################### #
    # ## WEB SCRAPING - COVID-19 AU CANADA ## #
    # ####################################### #

    # 2. Déclarer les variables à initialiser
    requests = 0  # numéro de la requête

    for _ in range(nbr_requests):
        # Afficher les informations sur la requête
        requests += 1  # on incrémente la variable requests
        print('Request: {}'.format(requests))  # on affiche le numéro de requête

        # 2. Téléchager l'url et faire une requête GET

        url = "https://www.canada.ca/fr/sante-publique/services/maladies/maladie-coronavirus-covid-19.html"
        url_html = url_to_html(url)

        # 3. Utiliser Beautifulsoup
        html_soup = html_to_soup(url_html)

        # 4. Utiliser la méthode find_all() pour extraire le container HTML
        containers_0 = html_soup.find_all('div', class_="row wb-eqht wb-init")

        # 5. Paramètres pour les balises des éléments à récupérer de la page HTML

        param_s = [
            "bg-success text-center brdr-lft brdr-lft brdr-rght brdr-tp brdr-bttm",
            "bg-info text-center brdr-lft brdr-lft brdr-rght brdr-tp brdr-bttm",
            "text-center brdr-lft brdr-lft brdr-rght brdr-tp brdr-bttm",
            "bg-warning text-center brdr-lft brdr-lft brdr-rght brdr-tp brdr-bttm",
            "bg-danger text-center brdr-lft brdr-lft brdr-rght brdr-tp brdr-bttm"
        ]

        # 6. Les balises de la page HTML
        param_t = ['section', 'p', "h2 mrgn-tp-md"]

        ls = len(param_s)

        # 7. Extraire les éléments de la page

        content0 = [containers_0[0].find(param_t[0], class_=param_s[l]) for l in range(0, ls)]

        # 8. Extraire les titres des éléments extraits
        title = [content0[l].p.text for l in range(0, ls)]
        titles = ["Date", "Heure"]  # Créer une liste de string pour les valeurs Date et Heure
        titles.extend(title)  # ajouter à la liste de titres extraite la date et l'heure

        # Préparer la date et l'heure de l'enregistrement

        now = datetime.now()  # Date et Heure d'enregistrement
        date_ = now.strftime("%Y-%m-%d")  # mettre la date au format string
        time_ = now.strftime("%H:%M:%S")  # mettre l'heure au format string
        contents = [date_, time_]  # stocker la date et l'heure

        content1 = [html_str_to_int(content0[l].find(param_t[1], class_=param_t[2]).text) for l in range(0, ls)]
        contents.extend(content1)

        db_covid_canada(contents)  # Stocker dans une base de données SQLite

        # Afficher les informations sur la date et heure de la requête
        print("date:", date_, "time:", time_)

        # Temps d'attente pour la prochaine requête
        sleep(elapsed_timer[requests])

    # Importer les résultats d'une requête SQLite dans un DataFrame pour l'exploration de données
    df = SQLite_to_DF_covid("covid_canada.dbf")

    # Verifier le résultat de la requête SQL est stocké dans un dataframe
    print(df.head(20))  # afficher les 20 premières valeurs de la table tabulaire (dataframe)


if __name__ == '__main__':
    main()
