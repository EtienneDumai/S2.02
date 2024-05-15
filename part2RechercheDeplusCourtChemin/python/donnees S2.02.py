import json
import pandas as pd
import numpy as np
import os
import sys
import random as r
import sys
sys.path.append('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\part3Visualisation\\python')
from graphics import *

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


def indice(nom_sommet):
    return ord(nom_sommet) - ord('A')

def nom_sommet(indice_sommet):
    return chr(ord('A') + indice_sommet)

def reconstituer(chemin_pred, depart, arrivee):
    chemin = []
    actuel = indice(arrivee)
    while actuel != indice(depart):
        chemin.append(nom_sommet(actuel))
        actuel = chemin_pred[actuel]
    chemin.append(nom_sommet(indice(depart)))
    return chemin[::-1]

def dijkstra(graphe, sommet_depart, sommet_arrivee):
    # Initialisation des variables nécessaires à l'exécution du programme
    distances = {sommet: float('inf') for sommet in graphe}
    distances[sommet_depart] = 0
    pred = {}
    sommet_non_traites = set(graphe.keys())

    while sommet_non_traites:
        # Sélectionner le sommet non traité avec la plus petite distance
        sommet_courant = min(sommet_non_traites, key=lambda sommet: distances[sommet])
        sommet_non_traites.remove(sommet_courant)

        if sommet_courant == sommet_arrivee:
            break  # On a trouvé le chemin le plus court

        for voisin, poids in graphe[sommet_courant].items():  # Utiliser .items() pour itérer sur les voisins
            # Calculer la nouvelle distance
            nouvelle_distance = distances[sommet_courant] + poids

            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                pred[voisin] = sommet_courant
            
    return reconstruire_chemin(sommet_depart, sommet_arrivee, pred)


# Exemple d'utilisation
point1Dij, point2Dij = point_alea(dicsuccdistInt)
print(f"Point 1 : ", point1Dij)
print(f"Point 2 : ", point2Dij)
chemin = dijkstra(dicsuccdistInt, point1Dij, point2Dij)
print("Chemin : ", chemin)
del point1Dij, point2Dij, chemin

def bellman(graphe, sommet_depart, sommet_arrivee):
    #initialisation des variables pour l'exécution de l'algorithme
    depart = int(sommet_depart)
    arrivee = int(sommet_arrivee)
    distances = {sommet: float('inf') for sommet in graphe}
    distances[sommet_depart] = 0
    pred = {}
    n=len(graphe)
    #Debut de l'algorithme
    for sommetCle in graphe.keys():
        for voisin in graphe[sommetCle]:
            relacher(sommetCle, voisin, distances, pred, poids)
    return 0



        

        
# Exemple d'utilisation
point1Bell, point2Bell = point_alea(dicsuccdistInt)
print(f"Point 1 : ", point1Bell)
print(f"Point 2 : ", point2Bell)
chemin, distance = bellman_ford(point1Bell, point2Bell)
print("Chemin le plus court :", chemin)
print("Distance minimale :", distance)


def floyd_warshall(depart, arrivee):

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





def a_etoile(depart, arrivee):
    

# Exemple d'utilisation
chemin, distance = a_etoile(8947020815, 1804838595)
print("Chemin le plus court :", chemin)
print("Distance minimale :", distance)




