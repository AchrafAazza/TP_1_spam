# TP_1_Solution.py
# Version script du notebook TP_1_Solution.ipynb : mêmes réponses, mêmes calculs.
# Exécution : python TP_1_Solution.py (le fichier corpus_ensembles_fr.csv est lu à côté du script).
# Dans VS Code, chaque bloc « # %% » peut aussi s'exécuter comme une cellule (Run Cell).

# %% [markdown]
# # Solution · Comparer des ensembles de termes avec Jaccard et Dice
#
# | Élément | Détail |
# |---|---|
# | **Données** | `corpus_ensembles_fr.csv` : une requête **Q** et huit documents **D1 à D8** |
# | **Langage** | Python 3, bibliothèque standard uniquement (`csv`, `io`, `re`, `pathlib`, `unicodedata`) |
# | **Exécution** | *Run All* (« Exécuter tout ») : toutes les cellules s'exécutent sans erreur |
#
# **Contenu du dossier `TP_1_Solution`**
#
# | Fichier | Rôle |
# |---|---|
# | `TP_1_Solution.ipynb` | ce notebook : toutes les réponses (tableaux, explications, code et résultats) |
# | `TP_1_Solution.py` | les mêmes réponses sous forme de script Python : `python TP_1_Solution.py` |
# | `TP_1_Resultats.md` | les résultats de la solution, en bref : ensembles, scores, classement, comparaison |
# | `corpus_ensembles_fr.csv` | les données du TP |
#
# **Sommaire**
#
# | Partie | Questions | Forme des réponses |
# |---|---|---|
# | 1. Comprendre le calcul | formules et exemple | formules, tableaux |
# | 2. Travailler à la main | 2.1, 2.2, 2.3 | tableaux, explications |
# | 3. Classer les huit documents | 3.1, 3.2, 3.3, 3.4 | code Python, résultats, tableaux |
# | Synthèse | toutes | tableau récapitulatif |


# %% [markdown]
# ## Partie 1 · Comprendre le calcul
#
# Pour deux ensembles $A$ et $B$, on note $k = |A \cap B|$ le nombre de termes communs.
#
# $$J(A,B) = \frac{k}{|A| + |B| - k} \qquad\qquad D(A,B) = \frac{2k}{|A| + |B|}$$
#
# - **Jaccard** divise $k$ par le nombre de termes distincts présents dans au moins un des deux ensembles, c'est-à-dire $|A \cup B| = |A| + |B| - k$.
# - **Dice** divise deux fois $k$ par la somme des tailles des deux ensembles.
#
# **Exemple de l'énoncé**
#
# | Texte | Ensemble | Taille |
# |---|---|:---:|
# | « bus bus tram gare » | { bus, tram, gare } | 3 |
# | « tram gare parking » | { tram, gare, parking } | 3 |
#
# Termes communs : tram et gare, donc $k = 2$ et $|A \cup B| = 3 + 3 - 2 = 4$.
# On obtient $J = 2/4 = 0{,}5$ et $D = 4/6 \approx 0{,}667$. Répéter « bus » ne change pas l'ensemble.
#
# **Cas particuliers (conventions du TP)**
#
# | Situation | Jaccard | Dice |
# |---|:---:|:---:|
# | Un seul des deux ensembles est vide | 0 | 0 |
# | Les deux ensembles sont vides | 1 | 1 |
# | La requête est vide après filtrage | signalée, non classée | signalée, non classée |


# %% [markdown]
# ## Partie 2 · Travailler à la main
#
# **Prétraitement appliqué à Q, D1 et D3**
#
# | Étape | Règle |
# |:---:|---|
# | 1 | Mettre le texte en minuscules |
# | 2 | Extraire les suites de lettres, accents compris ; un tiret ou une apostrophe coupe un mot |
# | 3 | Retirer exactement ces mots : *a au aux à ce ces d dans de des du en et l la le les leur leurs ne ou par pour que qui s se sur un une* |
# | 4 | Garder le pluriel et les accents tels quels |
# | 5 | Dédoublonner les termes |
#
# **Détail du prétraitement**
#
# | Texte | Mots extraits | Mots vides retirés | Mots restants | Doublons retirés | Termes distincts |
# |:---:|:---:|---|:---:|:---:|:---:|
# | **Q** | 25 | 12 (la, des, de, dans, les, des, aux, à, leur, et, à, les) | 13 | 1 (« vélo » ×2) | **12** |
# | **D1** | 24 | 10 (dans, les, du, la, des, de, des, les, à, leur) | 14 | 1 (« vélo » ×2) | **13** |
# | **D3** | 19 | 6 (les, des, et, des, aux, du) | 13 | 3 (« vélo » ×4) | **10** |


