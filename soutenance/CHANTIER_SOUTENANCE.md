# Chantier soutenance : projet Solitaire

> Source de vérité pour la soutenance du **vendredi 6 novembre 2026** et le rendu Moodle (**avant 14 h 00**).
> À lire avant de reprendre le sujet. À mettre à jour à la fin de chaque session.

## Le format de la soutenance (annoncé par le prof, 02/11/2026)

Chacun passe **seul**, avec son ordinateur. On **projette notre code**, les profs posent des questions dessus, puis demandent des **modifications en direct** (exemple donné : « au début du jeu, toutes les cartes doivent être retournées »). Il faut savoir modifier n'importe quelle partie du code, y compris celle écrite par l'autre. Les profs chercheront à nous mettre en difficulté. Le diaporama et le script de présentation ne servent donc plus.

**Mise à jour du 06/11/2026 (Mattias), ce format remplace le précédent** : passage de 20 minutes. 10 minutes de présentation du code avec le dossier de 2 pages comme support, puis 10 minutes de questions et de défis de code. Le script de présentation sert donc de nouveau : `script_oral.html`. Reste à confirmer sur place : passage à deux ou chacun seul (le script marche dans les deux cas).

## État au 30/10/2026

| Étape | Statut |
|---|---|
| Code : priorité des coups (`h`) | fait et testé, **pas encore commité** |
| Code : l'ordinateur joue tout seul (`ia`) | fait et testé, **pas encore commité** |
| Code : fin automatique quand tout est retourné | fait et testé, **pas encore commité** |
| Code : défausse en éventail (1, 2 ou 3 cartes selon le niveau) | fait et testé, **pas encore commité** |
| Dossier court de 2 pages (info du prof pas sûre) | fait le 04/11 : `Solitaire_Mathevon_Damour_2pages.pdf` |
| Dossier PDF (les 5 rubriques du sujet + annexes) | v1 faite, 12 pages : `Solitaire_Mathevon_Damour.pdf` |
| Mail au prof (un ou plusieurs `.py` ? diaporama ?) | écrit (`mail_prof.txt`), à envoyer par Mattias |
| Réponse du prof | reçue : un seul fichier `.py` à rendre |
| Fusion en un seul fichier : `Solitaire_Mathevon_Damour.py` | fait le 04/11, même sortie que `main.py` |
| Nettoyage avant le gel du code | à faire |
| Diaporama | abandonné (il reste en ligne, inutile) |
| Script oral de 10 minutes, sur le dossier de 2 pages | fait le 06/11 : https://claude.ai/artifact/4svRSRbQ4E7M7cVUXGLhzp (à partager avec Jules) et `Solitaire_Script_oral.pdf` |
| Site d'entraînement : 20 défis de modification (corrections testées), 95 questions, oral blanc, présentation du code, plan | fait : https://claude.ai/artifact/Aovw1Rf4nyWqddQVNxRemo |
| Partage du site avec Jules | à faire (menu Partager de la page) |
| Entraînement : défis de code et questions | en cours, suivre l'onglet Plan du site |
| Impression du dossier papier | à faire, juste avant le 6/11 |
| Dépôt Moodle (`.pdf` + `.py`, un seul dépôt pour le binôme) | à faire, avant le 6/11 à 14 h |

## Fichiers du dossier `soutenance/`

| Fichier | Rôle |
|---|---|
| `CHANTIER_SOUTENANCE.md` | ce fichier |
| `dossier.html` | la source du dossier : le texte et les captures d'écran en couleur |
| `Solitaire_Mathevon_Damour.pdf` | le dossier à déposer sur Moodle et à imprimer |
| `mail_prof.txt` | le mail au prof |
| `../Solitaire_Mathevon_Damour.py` | le fichier unique à déposer sur Moodle (fusion des 14 fichiers, à la racine du projet) |
| `dossier_2pages.html` | la source du dossier court (2 pages), même méthode d'impression que `dossier.html` |
| `Solitaire_Mathevon_Damour_2pages.pdf` | le dossier court, au cas où le prof veut bien 2 pages |
| `prepa_soutenance.html` | la source du site d'entraînement (republier ce fichier garde le même lien) |
| `script_oral.html` | la source du script oral : texte à dire, temps, démo, lignes à modifier dans le fichier unique |
| `Solitaire_Script_oral.pdf` | le script oral à imprimer pour soi (5 pages), à ne pas déposer sur Moodle |

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
- Préparation adaptée au format : des défis de modification au format exact de l'épreuve. Chaque correction a été appliquée sur une copie neuve du projet puis testée (script de test de la session du 02/11). Si le code change (nettoyage), revérifier les corrections qui touchent les lignes modifiées.
- L'onglet Script du site est remplacé par « Le code » : l'ordre de présentation des fichiers, où modifier quoi, les raccourcis PyCharm.
- Méthode devant le prof : reformuler, dire où on va modifier, plus petit changement, relancer, tester, penser aux effets de bord (h et ia, écran des règles, partie de démo, sauvegarde, annuler).
- Site : la progression de chacun est privée, sur son compte claude.ai ; sans accès Contributeur, elle reste dans le navigateur.

## Chiffres vérifiés, cités dans le dossier

