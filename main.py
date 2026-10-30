import os
from affichage import *
from deplacement import deplacement
from jeu_depart import nouvelle_partie, piles, cachees, index
from sauvegarder import recharger_partie, sauvegarde_existe
from verif_gagnee import *
from victoire import *
from menu import menu, choisir_difficulte

# ---------------------------------------------------------------------
# Lancement
# ---------------------------------------------------------------------
os.system("")    # active les couleurs dans le terminal de Windows

#nombre de cartes tirées à chaque pioche : 1 facile, 2 moyen, 3 difficile
#facile par défaut (la partie de démonstration a besoin de 1)
difficulte = 1

choix = menu(difficulte)

#on revient au menu tant que le joueur ne lance pas une partie :
#il change la difficulté, ou il veut reprendre alors qu'il n'y a pas de sauvegarde
while choix == "3" or (choix == "2" and sauvegarde_existe() == False):
    if choix == "3":
        difficulte = choisir_difficulte()
    else:
        print("Aucune partie sauvegardée")
        input("Appuyez sur Entrée pour revenir au menu")
    choix = menu(difficulte)

#nouvelle partie : on mélange et on distribue
if choix == "1":
    piles, cachees, index = nouvelle_partie()
    nb_coups = 0

#reprendre : on recharge la partie et son nombre de coups depuis le fichier
if choix == "2":
    piles, cachees, index, nb_coups, difficulte = recharger_partie()

#partie de démonstration : on garde la donne fixe de jeu_depart
if choix == "5":
    nb_coups = 0

if choix == "4":
    print("À bientôt !")
else:
    afficher(piles, cachees)#permet de lancer le premier affichage

    #tant que toute les fondations ne sont pas rempli
    while verif_gagnee(piles) == False:

        #maintenant, on va appeller le premier mouvement
        if deplacement(piles, cachees, index, nb_coups, difficulte):
            nb_coups+=1

    animation_victoire(nb_coups)
