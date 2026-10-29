import os
from affichage import *
from deplacement import deplacement
from jeu_depart import nouvelle_partie, piles, cachees, index
from verif_gagnee import *
from victoire import *
from menu import menu

# ---------------------------------------------------------------------
# Lancement
# ---------------------------------------------------------------------
os.system("")    # active les couleurs dans le terminal de Windows

choix = menu()

#reprendre et paramètres ne sont pas encore faits, on revient au menu
while choix == "2" or choix == "3":
    print("Pas encore disponible")
    input("Appuyez sur Entrée pour revenir au menu")
    choix = menu()

#nouvelle partie : on mélange et on distribue
#partie de démonstration (choix 5) : on garde la donne fixe de jeu_depart
if choix == "1":
    piles, cachees, index = nouvelle_partie()

if choix == "4":
    print("À bientôt !")
else:
    afficher(piles, cachees)#permet de lancer le premier affichage

    #nombre de coup jouer
    nb_coups=0

    #tant que toute les fondations ne sont pas rempli
    while verif_gagnee(piles) == False:


        #maintenant, on va appeller le premier mouvement
        if deplacement(piles, cachees, index):
            nb_coups+=1


    animation_victoire(nb_coups)