# %% [markdown]
# ### Question 2.1
#
# > Donnez les ensembles de Q, D1 et D3. Identifiez les intersections avec Q.
#
# **Ensembles de termes** (dans l'ordre d'apparition dans le texte)
#
# | Texte | Ensemble de termes | Taille |
# |:---:|---|:---:|
# | **Q** | mairie, lance, ateliers, réparation, vélo, écoles, bénévoles, apprennent, élèves, entretenir, réduire, déchets | 12 |
# | **D1** | écoles, quartier, mairie, organise, ateliers, réparation, vélo, bénévoles, aident, élèves, entretenir, chaque, mercredi | 13 |
# | **D3** | réparation, vélo, ateliers, proposent, pièces, outils, cyclistes, quartier, chaque, samedi | 10 |
#
# **Intersections avec Q**
#
# | Intersection | Termes communs | k | Termes de Q absents du document |
# |:---:|---|:---:|---|
# | **Q ∩ D1** | mairie, ateliers, réparation, vélo, écoles, bénévoles, élèves, entretenir | **8** | lance, apprennent, réduire, déchets |
# | **Q ∩ D3** | ateliers, réparation, vélo | **3** | mairie, lance, écoles, bénévoles, apprennent, élèves, entretenir, réduire, déchets |


# %% [markdown]
# ### Question 2.2
#
# > Calculez J et D pour les deux paires et interprétez les résultats.
#
# | Paire | Taille de Q | Taille de B | k | Taille de l'union | Jaccard J | Dice D |
# |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
# | **Q – D1** | 12 | 13 | 8 | 12 + 13 − 8 = 17 | 8 / 17 ≈ **0,471** | 16 / 25 = **0,640** |
# | **Q – D3** | 12 | 10 | 3 | 12 + 10 − 3 = 19 | 3 / 19 ≈ **0,158** | 6 / 22 ≈ **0,273** |
#
# **Interprétation**
# - **D1 est beaucoup plus proche de Q que D3** : J = 0,471 contre 0,158, et D = 0,640 contre 0,273. D1 traite le même sujet que Q (des ateliers de réparation vélo organisés par la mairie dans les écoles, avec des bénévoles et des élèves) : 8 des 12 termes de Q s'y retrouvent.
# - **D3 ne partage que 3 termes** avec Q (ateliers, réparation, vélo). Ses 7 autres termes (proposent, pièces, outils, cyclistes, quartier, chaque, samedi) n'apparaissent pas dans Q, d'où un score faible.
# - **Dice donne des valeurs plus élevées que Jaccard** (sauf en 0 et en 1), mais les deux mesures classent D1 devant D3.


# %% [markdown]
# ### Question 2.3
#
# > Dans D3, que deviennent les occurrences répétées de « vélo » ? Quel effet cela a-t-il sur le score ?
#
# |   | Texte de D3 | Ensemble de D3 |
# |---|:---:|:---:|
# | « vélo » | 4 occurrences | 1 seul élément |
#
# - **Ce qu'elles deviennent :** les 4 occurrences sont fusionnées en **un seul terme** lors du dédoublonnage, car un ensemble ne contient chaque élément qu'une fois.
# - **Effet sur le score : aucun.** Avec une seule occurrence de « vélo », on obtient exactement les mêmes valeurs : k = 3, |D3| = 10, J = 3/19 ≈ 0,158 et D = 6/22 ≈ 0,273.
# - **Conséquence :** Jaccard et Dice ignorent la fréquence des mots. Répéter un mot-clé ne rapproche pas un document de la requête, contrairement à une pondération TF ou TF-IDF.


# %% [markdown]
# ## Partie 3 · Classer les huit documents
#
# ### Question 3.1
#
# > Chargez le CSV avec `csv.DictReader`. La colonne `role` distingue la requête des documents.
#
# - Le fichier `corpus_ensembles_fr.csv` est lu avec `csv.DictReader` depuis le dossier du notebook.
# - Les lignes dont `role` vaut `requete` forment la requête ; celles dont `role` vaut `document` forment les documents.
# - Si le fichier est introuvable (notebook déposé seul), une copie intégrée du même corpus est utilisée : le notebook s'exécute donc toujours sans erreur.


# %%
import csv
import io
import re
import unicodedata
from pathlib import Path

# Dossier du script .py, ou dossier courant pour le notebook
DOSSIER = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
FICHIER = DOSSIER / "corpus_ensembles_fr.csv"

