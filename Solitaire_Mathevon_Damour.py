import os
import time
import random
import json


# ---------------------------------------------------------------------
# 1. Le paquet : les 52 cartes
# ---------------------------------------------------------------------

paquet = [
    "api", "2pi", "3pi", "4pi", "5pi", "6pi", "7pi", "8pi", "9pi", "10pi", "vpi", "dpi", "rpi",
    "aco", "2co", "3co", "4co", "5co", "6co", "7co", "8co", "9co", "10co", "vco", "dco", "rco",
    "aca", "2ca", "3ca", "4ca", "5ca", "6ca", "7ca", "8ca", "9ca", "10ca", "vca", "dca", "rca",
    "atr", "2tr", "3tr", "4tr", "5tr", "6tr", "7tr", "8tr", "9tr", "10tr", "vtr", "dtr", "rtr",
]


# ---------------------------------------------------------------------
# 2. Les piles : où sont les cartes, et dans quel ordre
# ---------------------------------------------------------------------

piles = {
    # Pioche : 24 cartes. La prochaine carte piochée est la dernière : "7co".
    "p": ["atr", "2tr", "7pi", "vca", "rco", "vco", "4co", "9tr",
          "8co", "5pi", "7ca", "rtr", "10co", "4pi", "2co", "10ca",
          "10tr", "5co", "2ca", "vtr", "9ca", "aca", "5tr", "7co"],

    # Défausse : vide au début.
    "d": [],

    # Colonnes : la première carte est tout en bas, la dernière est visible.
    "c1": ["7tr"],
    "c2": ["dco", "8tr"],
    "c3": ["dca", "4tr", "3ca"],
    "c4": ["dpi", "6pi", "4ca", "6tr"],
    "c5": ["aco", "10pi", "8pi", "6ca", "3tr"],
    "c6": ["vpi", "6co", "2pi", "rca", "3co", "5ca"],
    "c7": ["rpi", "api", "8ca", "9co", "3pi", "dtr", "9pi"],

    # Fondations : vides au début.
    "fca": [],
    "fpi": [],
    "fco": [],
    "ftr": [],
}


# ---------------------------------------------------------------------
# 3. Combien de cartes sont cachées en bas de chaque colonne
# ---------------------------------------------------------------------
# Exemple : c4 vaut 3, donc "dpi", "6pi" et "4ca" sont cachées,
# et seule "6tr" est visible.

cachees = {"c1": 0, "c2": 1, "c3": 2, "c4": 3, "c5": 4, "c6": 5, "c7": 6}


# ---------------------------------------------------------------------
# 4. L'index : pour chaque carte, le nom de sa pile
# ---------------------------------------------------------------------
# Il sert à retrouver une carte tout de suite quand le joueur tape "5ca-c4".

index = {
    "atr": "p", "2tr": "p", "7pi": "p", "vca": "p", "rco": "p", "vco": "p",
    "4co": "p", "9tr": "p", "8co": "p", "5pi": "p", "7ca": "p", "rtr": "p",
    "10co": "p", "4pi": "p", "2co": "p", "10ca": "p", "10tr": "p", "5co": "p",
    "2ca": "p", "vtr": "p", "9ca": "p", "aca": "p", "5tr": "p", "7co": "p",

    "7tr": "c1",
    "dco": "c2", "8tr": "c2",
    "dca": "c3", "4tr": "c3", "3ca": "c3",
    "dpi": "c4", "6pi": "c4", "4ca": "c4", "6tr": "c4",
    "aco": "c5", "10pi": "c5", "8pi": "c5", "6ca": "c5", "3tr": "c5",
    "vpi": "c6", "6co": "c6", "2pi": "c6", "rca": "c6", "3co": "c6", "5ca": "c6",
    "rpi": "c7", "api": "c7", "8ca": "c7", "9co": "c7", "3pi": "c7", "dtr": "c7", "9pi": "c7",
}


