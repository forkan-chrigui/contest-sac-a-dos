# PROTOCOLE.md : protocole expérimental

Projet Contest · Sac à dos 0-1 · 3GM PROD
Rédigé par l'équipe 1 (Fatma Trabelsi, M5). Version corrigée après relecture de Forkan (PR #3, issues #4 à #6).

Ce document complète `INTERFACE.md`. Il ne change aucune signature ni aucun format : il fixe les valeurs que `INTERFACE.md` laisse ouvertes (budget, répétitions, graines, mesure du temps). Toutes les valeurs ci-dessous sont **validées**.

---

## 1. Objectif

Comparer de manière équitable les algorithmes des équipes 2 et 3 sur le sac à dos 0-1. Tous les algorithmes sont exécutés avec :

- les mêmes instances ;
- les mêmes solutions de départ ;
- le même budget d'évaluations ;
- le même format de résultats.

## 2. Instances

### 2.1 Instances de réglage (dossier `data/`)

- Bibliothèque KPLib, plage **R01000**.
- Familles : **StronglyCorrelated** et **SubsetSum**.
- Tailles : **n = 100** et **n = 500**.
- 5 premières instances par famille et par taille, soit **20 instances**.
- Les optimums exacts (PyKP) sont dans `data/optimums.csv`.

Ces instances servent au **réglage des paramètres** et à la répétition générale. Les équipes peuvent les utiliser librement pour développer et régler leurs algorithmes.

### 2.2 Instances du test aveugle

- Elles ne sont **jamais déposées dans le dépôt avant le 5 décembre** et restent chez l'équipe 1.
- Même nature que les instances de réglage (mêmes familles, mêmes tailles, même plage R01000), mais **différentes** de celles-ci.
- **5 instances par famille et par taille**, soit **20 instances** de test aveugle.
- Le test aveugle est exécuté avec le **code gelé** (gel le 4 décembre à 17 h). Aucun réglage n'est permis après.

## 3. Algorithmes et solutions de départ

- Chaque algorithme respecte la signature de `INTERFACE.md` : `run(inst, x0, seed, max_evals, **params) -> dict`.
- Les métaheuristiques à solution unique (recherche locale, tabou, recuit, recherche locale probabiliste) partent des **mêmes solutions de départ** : `starting_solutions(inst, k, seed)`.
- **k = 5** solutions de départ par instance, identifiées par `start_id` de 0 à 4.
- Les solutions de départ sont générées avec une graine fixe, **la même pour tous les algorithmes**, et ne dépendent que de l'instance. Graine : `seed_start = 0`.
- Les algorithmes génétiques reçoivent `x0 = None` et construisent leur population initiale avec leur propre graine.

## 4. Répétitions et graines

- Chaque exécution stochastique utilise `seed = run_id` (règle de `INTERFACE.md`).
- **10 répétitions** par configuration : `run_id` de 0 à 9.

| Type d'algorithme | Organisation | Exécutions par instance |
|---|---|---|
| Solution unique (recherche locale, tabou, recuit, recherche locale probabiliste) | 5 départs × 10 répétitions | 50 |
| Algorithmes génétiques | 10 répétitions, sans `start_id` | 10 |
| Déterministes (gloutons, ou recherche locale sans aléa depuis un départ donné) | 1 exécution par départ, avec `run_id = 0` et `seed = 0` | 1 par départ |

Une ligne du CSV est identifiée par (`algorithm`, `variant`, `instance`, `start_id`, `run_id`), avec `seed = run_id` dans tous les cas. Pour les algorithmes génétiques, `start_id` est vide.

## 5. Budget d'évaluations

- Le budget est exprimé en **nombre d'évaluations** (`max_evals`), pas en secondes. Cela rend la comparaison indépendante de la machine et du langage.
- `max_evals = 100 × n`, soit **10 000** pour n = 100 et **50 000** pour n = 500.
- Le budget est **identique pour tous les algorithmes** sur une instance donnée.

### Définition d'une évaluation