# Copie intégrée du corpus, utilisée seulement si le fichier CSV est introuvable
CORPUS = """id,role,texte
Q,requete,La mairie lance des ateliers de réparation vélo dans les écoles. Des bénévoles apprennent aux élèves à entretenir leur vélo et à réduire les déchets.
D1,document,"Dans les écoles du quartier, la mairie organise des ateliers de réparation vélo. Des bénévoles aident les élèves à entretenir leur vélo chaque mercredi."
D2,document,La mairie ouvre des ateliers de couture dans les écoles. Des bénévoles montrent aux élèves comment réparer les vêtements et réduire les déchets du quartier.
D3,document,"Réparation vélo : vélo, vélo, vélo. Les ateliers proposent des pièces et des outils aux cyclistes du quartier chaque samedi."
D4,document,La municipalité propose des séances de remise en état des bicyclettes. Des volontaires montrent aux enfants comment prolonger la durée de vie de leur bicyclette.
D5,document,Les clubs de randonnée organisent une sortie en montagne. Pensez à réserver votre place et à apporter un repas pour le groupe.
D6,document,"La mairie annonce une campagne pour réduire les déchets. Dans les écoles, les élèves apprennent à trier le papier. Des bénévoles distribuent des affiches."
D7,document,Les ateliers de réparation vélo reprennent dans les écoles. La mairie mobilise les bénévoles pour aider les élèves à réduire les déchets et entretenir leur vélo.
D8,document,La mairie invite les élèves à un atelier de réparation de vélos. Les bénévoles expliquent comment entretenir les freins et réparer les pneus du vélo."""

if FICHIER.exists():
    with open(FICHIER, encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.DictReader(f))
    source = f"fichier {FICHIER.name}"
else:
    lignes = list(csv.DictReader(io.StringIO(CORPUS)))
    source = "copie intégrée du corpus"

requete = [ligne for ligne in lignes if ligne["role"] == "requete"]
documents = [ligne for ligne in lignes if ligne["role"] == "document"]

print(f"Source : {source}")
print(f"{len(requete)} requête, {len(documents)} documents\n")
print(f"{'id':<4}{'role':<10}texte")
for ligne in lignes:
    texte = ligne["texte"]
    apercu = texte if len(texte) <= 70 else texte[:67] + "..."
    print(f"{ligne['id']:<4}{ligne['role']:<10}{apercu}")


# %% [markdown]
# ### Question 3.2
#
# > Écrivez `termes(texte)`, `jaccard(a, b)` et `dice(a, b)`.
#
# | Fonction | Rôle | Renvoie |
# |---|---|---|
# | `termes(texte)` | met en minuscules, extrait les suites de lettres avec `[^\W\d_]+`, retire les mots vides | un ensemble (`set`) |
# | `jaccard(a, b)` | k divisé par la taille de l'union ; 1 si les deux ensembles sont vides | un réel entre 0 et 1 |
# | `dice(a, b)` | 2k divisé par la somme des tailles ; 1 si les deux ensembles sont vides | un réel entre 0 et 1 |
#
# L'expression `[^\W\d_]+` ne garde que des **lettres**, accents compris : tirets, apostrophes, chiffres et ponctuation servent de séparateurs. Les tests ci-dessous reprennent l'exemple et les conventions de l'énoncé.


# %%
MOTS_VIDES = set("""a au aux à ce ces d dans de des du en et l la le les leur leurs
ne ou par pour que qui s se sur un une""".split())


def termes(texte):
    """Ensemble des termes du texte : minuscules, lettres seulement, sans mots vides."""
    mots = re.findall(r"[^\W\d_]+", texte.lower())
    return {m for m in mots if m not in MOTS_VIDES}


def jaccard(a, b):
    """Indice de Jaccard : k / |A ∪ B| (vaut 1 si les deux ensembles sont vides)."""
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def dice(a, b):
    """Coefficient de Dice : 2k / (|A| + |B|) (vaut 1 si les deux ensembles sont vides)."""
    if not a and not b:
        return 1.0
    return 2 * len(a & b) / (len(a) + len(b))


# Tests : exemple et conventions de l'énoncé
assert len(MOTS_VIDES) == 30
A, B = termes("bus bus tram gare"), termes("tram gare parking")
assert A == {"bus", "tram", "gare"} and B == {"tram", "gare", "parking"}
assert jaccard(A, B) == 0.5 and round(dice(A, B), 3) == 0.667
assert jaccard(set(), A) == 0 and dice(set(), A) == 0
assert jaccard(set(), set()) == 1 and dice(set(), set()) == 1
assert termes("L'après-midi") == termes("L’après-midi") == {"après", "midi"}  # « l » est un mot vide