def nouvelle_partie():
    piles_jeu = {"p":[],"d":[],"c1":[],"c2":[],"c3":[],"c4":[],"c5":[],
                 "c6":[],"c7":[],"fca":[],"fpi":[],"fco":[],"ftr":[],}
    cachees_jeu = {}
    paquet_jeu = list(paquet)
    random.shuffle(paquet_jeu)
    nbr_colonne = 1
    while nbr_colonne <= 7:
        distrib_par_colonne = 1
        while distrib_par_colonne <= nbr_colonne:
            distrib = paquet_jeu.pop()
            piles_jeu["c"+str(nbr_colonne)].append(distrib)
            distrib_par_colonne = distrib_par_colonne + 1
        #toutes les cartes de la colonne sont cachées sauf la dernière
        cachees_jeu["c"+str(nbr_colonne)] = nbr_colonne - 1
        nbr_colonne = nbr_colonne + 1

    #les cartes qui restent dans le paquet vont dans la pioche
    while len(paquet_jeu) > 0:
        distrib = paquet_jeu.pop()
        piles_jeu["p"].append(distrib)

    #pour chaque carte on note dans quelle pile elle est
    index_jeu = {}
    for nom in piles_jeu:
        for carte in piles_jeu[nom]:
            index_jeu[carte] = nom

    return piles_jeu, cachees_jeu, index_jeu


# ---------------------------------------------------------------------
# 5. L'affichage du plateau
# ---------------------------------------------------------------------
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


#la défausse prend 2 cases : on y montre les dernières cartes piochées, 1, 2 ou 3 selon le niveau
#comme dans le vrai solitaire, seule la dernière peut être jouée : les autres sont en gris
def afficher_defausse(defausse, difficulte):
    visibles = defausse[-difficulte:]

    texte = ""
    longueur = 0
    for carte in visibles:
        if carte == visibles[-1]:
            #la dernière, la seule jouable, en rouge si c'est du coeur ou du carreau
            if carte[-2:] == "co" or carte[-2:] == "ca":
                texte = texte + rouge + nom_carte(carte) + normal
            else:
                texte = texte + nom_carte(carte)
        else:
            texte = texte + gris + nom_carte(carte) + normal
        #on compte la longueur sans les codes couleur, ils ne prennent pas de place à l'écran
        longueur = longueur + len(nom_carte(carte))

    #2 espaces devant comme les autres cartes, sauf si c'est trop large (trois 10 de suite)
    if longueur > 2 * largeur - 2:
        return " " + texte + " " * (2 * largeur - 1 - longueur)
    return "  " + texte + " " * (2 * largeur - 2 - longueur)


#affiche la pioche, la défausse et les fondations
def afficher_haut(piles, difficulte):
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
        cartes = cartes + afficher_defausse(piles["d"], difficulte)
    else:
        #la défausse vide, puis une case vide pour que les fondations soient au dessus de c4 à c7
        cartes = cartes + case(vide, gris) + " " * largeur

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
    print(gris + "  p : piocher  h : coups  ia : auto  annuler  ? : règles" + normal)
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
    print("  ia         : l'ordinateur joue tout seul")
    print("  annuler    : revenir avant le dernier coup")
    print("  sauvegarde : enregistrer la partie pour plus tard")
    print("  ?          : afficher ces règles")
    print()


#affiche tout le plateau
def afficher(piles, cachees, difficulte):
    print(effacer, end="")
    afficher_titre()
    afficher_haut(piles, difficulte)
    afficher_colonnes(piles, cachees)
    afficher_aide()


# ---------------------------------------------------------------------
# 6. Le menu
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
# 7. La sauvegarde
# ---------------------------------------------------------------------
#le nom du fichier où la partie est enregistrée
nom_sauvegarde = "sauvegarde.json"


#enregistre la partie en cours dans le fichier
def sauvegarder(piles, cachees, index, nbr_coup, difficulte):
    #on range tout dans un seul dictionnaire, json ne peut écrire qu'une seule chose
    sauvegarde={"piles": piles, "cachees": cachees, "index":index, "nbr_coup": nbr_coup, "difficulte":difficulte}

    #"w" : on ouvre en écriture, l'ancienne sauvegarde est remplacée
    fichier = open(nom_sauvegarde,"w")
    json.dump(sauvegarde, fichier)
    fichier.close()

    print("Partie sauvegardée, vous pourrez la reprendre depuis le menu")
    return True


#dit si une partie a déjà été sauvegardée
def sauvegarde_existe():
    return os.path.exists(nom_sauvegarde)


