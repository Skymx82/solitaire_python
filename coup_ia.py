from verif_fondations import verifier_fondation

def coups_ia(piles):
    coups = []                                    # la liste des coups trouvés
    colonnes = ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]

    for c in colonnes:
        if len(piles[c]) == 0:                    # colonne vide : rien à tester
            continue

        carte = piles[c][-1]                      # la carte du bas de la colonne
        fondation = "f" + carte[-2:]              # sa fondation, ex : "fca"

        if verifier_fondation(carte, piles, fondation, parler=False):
            coups.append(carte + "-" + fondation)

    return coups