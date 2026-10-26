"""
donnees_test_solitaire.py
=========================

Données de test pour le projet « Le Solitaire » (L3 MIAGE).

Ce fichier ne contient AUCUNE règle du jeu : seulement des données, rangées au
format choisi par le binôme (piles + compteur de cartes cachées + index).
Il sert à travailler chacun de son côté sans attendre l'autre :

  * l'interface peut coder l'affichage directement sur ces états ;
  * le moteur peut vérifier ses règles en rejouant SOLUTION, une donne réelle
    qu'on SAIT gagnable.

Ce fichier n'est pas à rendre : c'est un outil de développement.


CONVENTIONS
-----------
* Une carte = valeur + famille, toujours en minuscules :
      valeurs  : a 2 3 4 5 6 7 8 9 10 v d r
      familles : pi (pique)  co (cœur)  ca (carreau)  tr (trèfle)
  -> la famille, ce sont toujours les 2 derniers caractères ; la valeur, le reste.

* 13 piles : "p" (pioche), "d" (défausse), "c1" à "c7" (colonnes),
  "fca" "fpi" "fco" "ftr" (fondations, une par famille).

* Dans TOUTES les piles : indice 0 = le bas, DERNIER élément = le dessus.
      - pioche     : la prochaine carte tirée est la dernière ;
      - défausse   : la seule carte jouable est la dernière ;
      - colonne    : la carte du dessus est la dernière ;
      - fondation  : l'as est en indice 0, la dernière carte est la plus haute.

* "cachees"["c4"] = 3 veut dire : les 3 PREMIÈRES cartes de c4 (indices 0, 1, 2)
  sont face cachée, toutes les autres sont visibles.
  La pioche est toujours entièrement cachée, la défausse et les fondations
  toujours entièrement visibles : rien à stocker pour elles.

* "index" ne contient que le nom de la pile, jamais la place : la place, c'est
  la position dans la liste.


LA DONNE
--------
Vrai paquet de 52 cartes mélangé, puis distribution comme à la main : rang par
rang, de gauche à droite, la première carte de chaque rang face visible.
Elle est gagnable en 115 coups avec ces règles :
  - tirage d'une carte à la fois ;
  - UN SEUL passage dans la pioche (la solution ne remet jamais la défausse
    dans la pioche, donc elle reste valable si vous limitez les passages) ;
  - seul un roi peut aller sur une colonne vide ;
  - déplacer une carte d'une colonne déplace aussi toutes celles posées dessus.

Position de départ (## = carte face cachée) :

    Pioche : 24 cartes      Défausse : vide
    Fondations : fca = -   fpi = -   fco = -   ftr = -
    c1 : 7tr
    c2 : ## 8tr
    c3 : ## ## 3ca
    c4 : ## ## ## 6tr
    c5 : ## ## ## ## 3tr
    c6 : ## ## ## ## ## 5ca
    c7 : ## ## ## ## ## ## 9pi


LES ÉTATS FOURNIS
-----------------
  etat_debut()         juste après la distribution
  etat_milieu()        après les 39 premiers coups de SOLUTION
                       (une colonne vide, une fondation commencée, pioche entamée)
  etat_pioche_vide()   après les 75 premiers coups de SOLUTION
                       (pioche vide : idéal pour tester le recyclage de la défausse
                       et l'affichage d'une pioche vide)
  etat_fin()           après les 115 coups : les 4 fondations sont complètes

Chaque fonction renvoie une COPIE TOUTE NEUVE (copy.deepcopy). Vous pouvez donc
modifier l'état reçu sans abîmer les données des tests suivants. Ne travaillez
jamais directement sur les constantes _ETAT_... : une liste modifiée par un test
resterait modifiée pour tous les autres.


LA SOLUTION
-----------
SOLUTION est un tuple de 115 coups. Chaque coup est un tuple (carte, destination),
exactement au format de vos commandes « carte-destination » :

    ("9co", "c3")    le 9 de cœur (et tout ce qui est posé dessus) va sur c3
    ("api", "fpi")   l'as de pique va sur sa fondation
    ("7tr", "d")     PIOCHER : la carte du dessus de la pioche doit être le 7tr,
                     elle passe sur la défausse

Le commentaire de chaque coup dit d'où vient la carte et quelle carte doit être
retournée juste après. Si votre programme retourne une autre carte, ou refuse
un coup de la liste, c'est qu'il y a un bug (ou une convention différente).


IDÉES DE TESTS
--------------
1. Afficher etat_debut() : vérifier à l'œil que l'écran correspond au schéma
   ci-dessus.

2. Partir de etat_debut(), jouer les 39 premiers coups de SOLUTION avec
   VOTRE moteur, puis comparer vos "piles", "cachees" et "index" avec ceux de
   etat_milieu() (une simple comparaison avec == suffit). Même chose avec les
   75 premiers coups et etat_pioche_vide().

3. Jouer les 115 coups : votre détection de victoire doit se déclencher au
   dernier coup, et pas avant.

4. Coups INTERDITS, qui doivent tous être refusés avec un message clair :
     dans etat_debut() :
       7tr -> c2    même couleur (7 noir sur 8 noir)
       3ca -> c7    mauvaise valeur (3 sur un 9)
       dco -> c3    la dame de cœur est face cachée
       3ca -> fca   une fondation vide n'accepte qu'un as
     dans etat_milieu() :
       dpi -> c1    une dame sur une colonne vide (si "roi_seul" vaut True)

5. Recyclage : dans etat_pioche_vide(), la pioche est vide et la défausse vaut
   ["9ca", "10tr", "10co", "rtr", "9tr", "rco", "7pi"]. Après le recyclage, la
   pioche doit valoir ["7pi", "rco", "9tr", "rtr", "10co", "10tr", "9ca"] et la
   défausse être vide : la prochaine carte tirée redevient le 9ca, la première
   carte qui avait été tirée. "passages" doit passer à 1.

6. Sauvegarder etat_milieu(), recharger, comparer : on doit retrouver
   exactement le même état.
"""