#relit le fichier et redonne la partie sauvegardée
def recharger_partie():
    #"r" : on ouvre en lecture, surtout pas "w" qui viderait le fichier
    fichier = open(nom_sauvegarde, "r")
    sauvegarde = json.load(fichier)
    fichier.close()

    # on ressort chaque morceau avec le nom qu'on lui avait donné
    piles = sauvegarde["piles"]
    cachees = sauvegarde["cachees"]
    index = sauvegarde["index"]
    nbr_coup = sauvegarde["nbr_coup"]
    difficulte = sauvegarde["difficulte"]

    return piles, cachees, index, nbr_coup, difficulte


# ---------------------------------------------------------------------
# 8. Les vérifications d'un coup
# ---------------------------------------------------------------------
def verif_coup(move):
    move_possible = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "fca", "fpi", "fco", "ftr"]


    if "-" not in move:
        print("Il faut un tiret(-) entre la carte et le deplacement")
        return False

    if move.count("-") != 1:
        print("Ce mouvement n'existe pas")
        return False

    # obtenir la carte ainsi que la destination dans deux variables différente
    carte, destination = move.split("-")

    if carte == "" or destination == "":
        print("Ce mouvement n'existe pas, exemple : 5ca-c4")
        return False

    if carte not in paquet:
        print("La carte n'existe pas")
        return False

    if destination not in move_possible:
        print("Mouvement impossible")
        return False

    return carte, destination


#le but de vérif carte est d'empecher de bouger une carte caché ou dans la pioche ainsi
#que déplacer qu'une seule carte à la fois dans les fondations

#parler = False : on vérifie sans afficher de message (sert pour la liste des coups possibles)
def verif_carte(carte, destination, cachees, morceau,index,piles,parler=True):

    if index[carte] == "p":
        if parler:
            print("la carte se trouve dans la pioche")
        return False

    depart = index[carte]
    position = piles[depart].index(carte)

    if depart in cachees:
        if position < cachees[depart]:  # même test que l'affichage
            if parler:
                print("Cette carte est face cachée, elle ne peut pas bouger")
            return False

    #dans la défausse seule la carte du dessus peut bouger
    if depart == "d" and piles["d"][-1] != carte :
        if parler:
            print("la carte se trouve en dessous dans la défausse")
        return False

    #dans une fondation aussi, seule la carte du dessus peut bouger
    if depart[0] == "f" and piles[depart][-1] != carte :
        if parler:
            print("la carte se trouve en dessous dans la fondation")
        return False


    if destination[0] == "f" and len(morceau) > 1 : # seulement 1 cartes à la fois dans les fondations
        if parler:
            print("une seule carte à la fois dans fondations")
        return False

    return True


# cette verification va permettre de vérifier si notre déplacement d'une colonne
# a une autre est correct en termes de rouge/noir ainsi que décroissant
#parler = False : on vérifie sans afficher de message (sert pour la liste des coups possibles)
def verif_colonne(carte,destination, piles, parler=True):

    #on répertorie dans l'ordre croissant les valeurs d'une carte ainsi que sa couleur
    rouge = ["ca","co"]
    valeur = ["a","2","3","4","5","6","7","8","9","10","v","d","r"]

    # si la colonne est vide, seul un roi peut y aller
    if len(piles[destination]) == 0:
        if carte[:-2] == "r":
            return True
        else:
            if parler:
                print("Seul un roi peut aller sur une colonne vide")
            return False

    # sinon on récupère la dernière carte de la pile de destination
    dernière_carte_destination = piles[destination][-1]

    #on vérifie si notre carte est rouge ou noir
    if dernière_carte_destination[-2:] in rouge:
        carte_destination_rouge = True
    else:
        carte_destination_rouge = False

    #pareil pour la carte qu'on déplace
    if carte[-2:] in rouge:
        carte_rouge = True
    else:
        carte_rouge = False

    #ici on vérifie si la couleur est différente
    if carte_rouge==True and carte_destination_rouge==True:
        if parler:
            print("carte de la même couleur")
        return False
    elif carte_rouge==False and carte_destination_rouge==False:
        if parler:
            print("carte de la même couleur")
        return False

    #ici on recupère que la valeur de la carte avec le carte[:-2] et ensuite
    #on regarde sont classement dedans la liste
    position_carte = valeur.index(carte[:-2])  # "7tr" → "7" → 6
    position_destination = valeur.index(dernière_carte_destination[:-2])  # "8co" → "8" → 7

    #ici on vérifie que la carte est inférieur a la dernière colonne
    if position_carte != position_destination - 1:
        if parler:
            print("Seul une carte inférieur a la carte de destination est autorisé")
        return False

    return True


