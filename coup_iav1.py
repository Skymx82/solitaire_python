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

            #parler=False : les vérifs testent sans afficher leurs messages de refus
            if not verif_carte(carte, destination, cachees, morceau, index, piles, parler=False):
                continue

            if destination[0] == "f":
                bon = verifier_fondation(carte, piles, destination, parler=False)
            else:
                bon = verif_colonne(carte, destination, piles, parler=False)

            if bon:
                coups.append(carte + "-" + destination)

    # ----- 2. Piocher -----
    #on ne dit pas quelle carte va sortir : le joueur ne doit pas voir les cartes cachées de la pioche
    if len(piles["p"]) > 0 or len(piles["d"]) > 0:
        coups.append("p")

    return coups


def afficher_coups(piles, cachees, index):
    coups = trouver_coups(piles, cachees, index)

    print()
    if len(coups) == 0:
        print("Aucun coup possible.")
    else:
        print("Coups possibles :")
        for coup in coups:
            print("   ", coup)