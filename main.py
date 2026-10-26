# =====================================================================
#  UNE VRAIE PARTIE, JUSTE APRÈS LA DISTRIBUTION
# =====================================================================
#
#  Ce que vous voyez à l'écran au début :
#
#     c1 : 7tr
#     c2 : ## 8tr
#     c3 : ## ## 3ca
#     c4 : ## ## ## 6tr
#     c5 : ## ## ## ## 3tr
#     c6 : ## ## ## ## ## 5ca
#     c7 : ## ## ## ## ## ## 9pi
#
#     (## = carte face cachée)
#
#  Règle à retenir : dans chaque liste, la DERNIÈRE carte est celle du DESSUS.


# ---------------------------------------------------------------------
# 1. Le paquet : les 52 cartes
# ---------------------------------------------------------------------

paquet = [
    "api", "2pi", "3pi", "4pi", "5pi", "6pi", "7pi", "8pi", "9pi", "10pi", "vpi", "dpi", "rpi",
    "aco", "2co", "3co", "4co", "5co", "6co", "7co", "8co", "9co", "10co", "vco", "dco", "rco",
    "aca", "2ca", "3ca", "4ca", "5ca", "6ca", "7ca", "8ca", "9ca", "10ca", "vca", "dca", "rca",
    "atr", "2tr", "3tr", "4tr", "5tr", "6tr", "7tr", "8tr", "9tr", "10tr", "vtr", "dtr", "rtr",
]


# ---------------------------------------------------------------------
# 2. Les piles : où sont les cartes, et dans quel ordre
# ---------------------------------------------------------------------

piles = {
    # Pioche : 24 cartes. La prochaine carte piochée est la dernière : "7co".
    "p": ["atr", "2tr", "7pi", "vca", "rco", "vco", "4co", "9tr",
          "8co", "5pi", "7ca", "rtr", "10co", "4pi", "2co", "10ca",
          "10tr", "5co", "2ca", "vtr", "9ca", "aca", "5tr", "7co"],

    # Défausse : vide au début.
    "d": [],

    # Colonnes : la première carte est tout en bas, la dernière est visible.
    "c1": ["7tr"],
    "c2": ["dco", "8tr"],
    "c3": ["dca", "4tr", "3ca"],
    "c4": ["dpi", "6pi", "4ca", "6tr"],
    "c5": ["aco", "10pi", "8pi", "6ca", "3tr"],
    "c6": ["vpi", "6co", "2pi", "rca", "3co", "5ca"],
    "c7": ["rpi", "api", "8ca", "9co", "3pi", "dtr", "9pi"],

    # Fondations : vides au début.
    "fca": [],
    "fpi": [],
    "fco": [],
    "ftr": [],
}


# ---------------------------------------------------------------------
# 3. Combien de cartes sont cachées en bas de chaque colonne
# ---------------------------------------------------------------------
# Exemple : c4 vaut 3, donc "dpi", "6pi" et "4ca" sont cachées,
# et seule "6tr" est visible.

cachees = {"c1": 0, "c2": 1, "c3": 2, "c4": 3, "c5": 4, "c6": 5, "c7": 6}


# ---------------------------------------------------------------------
# 4. L'index : pour chaque carte, le nom de sa pile
# ---------------------------------------------------------------------
# Il sert à retrouver une carte tout de suite quand le joueur tape "5ca-c4".

index = {
    "atr": "p", "2tr": "p", "7pi": "p", "vca": "p", "rco": "p", "vco": "p",
    "4co": "p", "9tr": "p", "8co": "p", "5pi": "p", "7ca": "p", "rtr": "p",
    "10co": "p", "4pi": "p", "2co": "p", "10ca": "p", "10tr": "p", "5co": "p",
    "2ca": "p", "vtr": "p", "9ca": "p", "aca": "p", "5tr": "p", "7co": "p",

    "7tr": "c1",
    "dco": "c2", "8tr": "c2",
    "dca": "c3", "4tr": "c3", "3ca": "c3",
    "dpi": "c4", "6pi": "c4", "4ca": "c4", "6tr": "c4",
    "aco": "c5", "10pi": "c5", "8pi": "c5", "6ca": "c5", "3tr": "c5",
    "vpi": "c6", "6co": "c6", "2pi": "c6", "rca": "c6", "3co": "c6", "5ca": "c6",
    "rpi": "c7", "api": "c7", "8ca": "c7", "9co": "c7", "3pi": "c7", "dtr": "c7", "9pi": "c7",
}


# =====================================================================
#  EXEMPLES : CE QUI CHANGE QUAND ON JOUE
# =====================================================================
#
#  Coup 1 : le joueur tape  5ca-c4   (5 rouge sur 6 noir : autorisé)
#
#     c6 avant : ["vpi", "6co", "2pi", "rca", "3co", "5ca"]
#     c6 après : ["vpi", "6co", "2pi", "rca", "3co"]
#
#     c4 avant : ["dpi", "6pi", "4ca", "6tr"]
#     c4 après : ["dpi", "6pi", "4ca", "6tr", "5ca"]
#
#     index["5ca"] : "c6"  devient  "c4"
#
#     Il reste 5 cartes dans c6 et elles sont toutes cachées :
#     on retourne celle du dessus ("3co").
#     cachees["c6"] : 5  devient  4
#
#
#  Coup 2 : le joueur pioche
#
#     p : la dernière carte ("7co") est enlevée
#     d avant : []
#     d après : ["7co"]
#
#     index["7co"] : "p"  devient  "d"