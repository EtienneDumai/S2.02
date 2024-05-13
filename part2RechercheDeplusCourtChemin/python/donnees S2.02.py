import json
import pandas as pd
import numpy as np
import os
import sys
import random as r

os.chdir('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\part2RechercheDeplusCourtChemin\\donnees')

# import dicsucc.json et dicsuccdist.json (--> dictionnaire)
with open("dicsucc.json", "r") as fichier:
    dicsucc = json.load(fichier)
with open("dicsuccdist.json", "r") as fichier:
    dicsuccdist = json.load(fichier)

# import aretes.csv (--> dataframe) et transformation de lstpoints (chaîne-->liste)
aretes = pd.read_table('aretes.csv', sep  =';', index_col= 0)

for ind in aretes.index :
    ls = aretes.loc[ind,'lstpoints'].replace(" ","").replace("]", "").replace("[", "").split(',')
    lst = []
    for val in ls :
        lst.append(int(val))
    aretes.at[ind,'lstpoints'] = lst


# import sommets.csv, matrice_poids.csv (--> dataframe)
sommets = pd.read_table('sommets.csv', sep  =';', index_col= 0)
matrice_poids = pd.read_csv('matrice_poids.csv', sep = ';', index_col = 0)

# transformation dataframe matrice des poids en tableau    
tableau_poids = np.array(matrice_poids)

# transformation matrice des poids en liste de listes
liste_poids = [[None for j in range(len(tableau_poids))] for i in range(len(tableau_poids))]
for i in range(len(tableau_poids)):
    for j in range(len(tableau_poids)):
        liste_poids[i][j]  = tableau_poids[i,j]


del fichier, i, j, val, ls, lst, ind 

def transformer_graphe_en_dictionnaire(graphe):
    nouveau_graphe = {}
    for sommet_str, voisins in graphe.items():
        sommet_int = int(sommet_str)     
        nouveau_graphe[sommet_int] = {}  
        for voisin, poids in voisins:
            nouveau_graphe[sommet_int][voisin] = poids  
    return nouveau_graphe
dicsuccdistInt = transformer_graphe_en_dictionnaire(dicsuccdist)

def point_alea(graphe):
    keys = list(graphe.keys())
    nombre_alea = 0
    cle_alea1= 0
    cle_alea2 = 0
    while True:
        nombre_alea = r.randint(0,(len(graphe)-1))
        cle_alea1 = keys[nombre_alea]
        nombre_alea = r.randint(0, (len(graphe)-1))
        cle_alea2 = keys[nombre_alea]
        if cle_alea1 != cle_alea2:
            break
    return cle_alea1, cle_alea2

def dijkstra(depart, arrivee):
    depart = int(depart)
    arrivee = int(arrivee)

    # Initialisation des distances pour tous les nœuds mentionnés dans dicsucc et dicsuccdistInt
    distances = {noeud: float('inf') for noeud in set(dicsucc) | {voisin for values in dicsuccdistInt.values() for voisin in values}}
    distances[depart] = 0

    # Dictionnaire pour suivre le noeud précédent
    noeuds_precedents = {noeud: None for noeud in distances}

    # Liste des noeuds à visiter
    noeuds_a_visiter = [depart]

    while noeuds_a_visiter:
        # Sélection du noeud avec la distance minimale
        noeud_courant = min(noeuds_a_visiter, key=lambda noeud: distances[noeud])
        noeuds_a_visiter.remove(noeud_courant)

        # Arrêt si le noeud courant est l'arrivée
        if noeud_courant == arrivee:
            break

        # Exploration des voisins
        for voisin, distance in dicsuccdistInt.get(noeud_courant, {}).items():
            if voisin in distances:
                nouvelle_distance = distances[noeud_courant] + distance
                if nouvelle_distance < distances[voisin]:
                    distances[voisin] = nouvelle_distance
                    noeuds_precedents[voisin] = noeud_courant
                    if voisin not in noeuds_a_visiter:
                        noeuds_a_visiter.append(voisin)

    # Reconstruction du chemin le plus court
    chemin, noeud_courant = [], arrivee
    while noeud_courant is not None:
        chemin.insert(0, noeud_courant)
        noeud_courant = noeuds_precedents[noeud_courant]

    # Obtention de la distance minimale
    distance_minimale = distances[arrivee]
    return chemin, distance_minimale

# Exemple d'utilisation
point1Dij, point2Dij = point_alea()
print(f"Point 1 : ", point1Dij)
print(f"Point 2 : ", point2Dij)
chemin, distance = dijkstra(8947020815, 1804838595)
print("Chemin le plus court :", chemin)
print("Distance minimale :", distance)

def bellman_ford(depart, arrivee):
    depart = int(depart)
    arrivee = int(arrivee)

    # Initialisation des distances pour tous les nœuds mentionnés dans dicsuccdistInt
    distances = {noeud: float('inf') for noeud in set(dicsucc) | {voisin for values in dicsuccdistInt.values() for voisin in values}}
    distances[depart] = 0

    # Initialisation du dictionnaire pour suivre les noeuds précédents dans le chemin optimal
    noeuds_precedents = {noeud: None for noeud in distances}
    print(distances)
    # Relaxation des arêtes |V|-1 fois (V étant le nombre de nœuds dans le graphe)
    for _ in range(len(distances) - 1):
        for noeud in dicsuccdistInt:
            for voisin, poids in dicsuccdistInt[noeud].items():
                if distances[noeud] + poids < distances[voisin]:
                    distances[voisin] = distances[noeud] + poids
                    noeuds_precedents[voisin] = noeud

    # Vérification de l'existence de cycles de poids négatif
    for noeud in dicsuccdistInt:
        for voisin, poids in dicsuccdistInt[noeud].items():
            if distances[noeud] + poids < distances[voisin]:
                raise ValueError("Le graphe contient un cycle de poids négatif")

    # Reconstruction du chemin le plus court
    chemin, noeud_courant = [], arrivee
    while noeud_courant is not None:
        chemin.insert(0, noeud_courant)
        noeud_courant = noeuds_precedents[noeud_courant]

    # Obtention de la distance minimale pour atteindre 'arrivee'
    distance_minimale = distances[arrivee]
    return chemin, distance_minimale


