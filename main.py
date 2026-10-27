import os
from affichage import *
from deplacement import deplacement
from jeu_depart import *

# ---------------------------------------------------------------------
# Lancement
# ---------------------------------------------------------------------
os.system("")    # active les couleurs dans le terminal de Windows
afficher(piles, cachees)#permet de lancer le premier affichage

#continue tant que toutes les cartes ne sont pas retournée
while sum(cachees.values()) != 0:

    #maintenant, on va appeller le premier mouvement
    deplacement(piles, cachees, index)

if sum(cachees.values()) == 0:
    