from verif_carte import verif_carte
from verif_colonne import verif_colonne
from verif_fondations import verifier_fondation


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