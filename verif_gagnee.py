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
