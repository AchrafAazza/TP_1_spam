# Résultats de la solution · Jaccard et Dice

- Données : `corpus_ensembles_fr.csv` (requête Q, documents D1 à D8)
- Programme : `TP_1_Solution.py` ou `TP_1_Solution.ipynb`
- Formules, avec k = nombre de termes communs : J = k / (|A| + |B| − k) et D = 2k / (|A| + |B|)
- Scores arrondis à 3 décimales


## 1. Ensembles de termes

- Q, 12 termes : mairie, lance, ateliers, réparation, vélo, écoles, bénévoles, apprennent, élèves, entretenir, réduire, déchets
- D1, 13 termes : écoles, quartier, mairie, organise, ateliers, réparation, vélo, bénévoles, aident, élèves, entretenir, chaque, mercredi
- D3, 10 termes : réparation, vélo, ateliers, proposent, pièces, outils, cyclistes, quartier, chaque, samedi

Termes communs avec Q :

- Q ∩ D1, k = 8 : mairie, ateliers, réparation, vélo, écoles, bénévoles, élèves, entretenir
- Q ∩ D3, k = 3 : ateliers, réparation, vélo


## 2. Scores de D1 et D3

| Paire  | k   | Union | Jaccard      | Dice          |
| ------ | :-: | :---: | :----------: | :-----------: |
| Q – D1 | 8   | 17    | 8/17 ≈ 0,471 | 16/25 = 0,640 |
| Q – D3 | 3   | 19    | 3/19 ≈ 0,158 | 6/22 ≈ 0,273  |

D1 est bien plus proche de Q que D3 : il traite le même sujet (ateliers de réparation vélo de la mairie dans les écoles) et partage 8 des 12 termes de Q.


## 3. Les répétitions de « vélo » dans D3

« vélo » apparaît 4 fois dans le texte de D3, mais ne compte que pour 1 terme dans l'ensemble. Aucun effet sur les scores : J ≈ 0,158 et D ≈ 0,273 dans tous les cas.


## 4. Classement des huit documents

| Rang | Doc | Taille | k   | Union | Jaccard | Dice  |
| :--: | :-: | :----: | :-: | :---: | :-----: | :---: |
| 1    | D7  | 13     | 10  | 15    | 0,667   | 0,800 |
| 2    | D1  | 13     | 8   | 17    | 0,471   | 0,640 |
| 3    | D6  | 13     | 7   | 18    | 0,389   | 0,560 |
| 4    | D2  | 14     | 7   | 19    | 0,368   | 0,538 |
| 5    | D8  | 14     | 6   | 20    | 0,300   | 0,462 |
| 6    | D3  | 10     | 3   | 19    | 0,158   | 0,273 |
| 7    | D4  | 14     | 0   | 26    | 0,000   | 0,000 |
| 8    | D5  | 12     | 0   | 24    | 0,000   | 0,000 |

- Taille = nombre de termes du document ; Union = nombre de termes distincts de Q et du document réunis.
- Tri : score décroissant, puis identifiant croissant. D4 et D5 sont à égalité (0) et départagés par identifiant.


## 5. Comparaison des deux classements

- Les deux classements sont identiques : D7 > D1 > D6 > D2 > D8 > D3 > D4 = D5.
- Raison : D = 2J / (1 + J) augmente toujours avec J. Dice garde donc l'ordre et les égalités de Jaccard ; seule l'échelle change (D ≥ J).
- Limites : seuls les mots identiques comptent. D4 traite le même sujet avec des synonymes (municipalité, bicyclettes, volontaires) mais obtient 0 ; « atelier » et « ateliers » ne sont pas regroupés ; les répétitions sont ignorées.
