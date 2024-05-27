#Initialisation des variables et des fonctions n√©cessaires au bon fonctionnement des algos
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

# import aretes.csv (--> dataframe) et transformation de lstpoints (cha√Æne-->liste)
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

#Definition des focntions utiles aux algorithmes
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

def indice(nom_sommet):
    return ord(nom_sommet) - ord('A')

def nom_sommet(indice_sommet):
    return chr(ord('A') + indice_sommet)

def reconstruire_chemin(sommet_depart, sommet_arrivee, pred):
    chemin = []
    sommet = sommet_arrivee
    while sommet != sommet_depart:
        chemin.insert(0, sommet)
        sommet = pred[sommet]
    chemin.insert(0, sommet_depart)
    return chemin


def extraire_min(distances, a_traiter):
    sommet_min = a_traiter[0]
    for sommet in a_traiter:
        if distances[sommet] < distances[sommet_min]:
            sommet_min = sommet
    return sommet_min

def relacher(pnt1, pnt2, distances, predecesseurs, poids):
    if distances[pnt1] > distances[pnt2] + poids[(pnt2, pnt1)]:
        distances[pnt1] = distances[pnt2] + poids[(pnt2, pnt1)]
        predecesseurs[pnt1] = pnt2


#Debut des algos



def dijkstra(graphe, sommet_depart, sommet_arrivee):
    # Initialisation des variables ecessaire au programme
    distances = {sommet: float('inf') for sommet in graphe}
    distances[sommet_depart] = 0
    pred = {}
    sommet_non_traites = set(graphe.keys())

    while sommet_non_traites:
        # Selectionner le sommet non traite avec la plus petite distance
        sommet_courant = min(sommet_non_traites, key=lambda sommet: distances[sommet])
        sommet_non_traites.remove(sommet_courant)

        if sommet_courant == sommet_arrivee:
            break  # On a trouv√© le chemin le plus court

        for voisin, poids in graphe[sommet_courant].items():  # Utiliser .items() pour iterer sur les voisins
            # Calculer la nouvelle distance
            nouvelle_distance = distances[sommet_courant] + poids

            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                pred[voisin] = sommet_courant
    chemin = reconstruire_chemin(sommet_depart, sommet_arrivee, pred)
    distance_totale = distances[sommet_arrivee]
    return chemin, round(distance_totale)


# Exemple d'utilisation
point1Dij, point2Dij = point_alea(dicsuccdistInt)
print(f"Point 1 : ", point1Dij)
print(f"Point 2 : ", point2Dij)
chemin, distance = dijkstra(dicsuccdistInt, point1Dij, point2Dij)
print("Chemin : ", chemin)
print("Distance : ", distance)
del point1Dij, point2Dij, chemin, distance


def bellman_ford(graphe, sommet_depart):
 # Initialisation
 distances = {sommet: float('inf') for sommet in graphe}
 distances[sommet_depart] = 0
 pred = {sommet: None for sommet in graphe}

 # Rel√¢cher chaque arete (V-1) fois
 for _ in range(len(graphe) - 1):
     for sommet in graphe:
         for voisin, poids in graphe[sommet].items():
             if distances[sommet] + poids < distances[voisin]:
                 distances[voisin] = distances[sommet] + poids
                 pred[voisin] = sommet

 # V√©rification de cycles de poids negatif
 for sommet in graphe:
     for voisin, poids in graphe[sommet].items():
         if distances[sommet] + poids < distances[voisin]:
             raise ValueError("Le graphe contient un cycle de poids n√©gatif")

 return distances, pred



        

        
# Exemple d'utilisation
point1Bell, point2Bell = point_alea(dicsuccdistInt)
print(f"Point 1 : ", point1Bell)
print(f"Point 2 : ", point2Bell)
distances, pred = bellman_ford(dicsuccdistInt, point1Bell)
chemin = reconstruire_chemin( point1Bell, point2Bell, pred)
print("Distances:", distances)
print("Chemin du point 1 au point 2 :", chemin)
del point1Bell, point2Bell, distances, chemin


#Floyd Warshall a faire 


import time


def floyd_warshall(matricePonderee):
    taille = len(matricePonderee)
    
    # Remplissage de M0 et P0
    M = np.array(matricePonderee)
    P = np.full((taille, taille), -1, dtype=int)
    
    for i in range(taille):
        for j in range(taille):
            if M[i][j] != 0 and i != j:
                P[i][j] = i
            else:
                P[i][j] = -1  
    debutTemps = time.time()
    
    # Début des itérations sur les lignes et les colonnes
    for k in range(taille):       
        for i in range(taille):
            for j in range(taille):
                
                if M[i][k] + M[k][j] < M[i][j]:
                    M[i][j] = M[i][k] + M[k][j]
                    P[i][j] = P[k][j]
        temps = time.time()
        
        print ("étape numéro : ", k, " terminée en : ", round(temps) - round(debutTemps), "secondes")
    
    return M, P
matrice, poids = floyd_warshall(matrice_poids)
print(matrice)
print(poids)
