# =====================================================================
#  AFFICHAGE DE LA PARTIE DANS LE TERMINAL
# =====================================================================
#
#  Pour lancer :   python affichage.py
#  (jeu_depart.py doit être dans le même dossier)

import os

from jeu_depart import piles, cachees


COLONNES = ("c1", "c2", "c3", "c4", "c5", "c6", "c7")
FONDATIONS = ("fca", "fpi", "fco", "ftr")

LARGEUR = 8           # largeur d'une case, en caractères
ROUGE = "\033[31m"    # code qui écrit en rouge dans le terminal
NORMAL = "\033[0m"    # code qui revient à la couleur normale


def case(texte):
    """Met un texte au centre d'une case.
    Les cartes de cœur et de carreau sont écrites en rouge."""
    centre = texte.center(LARGEUR)
    # On colore APRÈS avoir centré : sinon les codes couleur
    # compteraient comme des caractères et décaleraient tout.
    if texte[-2:] in ("co", "ca"):
        return ROUGE + centre + NORMAL
    return centre


def dessus(pile):
    """Carte du dessus d'une pile, ou "--" si la pile est vide."""
    if pile:
        return pile[-1]
    return "--"


def afficher(piles, cachees):
    """Affiche tout le plateau : pioche, défausse, fondations, colonnes."""

    # ----- Ligne du haut : pioche, défausse, puis les 4 fondations -----
    titres = "pioche".center(LARGEUR) + "défausse".center(LARGEUR) + " " * LARGEUR
    cartes = ""

    # Pioche : on ne montre pas la carte (elle est cachée), juste le nombre.
    if piles["p"]:
        cartes += case("[" + str(len(piles["p"])) + "]")
    else:
        cartes += case("--")

    # Défausse : on montre la carte du dessus.
    cartes += case(dessus(piles["d"]))

    # Une case vide pour que les fondations tombent au-dessus de c4 à c7.
    cartes += " " * LARGEUR

    for f in FONDATIONS:
        titres += f.center(LARGEUR)
        cartes += case(dessus(piles[f]))

    print()
    print(titres)
    print(cartes)
    print()

    # ----- Les 7 colonnes -----
    titres = ""
    for c in COLONNES:
        titres += c.center(LARGEUR)
    print(titres)

    # Nombre de lignes à afficher = la colonne la plus longue.
    # (au moins 1 ligne, pour voir les "--" même si toutes les colonnes sont vides)
    hauteur = 1
    for c in COLONNES:
        if len(piles[c]) > hauteur:
            hauteur = len(piles[c])

    # On écrit ligne par ligne : à chaque ligne, une carte de chaque colonne.
    for ligne in range(hauteur):
        texte = ""
        for c in COLONNES:
            colonne = piles[c]
            if not colonne and ligne == 0:
                texte += case("--")                 # colonne vide
            elif ligne >= len(colonne):
                texte += " " * LARGEUR              # plus de carte ici
            elif ligne < cachees[c]:
                texte += case("##")                 # carte face cachée
            else:
                texte += case(colonne[ligne])       # carte visible
        print(texte)
    print()


