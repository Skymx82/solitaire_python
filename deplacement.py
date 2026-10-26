from affichage import *
from jeu_depart import piles,cachees, index

def deplacement(move, piles, cachees, index):
    carte, destination = move.split("-")

    depart = index[carte]  # la pile où est la carte, ex : "c6"
    position = piles[depart].index(carte)  # sa place dans cette pile
    morceau = piles[depart][position:]  # la carte + toutes celles posées dessus

    del piles[depart][position:]  # on enlève le morceau du départ
    piles[destination].extend(morceau)  # on le pose sur l'arrivée

    for c in morceau:  # chaque carte déplacée change de pile
        index[c] = destination

    # Si le départ est une colonne et qu'il ne reste que des cartes cachées,
    # on retourne celle du dessus.
    if depart in cachees:
        if len(piles[depart]) > 0 and len(piles[depart]) == cachees[depart]:
            cachees[depart] = cachees[depart] - 1


# Test : les 4 premiers coups de la partie
deplacement("5ca-c4", piles, cachees, index)
deplacement(piles["p"][-1] + "-d", piles, cachees, index)   # piocher
deplacement("7co-c2", piles, cachees, index)
deplacement("6tr-c2", piles, cachees, index)

afficher(piles, cachees)