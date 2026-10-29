from sauvegarder import sauvegarder
from verif_coup import *
from affichage import *
from jeu_depart import piles,cachees, index
from verif_colonne import *
from pioche import *
from verif_fondations import *
from verif_carte import *


def deplacement( piles, cachees, index, nb_coups ):


    move_possible=["c1","c2","c3","c4","c5","c6","c7","fca","fpi","fco","ftr"]
    colonne = ["c1","c2","c3","c4","c5","c6","c7"]
    fondation = ["fca","fco","fpi","ftr"]


    #permet de demander la deplacement
    move = input("Choisissez la carte a deplacer ainsi que sa direction :")



    if move == "sauvegarde":
        sauvegarder(piles, cachees, index, nb_coups)
        return False

    if move == "p":
        piocher(piles, cachees, index)
        return False


    if verif_coup(move) == False:
        return False
    else :
        carte, destination = verif_coup(move)


    depart = index[carte]  # la pile où est la carte, ex : "c6"
    position = piles[depart].index(carte)  # sa place dans cette pile
    morceau = piles[depart][position:]  # la carte + toutes celles posées dessus


    if verif_carte(carte, destination, cachees,morceau,index) == False:
        return False

    #ici on va mettre tout les verifs avant de deplacer les cartes
    if destination in colonne :
        if verif_colonne(carte, destination, piles) == False:
            return False

    if destination in fondation :
        if verifier_fondation(carte, piles, destination) == False:
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
    return True
