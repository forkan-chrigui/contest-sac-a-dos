
from dataclasses import dataclass
from pathlib import Path

import numpy as np


# ============================================================
# 1. Structure de données
# ============================================================

@dataclass(frozen=True)
class Instance:
    name: str
    n: int
    c: int
    p: np.ndarray
    w: np.ndarray


# ============================================================
# 2. Lecture d'une instance
# ============================================================

def read_instance(path: str | Path) -> Instance:
    path = Path(path)

    values = np.fromstring(
        path.read_text(encoding="utf-8"),
        sep=" ",
        dtype=np.int64
    )

    if len(values) < 2:
        raise ValueError(f"Invalid instance file: {path}")

    n = int(values[0])
    c = int(values[1])

    if n < 0 or c < 0:
        raise ValueError(f"Invalid instance parameters: {path}")

    if len(values) != 2 + 2 * n:
        raise ValueError(f"Invalid number of values in file: {path}")

    items = values[2:].reshape(n, 2)

    p = items[:, 0].copy()
    w = items[:, 1].copy()

    return Instance(
        name=f"{path.parents[2].name}_{path.parents[1].name}_{path.parent.name}_{path.stem}",
        n=n,
        c=c,
        p=p,
        w=w
    )


# ============================================================
# 3. Calcul du poids total
# ============================================================

def total_weight(inst: Instance, x: np.ndarray) -> int:
    x = np.asarray(x)

    if x.shape != (inst.n,):
        raise ValueError("Solution has an incorrect shape.")

    return int(np.dot(inst.w, x))


# ============================================================
# 4. Calcul du gain total
# ============================================================

def gain(inst: Instance, x: np.ndarray) -> int:
    x = np.asarray(x)

    if x.shape != (inst.n,):
        raise ValueError("Solution has an incorrect shape.")

    return int(np.dot(inst.p, x))


# ============================================================
# 5. Vérification de l'admissibilité
# ============================================================

def is_feasible(inst: Instance, x: np.ndarray) -> bool:
    return total_weight(inst, x) <= inst.c


# ============================================================
# 6. Réparation d'une solution
# ============================================================

def repair(inst: Instance, x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.int8).copy()

    if x.shape != (inst.n,):
        raise ValueError("Solution has an incorrect shape.")

    if not np.all((x == 0) | (x == 1)):
        raise ValueError("Solution must be binary.")

    # Si la solution est déjà admissible, on retourne une copie.
    if is_feasible(inst, x):
        return x

    # Calcul des ratios profit / poids.
    ratios = np.divide(
        inst.p,
        inst.w,
        out=np.full(inst.n, np.inf, dtype=float),
        where=inst.w != 0
    )

    # Trier les objets du plus mauvais au meilleur ratio.
    order = np.argsort(ratios, kind="stable")

    # Retirer les objets jusqu'à respecter la capacité.
    for i in order:
        if total_weight(inst, x) <= inst.c:
            break

        if x[i] == 1:
            x[i] = 0

    return x


# ============================================================
# 7. Génération d'une solution aléatoire admissible
# ============================================================

def random_solution(
    inst: Instance,
    rng: np.random.Generator
) -> np.ndarray:

    x = np.zeros(inst.n, dtype=np.int8)

    # Générer un ordre aléatoire des objets.
    order = rng.permutation(inst.n)

    current_weight = 0

    # Ajouter les objets tant que la capacité le permet.
    for i in order:
        if current_weight + inst.w[i] <= inst.c:
            x[i] = 1
            current_weight += int(inst.w[i])

    return x


# ============================================================
# 8. Génération des solutions de départ communes
# ============================================================

def starting_solutions(
    inst: Instance,
    k: int,
    seed: int
) -> list[np.ndarray]:

    if k < 0:
        raise ValueError("k must be non-negative.")

    # Générateur reproductible.
    rng = np.random.default_rng(seed)

    solutions = []

    for _ in range(k):
        x = random_solution(inst, rng)
        solutions.append(x)

    return solutions