- Écran de départ : 18 lignes sur 56 caractères.
- `partie_gagnante.txt` : victoire en 95 coups (la fin se fait toute seule).
- `h` : 4 268 coups proposés sur 25 parties au hasard, 0 refusé par le jeu, 0 coup jouable oublié.
- `ia` gagne la partie de démonstration aux 3 niveaux : 91, 96 et 89 coups.
- `ia` sur 500 parties au hasard par niveau : 41 % gagnées en facile, 21 % en moyen, 11 % en difficile. 0 plantage, 0 boucle infinie.

## À vérifier avant d'imprimer

- [x] Réponse du prof : un seul fichier. Fusion faite (04/11).
- [ ] Mettre à jour l'annexe A, les noms de fichiers cités dans le dossier (`coup_iav1.py`, `main.py`, `verif_*.py`…) et la commande de l'annexe C.
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
5. **Partager** le site avec Jules (menu Partager de la page) : il passe seul lui aussi.
6. **S'entraîner** en suivant l'onglet Plan du site : défis faciles le lundi, moyens le mardi, vicieux le mercredi, examen blanc le jeudi, plus une séance de questions par jour.
7. Le nettoyage du point 4 est plus important qu'avant : le code est projeté, les profs liront les commentaires et les messages.
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

### 02/11/2026
- Le prof a donné le format : passage seul, code projeté, questions et modifications en direct. Diaporama et script abandonnés.
- Site refait pour ce format : 20 défis de modification (7 faciles, 8 moyens, 5 vicieux) avec deux indices, la correction avant/après, le test à faire et les pièges ; chaque correction a été appliquée et testée sur une copie du projet. Onglet « Le code » (ordre de présentation, où modifier quoi, raccourcis PyCharm), 8 questions pièges de plus (95 au total), plan du 2 au 6 novembre. Tous les parcours testés dans un navigateur.

### 04/11/2026
- Le prof veut un seul fichier : création de `Solitaire_Mathevon_Damour.py` à la racine, qui regroupe les 14 fichiers dans l'ordre : paquet et donne, affichage, menu, sauvegarde, vérifications, fin de partie, pioche, coups possibles et `ia`, jouer un coup, victoire, lancement. Les anciens fichiers sont gardés.
- Dans le fichier unique : plus d'imports entre fichiers, `from operator import truediv` enlevé, le `if __name__ == "__main__"` de la victoire enlevé (il aurait lancé l'animation au démarrage), la docstring et le « À AJOUTER » de la pioche remplacés par un commentaire, « Je fais demain » remplacé, les « main.py » des commentaires remplacés.
- Tests dans une copie : `partie_gagnante.txt` donne exactement la même sortie qu'avec `main.py` (95 coups) ; `ia` sur la démo, même sortie aux 3 niveaux ; sauvegarde puis reprise OK.
- Attention : si on modifie le code maintenant, le faire dans `Solitaire_Mathevon_Damour.py` (c'est lui qui est rendu et projeté). Les fautes dans les messages ne sont pas encore corrigées.
- Le prof aurait parlé d'un dossier de 2 pages (pas sûr). Fait quand même : `dossier_2pages.html` et `Solitaire_Mathevon_Damour_2pages.pdf`, les 5 rubriques du sujet en 2 pages A4, avec la commande du fichier unique. Le grand dossier reste celui qu'on compte utiliser.

### 06/11/2026
- Nouveau format annoncé par Mattias : 10 minutes de présentation sur le dossier de 2 pages, puis 10 minutes de questions et de défis. C'est donc le dossier de 2 pages qui sert de support.
- Script oral écrit et publié : les 5 rubriques dans l'ordre du dossier, puis une démo, réparti entre Mattias et Jules et lisible seul. 1 210 mots, soit 9 min 20 à 130 mots par minute, plus les 30 s d'`ia` et la frappe. Pas encore chronométré à voix haute.
- Vérifié sur `Solitaire_Mathevon_Damour.py`, dans une copie : partie gagnante en 95 coups ; `ia` en 91, 96 et 89 coups selon le niveau ; plateau de 18 × 56 ; enchaînement exact de la démo en 91 coups, avec ou sans `annuler` ; `ia` dure 27 s, plus 3 s d'animation. Les 41 %, 21 % et 11 % n'ont pas été recalculés (chiffres du 30/10).
- Défis du site : le code à remplacer a été retrouvé dans le fichier unique, sauf un import de `pioche.py` devenu inutile. Contrôle de texte seulement, les corrections n'ont pas été rejouées sur le fichier unique.
- Commit `0e9dab2` de Mattias (13 h 39) : le fichier unique est suivi par git, sur `origin/mattias` seulement, pas sur `main`.
- Restent dans le fichier rendu, signalés à Mattias : le commentaire faux sur `[-2:]` (ligne 534), `move_possible` inutile (ligne 756), les fautes des messages (lignes 408, 525 et 567).
- Dépôt Moodle (avant 14 h) et impression du dossier : rappelés à 13 h 39, non confirmés ici.
- Demande du prof : toutes les cartes rouges des colonnes doivent être affichées. Fait dans `afficher_colonnes` de `Solitaire_Mathevon_Damour.py` (ligne 255), puis annulé à la demande de Mattias : le fichier est revenu à son état d'avant.
- Nouvelle demande de Mattias : toutes les cartes visibles dès le début. Fait dans `Solitaire_Mathevon_Damour.py` : `cachees` à 0 pour la démo (ligne 54) et dans `nouvelle_partie` (ligne 92). Annulé à la demande de Mattias, qui a fait le changement lui-même dans `jeu_depart.py`.
