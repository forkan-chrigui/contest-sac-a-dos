PROTOCOLE.md : protocole expérimental

Projet Contest · Sac à dos 0-1 · 3GM PROD Rédigé par l'équipe 1 (Fatma Trabelsi, M5). Brouillon à valider par Forkan, puis par les équipes 2 et 3.

Ce document complète INTERFACE.md. Il ne change aucune signature ni aucun format : il fixe les valeurs que INTERFACE.md laisse ouvertes (budget, répétitions, graines, mesure du temps). Les points marqués [à valider] attendent une décision.

1. Objectif

Comparer de manière équitable les algorithmes des équipes 2 et 3 sur le sac à dos 0-1. Tous les algorithmes sont exécutés avec les mêmes instances, les mêmes solutions de départ, le même budget et le même format de résultats.

2. Instances
2.1 Instances de réglage (déposées dans data/)
Bibliothèque KPLib, plage R01000.
Familles : StronglyCorrelated et SubsetSum.
Tailles : n = 100 et n = 500.
5 premières instances par famille et par taille, soit 20 instances.
Les optimums exacts (PyKP) sont dans data/optimums.csv.

Ces instances servent au réglage des paramètres et à la répétition générale. Les équipes peuvent les utiliser librement pour développer et régler leurs algorithmes.

2.2 Instances du test aveugle
Elles ne sont jamais déposées dans le dépôt avant le 5 décembre et restent chez l'équipe 1.
Elles sont de même nature que les instances de réglage (mêmes familles, mêmes tailles, même plage), mais différentes de celles-ci.
Nombre d'instances par famille et par taille : [à valider]. Proposition : 5.
Le test aveugle est exécuté avec le code gelé (gel le 4 décembre à 17 h). Aucun réglage n'est permis après.

Point à confirmer avec l'enseignante : le choix exact des instances du test aveugle (autres numéros dans KPLib, même plage R01000). [à valider]

3. Algorithmes et solutions de départ
Chaque algorithme respecte la signature de INTERFACE.md : run(inst, x0, seed, max_evals, **params) -> dict.
Les métaheuristiques à solution unique (recherche locale, tabou, recuit, recherche locale probabiliste) partent des mêmes solutions de départ : starting_solutions(inst, k, seed).
k = 5 solutions de départ par instance. [à valider]
Les solutions de départ sont générées avec une graine fixe, la même pour tous les algorithmes, et ne dépendent que de l'instance. Graine proposée : seed_start = 0. [à valider]
Chaque solution de départ porte un start_id de 0 à k-1.
Les algorithmes génétiques reçoivent x0 = None et construisent leur population initiale avec leur propre graine.
4. Répétitions et graines
Chaque exécution stochastique utilise seed = run_id (règle de INTERFACE.md).
10 répétitions par configuration : run_id de 0 à 9. [à valider] (INTERFACE.md autorise de 5 à 20.)
Métaheuristiques à solution unique : pour chaque instance, on lance les 10 répétitions à partir de chacune des 5 solutions de départ. Cela fait 5 × 10 = 50 exécutions par couple (algorithme, instance). [à valider]
Algorithmes génétiques : 10 répétitions par instance, sans start_id. Soit 10 exécutions par couple (algorithme, instance).
Algorithmes déterministes (gloutons, ou recherche locale sans aléa depuis un départ donné) : une seule exécution par départ. Répéter n'apporte rien. Comment enregistrer run_id et seed dans ce cas ? [à valider] Proposition : run_id = 0, seed = 0.
5. Budget d'évaluations
Le budget est exprimé en nombre d'évaluations du gain (max_evals), pas en secondes. Cela rend la comparaison indépendante de la machine et du langage.
Proposition : max_evals = 100 × n, soit 10 000 pour n = 100 et 50 000 pour n = 500. [à valider]
Le budget est identique pour tous les algorithmes sur une instance donnée.
Une évaluation = un appel à gain(inst, x) sur une solution. L'algorithme s'arrête dès que evaluations >= max_evals.
La solution de départ x0 est évaluée une fois et compte dans le budget. [à valider]
Le champ evaluations du dictionnaire renvoyé doit être exact. Il est vérifié lors de la relecture croisée.
6. Solutions non admissibles et repair
Toute solution renvoyée dans best_x doit être admissible (feasible = 1 dans le CSV).
Une solution non admissible peut apparaître au cours de la recherche (mutation, croisement). Elle est réparée par repair(inst, x).
Comptage : repair en lui-même ne compte pas comme une évaluation. Seul le gain de la solution réparée compte. [à valider] (Alternative : compter aussi les appels à repair.)
Les équipes 2 et 3 doivent utiliser le repair du socle commun et ne pas écrire leur propre version, sauf accord via une issue.
7. Mesure du temps
Mesure avec time.perf_counter().
time_total_s : temps de la fonction run du début à la fin.
time_to_best_s : temps écoulé jusqu'à la première apparition de best_gain.
Tous les temps de comparaison finale sont mesurés sur la même machine, sans autre programme lourd en parallèle, et sans parallélisme entre exécutions. [à valider]
Le temps est un indicateur secondaire. La comparaison principale se fait à budget d'évaluations égal.
8. Résultats et format CSV
Le format est celui de la section 7 de INTERFACE.md. Un fichier CSV par algorithme et par série de tests, dans results/.
Seul benchmark.py (équipe 1) écrit les CSV.
Les calculs de gap_pct et is_optimal utilisent l'optimum de data/optimums.csv.
Points du format à clarifier (issues à ouvrir)
Colonne max_evals absente : sans elle, le respect du budget ne se vérifie pas depuis le CSV.
Historique de convergence : history n'est pas dans le CSV, or les courbes de convergence en ont besoin. Proposition : un fichier JSON séparé par exécution dans results/history/.
Lien entre run_id et start_id : voir la section 4. Il faut préciser qu'une ligne du CSV est identifiée par (algorithme, variante, instance, start_id, run_id).
Algorithmes déterministes : valeurs de seed et run_id à convenir (section 4).
9. Indicateurs de performance

