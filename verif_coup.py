from jeu_depart import paquet

def verif_coup(move):
    move_possible = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "fca", "fpi", "fco", "ftr"]


    if "-" not in move:
        print("Il faut un tiret(-) entre la carte et le deplacement")
        return False

    if move.count("-") != 1:
        print("Ce mouvement n'existe pas")
        return False

    # obtenir la carte ainsi que la destination dans deux variables différente
    carte, destination = move.split("-")

    if carte == "" or destination == "":
        print("Ce mouvement n'existe pas, exemple : 5ca-c4")
        return False

    if carte not in paquet:
        print("La carte n'existe pas")
        return False

    if destination not in move_possible:
        print("Mouvement impossible")
        return False

    return carte, destination
