# Chantier soutenance : projet Solitaire

> Source de vérité pour la soutenance du **vendredi 6 novembre 2026** et le rendu Moodle (**avant 14 h 00**).
> À lire avant de reprendre le sujet. À mettre à jour à la fin de chaque session.

## État au 30/10/2026

| Étape | Statut |
|---|---|
| Code : priorité des coups (`h`) | fait et testé, **pas encore commité** |
| Code : l'ordinateur joue tout seul (`ia`) | fait et testé, **pas encore commité** |
| Code : fin automatique quand tout est retourné | fait et testé, **pas encore commité** |
| Code : défausse en éventail (1, 2 ou 3 cartes selon le niveau) | fait et testé, **pas encore commité** |
| Dossier PDF (les 5 rubriques du sujet + annexes) | v1 faite, 12 pages : `Solitaire_Mathevon_Damour.pdf` |
| Mail au prof (un ou plusieurs `.py` ? diaporama ?) | écrit (`mail_prof.txt`), à envoyer par Mattias |
| Réponse du prof | en attente |
| Nettoyage avant le gel du code | à faire |
| Diaporama (11 diapos, le script dans les notes) | fait : https://claude.ai/artifact/2KnRT7MPrF2fyRRiivtwMV |
| Script de la soutenance et des démos (≈ 14 min, version courte ≈ 12 min) | fait : notes du diaporama et onglet Script du site |
| Site d'entraînement (87 questions, oral blanc, script chronométré, plan) | fait : https://claude.ai/artifact/Aovw1Rf4nyWqddQVNxRemo |
| Partage du diaporama et du site avec Jules | à faire (menu Partager de chaque page) |
| Entraînement aux questions individuelles | en cours : une séance par jour sur le site |
| Impression du dossier papier | à faire, juste avant le 6/11 |
| Dépôt Moodle (`.pdf` + `.py`, un seul dépôt pour le binôme) | à faire, avant le 6/11 à 14 h |

## Fichiers du dossier `soutenance/`

| Fichier | Rôle |
|---|---|
| `CHANTIER_SOUTENANCE.md` | ce fichier |
| `dossier.html` | la source du dossier : le texte et les captures d'écran en couleur |
| `Solitaire_Mathevon_Damour.pdf` | le dossier à déposer sur Moodle et à imprimer |
| `mail_prof.txt` | le mail au prof |
| `prepa_soutenance.html` | la source du site d'entraînement (republier ce fichier garde le même lien) |

Le diaporama n'a pas de fichier local : il se modifie dans sa page (ou en demandant à Claude, avec son lien).

## Refaire le PDF après une modification de `dossier.html`

