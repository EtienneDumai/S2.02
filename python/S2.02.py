import pandas as pd
import os
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt



os.chdir('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\donnees')
points=pd.read_table('points.csv', sep=";",index_col=0, encoding='ANSI')
arcs=pd.read_table('arcs.csv', sep=";",index_col=0, encoding='ANSI')

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
