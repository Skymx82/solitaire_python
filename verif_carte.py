#le but de vérif carte est d'empecher de bouger une carte caché ou dans la pioche ainsi
#que déplacer qu'une seule carte à la fois dans les fondations

def verif_carte(carte, destination, cachees, morceau,index,piles,parler=True):

    if index[carte] == "p":
        print("la carte se trouve dans la pioche")
        return False

    depart = index[carte]
    position = piles[depart].index(carte)

    if depart in cachees:
        if position < cachees[depart]:  # même test que l'affichage
            print("Cette carte est face cachée, elle ne peut pas bouger")
            return False

    #dans la défausse seule la carte du dessus peut bouger
    if depart == "d" and piles["d"][-1] != carte :
        print("la carte se trouve en dessous dans la défausse")
        return False

    #dans une fondation aussi, seule la carte du dessus peut bouger
    if depart[0] == "f" and piles[depart][-1] != carte :
        print("la carte se trouve en dessous dans la fondation")
        return False


    if destination[0] == "f" and len(morceau) > 1 : # seulement 1 cartes à la fois dans les fondations
        print("une seule carte à la fois dans fondations")
        return False

    return True
