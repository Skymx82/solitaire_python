#le but de vérif carte est d'empecher de bouger une carte caché ou dans la pioche ainsi
#que déplacer qu'une seule carte à la fois dans les fondations
import pioche
import affichage
from jeu_depart import piles, cachees, index


def verif_carte(carte, destination, cachees, morceau,index):

    if index[carte] == "p":
        print("la carte n'est pas disponible")
        return False

    if index[carte] in cachees : # les cartes dans la pioche ne peuvent plus bougé
        print("la carte n'est pas disponible")
        return False

    if index[carte] == "d" and piles["d"][-1] != carte :
        print("la carte n'est pas disponible")
        return False

    if index[carte][0] == "f" and piles[index[carte]][-1] != carte:
        print("la carte n'est pas disponible")
        return False

    if destination[0] == "f" and len(morceau) > 1 : # seulement 1 cartes à la fois dans les fondations
        print("une seule carte à la fois dans fondations")
        return False

    return True
