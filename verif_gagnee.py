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