#le but est que chaque colonnes soit attribuer à 1 signes


# [-2:] veut dire « à partir de l’avant-avant-dernière lettre jusqu’à la fin »
# [:-2] veut dire « du début jusqu’à 2 lettres avant la fin »


ordre = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "v", "d", "r"]

#parler = False : on vérifie sans afficher de message (sert pour la liste des coups possibles)
def verifier_fondation(carte, piles,destination, parler=True):
    valeur_cartes_origines=carte[:-2]
    couleur_carte_origines=carte[-2:]
    couleur_fondations=destination[-2:]

    if couleur_carte_origines != couleur_fondations :
        if parler:
            print("Il faut mettre la bonne couleur dans la bonne fondation")
        return False

    if len(piles[destination]) == 0:      ## obligé car sinon aucun as ne peut être accepté
        if valeur_cartes_origines != "a":
            if parler:
                print("Seul un as peut aller sur la fondation vide")
            return False
        if valeur_cartes_origines == "a" :
            return True

    ordredelacarte = ordre.index(valeur_cartes_origines)
    derniere = piles[destination][-1]
    valeur_derniere = derniere[:-2]
    ordredelacarte_destination = ordre.index(valeur_derniere)


    if ordredelacarte != ordredelacarte_destination +1 :
        if parler:
            print("Seul une carte avec une valeur supérieur de 1 est accepté")
        return False
    return True


# ---------------------------------------------------------------------
# 9. La fin de partie
# ---------------------------------------------------------------------
def verif_gagnee(piles):
    fondation = ["fca", "fco", "fpi", "ftr"]

    nbr_fondation_fini = 0

    for f in fondation:
        if len(piles[f]) == 13:
            nbr_fondation_fini += 1

    if nbr_fondation_fini == 4:
        return True
    else:
        return False


#comme dans le vrai solitaire : plus aucune carte cachée, et la pioche et la défausse sont vides
#la partie est alors forcément gagnée, il ne reste qu'à ranger les cartes dans les fondations
def tout_est_retourne(piles, cachees):
    colonnes = ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]

    if len(piles["p"]) > 0 or len(piles["d"]) > 0:
        return False

    for c in colonnes:
        if cachees[c] > 0:
            return False

    return True


# ---------------------------------------------------------------------
# 10. La pioche
# ---------------------------------------------------------------------
#joue la commande p : on retourne 1 à 3 cartes sur la défausse selon le niveau
#si la pioche est vide, on remet toute la défausse dans la pioche
def piocher(piles, cachees, index, difficulte):
    # Deux noms plus parlants. Ce ne sont PAS des copies : « pioche » et
    # piles["p"] sont la même liste, donc modifier l'une modifie l'autre.
    pioche = piles["p"]
    defausse = piles["d"]

    # ----- Cas 1 : il reste au moins une carte dans la pioche -----
    if len(pioche) > 0:
        i=1
        while i <= difficulte:
            if len(pioche) == 0:
                break
            carte = pioche.pop()          # on enlève la carte du dessus de la pioche...
            defausse.append(carte)        # ... et on la pose sur la défausse
            index[carte] = "d"
            i=i+1

    # ----- Cas 2 : la pioche est vide, on remet la défausse dans la pioche -----
    else:
        while len(defausse) > 0:      # tant qu'il reste des cartes dans la défausse
            carte = defausse.pop()    # on prend la carte du dessus de la défausse...
            pioche.append(carte)
            index[carte] = "p"

    afficher(piles, cachees, difficulte)


# ---------------------------------------------------------------------
# 11. Les coups possibles (h) et l'ordinateur (ia)
# ---------------------------------------------------------------------
#dit si une carte peut monter tout de suite sur la fondation de sa famille
def peut_monter(carte, piles):
    return verifier_fondation(carte, piles, "f" + carte[-2:], parler=False)


