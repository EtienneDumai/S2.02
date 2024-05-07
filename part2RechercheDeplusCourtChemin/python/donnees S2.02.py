import json
import pandas as pd
import numpy as np
import os


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

def charger_graphes():
    with open("dicsucc.json", "r") as fichier:
        successeurs = json.load(fichier)
    with open("dicsuccdist.json", "r") as fichier:
        distances = json.load(fichier)
    return successeurs, distances

def transformer_distances(distances):
    transforme = {}
    for noeud, aretes in distances.items():
        transforme[str(noeud)] = {str(arete[0]): arete[1] for arete in aretes}
    return transforme

def dijkstra(depart, arrivee):
    successeurs, distances_brutes = charger_graphes()
    distances = transformer_distances(distances_brutes)

    depart, arrivee = str(depart), str(arrivee)
    distances_minimales = {str(noeud): float('inf') for noeud in successeurs}
    predecesseur = {str(noeud): None for noeud in successeurs}
    distances_minimales[depart] = 0

    non_visites = set(successeurs.keys())

    while non_visites:
        noeud_courant = min(non_visites, key=lambda noeud: distances_minimales[noeud])
        if distances_minimales[noeud_courant] == float('inf'):
            break

        for voisin in successeurs[noeud_courant]:
            if str(voisin) in distances[noeud_courant]:
                distance = distances_minimales[noeud_courant] + distances[noeud_courant][str(voisin)]
                if distance < distances_minimales[voisin]:
                    distances_minimales[voisin] = distance
                    predecesseur[voisin] = noeud_courant

        non_visites.remove(noeud_courant)

    chemin = []
    etape = arrivee
    while etape is not None:
        chemin.append(etape)
        etape = predecesseur[etape]
    chemin.reverse()

    return chemin, distances_minimales[arrivee]
chemin, distance = dijkstra(8947020815, 179717708)
print(chemin)
print(distance)