from verif_carte import verif_carte
from verif_colonne import verif_colonne
from verif_fondations import verifier_fondation


def trouver_coups(piles, cachees, index):
    coups = []
    colonnes = ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]
    destinations = colonnes + ["fca", "fpi", "fco", "ftr"]

    # ----- 1. Les cartes déjà jouables (colonnes, défausse, fondations) -----
    for carte in index:
        depart = index[carte]

        if depart == "p":                       # pioche : traitée plus bas
            continue

        position = piles[depart].index(carte)
        morceau = piles[depart][position:]

        # Un roi déjà tout en bas d'une colonne : le déplacer ne sert à rien
        if carte[:-2] == "r" and depart in colonnes and position == 0:
            continue

        for destination in destinations:
            if destination == depart:
                continue

            if not verif_carte(carte, destination, cachees, morceau, index, piles):
                continue

            if destination[0] == "f":
                bon = verifier_fondation(carte, piles, destination)
            else:
                bon = verif_colonne(carte, destination, piles)

            if bon:
                coups.append(carte + "-" + destination)

    # ----- 2. La carte du haut de la pioche (après avoir pioché) -----
    if len(piles["p"]) > 0:
        carte = piles["p"][-1]
        for destination in destinations:
            if destination[0] == "f":
                bon = verifier_fondation(carte, piles, destination)
            else:
                bon = verif_colonne(carte, destination, piles)

            if bon:
                coups.append("p puis " + carte + "-" + destination)

    return coups


def afficher_coups(piles, cachees, index):
    coups = trouver_coups(piles, cachees, index)

    print()
    if len(coups) == 0:
        print("Aucun coup possible : essayez de piocher (p).")
    else:
        print("Coups possibles :")
        for coup in coups:
            print("   ", coup)