Depuis la racine du projet (macOS) :

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --no-pdf-header-footer --user-data-dir=/tmp/chrome-pdf --print-to-pdf=soutenance/Solitaire_Mathevon_Damour.pdf "file://$PWD/soutenance/dossier.html"
```

Sans terminal (ou sous Windows) : ouvrir `dossier.html` dans Chrome, Imprimer, « Enregistrer au format PDF », et décocher « En-têtes et pieds de page ».

Les captures d'écran sont figées dans `dossier.html` : si l'affichage du jeu change, il faut les refaire.

## Décisions actées

- Le dossier est une page HTML imprimée en PDF par Chrome : un seul fichier source, suivi par git.
- Nom du PDF : `Solitaire_Mathevon_Damour.pdf` (le sujet demande `Solitaire_Nom1_Nom2.pdf`).
- Priorité des coups, en 8 rangs : vers une fondation, retourne une carte cachée, défausse vers une colonne, libère une carte pour sa fondation, vide une colonne pour un roi qui attend, `p`, les autres changements de colonne, redescendre d'une fondation.
- `ia` joue le premier coup utile (rangs 1 à 6), jamais les rangs 7 et 8. Il s'arrête s'il doit retourner la défausse une 2e fois sans avoir rien joué.
- Fin automatique seulement si plus aucune carte n'est cachée **et** si la pioche et la défausse sont vides : sinon la victoire n'est pas garantie au niveau difficile.
- Défausse : on montre les `difficulte` dernières cartes ; celles qu'on ne peut pas jouer sont en gris.
- Ligne d'aide : `p : piocher  h : coups  ia : auto  annuler  ? : règles` (56 caractères : l'écran de départ reste à 18 × 56).
- Le script existe à deux endroits, avec le même texte : les notes du diaporama et l'onglet Script du site. Si on le change, changer les deux.
- Répartition : Mattias présente les diapos 1, 3, 4, 6 (démo 1 au clavier) et 8 ; Jules les diapos 2, 5, 7, 9 (démo 2 au clavier) et 10. Chacun présente ce qu'il a codé.
- Démo : la reprise de la sauvegarde se montre dans un 2e onglet du terminal, car il n'y a pas de commande pour quitter pendant la partie.
- Site : la progression de chacun est privée, sur son compte claude.ai ; sans accès Contributeur, elle reste dans le navigateur.

## Chiffres vérifiés, cités dans le dossier

- Écran de départ : 18 lignes sur 56 caractères.
- `partie_gagnante.txt` : victoire en 95 coups (la fin se fait toute seule).
- `h` : 4 268 coups proposés sur 25 parties au hasard, 0 refusé par le jeu, 0 coup jouable oublié.
- `ia` gagne la partie de démonstration aux 3 niveaux : 91, 96 et 89 coups.
- `ia` sur 500 parties au hasard par niveau : 41 % gagnées en facile, 21 % en moyen, 11 % en difficile. 0 plantage, 0 boucle infinie.

## À vérifier avant d'imprimer

- [ ] Réponse du prof. Si un seul fichier est exigé : fusionner, puis mettre à jour l'annexe A, les noms de fichiers cités dans le dossier (`coup_iav1.py`, `main.py`, `verif_*.py`…) et la commande de l'annexe C.
- [ ] Nettoyage fait (liste ci-dessous), et `partie_gagnante.txt` toujours gagnée en 95 coups.
- [ ] Relire le dossier en entier : le prof peut interroger sur n'importe quelle phrase.

## Prochaines actions

1. **Mattias** : envoyer le mail au prof.
2. **Mattias** : commit, push et PR `mattias` → `main`. Elle contient aussi `3bb372a` (les correctifs de `h`), qui n'est toujours pas dans `main`.
3. **Prévenir Jules** : la priorité et `ia` sont faites, il arrête de travailler dessus et fait `git pull origin main` après la fusion. Il doit lire `coup_iav1.py` : c'est son fichier, il sera interrogé dessus.
4. **Nettoyage avant le gel du code** :
   - `verif_colonne.py` : enlever `from operator import truediv` (inutile, et le dossier ne cite que `random`, `json`, `os` et `time`), et le commentaire « Je fais demain pour la carte d'origine ».
   - `deplacement.py` et `verif_fondations.py` : imports inutiles depuis `jeu_depart`, et les `import *`.
   - `pioche.py` : le commentaire « À AJOUTER : il manque un paramètre (lequel ?) » et la docstring.
   - Fautes dans les messages : « Seul une carte inférieur a la carte de destination est autorisé », « Seul une carte avec une valeur supérieur de 1 est accepté », « Il faut un tiret(-) entre la carte et le deplacement ».
   - Idée : une commande pour quitter pendant la partie. Aujourd'hui, après `sauvegarde`, il faut faire Ctrl+C.
5. **Partager** le diaporama et le site avec Jules (menu Partager de chaque page).
6. **Répéter** en suivant l'onglet Plan du site : une séance de questions par jour, des répétitions chronométrées. Télécharger le PDF du diaporama en secours (menu Partager, Exporter).
7. **Imprimer** le dossier, puis **déposer** le PDF et le `.py` sur Moodle avant le 6/11 à 14 h.

## Journal

### 30/10/2026
- Session coupée par un Ctrl+Z : contexte repris depuis l'historique de la session précédente.
- Création de `soutenance/` et de ce chantier.
- Code : priorité des coups dans `h` (8 rangs), commande `ia`, fin automatique quand tout est retourné, défausse en éventail.
- Bug corrigé dans `coup_iav1.py` : un roi seul en première carte de sa colonne n'était jamais proposé vers sa fondation. En fin de partie, `h` ne trouvait donc pas le coup gagnant.
- Tests : partie gagnante en 95 coups ; `h` ne propose que des coups acceptés et n'en oublie aucun ; `ia` gagne la démo aux 3 niveaux ; 1 500 parties au hasard sans plantage.
- Dossier v1 (12 pages) et mail au prof écrits.
- Incident : un test a écrasé `sauvegarde.json` (une partie de test, 0 coup joué). Fichier reconstruit à l'identique, sauf le niveau, remis à facile.
- Diaporama publié : 11 diapos, captures du vrai jeu, script de chacun dans les notes. Les deux démos ont été jouées pour de vrai, étape par étape, dans une copie du projet.
- Site d'entraînement publié : 87 questions d'oral sur tout le code (répétition espacée, indice de confiance, cartes rouges), oral blanc chronométré, script avec chrono de répétition, plan jusqu'au 6/11.
- Site corrigé : le bouton « Retourner la carte » restait grisé tant qu'on n'avait pas choisi sa confiance. Il est remplacé par trois boutons qui retournent la carte (Je suis sûr, J'hésite, Je ne sais pas). Tous les parcours ont été testés dans un navigateur.
- Commit et push sur la branche mattias : le code, puis la soutenance.