#renvoie les coups possibles, rangés du plus utile au moins utile
#seulement_utiles=True : on garde seulement ceux qui font avancer la partie (sert quand l'ordinateur joue tout seul)
def trouver_coups(piles, cachees, index, seulement_utiles=False):
    colonnes = ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]
    destinations = colonnes + ["fca", "fpi", "fco", "ftr"]

    #une liste par type de coup, de la plus utile à la moins utile
    vers_fondation = []
    retourne_carte = []
    depuis_defausse = []
    libere_carte = []
    vide_colonne = []
    entre_colonnes = []
    depuis_fondation = []

    #vider une colonne ne sert que si un roi attend d'y aller et qu'aucune colonne n'est déjà vide
    #un roi attend quand il est posé sur des cartes cachées, ou sur le dessus de la défausse
    roi_attend = False
    colonne_vide = False
    for c in colonnes:
        if len(piles[c]) == 0:
            colonne_vide = True
        elif cachees[c] > 0 and piles[c][cachees[c]][:-2] == "r":
            roi_attend = True
    if len(piles["d"]) > 0 and piles["d"][-1][:-2] == "r":
        roi_attend = True

    # ----- 1. Les cartes déjà jouables (colonnes, défausse, fondations) -----
    for carte in index:
        depart = index[carte]

        if depart == "p":                       # pioche : traitée plus bas
            continue

        position = piles[depart].index(carte)
        morceau = piles[depart][position:]

        for destination in destinations:
            if destination == depart:
                continue

            # Un roi déjà tout en bas d'une colonne : le changer de colonne ne sert à rien
            #mais il doit pouvoir monter sur sa fondation, donc on ne saute que les colonnes
            if carte[:-2] == "r" and depart in colonnes and position == 0 and destination in colonnes:
                continue

            #parler=False : les vérifs testent sans afficher leurs messages de refus
            if not verif_carte(carte, destination, cachees, morceau, index, piles, parler=False):
                continue

            if destination[0] == "f":
                bon = verifier_fondation(carte, piles, destination, parler=False)
            else:
                bon = verif_colonne(carte, destination, piles, parler=False)

            if bon:
                coup = carte + "-" + destination

                #on range le coup dans la liste de son type
                if destination[0] == "f":
                    vers_fondation.append(coup)
                #la première carte visible part et il reste des cartes cachées dessous : une carte va se retourner
                elif depart in colonnes and position == cachees[depart] and position > 0:
                    retourne_carte.append(coup)
                elif depart == "d":
                    depuis_defausse.append(coup)
                #la carte juste en dessous est visible et pourra monter sur sa fondation
                elif depart in colonnes and position > cachees[depart] and peut_monter(piles[depart][position - 1], piles):
                    libere_carte.append(coup)
                #toute la colonne part : elle sera libre pour le roi qui attend
                elif depart in colonnes and position == 0 and roi_attend and colonne_vide == False:
                    vide_colonne.append(coup)
                elif depart in colonnes:
                    entre_colonnes.append(coup)
                else:
                    depuis_fondation.append(coup)

    #le + colle les listes bout à bout, dans l'ordre de priorité
    coups = vers_fondation + retourne_carte + depuis_defausse + libere_carte + vide_colonne

    # ----- 2. Piocher -----
    #on ne dit pas quelle carte va sortir : le joueur ne doit pas voir les cartes cachées de la pioche
    #piocher passe avant les deux derniers types : ça amène une nouvelle carte, eux ne font que changer une carte de place
    if len(piles["p"]) > 0 or len(piles["d"]) > 0:
        coups.append("p")

    #les autres changements de colonne, ou redescendre une carte d'une fondation, ne font pas avancer la partie
    #l'ordinateur ne les joue pas tout seul, sinon il pourrait faire des allers-retours sans fin
    if seulement_utiles == False:
        coups = coups + entre_colonnes + depuis_fondation

    return coups


def afficher_coups(piles, cachees, index):
    coups = trouver_coups(piles, cachees, index)

    print()
    if len(coups) == 0:
        print("Aucun coup possible.")
    else:
        print("Coups possibles, du plus utile au moins utile :")
        for coup in coups:
            print("   ", coup)


