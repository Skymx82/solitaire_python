# =====================================================================
#  ANIMATION DE VICTOIRE : "VICTOIRE" en grand, qui change de couleur
# =====================================================================
#
#  Pour tester tout seul :   python victoire.py
#  Dans votre jeu :          from victoire import animation_victoire
#                            animation_victoire(nb_coups)

import os
import time

# rouge, jaune, vert, cyan, bleu, violet
COULEURS = ["\033[31m", "\033[33m", "\033[32m", "\033[36m", "\033[34m", "\033[35m"]
NORMAL = "\033[0m"

BANNIERE = [
    "█   █ ███  ████ █████  ███  ███ ████  █████ █",
    "█   █  █  █       █   █   █  █  █   █ █     █",
    "█   █  █  █       █   █   █  █  ████  ████  █",
    " █ █   █  █       █   █   █  █  █  █  █      ",
    "  █   ███  ████   █    ███  ███ █   █ █████ █",
]


def animation_victoire(nb_coups=None):
    os.system("")                  # active les couleurs dans le terminal de Windows
    print("\033[2J", end="")       # efface l'écran, une seule fois

    for image in range(15):        # 15 changements de couleur
        print("\033[H")            # retour en haut à gauche : on réécrit par-dessus
        for i in range(len(BANNIERE)):
            # chaque ligne a sa couleur, et les couleurs tournent à chaque image
            couleur = COULEURS[(i + image) % len(COULEURS)]
            print("    " + couleur + BANNIERE[i] + NORMAL)
        time.sleep(0.2)

    print()
    if nb_coups is not None:
        print("    Partie gagnée en " + str(nb_coups) + " coups !")
    print()


if __name__ == "__main__":
    animation_victoire(115)