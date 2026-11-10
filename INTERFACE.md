# INTERFACE.md : conventions communes du projet Contest

Sac à dos 0-1 · 3GM PROD · Brouillon proposé par l'équipe 1, à valider par les équipes 2 et 3.

Ce document fixe les noms, signatures et formats que tout le monde utilise. Si un point doit changer, on ouvre une issue et on modifie ce fichier par pull request. Personne ne change une signature dans son coin.

## 1. Conventions générales

- Python 3.12, NumPy uniquement (pytest pour les tests).
- Le socle commun est dans `src/knapsack.py`. Les équipes 2 et 3 l'importent, elles ne le recopient pas.
- Les solveurs externes (PyKP) servent seulement à calculer les optimums. Ils sont interdits dans les métaheuristiques.
- Toute fonction aléatoire reçoit un générateur `rng = np.random.default_rng(seed)`. On n'utilise ni `random` ni `np.random.seed` global. Cela rend les résultats reproductibles.
- Les gains et les poids sont des **entiers** (`np.int64`).

## 2. Instances

Fichier kplib, un fichier par instance :

```
n
c
p_1 w_1
...
p_n w_n
```

Hypothèses de départ (à confirmer avec l'enseignante) : plage `R01000`, familles `StronglyCorrelated` et `SubsetSum`, n = 100 et 500, 5 instances par famille.

Organisation des fichiers :

```
data/<famille>/n<taille>/<nom_fichier>.kp
data/optimums.csv        # colonnes : instance, optimum
```

Le champ `instance` utilisé partout (CSV, optimums) est `<famille>_n<taille>_<numero>`, par exemple `StronglyCorrelated_n100_01`.

## 3. Structures de données

```python
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Instance:
    name: str           # ex. "StronglyCorrelated_n100_01"
    n: int              # nombre d'objets
    c: int              # capacité
    p: np.ndarray       # profits, shape (n,), dtype int64
    w: np.ndarray       # poids,   shape (n,), dtype int64
```

Une **solution** est un vecteur binaire NumPy `x` de forme `(n,)` et de type `np.int8`, avec `x[i] = 1` si l'objet `i` est dans le sac. Les fonctions ne modifient jamais `x` en place : elles renvoient une copie.

## 4. Fonctions du socle (équipe 1)

| Fonction | Rôle |
|---|---|
| `read_instance(path) -> Instance` | Lit un fichier kplib. |
| `random_solution(inst, rng) -> np.ndarray` | Solution aléatoire **admissible**. |
| `is_feasible(inst, x) -> bool` | Vrai si le poids total ne dépasse pas `c`. |
| `total_weight(inst, x) -> int` | Poids total de la solution. |
| `gain(inst, x) -> int` | Profit total de la solution. |
| `repair(inst, x, rng) -> np.ndarray` | Rend `x` admissible : retire des objets jusqu'à respecter `c`, en commençant par le plus mauvais ratio p/w. Renvoie `x` inchangé s'il est déjà admissible. |
| `starting_solutions(inst, k, seed) -> list[np.ndarray]` | `k` solutions de départ admissibles, identiques pour tous les algorithmes (voir section 6). |

## 5. Fonctions de l'équipe 2 (fournies à l'équipe 3)

| Fonction | Rôle |
|---|---|
| `greedy_ratio(inst) -> np.ndarray` | Glouton par ratio p/w décroissant. |
| `greedy_profit(inst) -> np.ndarray` | Glouton par profit décroissant. |
| `flip(x, i) -> np.ndarray` | Mouvement : inverse le bit `i` (renvoie une copie). |
| `neighbors(inst, x) -> list[np.ndarray]` | Voisinage par flip ; ne garde que les voisins admissibles. |
| `mutate(inst, x, rng, k=1) -> np.ndarray` | Mutation de `k` flips, utilisée par l'équipe 3. L'équipe 3 appelle ensuite `repair` si besoin. |

Les gloutons sont placés dans `src/greedy.py`, le voisinage et les mouvements dans `src/neighborhood.py`.

## 6. Signature commune d'un algorithme

Chaque algorithme (recherche locale, tabou, recuit, AG...) est une fonction qui a cette forme :

```python
def run(inst: Instance, x0: np.ndarray | None, seed: int, **params) -> dict:
    ...
```

- `x0` : solution de départ (métaheuristiques à solution unique). Pour les AG, on passe `None` et la population initiale est construite avec `seed`.
- `seed` : graine du générateur aléatoire de cette exécution.
- `params` : paramètres propres à l'algorithme (taille de la liste tabou, température initiale, taille de population...).

Elle renvoie un dictionnaire :

```python
{
    "best_x": np.ndarray,        # meilleure solution admissible trouvée
    "best_gain": int,
    "time_to_best_s": float,     # temps écoulé jusqu'à la première apparition de best_gain
    "time_total_s": float,
    "evaluations": int,          # nombre d'évaluations du gain
    "history": list[tuple[int, int]],   # (itération ou génération, meilleur gain jusque-là)
}
```

`history` sert aux courbes de convergence. Elle est enregistrée à chaque amélioration, ou à chaque génération pour les AG.

**Comparaison équitable des métaheuristiques à solution unique.** On utilise `starting_solutions(inst, k, seed)` : toutes les méthodes (recherche locale, tabou, recuit, recherche locale probabiliste) partent des mêmes `k` solutions sur la même instance. Chaque solution de départ est identifiée par `start_id` (0 à k-1).

**Répétitions.** Tout algorithme stochastique est lancé entre 5 et 20 fois par instance (valeur fixée par le protocole), avec des graines différentes : `seed = run_id` pour l'exécution numéro `run_id`.

## 7. Format du CSV de résultats

Un fichier CSV par algorithme et par série de tests, dans `results/`, encodage UTF-8, séparateur virgule, une ligne par exécution :

| Colonne | Contenu |
|---|---|
| `team` | 2 ou 3 |
| `algorithm` | `local_search`, `tabu`, `annealing`, `prob_local_search`, `ga` |
| `variant` | variante (ex. `tournoi_2pts`) ; vide s'il n'y en a pas |
| `family` | `StronglyCorrelated` ou `SubsetSum` |
| `instance` | nom de l'instance (section 2) |
| `n` | nombre d'objets |
| `run_id` | numéro de l'exécution |
| `seed` | graine utilisée |
| `start_id` | numéro de la solution de départ ; vide pour les AG |
| `params` | paramètres, au format JSON compact |
| `best_gain` | meilleur gain trouvé |
| `optimum` | optimum exact de l'instance |
| `gap_pct` | écart relatif à l'optimum, en pourcentage : `100 * (optimum - best_gain) / optimum` |
| `is_optimal` | 1 si `best_gain == optimum`, sinon 0 |
| `feasible` | 1 si la solution est admissible (doit toujours valoir 1) |
| `time_to_best_s` | temps jusqu'à la meilleure solution, en secondes |
| `time_total_s` | temps total, en secondes |
| `evaluations` | nombre d'évaluations |

Le script `benchmark.py` (équipe 1) écrit ces colonnes. Les équipes 2 et 3 n'écrivent pas elles-mêmes les CSV : elles fournissent la fonction `run`.

## 8. Indicateurs de performance (équipe 1)

Par algorithme et par instance (ou famille) :
- écart relatif moyen à l'optimum, et écart-type ;
- meilleur résultat obtenu ;
- nombre d'optimums trouvés ;
- temps moyen jusqu'à la meilleure solution.

## 9. Règles de travail

- Une branche par fonctionnalité (`feature/...`), une pull request relue avant fusion dans `main`.
- Tests unitaires obligatoires dans `tests/` pour chaque fonction livrée (`pytest`).
- Les retours entre équipes passent par des issues Git.
- Déclarer dans le rapport tout usage d'IA générative.

## 10. Points à valider par les équipes 2 et 3

1. Les noms et signatures des sections 4 à 6 conviennent-ils ?
2. Le type `np.int8` pour les solutions et la structure `Instance` conviennent-ils ?
3. La stratégie de `repair` (retirer d'abord le plus mauvais ratio p/w) vous convient-elle, ou voulez-vous aussi une phase d'ajout glouton ?
4. Nombre de solutions de départ `k` et nombre de répétitions : proposition de départ `k = 5` et 10 exécutions.