# ---------------------------------------------------------------------
# 12. Jouer un coup
# ---------------------------------------------------------------------
def deplacement( piles, cachees, index, nb_coups , difficulte, coup_ordi=""):

    move_possible=["c1","c2","c3","c4","c5","c6","c7","fca","fpi","fco","ftr"]
    colonne = ["c1","c2","c3","c4","c5","c6","c7"]
    fondation = ["fca","fco","fpi","ftr"]


    #permet de demander la deplacement
    #quand l'ordinateur joue tout seul, c'est le lancement du jeu qui donne son coup dans coup_ordi
    if coup_ordi == "":
        move = input("Choisissez la carte à déplacer ainsi que sa direction : ")
    else:
        move = coup_ordi

    #affiche les coups possibles, puis on revient au plateau (ce n'est pas un coup)
    if move == "h":
        afficher_coups(piles, cachees, index)
        input("Appuyez sur Entrée pour continuer")
        afficher(piles, cachees, difficulte)
        return False

    if move == "sauvegarde":
        sauvegarder(piles, cachees, index, nb_coups, difficulte)
        return False

    #la pioche change le plateau sans compter comme un coup, le lancement du jeu doit le savoir
    if move == "p":
        piocher(piles, cachees, index, difficulte)
        return "pioche"

    #affiche les règles, puis on revient au plateau (ce n'est pas un coup)
    if move == "?":
        afficher_regles()
        input("Appuyez sur Entrée pour revenir au jeu")
        afficher(piles, cachees, difficulte)
        return False

    #c'est le lancement du jeu qui garde la copie de la partie, on le prévient juste
    if move == "annuler":
        return "annuler"

    #l'ordinateur va jouer tout seul : c'est le lancement du jeu qui lui fait jouer les coups un par un
    if move == "ia":
        return "ia"



    if verif_coup(move) == False:
        return False
    else :
        carte, destination = verif_coup(move)


    depart = index[carte]  # la pile où est la carte, ex : "c6"
    position = piles[depart].index(carte)  # sa place dans cette pile
    morceau = piles[depart][position:]  # la carte + toutes celles posées dessus

    if verif_carte(carte, destination, cachees,morceau,index,piles) == False:
        return False

    #ici on va mettre tout les verifs avant de deplacer les cartes
    if destination in colonne :
        if verif_colonne(carte, destination, piles) == False:
            return False

    if destination in fondation :
        if verifier_fondation(carte, piles, destination) == False:
            return False


    del piles[depart][position:]  # on enlève le morceau du départ
    piles[destination].extend(morceau)  # on le pose sur l'arrivée

    for c in morceau:  # chaque carte déplacée change de pile
        index[c] = destination

    # Si le départ est une colonne et qu'il ne reste que des cartes cachées,
    # on retourne celle du dessus.
    if depart in cachees:
        if len(piles[depart]) > 0 and len(piles[depart]) == cachees[depart]:
            cachees[depart] = cachees[depart] - 1

    afficher(piles, cachees, difficulte)
    return True


# ---------------------------------------------------------------------
# 13. L'animation de victoire : "VICTOIRE" en grand, qui change de couleur
# ---------------------------------------------------------------------

# rouge, jaune, vert, cyan, bleu, violet
COULEURS = ["\033[31m", "\033[33m", "\033[32m", "\033[36m", "\033[34m", "\033[35m"]
NORMAL = "\033[0m"

BANNIERE = [
    "█   █ ███  ████ █████  ███  ███ ████  █████ █",
    "█   █  █  █       █   █   █  █  █   █ █     █",
    "█   █  █  █       █   █   █  █  ████  ████  █",
    " █ █   █  █       █   █   █  █  █  █  █      ",
    "  █   ███  ████   █    ███  ███ █   █ █████ █",
]


def animation_victoire(nb_coups=None):
    os.system("")                  # active les couleurs dans le terminal de Windows
    print("\033[2J", end="")       # efface l'écran, une seule fois

    for image in range(15):        # 15 changements de couleur
        print("\033[H")            # retour en haut à gauche : on réécrit par-dessus
        for i in range(len(BANNIERE)):
            # chaque ligne a sa couleur, et les couleurs tournent à chaque image
            couleur = COULEURS[(i + image) % len(COULEURS)]
            print("    " + couleur + BANNIERE[i] + NORMAL)
        time.sleep(0.2)

    print()
    if nb_coups is not None:
        print("    Partie gagnée en " + str(nb_coups) + " coups !")
    print()



# ---------------------------------------------------------------------
# 14. Lancement du jeu
# ---------------------------------------------------------------------
os.system("")    # active les couleurs dans le terminal de Windows

#nombre de cartes tirées à chaque pioche : 1 facile, 2 moyen, 3 difficile
#facile par défaut (la partie de démonstration a besoin de 1)
difficulte = 1

