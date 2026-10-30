from affichage import afficher


def piocher(piles, cachees, index, difficulte):       # À AJOUTER : il manque un paramètre (lequel ?)
    """Joue la commande « p ».

    - S'il reste des cartes dans la pioche : on retourne la carte du dessus
      sur la défausse.
    - Si la pioche est vide : on remet toute la défausse dans la pioche.
    """

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