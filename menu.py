from affichage import effacer, gras, gris, normal

#le nom de chaque niveau : difficulte 1 = facile, 2 = moyen, 3 = difficile
noms_difficulte = ["facile", "moyen", "difficile"]


#affiche le menu de départ et renvoie le choix du joueur
def menu(difficulte):
    choix_possibles = ["1", "2", "3", "4", "5"]

    print(effacer, end="")
    print(gras + "S O L I T A I R E".center(56) + normal)
    print(gris + "─" * 56 + normal)
    print()
    print("   1 : nouvelle partie")
    print("   2 : reprendre la partie sauvegardée")
    print("   3 : difficulté (actuellement : " + noms_difficulte[difficulte - 1] + ")")
    print("   4 : quitter")
    print("   5 : partie de démonstration (toujours la même donne)")
    print()

    choix = input("Votre choix : ")

    #on redemande tant que le choix n'existe pas
    while choix not in choix_possibles:
        print("Ce choix n'existe pas, tapez un nombre entre 1 et 5")
        choix = input("Votre choix : ")

    return choix


#demande le niveau et renvoie le nombre de cartes à tirer à chaque pioche
def choisir_difficulte():
    choix_possibles = ["1", "2", "3"]

    print()
    print("   1 : facile    (1 carte à chaque pioche)")
    print("   2 : moyen     (2 cartes à chaque pioche)")
    print("   3 : difficile (3 cartes à chaque pioche)")
    print()

    choix = input("Votre niveau : ")

    #on redemande tant que le niveau n'existe pas
    while choix not in choix_possibles:
        print("Ce niveau n'existe pas, tapez 1, 2 ou 3")
        choix = input("Votre niveau : ")

    #on renvoie un nombre et pas un texte : piocher() s'en sert pour compter les cartes
    return int(choix)
