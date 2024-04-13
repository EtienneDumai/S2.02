import os
import pandas as pd
import numpy as np
import math 
os.chdir('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\donnees')
arcs=pd.read_table('arcs.csv', sep=';', encoding="ANSI")
points = pd.read_table('points.csv', sep=';', index_col=0, encoding="ANSI")

listeDesArcs={}


for i in range(arcs.shape[0]):
    sommets = arcs['lstpoints'].iloc[i].split()
    listeDesArcs[i] = sommets
    
for i in range(arcs.shape[0]):
    sommets = arcs['lstpoints'].iloc[i]
    sommets_clean = sommets.replace('[', '').replace(']', '').replace(',', '')
    listeDesArcs[i] = sommets_clean

print(listeDesArcs)


for k, val in listeDesArcs.items():
    sommets = val.split()
    sommets_clean = [int(sommet) for sommet in sommets]
    listeDesArcs[k] = sommets_clean
    

for cle, val in listeDesArcs.items():
    if len(val) > 2:
        listeDesArcs[cle] = [val[0], val[-1]]


listSom=[]

for val in listeDesArcs.values():
    for sommet in val:
        if sommet not in listSom:
            listSom.append(sommet)


dic_graph={}
for liste in listeDesArcs.values():
    if liste[0] not in dic_graph.keys():
        dic_graph[liste[0]]=[liste[1]]
    else:
        dic_graph[liste[0]].append(liste[1])
        
    if liste[1] not in dic_graph.keys():
        dic_graph[liste[1]]=[liste[0]]
    else:
        dic_graph[liste[1]].append(liste[0])



sommets = sorted(dic_graph.keys())  # Recuperer et trier tout les sommets récupérés
n = len(sommets)
matrice_adja = [[0] * n for i in range(n)]  # Créer une matrice remplie de zéros de taille n x n

  
for i, sommet1 in enumerate(sorted(dic_graph.keys())):
    for j, sommet2 in enumerate(sorted(dic_graph.keys())):
        if sommet2 in dic_graph[sommet1]:  # Vérifier s'il y a un lien entre les sommet1 et sommet2
            matrice_adja[i][j] = 1  # S'il y a un lien, mettre 1 dans la matrice

def distanceGPS(latA,latB,longA,longB):
    
# Conversions des latitudes en radians
    ltA=latA/180*math.pi
    ltB=latB/180*math.pi
    loA=longA/180*math.pi
    loB=longB/180*math.pi
    # Rayon de la terre en mètres 
    RT = 6378137
    # angle en radians entre les 2 points
    S = math.acos(round(math.sin(ltA)*math.sin(ltB) + math.cos(ltA)*math.cos(ltB)*math.cos(abs(loB-loA)),14))
    # distance entre les 2 points, comptée sur un arc de grand cercle
    return S*RT
matrice_longueurs_arcs = []
for arc in listeDesArcs:
    (latA, longA), (latB, longB) = arc
    longueur_arc = distanceGPS(latA, latB, longA, longB)
    matrice_longueurs_arcs.append(longueur_arc)