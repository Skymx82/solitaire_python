
import os

from jeu_depart import piles, cachees

def piocher(piles,):
    if len(piles["p"]) > 0:
        cartepiocher = piles["p"].pop()
        piles["d"].append(cartepiocher)
    else :
        while piles["d"]:

#une liste vide vaut « faux » et une liste non vide vaut « vrai »
#donc le while dis que tant qu'il y a des cartes dans la défausse on les range dans la pioche

            retournerpioche=piles["p"].pop()
            piles["d"].append(i)



    print("pioche :", piles["p"])
    print("défausse :", piles["d"])


piocher(piles)