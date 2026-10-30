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

    #la partie telle qu'elle était avant le dernier coup, pour pouvoir l'annuler
    #None veut dire qu'il n'y a rien à annuler
    copie_piles = None

    #tant que toute les fondations ne sont pas rempli
    while verif_gagnee(piles) == False:

        #on copie la partie avant le coup
        #chaque liste est copiée une par une, sinon la copie partagerait les mêmes cartes
        avant_piles = {}
        for i in piles:
            avant_piles[i] = list(piles[i])
        avant_cachees = dict(cachees)
        avant_index = dict(index)
        avant_nb_coups = nb_coups

        #maintenant, on va appeller le premier mouvement
        resultat = deplacement(piles, cachees, index, nb_coups, difficulte)

        #un coup joué ou une pioche ont changé le plateau : on garde la copie d'avant
        if resultat == True or resultat == "pioche":
            copie_piles = avant_piles
            copie_cachees = avant_cachees
            copie_index = avant_index
            copie_nb_coups = avant_nb_coups

        #seul un vrai coup compte, pas une pioche
        if resultat == True:
            nb_coups+=1

        #annuler : on remet la partie comme avant le dernier coup
        if resultat == "annuler":
            if copie_piles is None:
                print("Il n'y a rien à annuler")
            else:
                piles = copie_piles
                cachees = copie_cachees
                index = copie_index
                nb_coups = copie_nb_coups
                #on ne peut annuler qu'une fois, le coup d'encore avant n'est pas gardé
                copie_piles = None
                afficher(piles, cachees)

    animation_victoire(nb_coups)
