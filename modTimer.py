from datetime import datetime, time, timedelta
from random import randrange


### Générer une séquence de dates ###

def seq_date(start, end, step):
    """
    Générer une séquence de dates
    :param start: Date de début (objet datetime)
    :param end: Date de fin (objet datetime)
    :param step: Pas (par jour, par heure, etc.) - objet timedelta
    :return:
    """
    dstamp = []

    while start < end:
        dstamp.append(datetime.date(start))
        start += step

    return sorted(dstamp)


# Générer une séqunec de temps aléatoires

def random_seq_time(l):
    """
    Générer une séquence aléatoire de temps (heures, minutes, secondes)
    :param l: nombre d'enregistrement par 24 heures
    :return: séquence aléatoire ordonnée
    """
    seq_time = []

    while l > 0:
        seq_time.append(time(randrange(0, 24, 1),
                             randrange(0, 60, 1),
                             randrange(0, 60, 1)))
        l -= 1

    return sorted(seq_time)


def random_timestamp(start_date, end_date, step, p):
    """
    Générer aléatoirement une séquence de timestamp

    :param start_date: Date de début au format de l'objet datetime - datetime(2020, 8, 2)
    :param end_date: Date de fin au format objet datetime
    :param step: pas de changement de date au format objet - timedelta(days=1)
    :param p: Nombre d'enregistrement par jour
    :return: une séquence de horodatage (timestamp) aléatoirement
    """
    # Créer une liste d'objet datetime - timeline pour l'enregistrement

    date_seq = seq_date(start_date, end_date, step)
    timeline = []
    for date_ in date_seq:
        dt = random_seq_time(p)
        for i in range(len(dt)):
            timeline.append(datetime(date_.year, date_.month, date_.day,
                                     dt[i].hour, dt[i].minute, dt[i].second))

    # Créer une liste de datetime - timestamp pour l'enregistrement

    timestamp = [datetime.timestamp(timeline[k]) for k in range(0, len(timeline))]

    return timestamp
