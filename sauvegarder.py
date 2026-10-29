import json
import os

#le nom du fichier où la partie est enregistrée
nom_sauvegarde = "sauvegarde.json"


#enregistre la partie en cours dans le fichier
def sauvegarder(piles, cachees, index, nbr_coup):
    #on range tout dans un seul dictionnaire, json ne peut écrire qu'une seule chose
    sauvegarde={"piles": piles, "cachees": cachees, "index":index, "nbr_coup": nbr_coup}

    #"w" : on ouvre en écriture, l'ancienne sauvegarde est remplacée
    fichier = open(nom_sauvegarde,"w")
    json.dump(sauvegarde, fichier)
    fichier.close()

    print("Partie sauvegardée, vous pourrez la reprendre depuis le menu")
    return True


#dit si une partie a déjà été sauvegardée
def sauvegarde_existe():
    return os.path.exists(nom_sauvegarde)


#relit le fichier et redonne la partie sauvegardée
def recharger_partie():
    #"r" : on ouvre en lecture, surtout pas "w" qui viderait le fichier
    fichier = open(nom_sauvegarde, "r")
    sauvegarde = json.load(fichier)
    fichier.close()

    # on ressort chaque morceau avec le nom qu'on lui avait donné
    piles = sauvegarde["piles"]
    cachees = sauvegarde["cachees"]
    index = sauvegarde["index"]
    nbr_coup = sauvegarde["nbr_coup"]

    return piles, cachees, index, nbr_coup