choix = menu(difficulte)

#on revient au menu tant que le joueur ne lance pas une partie :
#il change la difficulté, ou il veut reprendre alors qu'il n'y a pas de sauvegarde
while choix == "3" or (choix == "2" and sauvegarde_existe() == False):
    if choix == "3":
        difficulte = choisir_difficulte()
    else:
        print("Aucune partie sauvegardée")
        input("Appuyez sur Entrée pour revenir au menu")
    choix = menu(difficulte)

#nouvelle partie : on mélange et on distribue
if choix == "1":
    piles, cachees, index = nouvelle_partie()
    nb_coups = 0

#reprendre : on recharge la partie et son nombre de coups depuis le fichier
if choix == "2":
    piles, cachees, index, nb_coups, difficulte = recharger_partie()

#partie de démonstration : on garde la donne fixe du début du fichier
if choix == "5":
    nb_coups = 0

if choix == "4":
    print("À bientôt !")
else:
    afficher(piles, cachees, difficulte)#permet de lancer le premier affichage

    #la partie telle qu'elle était avant le dernier coup, pour pouvoir l'annuler
    #None veut dire qu'il n'y a rien à annuler
    copie_piles = None

    #auto vaut True quand l'ordinateur joue tout seul (commande ia)
    auto = False
    #combien de fois l'ordinateur a retourné la défausse sans rien jouer d'autre
    nb_tours = 0

    #tant que toute les fondations ne sont pas rempli
    while verif_gagnee(piles) == False:

        #on copie la partie avant le coup
        #chaque liste est copiée une par une, sinon la copie partagerait les mêmes cartes
        avant_piles = {}
        for i in piles:
            avant_piles[i] = list(piles[i])
        avant_cachees = dict(cachees)
        avant_index = dict(index)
        avant_nb_coups = nb_coups

        #comme dans le vrai solitaire : quand tout est retourné, la partie est gagnée
        #l'ordinateur range alors tout seul les cartes qui restent dans les fondations
        if auto == False and tout_est_retourne(piles, cachees):
            auto = True
            print("Toutes les cartes sont retournées, la partie est gagnée : l'ordinateur range les cartes")
            time.sleep(1)

        #quand l'ordinateur joue tout seul, il prend le premier coup utile de la liste
        coup_ordi = ""
        if auto == True:
            coups = trouver_coups(piles, cachees, index, seulement_utiles=True)
            if len(coups) > 0:
                coup_ordi = coups[0]

            #la pioche est vide : ce p va retourner la défausse
            if coup_ordi == "p" and len(piles["p"]) == 0:
                nb_tours = nb_tours + 1

            #deuxième fois sans avoir rien joué : il a vu toutes les cartes de la pioche, il est bloqué
            if nb_tours == 2:
                coup_ordi = ""

            if coup_ordi == "":
                auto = False
                print("L'ordinateur ne trouve plus de coup utile, à vous de jouer")

        #maintenant, on va appeller le premier mouvement
        resultat = deplacement(piles, cachees, index, nb_coups, difficulte, coup_ordi)

        #on laisse le coup de l'ordinateur affiché un petit moment avant le suivant
        if coup_ordi != "":
            print("L'ordinateur a joué : " + coup_ordi)
            time.sleep(0.2)

        #l'ordinateur prend la main
        if resultat == "ia":
            auto = True
            nb_tours = 0

        #un vrai coup a été joué : on repart de zéro pour les tours de pioche
        if resultat == True:
            nb_tours = 0

        #un coup joué ou une pioche ont changé le plateau : on garde la copie d'avant
        if resultat == True or resultat == "pioche":
            copie_piles = avant_piles
            copie_cachees = avant_cachees
            copie_index = avant_index
            copie_nb_coups = avant_nb_coups

        #seul un vrai coup compte, pas une pioche
        if resultat == True:
            nb_coups+=1

        #annuler : on remet la partie comme avant le dernier coup
        if resultat == "annuler":
            if copie_piles is None:
                print("Il n'y a rien à annuler")
            else:
                piles = copie_piles
                cachees = copie_cachees
                index = copie_index
                nb_coups = copie_nb_coups
                #on ne peut annuler qu'une fois, le coup d'encore avant n'est pas gardé
                copie_piles = None
                afficher(piles, cachees, difficulte)

    animation_victoire(nb_coups)
