from sauvegarder import sauvegarder
from verif_coup import *
from affichage import *
from jeu_depart import piles,cachees, index
from verif_colonne import *
from pioche import *
from verif_fondations import *
from verif_carte import *
from coup_iav1 import afficher_coups


def deplacement( piles, cachees, index, nb_coups , difficulte, coup_ordi=""):

    move_possible=["c1","c2","c3","c4","c5","c6","c7","fca","fpi","fco","ftr"]
    colonne = ["c1","c2","c3","c4","c5","c6","c7"]
    fondation = ["fca","fco","fpi","ftr"]


    #permet de demander la deplacement
    #quand l'ordinateur joue tout seul, c'est main.py qui donne son coup dans coup_ordi
    if coup_ordi == "":
        move = input("Choisissez la carte à déplacer ainsi que sa direction : ")
    else:
        move = coup_ordi

    #affiche les coups possibles, puis on revient au plateau (ce n'est pas un coup)
    if move == "h":
        afficher_coups(piles, cachees, index)
        input("Appuyez sur Entrée pour continuer")
        afficher(piles, cachees, difficulte)
        return False

    if move == "sauvegarde":
        sauvegarder(piles, cachees, index, nb_coups, difficulte)
        return False

    #la pioche change le plateau sans compter comme un coup, main.py doit le savoir
    if move == "p":
        piocher(piles, cachees, index, difficulte)
        return "pioche"

    #affiche les règles, puis on revient au plateau (ce n'est pas un coup)
    if move == "?":
        afficher_regles()
        input("Appuyez sur Entrée pour revenir au jeu")
        afficher(piles, cachees, difficulte)
        return False

    #c'est main.py qui garde la copie de la partie, on le prévient juste
    if move == "annuler":
        return "annuler"

    #l'ordinateur va jouer tout seul : c'est main.py qui lui fait jouer les coups un par un
    if move == "ia":
        return "ia"



    if verif_coup(move) == False:
        return False
    else :
        carte, destination = verif_coup(move)


    depart = index[carte]  # la pile où est la carte, ex : "c6"
    position = piles[depart].index(carte)  # sa place dans cette pile
    morceau = piles[depart][position:]  # la carte + toutes celles posées dessus

    if verif_carte(carte, destination, cachees,morceau,index,piles) == False:
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

    afficher(piles, cachees, difficulte)
    return True
