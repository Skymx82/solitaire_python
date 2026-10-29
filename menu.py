from affichage import effacer, gras, gris, normal


#affiche le menu de départ et renvoie le choix du joueur
def menu():
    choix_possibles = ["1", "2", "3", "4", "5"]

    print(effacer, end="")
    print(gras + "S O L I T A I R E".center(56) + normal)
    print(gris + "─" * 56 + normal)
    print()
    print("   1 : nouvelle partie")
    print("   2 : reprendre la partie sauvegardée")
    print("   3 : paramètres")
    print("   4 : quitter")
    print("   5 : partie de démonstration (toujours la même donne)")
    print()

    choix = input("Votre choix : ")

    #on redemande tant que le choix n'existe pas
    while choix not in choix_possibles:
        print("Ce choix n'existe pas, tapez un nombre entre 1 et 5")
        choix = input("Votre choix : ")

    return choix