print("Tous les tests passent.")
print(f"Exemple de l'énoncé : J = {jaccard(A, B):.3f}   D = {dice(A, B):.3f}")


# %% [markdown]
# ### Question 3.3
#
# > Pour chaque document, affichez |B|, k, |A ∪ B|, J et D. Triez par score décroissant, puis par identifiant croissant en cas d'égalité. Triez sur les scores complets et arrondissez uniquement à l'affichage.
#
# - $A$ est l'ensemble de la requête Q et $B$ celui du document ; dans l'affichage, `|AUB|` désigne $|A \cup B|$.
# - Le tri utilise la clé `(-score, identifiant)` sur les valeurs exactes ; l'arrondi à 3 décimales n'intervient que dans `print`.
# - Une requête vide après filtrage est signalée au lieu d'être classée.


# %%
def classer(Q, docs, score):
    """Identifiants triés par score décroissant, puis par identifiant croissant."""
    return sorted(docs, key=lambda d: (-score(Q, docs[d]), d))


def afficher(nom, ordre, Q, docs):
    """Affiche |B|, k, |A ∪ B|, J et D (arrondis à 3 décimales) dans l'ordre donné."""
    print(f"Classement par {nom}   (|Q| = {len(Q)})")
    print(f"{'Rang':<6}{'Doc':<5}{'|B|':>5}{'k':>4}{'|AUB|':>7}{'J':>8}{'D':>8}")
    for rang, d in enumerate(ordre, start=1):
        B = docs[d]
        print(f"{rang:<6}{d:<5}{len(B):>5}{len(Q & B):>4}{len(Q | B):>7}"
              f"{jaccard(Q, B):>8.3f}{dice(Q, B):>8.3f}")
    print()


Q = termes(requete[0]["texte"]) if requete else set()
docs = {ligne["id"]: termes(ligne["texte"]) for ligne in documents}

if not Q:
    ordre_j = ordre_d = []
    print("Requête vide après filtrage : elle est signalée et n'est pas classée.")
else:
    ordre_j = classer(Q, docs, jaccard)
    ordre_d = classer(Q, docs, dice)
    afficher("Jaccard", ordre_j, Q, docs)
    afficher("Dice", ordre_d, Q, docs)


# %% [markdown]
# **Vérification de la partie 2 par le code** : on retrouve les ensembles, les intersections et les scores calculés à la main, ainsi que la réponse à la question 2.3.


# %%
def tri_fr(mots):
    """Tri alphabétique qui ignore les accents (« é » est rangé avec « e »)."""
    return sorted(mots, key=lambda m: (unicodedata.normalize("NFD", m).encode("ascii", "ignore"), m))


print(f"Q ({len(Q)} termes) : {tri_fr(Q)}\n")

for nom in ("D1", "D3"):
    B = docs[nom]
    print(f"{nom} ({len(B)} termes) : {tri_fr(B)}")
    print(f"   termes communs avec Q : {tri_fr(Q & B)}")
    print(f"   k = {len(Q & B)}, |AUB| = {len(Q | B)}, "
          f"J = {jaccard(Q, B):.3f}, D = {dice(Q, B):.3f}\n")

# Question 2.3 : les occurrences répétées de « vélo » dans D3
texte_d3 = next(ligne["texte"] for ligne in documents if ligne["id"] == "D3")
nb_texte = re.findall(r"[^\W\d_]+", texte_d3.lower()).count("vélo")
nb_ensemble = sum(1 for t in docs["D3"] if t == "vélo")
print(f"« vélo » : {nb_texte} occurrences dans le texte de D3, {nb_ensemble} seul élément dans l'ensemble")

texte_un_velo = texte_d3.replace("vélo : vélo, vélo, vélo.", "vélo.")
d3_un_velo = termes(texte_un_velo)
nb_un = re.findall(r"[^\W\d_]+", texte_un_velo.lower()).count("vélo")
print(f"Avec {nb_un} seule occurrence : même ensemble = {d3_un_velo == docs['D3']}, "
      f"J = {jaccard(Q, d3_un_velo):.3f}, D = {dice(Q, d3_un_velo):.3f}")


