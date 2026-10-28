from affichage import *
from jeu_depart import piles,cachees, index
from verif_colonne import *
from pioche import *

def deplacement( piles, cachees, index):


    move_possible

    #permet de demander la deplacement
    move = input(print("Choisissez la carte a deplacer ainsi que sa direction"))


    if move == "p":
        piocher(piles, cachees, index)
        return False


    #obtenir la carte ainsi que la destination dans deux variable différente
    carte, destination = move.split("-")

    if destination is not in

    depart = index[carte]  # la pile où est la carte, ex : "c6"
    position = piles[depart].index(carte)  # sa place dans cette pile
    morceau = piles[depart][position:]  # la carte + toutes celles posées dessus

    #ici on va mettre tout les verifs avant de deplacer les cartes
    if verif_colonne(carte, destination, piles) == False:
        return False

    del piles[depart][position:]  # on enlève le morceau du départ
    piles[destination].extend(morceau)  # on le pose sur l'arrivée

    for c in morceau:  # chaque carte déplacée change de pile
        index[c] = destination

    # Si le départ est une colonne et qu'il ne reste que des cartes cachées,
    # on retourne celle du dessus.
    if depart in cachees:
        if len(piles[depart]) > 0 and len(piles[depart]) == cachees[depart]:
            cachees[depart] = cachees[depart] - 1

    afficher(piles, cachees)
