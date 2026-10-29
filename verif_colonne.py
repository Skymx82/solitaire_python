from operator import truediv


# cette verification va permettre de vérifier si notre déplacement d'une colonne
# a une autre est correct en termes de rouge/noir ainsi que décroissant
def verif_colonne(carte,destination, piles):

    #on répertorie dans l'ordre croissant les valeurs d'une carte ainsi que sa couleur
    rouge = ["ca","co"]
    valeur = ["a","2","3","4","5","6","7","8","9","10","v","d","r"]

    # si la colonne est vide, seul un roi peut y aller
    if len(piles[destination]) == 0:
        if carte[:-2] == "r":
            return True
        else:
            print("Seul un roi peut aller sur une colonne vide")
            return False

    # sinon on récupère la dernière carte de la pile de destination
    dernière_carte_destination = piles[destination][-1]

    #on vérifie si notre carte est rouge ou noir
    if dernière_carte_destination[-2:] in rouge:
        carte_destination_rouge = True
    else:
        carte_destination_rouge = False

    #Je fais demain pour la carte d'origine
    if carte[-2:] in rouge:
        carte_rouge = True
    else:
        carte_rouge = False

    #ici on vérifie si la couleur est différente
    if carte_rouge==True and carte_destination_rouge==True:
        print("carte de la même couleur")
        return False
    elif carte_rouge==False and carte_destination_rouge==False:
        print("carte de la même couleur")
        return False

    #ici on recupère que la valeur de la carte avec le carte[:-2] et ensuite
    #on regarde sont classement dedans la liste
    position_carte = valeur.index(carte[:-2])  # "7tr" → "7" → 6
    position_destination = valeur.index(dernière_carte_destination[:-2])  # "8co" → "8" → 7

    #ici on vérifie que la carte est inférieur a la dernière colonne
    if position_carte != position_destination - 1:
        print("Seul une carte inférieur a la carte de destination est autorisé")
        return False

    return True