Une **évaluation** est une solution dont le gain est évalué, soit avec `gain(inst, x)`, soit par un calcul incrémental (par exemple, le gain d'un voisin obtenu à partir du gain de la solution courante). Chaque solution dont le gain est évalué compte pour une évaluation.

### Ce qui compte dans le budget

- La solution de départ `x0` est évaluée une fois : elle **compte** dans le budget.
- La **population initiale des algorithmes génétiques compte** dans le budget : chaque individu évalué compte pour une évaluation.
- `repair` **ne compte pas** (voir la section 6).

### Arrêt

L'algorithme s'arrête dès que `evaluations >= max_evals`. Le champ `evaluations` du dictionnaire renvoyé doit être exact. Il est vérifié lors de la relecture croisée.

## 6. Solutions non admissibles et `repair`

- Toute solution renvoyée dans `best_x` doit être **admissible** (`feasible = 1` dans le CSV).
- Une solution non admissible peut apparaître au cours de la recherche (mutation, croisement). Elle est réparée par `repair(inst, x)`.
- **`repair` ne compte pas** comme une évaluation. Seule l'évaluation du gain de la solution réparée compte, comme défini à la section 5.
- Les équipes 2 et 3 utilisent le `repair` du socle commun. Elles n'écrivent pas leur propre version, sauf accord via une issue.

## 7. Mesure du temps

- Mesure avec `time.perf_counter()`.
- `time_total_s` : temps de la fonction `run` du début à la fin.
- `time_to_best_s` : temps écoulé jusqu'à la **première apparition** de `best_gain`.
- Les temps de la comparaison finale sont mesurés **sur la même machine**, sans autre programme lourd en parallèle et **sans parallélisme** entre exécutions.
- Le temps est un indicateur **secondaire**. La comparaison principale se fait à budget d'évaluations égal.

## 8. Résultats et format CSV

- Le format est celui de la section 7 de `INTERFACE.md`. Un fichier CSV par algorithme et par série de tests, dans `results/`.
- Seul `benchmark.py` (équipe 1) écrit les CSV.
- `gap_pct` et `is_optimal` utilisent l'optimum de `data/optimums.csv`.

### Modifications du format décidées

- **Colonne `max_evals`** ajoutée au CSV, pour vérifier le respect du budget.
- **Fichiers `history`** : un fichier JSON par (algorithme, variante, instance) dans `results/history/`, contenant toutes les exécutions (`start_id`, `run_id`, `history`). Les points de `history` sont (nombre d'évaluations, meilleur gain), et non (itération, meilleur gain) : toutes les courbes ont ainsi le même axe et se comparent à budget égal. Ils servent aux courbes de convergence.
- Ces modifications sont faites dans `INTERFACE.md` par la PR #7, qui répond aux issues #4, #5 et #6.

## 9. Indicateurs de performance

Définis avec Nesrine (M6), calculés par instance puis par famille :

- écart relatif moyen à l'optimum (`gap_pct`) et son écart-type ;
- meilleur résultat obtenu ;
- nombre d'optimums trouvés (`is_optimal`) ;
- temps moyen jusqu'à la meilleure solution (`time_to_best_s`) ;
- courbes de convergence à partir des fichiers `history`.

## 10. Reproductibilité et contrôles

- Générateur aléatoire : `np.random.default_rng(seed)` uniquement. Pas de `random` ni de `np.random.seed` global.
- **Test de reproductibilité** : deux exécutions avec la même instance, le même `x0`, la même graine et les mêmes paramètres donnent le même `best_gain` et le même `evaluations`.
- **Contrôle du code des équipes 2 et 3** (du 28 novembre au 4 décembre) :
  - budget respecté (`evaluations <= max_evals`) ;
  - graines fixées, aucun appel à un solveur externe ;
  - solutions renvoyées admissibles ;
  - format de retour conforme à `INTERFACE.md`.
- Chaque écart est signalé par une **issue Git**.

## 11. Calendrier

| Date | Étape |
|---|---|
| Avant le mercredi 25 nov | Validation finale du protocole et fusion de la PR #3 |
| 20 → 27 nov | Script de benchmark et répétition générale sur les instances de réglage |
| Vendredi 27 nov | Point d'étape avec l'enseignante |
| 28 nov → 4 déc | Relecture et tests de reproductibilité du code des équipes 2 et 3 |
| Vendredi 4 déc, 17 h | Gel du code |
| 5 → 8 déc | Test aveugle avec le code gelé, vérification, classement |
| 9 déc | Rapport, README, résultats bruts et fiches de contribution |
| Vendredi 11 déc | Soutenance |

## 12. Récapitulatif des décisions (validées par Forkan)

| # | Point | Décision |
|---|---|---|
| 1 | Budget `max_evals` | 100 × n |
| 2 | Nombre de répétitions | 10 (`run_id` de 0 à 9) |
| 3 | Nombre de solutions de départ k | 5 |
| 4 | Organisation des exécutions | 5 départs × 10 répétitions (solution unique), 10 répétitions (AG) |
| 5 | Algorithmes déterministes | `run_id = 0`, `seed = 0` |
| 6 | Solution de départ `x0` | Compte dans le budget |
| 7 | Population initiale des AG | Compte dans le budget |
| 8 | Comptage de `repair` | Ne compte pas |
| 9 | Définition d'une évaluation | Une solution dont le gain est évalué (`gain()` ou calcul incrémental) |
| 10 | Instances du test aveugle | 5 par famille et par taille |
| 11 | Format CSV | Ajout de la colonne `max_evals` et de fichiers `history` |