Définis avec Nesrine (M6), calculés par instance puis par famille :

écart relatif moyen à l'optimum (gap_pct) et son écart-type ;
meilleur résultat obtenu ;
nombre d'optimums trouvés (is_optimal) ;
temps moyen jusqu'à la meilleure solution (time_to_best_s) ;
courbes de convergence à partir de history.
10. Reproductibilité et contrôles
Générateur aléatoire : np.random.default_rng(seed) uniquement. Pas de random ni de np.random.seed global.
Test de reproductibilité : deux exécutions avec la même instance, le même x0, la même graine et les mêmes paramètres doivent donner le même best_gain et le même evaluations.
Contrôle du code des équipes 2 et 3 (du 28 novembre au 4 décembre) :
budget respecté (evaluations <= max_evals) ;
graines fixées, aucun appel à un solveur externe ;
solutions renvoyées admissibles ;
format de retour conforme à INTERFACE.md.
Chaque écart est signalé par une issue Git.
11. Calendrier du protocole
Date	Étape
13 nov	Protocole proposé, pull request ouverte
19 nov, 17 h	Livrable 1 : protocole validé
22 → 27 nov	Répétition générale sur les instances de réglage
27 nov	Point d'étape avec l'enseignante
4 déc, 17 h	Gel du code
5 → 8 déc	Test aveugle avec le code gelé
12. Récapitulatif des points à valider
#	Point	Proposition
1	Budget max_evals	100 × n
2	Nombre de répétitions	10 (run_id 0 à 9)
3	Nombre de solutions de départ k	5
4	Organisation des exécutions	5 départs × 10 répétitions (solution unique), 10 répétitions (AG)
5	Algorithmes déterministes	run_id = 0, seed = 0
6	Évaluation de x0 dans le budget	Oui
7	Comptage de repair	Non, seul le gain compte
8	Instances du test aveugle	5 par famille et par taille
9	Colonne max_evals et fichier history	À ajouter au format via une issue