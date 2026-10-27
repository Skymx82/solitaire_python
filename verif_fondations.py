#le but est que chaque colonnes soit attribuer à 1 signes


# [-2:] veut dire « à partir de l’avant-avant-dernière lettre jusqu’à la fin »
# [:-2] veut dire « du début jusqu’à 2 lettres avant la fin »


ORDRE = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "v", "d", "r"]

def verifier_fondation(carte, piles):
    couleur = carte[-2:]
    nom = "f" + couleur
    nombre = len(piles[nom])

    if nombre == 13:
        print("Refusé :", nom, "est déjà complète.")
        return False

    attendue = ORDRE[nombre] + couleur

    if carte == attendue:
        return True

    print("Refusé :", carte, "ne peut pas aller sur", nom, "- il faut", attendue)
    return False
piles = {"fpi": ["api", "2pi"], "fco": [], "fca": [], "ftr": []}

print(verifier_fondation("aca", piles))