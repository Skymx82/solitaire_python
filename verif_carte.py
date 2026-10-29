#le but de vérif carte est d'empecher de bouger une carte caché ou dans la pioche ainsi
#que déplacer qu'une seule carte à la fois dans les fondations

import pioche

def verif_carte(carte, destination, cachees, morceau):

    if carte in pioche : # les cartes caché ne peuvent plus bougé
        print("la carte n'est pas disponible")
        return False

    if carte in cachees : # les cartes dans la pioche ne peuvent plus bougé
        print("la carte n'est pas disponible")
        return False

    if destination[0] == "f" and morceau>1 : # seulement 1 cartes à la fois dans les fondations
        print("une seule carte à la fois dans fondations")
        return False