import copy


# =============================================================================
# CONSTANTES (tuples : elles ne changent jamais pendant la partie)
# =============================================================================

# La position dans le tuple donne l'ordre des valeurs : "a" est la plus petite.
VALEURS = ("a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "v", "d", "r")

FAMILLES = ("pi", "co", "ca", "tr")
ROUGES = ("co", "ca")

COLONNES = ("c1", "c2", "c3", "c4", "c5", "c6", "c7")
FONDATIONS = ("fca", "fpi", "fco", "ftr")
NOMS_PILES = ("p", "d") + COLONNES + FONDATIONS

# Les 52 cartes, rangées (avant mélange).
PAQUET = (
    "api", "2pi", "3pi", "4pi", "5pi", "6pi", "7pi", "8pi", "9pi", "10pi", "vpi", "dpi", "rpi",
    "aco", "2co", "3co", "4co", "5co", "6co", "7co", "8co", "9co", "10co", "vco", "dco", "rco",
    "aca", "2ca", "3ca", "4ca", "5ca", "6ca", "7ca", "8ca", "9ca", "10ca", "vca", "dca", "rca",
    "atr", "2tr", "3tr", "4tr", "5tr", "6tr", "7tr", "8tr", "9tr", "10tr", "vtr", "dtr", "rtr",
)

# =============================================================================
# ÉTAT 1 : juste après la distribution
# =============================================================================

_ETAT_DEBUT = {
    "piles": {
        # Pioche : 24 cartes, toutes face cachée. Prochaine carte tirée = la DERNIÈRE.
        "p": [
            "atr", "2tr", "7pi", "vca", "rco", "vco", "4co", "9tr",
            "8co", "5pi", "7ca", "rtr", "10co", "4pi", "2co", "10ca",
            "10tr", "5co", "2ca", "vtr", "9ca", "aca", "5tr", "7co",
        ],
        # Défausse : vide.
        "d": [],
        # Colonnes : du bas (indice 0) vers le dessus (dernier élément).
        "c1": ["7tr"],                                                  # aucune cachée, visible : 7tr
        "c2": ["dco", "8tr"],                                           # 1 cachée, visible : 8tr
        "c3": ["dca", "4tr", "3ca"],                                    # 2 cachées, visible : 3ca
        "c4": ["dpi", "6pi", "4ca", "6tr"],                             # 3 cachées, visible : 6tr
        "c5": ["aco", "10pi", "8pi", "6ca", "3tr"],                     # 4 cachées, visible : 3tr
        "c6": ["vpi", "6co", "2pi", "rca", "3co", "5ca"],               # 5 cachées, visible : 5ca
        "c7": ["rpi", "api", "8ca", "9co", "3pi", "dtr", "9pi"],        # 6 cachées, visible : 9pi
        # Fondations : une par famille, de l'as (indice 0) vers le roi.
        "fca": [],
        "fpi": [],
        "fco": [],
        "ftr": [],
    },
    # Nombre de cartes face cachée en BAS de chaque colonne.
    "cachees": {"c1": 0, "c2": 1, "c3": 2, "c4": 3, "c5": 4, "c6": 5, "c7": 6},
    # Index : carte -> nom de la pile où elle se trouve (52 entrées, rangées par pile).
    "index": {
        # p
        "atr": "p", "2tr": "p", "7pi": "p", "vca": "p", "rco": "p", "vco": "p",
        "4co": "p", "9tr": "p", "8co": "p", "5pi": "p", "7ca": "p", "rtr": "p",
        "10co": "p", "4pi": "p", "2co": "p", "10ca": "p", "10tr": "p", "5co": "p",
        "2ca": "p", "vtr": "p", "9ca": "p", "aca": "p", "5tr": "p", "7co": "p",
        # c1
        "7tr": "c1",
        # c2
        "dco": "c2", "8tr": "c2",
        # c3
        "dca": "c3", "4tr": "c3", "3ca": "c3",
        # c4
        "dpi": "c4", "6pi": "c4", "4ca": "c4", "6tr": "c4",
        # c5
        "aco": "c5", "10pi": "c5", "8pi": "c5", "6ca": "c5", "3tr": "c5",
        # c6
        "vpi": "c6", "6co": "c6", "2pi": "c6", "rca": "c6", "3co": "c6", "5ca": "c6",
        # c7
        "rpi": "c7", "api": "c7", "8ca": "c7", "9co": "c7", "3pi": "c7", "dtr": "c7",
        "9pi": "c7",
    },
    # Paramètres de la partie (proposition, à adapter).
    "params": {
        "tirage": 1,            # nombre de cartes retournées à chaque pioche (1 ou 3)
        "passages_max": None,   # nombre de passages autorisés dans la pioche (None = illimité)
        "roi_seul": True,       # True : seul un roi peut aller sur une colonne vide
        "aide": True,           # True : le joueur peut demander les coups possibles
    },
    "passages": 0,              # nombre de fois où la défausse a été remise dans la pioche
    "coups": 0,                 # nombre de coups joués depuis le début
}

# =============================================================================
# ÉTAT 2 : après les 39 premiers coups de SOLUTION
# =============================================================================
#
# Pioche : 8 cartes      Défausse : 5pi (sur 5)
# Fondations : fca = 3ca   fpi = -   fco = -   ftr = -
# c1 : (vide)
# c2 : ## 8tr 7co 6tr 5ca 4tr 3co
# c3 : dca vtr 10ca 9pi 8co 7tr 6ca 5tr 4ca 3tr 2co
# c4 : dpi
# c5 : ## ## 8pi 7ca 6pi 5co 4pi
# c6 : ## ## ## rca dtr
# c7 : ## ## ## ## 3pi

_ETAT_MILIEU = {
    "piles": {
        # Pioche : 8 cartes, toutes face cachée. Prochaine carte tirée = la DERNIÈRE.
        "p": ["atr", "2tr", "7pi", "vca", "rco", "vco", "4co", "9tr"],
        # Défausse : 5 cartes, face visible. Seule la DERNIÈRE est jouable.
        "d": ["9ca", "10tr", "10co", "rtr", "5pi"],
        # Colonnes : du bas (indice 0) vers le dessus (dernier élément).
        "c1": [],                                                       # vide
        "c2": ["dco", "8tr", "7co", "6tr", "5ca", "4tr", "3co"],        # 1 cachée, visibles : 8tr 7co 6tr 5ca 4tr 3co
        "c3": [
            "dca", "vtr", "10ca", "9pi", "8co", "7tr", "6ca", "5tr", "4ca", "3tr",
            "2co",
        ],  # aucune cachée, visibles : dca vtr 10ca 9pi 8co 7tr 6ca 5tr 4ca 3tr 2co
        "c4": ["dpi"],                                                  # aucune cachée, visible : dpi
        "c5": ["aco", "10pi", "8pi", "7ca", "6pi", "5co", "4pi"],       # 2 cachées, visibles : 8pi 7ca 6pi 5co 4pi
        "c6": ["vpi", "6co", "2pi", "rca", "dtr"],                      # 3 cachées, visibles : rca dtr
        "c7": ["rpi", "api", "8ca", "9co", "3pi"],                      # 4 cachées, visible : 3pi
        # Fondations : une par famille, de l'as (indice 0) vers le roi.
        "fca": ["aca", "2ca", "3ca"],
        "fpi": [],
        "fco": [],
        "ftr": [],
    },
    # Nombre de cartes face cachée en BAS de chaque colonne.
    "cachees": {"c1": 0, "c2": 1, "c3": 0, "c4": 0, "c5": 2, "c6": 3, "c7": 4},
    # Index : carte -> nom de la pile où elle se trouve (52 entrées, rangées par pile).
    "index": {
        # p
        "atr": "p", "2tr": "p", "7pi": "p", "vca": "p", "rco": "p", "vco": "p",
        "4co": "p", "9tr": "p",
        # d
        "9ca": "d", "10tr": "d", "10co": "d", "rtr": "d", "5pi": "d",
        # c2
        "dco": "c2", "8tr": "c2", "7co": "c2", "6tr": "c2", "5ca": "c2", "4tr": "c2",
        "3co": "c2",
        # c3
        "dca": "c3", "vtr": "c3", "10ca": "c3", "9pi": "c3", "8co": "c3", "7tr": "c3",
        "6ca": "c3", "5tr": "c3", "4ca": "c3", "3tr": "c3", "2co": "c3",
        # c4
        "dpi": "c4",
        # c5
        "aco": "c5", "10pi": "c5", "8pi": "c5", "7ca": "c5", "6pi": "c5", "5co": "c5",
        "4pi": "c5",
        # c6
        "vpi": "c6", "6co": "c6", "2pi": "c6", "rca": "c6", "dtr": "c6",
        # c7
        "rpi": "c7", "api": "c7", "8ca": "c7", "9co": "c7", "3pi": "c7",
        # fca
        "aca": "fca", "2ca": "fca", "3ca": "fca",
    },
    # Paramètres de la partie (proposition, à adapter).
    "params": {
        "tirage": 1,            # nombre de cartes retournées à chaque pioche (1 ou 3)
        "passages_max": None,   # nombre de passages autorisés dans la pioche (None = illimité)
        "roi_seul": True,       # True : seul un roi peut aller sur une colonne vide
        "aide": True,           # True : le joueur peut demander les coups possibles
    },
    "passages": 0,              # nombre de fois où la défausse a été remise dans la pioche
    "coups": 39,                # nombre de coups joués depuis le début
}

# =============================================================================
# ÉTAT 3 : après les 75 premiers coups de SOLUTION (pioche vide)
# =============================================================================
#
# Pioche : vide      Défausse : 7pi (sur 7)
# Fondations : fca = 7ca   fpi = -   fco = 2co   ftr = 8tr
# c1 : rca dtr vco 10pi
# c2 : dco
# c3 : dca vtr 10ca 9pi 8co
# c4 : dpi vca
# c5 : (vide)
# c6 : ## 6co 5pi 4co 3pi
# c7 : ## ## ## 9co 8pi 7co 6pi 5co 4pi 3co 2pi

_ETAT_PIOCHE_VIDE = {
    "piles": {
        # Pioche : vide.
        "p": [],
        # Défausse : 7 cartes, face visible. Seule la DERNIÈRE est jouable.
        "d": ["9ca", "10tr", "10co", "rtr", "9tr", "rco", "7pi"],
        # Colonnes : du bas (indice 0) vers le dessus (dernier élément).
        "c1": ["rca", "dtr", "vco", "10pi"],                            # aucune cachée, visibles : rca dtr vco 10pi
        "c2": ["dco"],                                                  # aucune cachée, visible : dco
        "c3": ["dca", "vtr", "10ca", "9pi", "8co"],                     # aucune cachée, visibles : dca vtr 10ca 9pi 8co
        "c4": ["dpi", "vca"],                                           # aucune cachée, visibles : dpi vca
        "c5": [],                                                       # vide
        "c6": ["vpi", "6co", "5pi", "4co", "3pi"],                      # 1 cachée, visibles : 6co 5pi 4co 3pi
        "c7": [
            "rpi", "api", "8ca", "9co", "8pi", "7co", "6pi", "5co", "4pi", "3co",
            "2pi",
        ],  # 3 cachées, visibles : 9co 8pi 7co 6pi 5co 4pi 3co 2pi
        # Fondations : une par famille, de l'as (indice 0) vers le roi.
        "fca": ["aca", "2ca", "3ca", "4ca", "5ca", "6ca", "7ca"],
        "fpi": [],
        "fco": ["aco", "2co"],
        "ftr": ["atr", "2tr", "3tr", "4tr", "5tr", "6tr", "7tr", "8tr"],
    },
    # Nombre de cartes face cachée en BAS de chaque colonne.
    "cachees": {"c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 1, "c7": 3},
    # Index : carte -> nom de la pile où elle se trouve (52 entrées, rangées par pile).
    "index": {
        # d
        "9ca": "d", "10tr": "d", "10co": "d", "rtr": "d", "9tr": "d", "rco": "d",
        "7pi": "d",
        # c1
        "rca": "c1", "dtr": "c1", "vco": "c1", "10pi": "c1",
        # c2
        "dco": "c2",
        # c3
        "dca": "c3", "vtr": "c3", "10ca": "c3", "9pi": "c3", "8co": "c3",
        # c4
        "dpi": "c4", "vca": "c4",
        # c6
        "vpi": "c6", "6co": "c6", "5pi": "c6", "4co": "c6", "3pi": "c6",
        # c7
        "rpi": "c7", "api": "c7", "8ca": "c7", "9co": "c7", "8pi": "c7", "7co": "c7",
        "6pi": "c7", "5co": "c7", "4pi": "c7", "3co": "c7", "2pi": "c7",
        # fca
        "aca": "fca", "2ca": "fca", "3ca": "fca", "4ca": "fca", "5ca": "fca", "6ca": "fca",
        "7ca": "fca",
        # fco
        "aco": "fco", "2co": "fco",
        # ftr
        "atr": "ftr", "2tr": "ftr", "3tr": "ftr", "4tr": "ftr", "5tr": "ftr", "6tr": "ftr",
        "7tr": "ftr", "8tr": "ftr",
    },
    # Paramètres de la partie (proposition, à adapter).
    "params": {
        "tirage": 1,            # nombre de cartes retournées à chaque pioche (1 ou 3)
        "passages_max": None,   # nombre de passages autorisés dans la pioche (None = illimité)
        "roi_seul": True,       # True : seul un roi peut aller sur une colonne vide
        "aide": True,           # True : le joueur peut demander les coups possibles
    },
    "passages": 0,              # nombre de fois où la défausse a été remise dans la pioche
    "coups": 75,                # nombre de coups joués depuis le début
}

# =============================================================================
# ÉTAT 4 : après les 115 coups de SOLUTION (partie gagnée)
# =============================================================================

_ETAT_FIN = {
    "piles": {
        # Pioche : vide.
        "p": [],
        # Défausse : vide.
        "d": [],
        # Colonnes : du bas (indice 0) vers le dessus (dernier élément).
        "c1": [],                                                       # vide
        "c2": [],                                                       # vide
        "c3": [],                                                       # vide
        "c4": [],                                                       # vide
        "c5": [],                                                       # vide
        "c6": [],                                                       # vide
        "c7": [],                                                       # vide
        # Fondations : une par famille, de l'as (indice 0) vers le roi.
        "fca": ["aca", "2ca", "3ca", "4ca", "5ca", "6ca", "7ca", "8ca", "9ca", "10ca", "vca", "dca", "rca"],
        "fpi": ["api", "2pi", "3pi", "4pi", "5pi", "6pi", "7pi", "8pi", "9pi", "10pi", "vpi", "dpi", "rpi"],
        "fco": ["aco", "2co", "3co", "4co", "5co", "6co", "7co", "8co", "9co", "10co", "vco", "dco", "rco"],
        "ftr": ["atr", "2tr", "3tr", "4tr", "5tr", "6tr", "7tr", "8tr", "9tr", "10tr", "vtr", "dtr", "rtr"],
    },
    # Nombre de cartes face cachée en BAS de chaque colonne.
    "cachees": {"c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0},
    # Index : carte -> nom de la pile où elle se trouve (52 entrées, rangées par pile).
    "index": {
        # fca
        "aca": "fca", "2ca": "fca", "3ca": "fca", "4ca": "fca", "5ca": "fca", "6ca": "fca",
        "7ca": "fca", "8ca": "fca", "9ca": "fca", "10ca": "fca", "vca": "fca", "dca": "fca",
        "rca": "fca",
        # fpi
        "api": "fpi", "2pi": "fpi", "3pi": "fpi", "4pi": "fpi", "5pi": "fpi", "6pi": "fpi",
        "7pi": "fpi", "8pi": "fpi", "9pi": "fpi", "10pi": "fpi", "vpi": "fpi", "dpi": "fpi",
        "rpi": "fpi",
        # fco
        "aco": "fco", "2co": "fco", "3co": "fco", "4co": "fco", "5co": "fco", "6co": "fco",
        "7co": "fco", "8co": "fco", "9co": "fco", "10co": "fco", "vco": "fco", "dco": "fco",
        "rco": "fco",
        # ftr
        "atr": "ftr", "2tr": "ftr", "3tr": "ftr", "4tr": "ftr", "5tr": "ftr", "6tr": "ftr",
        "7tr": "ftr", "8tr": "ftr", "9tr": "ftr", "10tr": "ftr", "vtr": "ftr", "dtr": "ftr",
        "rtr": "ftr",
    },
    # Paramètres de la partie (proposition, à adapter).
    "params": {
        "tirage": 1,            # nombre de cartes retournées à chaque pioche (1 ou 3)
        "passages_max": None,   # nombre de passages autorisés dans la pioche (None = illimité)
        "roi_seul": True,       # True : seul un roi peut aller sur une colonne vide
        "aide": True,           # True : le joueur peut demander les coups possibles
    },
    "passages": 0,              # nombre de fois où la défausse a été remise dans la pioche
    "coups": 115,               # nombre de coups joués depuis le début
}

# =============================================================================
# SOLUTION : 115 coups qui gagnent la partie depuis etat_debut()
# Format : (carte, destination). Destination "d" = piocher.
# =============================================================================

SOLUTION = (
    ("5ca", "c4"),        #   1. 5ca : c6 -> c4   => retourne 3co
    ("7co", "d"),         #   2. pioche : 7co passe sur la défausse
    ("7co", "c2"),        #   3. 7co : d -> c2
    ("6tr", "c2"),        #   4. 6tr (avec la carte posée dessus) : c4 -> c2   => retourne 4ca
    ("3tr", "c4"),        #   5. 3tr : c5 -> c4   => retourne 6ca
    ("6ca", "c1"),        #   6. 6ca : c5 -> c1   => retourne 8pi
    ("5tr", "d"),         #   7. pioche : 5tr passe sur la défausse
    ("5tr", "c1"),        #   8. 5tr : d -> c1
    ("4ca", "c1"),        #   9. 4ca (avec la carte posée dessus) : c4 -> c1   => retourne 6pi
    ("aca", "d"),         #  10. pioche : aca passe sur la défausse
    ("aca", "fca"),       #  11. aca : d -> fca
    ("9ca", "d"),         #  12. pioche : 9ca passe sur la défausse
    ("vtr", "d"),         #  13. pioche : vtr passe sur la défausse
    ("2ca", "d"),         #  14. pioche : 2ca passe sur la défausse
    ("2ca", "fca"),       #  15. 2ca : d -> fca
    ("3ca", "fca"),       #  16. 3ca : c3 -> fca   => retourne 4tr
    ("4tr", "c2"),        #  17. 4tr : c3 -> c2   => retourne dca
    ("3co", "c2"),        #  18. 3co : c6 -> c2   => retourne rca
    ("vtr", "c3"),        #  19. vtr : d -> c3
    ("5co", "d"),         #  20. pioche : 5co passe sur la défausse
    ("5co", "c4"),        #  21. 5co : d -> c4
    ("10tr", "d"),        #  22. pioche : 10tr passe sur la défausse
    ("10ca", "d"),        #  23. pioche : 10ca passe sur la défausse
    ("10ca", "c3"),       #  24. 10ca : d -> c3
    ("9pi", "c3"),        #  25. 9pi : c7 -> c3   => retourne dtr
    ("dtr", "c6"),        #  26. dtr : c7 -> c6   => retourne 3pi
    ("2co", "d"),         #  27. pioche : 2co passe sur la défausse
    ("2co", "c1"),        #  28. 2co : d -> c1
    ("4pi", "d"),         #  29. pioche : 4pi passe sur la défausse
    ("4pi", "c4"),        #  30. 4pi : d -> c4
    ("10co", "d"),        #  31. pioche : 10co passe sur la défausse
    ("rtr", "d"),         #  32. pioche : rtr passe sur la défausse
    ("7ca", "d"),         #  33. pioche : 7ca passe sur la défausse
    ("7ca", "c5"),        #  34. 7ca : d -> c5
    ("6pi", "c5"),        #  35. 6pi (avec les 2 cartes posées dessus) : c4 -> c5   => retourne dpi
    ("5pi", "d"),         #  36. pioche : 5pi passe sur la défausse
    ("8co", "d"),         #  37. pioche : 8co passe sur la défausse
    ("8co", "c3"),        #  38. 8co : d -> c3
    ("7tr", "c3"),        #  39. 7tr (avec les 5 cartes posées dessus) : c1 -> c3   => c1 est vide
    # ---------- ici : etat_milieu() ----------
    ("rca", "c1"),        #  40. rca (avec la carte posée dessus) : c6 -> c1 [colonne vide]   => retourne 2pi
    ("2pi", "c2"),        #  41. 2pi : c6 -> c2   => retourne 6co
    ("5pi", "c6"),        #  42. 5pi : d -> c6
    ("9tr", "d"),         #  43. pioche : 9tr passe sur la défausse
    ("4co", "d"),         #  44. pioche : 4co passe sur la défausse
    ("4co", "c6"),        #  45. 4co : d -> c6
    ("3pi", "c6"),        #  46. 3pi : c7 -> c6   => retourne 9co
    ("8tr", "c7"),        #  47. 8tr (avec les 6 cartes posées dessus) : c2 -> c7   => retourne dco
    ("vco", "d"),         #  48. pioche : vco passe sur la défausse
    ("vco", "c1"),        #  49. vco : d -> c1
    ("rco", "d"),         #  50. pioche : rco passe sur la défausse
    ("vca", "d"),         #  51. pioche : vca passe sur la défausse
    ("vca", "c4"),        #  52. vca : d -> c4
    ("7pi", "d"),         #  53. pioche : 7pi passe sur la défausse
    ("2tr", "d"),         #  54. pioche : 2tr passe sur la défausse
    ("atr", "d"),         #  55. pioche : atr passe sur la défausse
    ("atr", "ftr"),       #  56. atr : d -> ftr
    ("2tr", "ftr"),       #  57. 2tr : d -> ftr
    ("2co", "c6"),        #  58. 2co : c3 -> c6
    ("3tr", "ftr"),       #  59. 3tr : c3 -> ftr
    ("4ca", "fca"),       #  60. 4ca : c3 -> fca
    ("3co", "c5"),        #  61. 3co (avec la carte posée dessus) : c7 -> c5
    ("4tr", "ftr"),       #  62. 4tr : c7 -> ftr
    ("5tr", "ftr"),       #  63. 5tr : c3 -> ftr
    ("5ca", "fca"),       #  64. 5ca : c7 -> fca
    ("6ca", "fca"),       #  65. 6ca : c3 -> fca
    ("6tr", "ftr"),       #  66. 6tr : c7 -> ftr
    ("7tr", "ftr"),       #  67. 7tr : c3 -> ftr
    ("6pi", "c7"),        #  68. 6pi (avec les 4 cartes posées dessus) : c5 -> c7
    ("7ca", "fca"),       #  69. 7ca : c5 -> fca
    ("7co", "c5"),        #  70. 7co (avec les 5 cartes posées dessus) : c7 -> c5
    ("8tr", "ftr"),       #  71. 8tr : c7 -> ftr
    ("8pi", "c7"),        #  72. 8pi (avec les 6 cartes posées dessus) : c5 -> c7   => retourne 10pi
    ("10pi", "c1"),       #  73. 10pi : c5 -> c1   => retourne aco
    ("aco", "fco"),       #  74. aco : c5 -> fco   => c5 est vide
    ("2co", "fco"),       #  75. 2co : c6 -> fco
    # ---------- ici : etat_pioche_vide() ----------
    ("9co", "c1"),        #  76. 9co (avec les 7 cartes posées dessus) : c7 -> c1   => retourne 8ca
    ("8ca", "fca"),       #  77. 8ca : c7 -> fca   => retourne api
    ("api", "fpi"),       #  78. api : c7 -> fpi   => retourne rpi
    ("2pi", "fpi"),       #  79. 2pi : c1 -> fpi
    ("3co", "fco"),       #  80. 3co : c1 -> fco
    ("3pi", "fpi"),       #  81. 3pi : c6 -> fpi
    ("4pi", "fpi"),       #  82. 4pi : c1 -> fpi
    ("4co", "fco"),       #  83. 4co : c6 -> fco
    ("5co", "fco"),       #  84. 5co : c1 -> fco
    ("5pi", "fpi"),       #  85. 5pi : c6 -> fpi
    ("6pi", "fpi"),       #  86. 6pi : c1 -> fpi
    ("6co", "fco"),       #  87. 6co : c6 -> fco   => retourne vpi
    ("7co", "fco"),       #  88. 7co : c1 -> fco
    ("8co", "fco"),       #  89. 8co : c3 -> fco
    ("7pi", "fpi"),       #  90. 7pi : d -> fpi
    ("8pi", "fpi"),       #  91. 8pi : c1 -> fpi
    ("9co", "fco"),       #  92. 9co : c1 -> fco
    ("9pi", "fpi"),       #  93. 9pi : c3 -> fpi
    ("10pi", "fpi"),      #  94. 10pi : c1 -> fpi
    ("vpi", "fpi"),       #  95. vpi : c6 -> fpi   => c6 est vide
    ("dco", "c7"),        #  96. dco : c2 -> c7   => c2 est vide
    ("rco", "c2"),        #  97. rco : d -> c2
    ("9tr", "ftr"),       #  98. 9tr : d -> ftr
    ("dpi", "c2"),        #  99. dpi (avec la carte posée dessus) : c4 -> c2   => c4 est vide
    ("rtr", "c4"),        # 100. rtr : d -> c4
    ("10co", "fco"),      # 101. 10co : d -> fco
    ("vco", "fco"),       # 102. vco : c1 -> fco
    ("dco", "fco"),       # 103. dco : c7 -> fco
    ("10tr", "ftr"),      # 104. 10tr : d -> ftr
    ("9ca", "fca"),       # 105. 9ca : d -> fca
    ("10ca", "fca"),      # 106. 10ca : c3 -> fca
    ("vca", "fca"),       # 107. vca : c2 -> fca
    ("dpi", "fpi"),       # 108. dpi : c2 -> fpi
    ("rco", "fco"),       # 109. rco : c2 -> fco   => c2 est vide
    ("vtr", "ftr"),       # 110. vtr : c3 -> ftr
    ("dtr", "ftr"),       # 111. dtr : c1 -> ftr
    ("dca", "fca"),       # 112. dca : c3 -> fca   => c3 est vide
    ("rca", "fca"),       # 113. rca : c1 -> fca   => c1 est vide
    ("rtr", "ftr"),       # 114. rtr : c4 -> ftr   => c4 est vide
    ("rpi", "fpi"),       # 115. rpi : c7 -> fpi   => c7 est vide
)


# =============================================================================
# ACCÈS AUX ÉTATS (renvoient toujours une copie neuve)
# =============================================================================

def etat_debut():
    """État juste après la distribution."""
    return copy.deepcopy(_ETAT_DEBUT)


def etat_milieu():
    """État après les 39 premiers coups de SOLUTION."""
    return copy.deepcopy(_ETAT_MILIEU)


def etat_pioche_vide():
    """État après les 75 premiers coups de SOLUTION (pioche vide)."""
    return copy.deepcopy(_ETAT_PIOCHE_VIDE)


def etat_fin():
    """État après tous les coups de SOLUTION : partie gagnée."""
    return copy.deepcopy(_ETAT_FIN)