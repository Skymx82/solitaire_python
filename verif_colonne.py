from operator import truediv


# cette verification va permettre de vérifier si notre déplacement d'une colonne
# a une autre est correct en termes de rouge/noir ainsi que décroissant
def verif_colonne(carte,destination, piles):

    #on répertorie dans l'ordre croissant les valeurs d'une carte ainsi que sa couleur
    rouge = ["ca","co"]
    valeur = ["a","2","3","4","5","6","7","8","9","10","j","d","r"]

    #on récupère la dernière carte de la pile de destination
    dernière_carte_destination = piles[destination][-1]

    #on vérifie si notre carte est rouge ou noir
    if dernière_carte_destination[-2] in rouge:
        carte_destination_rouge = True
    else:
        carte_destination_rouge = False

    #Je fais demain pour la carte d'origine
    if carte[-2] in rouge:
        carte_rouge = True
    else:
        carte_rouge = False

    #ici on vérifie si la couleur est différente
    if carte_rouge==True and carte_destination_rouge==True:
        return False
    elif carte_rouge==False and carte_destination_rouge==False:
        return False

