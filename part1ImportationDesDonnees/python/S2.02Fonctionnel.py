import os
import pandas as pd
import numpy as np
import math 
""" Importation des fichiers"""
os.chdir('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\part1ImportationDesDonnees\\donnees')
arcs=pd.read_table('arcs.csv', sep=';', encoding="ANSI")
points = pd.read_table('points.csv', sep=';',  encoding="ANSI")
"""
Faire un dictionnaire avec toutes les infos possible pour les points
"""
def extract_points(lstpoints_str):
    sommet = lstpoints_str.strip("[]").split(", ")
    # Retourner le premier et le dernier point si la liste contient plus d'un point
    return [sommet[0], sommet[-1]] if len(sommet) > 1 else sommet

arcs['endpoints'] = arcs['lstpoints'].apply(extract_points)

# Initialiser un ensemble pour stocker les identifiants de points uniques (début et fin)
endpoints = set()

# Ajouter les points de début et de fin de chaque arc à l'ensemble des endpoints
for pair in arcs['endpoints']:
    endpoints.update(pair)


endpoints_list = list(endpoints)
endpoints_list = [int(point_id) for point_id in endpoints]
# Initialiser le dictionnaire pour stocker les informations des sommets correspondants
endpoints_info = {}

# Itérer sur chaque identifiant de point dans `endpoints`
for point_id in endpoints_list:
    if point_id in points.index:
        endpoints_info[point_id] = points.loc[point_id].to_dict()

"""
Recuperer tout les arcs et les mettre dand un dictionnaire en liste
"""

listeDesArcs={}


for i in range(arcs.shape[0]):
    sommets = arcs['lstpoints'].iloc[i].split()
    listeDesArcs[i] = sommets

"""
supprimer les caractères inutiles du dict
"""

for i in range(arcs.shape[0]):
    sommets = arcs['lstpoints'].iloc[i]
    sommets_clean = sommets.replace('[', '').replace(']', '').replace(',', '')
    listeDesArcs[i] = sommets_clean
"""
Verification  de la suppression
"""
print(listeDesArcs)

"""
conversion des listes de type string en int
"""
for k, val in listeDesArcs.items():
    sommets = val.split()
    sommets_clean = [int(sommet) for sommet in sommets]
    listeDesArcs[k] = sommets_clean
    
"""
Vérifier si il y a les arcs qu'on veut en l'occcurence le premier et le deuxième si il y en a plus on garde que ceux la (premier, dernier)
"""
for cle, val in listeDesArcs.items():
    if len(val) > 2:
        listeDesArcs[cle] = [val[0], val[-1]]

"""
trier chaque sommets
"""
listSom=[]

for val in listeDesArcs.values():
    for sommet in val:
        if sommet not in listSom:
            listSom.append(sommet)

"""
Creation d'un dictionnaire du graph
"""
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


"""
Creattion de la matrice d'adjacence à partir du dictionnaire
"""
sommets = sorted(dic_graph.keys())  # Recuperer et trier tout les sommets récupérés
n = len(sommets)
matrice_adja = [[0] * n for i in range(n)]  # Créer une matrice remplie de zéros de taille n x n

# Itérer sur les nœuds du graphe avec leur indice après les avoir triés.
for i, sommet1 in enumerate(sorted(dic_graph.keys())):
    # Réitérer pour chaque combinaison de nœuds, permettant de vérifier chaque paire.
    for j, sommet2 in enumerate(sorted(dic_graph.keys())):
        # Vérifier si sommet2 est directement connecté à sommet1 dans le graphe.
        if sommet2 in dic_graph[sommet1]:
            # Assigner 1 dans la matrice d'adjacence si une connexion existe entre les deux sommets.
            matrice_adja[i][j] = 1


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

# Initialiser une liste vide pour la matrice des longueurs des arcs (pas nécessaire si vous initialisez un numpy array après).
matrice_longueurs_arcs = []

# Obtenir la longueur de la liste des points d'intérêt.
n = len(endpoints_list)

# Initialiser un numpy array de zéros avec une forme de n x n, où n est le nombre de points d'intérêt.
# Cela prépare une matrice carrée pour contenir les distances entre chaque paire de points.
matrice_longueurs_arcs = np.zeros((n, n))

# Imprimer le contenu de endpoints_list pour vérifier qu'elle contient les bons éléments.
print("endpoints_list contient : ", endpoints_list)  # Vérifier le contenu de endpoints_list

# Filtrer le DataFrame 'points' pour ne garder que les lignes où 'id_point' est dans 'endpoints_list'.
# Cela réduit les points aux seuls points d'intérêt.
filtered_points = points[points['id_point'].isin(endpoints_list)]

# Créer un dictionnaire qui associe chaque 'id_point' de 'filtered_points' à son index dans le DataFrame.
# Cela est utilisé pour mapper les ID des points à leurs indices correspondants dans la matrice des distances.
index_map = {point_id: index for index, point_id in enumerate(filtered_points['id_point'])}

# Réinitialiser la matrice de distances en utilisant cette fois la taille de 'filtered_points'.
# Cela crée une matrice de zéros avec le nombre de points d'intérêt qui ont été filtrés.
matrice_longueurs_arcs = np.zeros((len(filtered_points), len(filtered_points)))

"""
Calculer la distance
"""
# Boucle sur chaque point dans le DataFrame filtré, avec son index et son ID.
for i, point_id_i in enumerate(filtered_points['id_point']):
    # Boucle à nouveau sur chaque point pour avoir une paire de points.
    for j, point_id_j in enumerate(filtered_points['id_point']):
        # Vérifie si l'index de la première boucle est inférieur à l'index de la seconde boucle.
        # Cela garantit que chaque paire est calculée une seule fois, car la matrice des distances est symétrique.
        if i < j:
            # Accéder aux valeurs de latitude et de longitude pour le premier point (i)
            # en utilisant l'indexation de position avec .iloc, ce qui est nécessaire car les indices ne sont pas nécessairement dans l'ordre.
            lat1, lon1 = filtered_points.iloc[i]['lat'], filtered_points.iloc[i]['lon']
            # Accéder aux valeurs de latitude et de longitude pour le second point (j)
            # de la même manière que pour le premier point.
            lat2, lon2 = filtered_points.iloc[j]['lat'], filtered_points.iloc[j]['lon']
            # Appeler la fonction distanceGPS avec les latitudes et longitudes des deux points
            # pour calculer la distance entre eux.
            distance = distanceGPS(lat1, lon1, lat2, lon2)
            # Stocker la distance calculée dans la matrice des longueurs des arcs à la position [i][j].
            matrice_longueurs_arcs[i][j] = distance
            # Comme la matrice est symétrique, la même distance est valable pour la position [j][i].
            matrice_longueurs_arcs[j][i] = distance

print(matrice_longueurs_arcs)