keys = list(dicsuccdistInt.keys())
for i in keys:
    print(i)


        
        
        
# Exemple d'utilisation
point1Bell, point2Bell = point_alea(dicsuccdistInt)
print(f"Point 1 : ", point1Bell)
print(f"Point 2 : ", point2Bell)
chemin, distance = bellman_ford(point1Bell, point2Bell)
print("Chemin le plus court :", chemin)
print("Distance minimale :", distance)


def floyd_warshall(depart, arrivee):
    depart = int(depart)
    arrivee = int(arrivee)

    noeuds = set(dicsuccdistInt.keys()) | {voisin for subdict in dicsuccdistInt.values() for voisin in subdict}
    noeuds = list(noeuds)
    index_noeuds = {noeuds: idx for idx, noeuds in enumerate(noeuds)}

    n = len(noeuds)
    inf = float('inf')
    dist = [[inf] * n for _ in range(n)]
    
    for i in range(n):
        dist[i][i] = 0

    for u in dicsuccdistInt:
        for v, poids in dicsuccdistInt[u].items():
            i, j = index_noeuds[u], index_noeuds[v]
            dist[i][j] = poids

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    distance_minimale = dist[index_noeuds[depart]][index_noeuds[arrivee]]
    return distance_minimale if distance_minimale != inf else None

# Exemple d'utilisation
distance = floyd_warshall(8947020815, 1804838595)
print("Distance minimale de 8947020815 à 1804838595 :", distance)

# Exemple d'utilisation


depart, arrivee = point_alea()  # Suppose que point_alea retourne deux entiers valides
print("Départ:", depart, "Arrivée:", arrivee)

distance = floyd_warshall(depart, arrivee)
print("Distance minimale de", depart, "à", arrivee, ":", distance)

def creer_sous_graphe_critere(dicsuccdistInt, critere):
    # Filtrer les clés selon un critère
    keys_selected = [key for key, neighbors in dicsuccdistInt.items() if critere(neighbors)]
    
    # Construire le sous-graphe
    sous_graphe = {key: dicsuccdistInt[key] for key in keys_selected}
    return sous_graphe

# Exemple d'utilisation avec un critère spécifique
# Supposons que le critère soit d'avoir plus de 5 voisins
sous_graphe = creer_sous_graphe_critere(dicsuccdistInt, lambda neighbors: len(neighbors) > 3)
print(sous_graphe)
point1Floyd, point2Floyd = point_alea(sous_graphe)
print(f"Point 1 : ", point1Floyd)
print(f"Point 2 : ", point2Floyd)
distance = floyd_warshall(point1Floyd, point2Floyd)
print("Distance minimale :", distance)



def heuristique(no, arrivee):
    # Fonction heuristique, à adapter selon le contexte de votre application.
    # Exemple trivial qui retourne toujours 0.
    return 0

def a_etoile(depart, arrivee):
    depart = int(depart)
    arrivee = int(arrivee)

    # Initialisation des distances
    distances = {noeud: float('inf') for noeud in set(dicsuccdistInt.keys()) | {voisin for values in dicsuccdistInt.values() for voisin in values}}
    distances[depart] = 0

    # Dictionnaire pour suivre le noeud précédent
    noeuds_precedents = {noeud: None for noeud in distances}

    # Liste pour simuler la file de priorité
    noeuds_a_visiter = [(0, depart)]  # (estimation coût, noeud)

    while noeuds_a_visiter:
        # Sélection du noeud avec le coût estimé le plus bas sans utiliser heapq
        noeuds_a_visiter.sort(key=lambda x: x[0])  # Trier la liste à chaque itération pour obtenir le minimum
        current_distance, noeud_courant = noeuds_a_visiter.pop(0)  # Retirer l'élément avec le plus petit coût

        # Arrêt si le noeud courant est l'arrivée
        if noeud_courant == arrivee:
            break

        # Exploration des voisins
        for voisin, distance in dicsuccdistInt.get(noeud_courant, {}).items():
            nouvelle_distance = distances[noeud_courant] + distance
            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                noeuds_precedents[voisin] = noeud_courant
                estimation_cout = nouvelle_distance + heuristique(voisin, arrivee)
                # Ajouter ou mettre à jour le voisin dans la liste
                for idx, (cost, node) in enumerate(noeuds_a_visiter):
                    if node == voisin:
                        if cost > estimation_cout:
                            noeuds_a_visiter.pop(idx)
                            noeuds_a_visiter.append((estimation_cout, voisin))
                        break
                else:
                    noeuds_a_visiter.append((estimation_cout, voisin))

    # Reconstruction du chemin le plus court
    chemin, noeud_courant = [], arrivee
    while noeud_courant is not None:
        chemin.insert(0, noeud_courant)
        noeud_courant = noeuds_precedents[noeud_courant]

    # Obtention de la distance minimale
    distance_minimale = distances[arrivee]
    return chemin, distance_minimale

# Exemple d'utilisation
chemin, distance = a_etoile(8947020815, 1804838595)
print("Chemin le plus court :", chemin)
print("Distance minimale :", distance)
