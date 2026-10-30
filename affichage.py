#les codes couleur du terminal
rouge = "\033[31m"
gris = "\033[90m"
gras = "\033[1m"
normal = "\033[0m"

#efface l'écran et remonte en haut, comme ça le plateau reste au même endroit
effacer = "\033[2J\033[H"

#chaque case fait 8 caractères de large
largeur = 8

dos = "[░░]"
vide = "[  ]"


#ce qu'on voit à l'écran pour une carte, ex : "7tr" -> "[7tr]"
def nom_carte(carte):
    if "ca" in carte:
        carte = carte.replace("ca", "♦")

    if "co" in carte:
        carte = carte.replace("co", "♥")

    if "pi" in carte:
        carte = carte.replace("pi","♠")

    if "tr" in carte:
        carte = carte.replace("tr","♣")
    return "[" + carte + "]"


#met un texte au milieu d'une case et le met en couleur
def case(texte, couleur):
    return couleur + texte.center(largeur) + normal


#case pour une vraie carte, en rouge si c'est du coeur ou du carreau
def case_carte(carte):
    #on colle la carte à gauche sinon [10co] est décalé par rapport aux autres
    texte = ("  " + nom_carte(carte)).ljust(largeur)

    if carte[-2:] == "co" or carte[-2:] == "ca":
        return rouge + texte + normal
    else:
        return normal + texte + normal


def afficher_titre():
    print(gras + "S O L I T A I R E".center(largeur * 7) + normal)
    print(gris + "─" * (largeur * 7) + normal)


#affiche la pioche, la défausse et les fondations
def afficher_haut(piles):
    fondation = ["fca", "fpi", "fco", "ftr"]

    #la ligne avec les noms
    titres = case("pioche", gris) + case("défausse", gris) + " " * largeur
    for f in fondation:
        titres = titres + case(f, gris)

    #la ligne avec les cartes
    if len(piles["p"]) > 0:
        cartes = case(dos, gris)
    else:
        cartes = case(vide, gris)

    if len(piles["d"]) > 0:
        cartes = cartes + case_carte(piles["d"][-1])
    else:
        cartes = cartes + case(vide, gris)

    #une case vide pour que les fondations soient au dessus de c4 à c7
    cartes = cartes + " " * largeur

    for f in fondation:
        if len(piles[f]) > 0:
            cartes = cartes + case_carte(piles[f][-1])
        else:
            cartes = cartes + case(vide, gris)

    #la ligne avec le nombre de cartes de chaque pile
    nombres = case(str(len(piles["p"])), gris) + case(str(len(piles["d"])), gris) + " " * largeur
    for f in fondation:
        nombres = nombres + case(str(len(piles[f])) + "/13", gris)

    print(titres)
    print(cartes)
    print(nombres)
    print()


#affiche les 7 colonnes
def afficher_colonnes(piles, cachees):
    colonnes = ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]

    titres = ""
    for c in colonnes:
        titres = titres + case(c, gris)
    print(titres)

    #on cherche la colonne la plus longue pour savoir combien de lignes il faut
    hauteur = 1
    for c in colonnes:
        if len(piles[c]) > hauteur:
            hauteur = len(piles[c])

    #on écrit ligne par ligne : à chaque ligne on prend une carte de chaque colonne
    for ligne in range(hauteur):
        texte = ""
        for c in colonnes:
            colonne = piles[c]

            if len(colonne) == 0 and ligne == 0:
                texte = texte + case(vide, gris)
            elif ligne >= len(colonne):
                #plus de carte dans cette colonne
                texte = texte + " " * largeur
            elif ligne < cachees[c]:
                texte = texte + case(dos, gris)
            else:
                texte = texte + case_carte(colonne[ligne])
        print(texte)
    print()


def afficher_aide():
    print(gris + "  p : piocher  h : coups possibles  annuler  ? : règles" + normal)
    print(gris + "  à taper :  ♠ = pi    ♥ = co    ♦ = ca    ♣ = tr" + normal)


#affiche les règles et toutes les commandes quand le joueur tape "?"
def afficher_regles():
    print(effacer, end="")
    print(gras + "R È G L E S   D U   J E U".center(largeur * 7) + normal)
    print(gris + "─" * (largeur * 7) + normal)
    print("  But : ranger les 52 cartes dans les 4 fondations,")
    print("        de l'as au roi, une famille par fondation.")
    print()
    print("  Jouer : carte-pile      ex : 5ca-c4   aca-fca")
    print("  - sur une colonne : couleur alternée, et une valeur")
    print("    juste en dessous (5♦ sur 6♣)")
    print("  - sur une colonne vide : seulement un roi")
    print("  - sur une fondation : même famille, de l'as au roi")
    print("  - une carte part avec toutes celles posées dessus")
    print()
    print("  valeurs : a = as   v = valet   d = dame   r = roi")
    print("  familles : ♠ = pi   ♥ = co   ♦ = ca   ♣ = tr")
    print()
    print("  p          : piocher (1 à 3 cartes selon le niveau)")
    print("  h          : voir les coups possibles")
    print("  annuler    : revenir avant le dernier coup")
    print("  sauvegarde : enregistrer la partie pour plus tard")
    print("  ?          : afficher ces règles")
    print()


#affiche tout le plateau
def afficher(piles, cachees):
    print(effacer, end="")
    afficher_titre()
    afficher_haut(piles)
    afficher_colonnes(piles, cachees)
    afficher_aide()