# %% [markdown]
# ### Question 3.4
#
# > Comparez les deux classements.
#
# | Rang | Classement Jaccard | J | Classement Dice | D |
# |:---:|:---:|:---:|:---:|:---:|
# | 1 | D7 | 0,667 | D7 | 0,800 |
# | 2 | D1 | 0,471 | D1 | 0,640 |
# | 3 | D6 | 0,389 | D6 | 0,560 |
# | 4 | D2 | 0,368 | D2 | 0,538 |
# | 5 | D8 | 0,300 | D8 | 0,462 |
# | 6 | D3 | 0,158 | D3 | 0,273 |
# | 7 | D4 | 0,000 | D4 | 0,000 |
# | 8 | D5 | 0,000 | D5 | 0,000 |
#
# **Constat : les deux classements sont identiques**, avec les mêmes égalités : D4 et D5 ont un score nul pour les deux mesures et sont départagés par identifiant croissant dans les deux cas.
#
# **Explication.** Notons $u = |A \cup B|$. Comme $|A| + |B| = u + k$ :
#
# $$D = \frac{2k}{u + k} = \frac{2\,k/u}{1 + k/u} = \frac{2J}{1 + J}$$
#
# La fonction $J \mapsto \frac{2J}{1 + J}$ est **strictement croissante** sur $[0, 1]$ (sa dérivée vaut $\frac{2}{(1 + J)^2} > 0$). Dice change donc l'échelle des scores ($D \ge J$, avec égalité seulement pour $J = 0$ ou $J = 1$), mais **jamais l'ordre** des documents ni les égalités. La cellule suivante le vérifie sur les huit documents.


# %%
print("Les deux classements sont identiques :", ordre_j == ordre_d)
egalite = all(abs(dice(Q, B) - 2 * jaccard(Q, B) / (1 + jaccard(Q, B))) < 1e-12 for B in docs.values())
print("D = 2J/(1+J) pour les huit documents :", egalite, "\n")

print(f"{'Doc':<5}{'J':>8}{'D':>8}{'2J/(1+J)':>11}")
for d in ordre_j:
    J, D = jaccard(Q, docs[d]), dice(Q, docs[d])
    print(f"{d:<5}{J:>8.3f}{D:>8.3f}{2 * J / (1 + J):>11.3f}")


# %% [markdown]
# **Analyse du classement**
#
# | Observation | Documents | Explication |
# |---|:---:|---|
# | Document le plus proche | D7 (k = 10) | presque une reformulation de Q : 10 des 12 termes de Q s'y retrouvent |
# | Termes de contexte favorisés | D6 et D2 devant D8 et D3 | D6 (campagne contre les déchets) et D2 (ateliers de couture) ne parlent pas de vélo, mais partagent chacun 7 termes avec Q, surtout des termes de contexte : mairie, écoles, bénévoles, élèves, réduire, déchets |
# | Variantes morphologiques non regroupées | D8 | « atelier » ≠ « ateliers » et « vélos » ≠ « vélo » : D8 perd un terme commun et compte un terme de plus ; une racinisation ou une lemmatisation corrigerait cela |
# | Synonymes ignorés | D4 (score 0) | même sujet que Q (remise en état de bicyclettes par des volontaires) mais avec d'autres mots : municipalité, bicyclettes, volontaires, enfants |
# | Document hors sujet | D5 (score 0) | sortie en montagne : aucun terme commun, le score nul est justifié |
# | Fréquence ignorée | D3 | « vélo » répété 4 fois ne compte qu'une fois |
#
# **Conclusion :** Jaccard et Dice mesurent un recouvrement **lexical** exact. Ces mesures sont simples et résistent au bourrage de mots-clés, mais elles ne voient ni les synonymes, ni les variantes d'un même mot, ni l'importance relative des termes.


# %% [markdown]
# ## Synthèse des réponses
#
# | Question | Réponse courte |
# |:---:|---|
# | 2.1 | Q : 12 termes, D1 : 13 termes, D3 : 10 termes. Q ∩ D1 : 8 termes ; Q ∩ D3 : 3 termes (ateliers, réparation, vélo) |
# | 2.2 | Q – D1 : J = 8/17 ≈ 0,471 et D = 16/25 = 0,640. Q – D3 : J = 3/19 ≈ 0,158 et D = 6/22 ≈ 0,273. D1 est bien plus proche de Q |
# | 2.3 | Les 4 « vélo » de D3 deviennent un seul terme : aucun effet sur les scores |
# | 3.1 | Lecture du CSV avec `csv.DictReader` ; la colonne `role` sépare la requête des documents |
# | 3.2 | Fonctions `termes`, `jaccard` et `dice`, validées sur l'exemple et les conventions de l'énoncé |
# | 3.3 | Classement (Jaccard comme Dice) : D7 > D1 > D6 > D2 > D8 > D3 > D4 = D5 (égalité départagée par identifiant) |
# | 3.4 | Classements identiques, car D = 2J / (1 + J) est strictement croissante en J |
