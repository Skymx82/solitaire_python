#le but est que chaque colonnes soit attribuer à 1 signes


# [-2:] veut dire « à partir de l’avant-avant-dernière lettre jusqu’à la fin »
# [:-2] veut dire « du début jusqu’à 2 lettres avant la fin »

from jeu_depart import piles

ordre = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "v", "d", "r"]

def verifier_fondation(carte, piles,destination):
    valeur_cartes_origines=carte[:-2]
    couleur_carte_origines=carte[-2:]
    couleur_fondations=destination[-2:]

    if couleur_carte_origines != couleur_fondations :
        print("Il faut mettre la bonne couleur dans la bonne fondation")
        return False

    if len(piles[destination]) == 0:      ## obligé car sinon aucun as ne peut être accepté
        if valeur_cartes_origines != "a":
            print("Seul un as peut aller sur la fondation vide")
            return False
        if valeur_cartes_origines == "a" :
            return True

    ordredelacarte = ordre.index(valeur_cartes_origines)
    derniere = piles[destination][-1]
    valeur_derniere = derniere[:-2]
    ordredelacarte_destination = ordre.index(valeur_derniere)


    if ordredelacarte != ordredelacarte_destination +1 :
        print("Seul une carte avec une valeur supérieur de 1 est accepté")
        return False
    return True

