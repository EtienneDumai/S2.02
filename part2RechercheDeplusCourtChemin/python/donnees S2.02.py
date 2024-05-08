import json
import pandas as pd
import numpy as np
import os
import sys


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
chemin, distance = dijkstra(1806175538, 1801848709)
print("Chemin le plus court :", chemin)
print("Distance minimale :", distance)