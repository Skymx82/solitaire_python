import os
from affichage import *
from deplacement import deplacement
from jeu_depart import nouvelle_partie
from verif_gagnee import *
from victoire import *

# ---------------------------------------------------------------------
# Lancement
# ---------------------------------------------------------------------
piles, cachees, index = nouvelle_partie()
os.system("")    # active les couleurs dans le terminal de Windows
afficher(piles, cachees)#permet de lancer le premier affichage

#nombre de coup jouer
nb_coups=0

#tant que toute les fondations ne sont pas rempli
while verif_gagnee(piles) == False:


    #maintenant, on va appeller le premier mouvement
    if deplacement(piles, cachees, index):
        nb_coups+=1


animation_victoire(nb_coups)
