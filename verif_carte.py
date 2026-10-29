#le but de vérif carte est d'empecher de bouger une carte caché ou dans la pioche ainsi
#que déplacer qu'une seule carte à la fois dans les fondations

import pioche

def verif_carte(carte, piles, destination, cachee):
    if carte in pioche : # les cartes caché ne peuvent plus bougé
        return False
    if carte in cachee : # les cartes dans la pioche ne peuvent plus bougé
        return False
    if destination[0] == "f" and carte