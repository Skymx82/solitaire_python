#le but de vérif carte est d'empecher de bouger une carte caché ou dans la pioche ainsi
#que déplacer qu'une seule carte à la fois dans les fondations
import pioche
import affichage
from jeu_depart import cachees, index
from operator import truediv

def verif_carte(carte, destination, cachees, morceau,index,piles):

    if index[carte] == "p":
        print("la carte se trouve dans la pioche")
        return False

    depart = index[carte]
    position = piles[depart].index(carte)

    if depart in cachees:
        if position < cachees[depart]:  # même test que l'affichage
            print("Cette carte est face cachée, elle ne peut pas bouger")
            return False

    if position == "d" and piles["d"][-1] != carte :
        print("la carte se trouve dans la défausse")
        return False

    if destination[0] == "f" and len(morceau) > 1 : # seulement 1 cartes à la fois dans les fondations
        print("une seule carte à la fois dans fondations")
        return False

    return True
