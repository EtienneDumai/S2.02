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

def construire_graphe_dans_dico(arcs_df, points_df):
    # Initialisation du graphe comme un dictionnaire vide
    graphe = {point_id: [] for point_id in points_df.index}

    # Extraction des points de départ et d'arrivée pour chaque arc
    arcs_df['point_debut'] = arcs_df['lstpoints'].apply(lambda x: int(x.strip("[]").split(", ")[0]))
    arcs_df['point_fin'] = arcs_df['lstpoints'].apply(lambda x: int(x.strip("[]").split(", ")[-1]))

    # Pour chaque arc, ajouter le point de fin à la liste des points connectés du point de départ, et vice versa
    for point_debut, point_fin in zip(arcs_df['point_debut'], arcs_df['point_fin']):
        if point_debut in graphe and point_fin in graphe:
            graphe[point_debut].append(point_fin)
            graphe[point_fin].append(point_debut)  # Pour un graphe non dirigé

    # Suppression des doublons dans les listes de connexion
    for point_id in graphe:
        graphe[point_id] = list(set(graphe[point_id]))

    return graphe
graphe = construire_graphe_dans_dico(arcs, points)
def construire_graphe_filtre(arcs_df, points_df, endpoints):
    # Initialisation du graphe avec les points utiles uniquement
    graphe = {point_id: [] for point_id in endpoints }

    # Extraction des points de départ et d'arrivée pour chaque arc
    arcs_df['point_debut'] = arcs_df['lstpoints'].apply(lambda x: int(x.strip("[]").split(", ")[0]))
    arcs_df['point_fin'] = arcs_df['lstpoints'].apply(lambda x: int(x.strip("[]").split(", ")[-1]))

    # Filtrer les arcs pour ne garder que ceux dont les points de départ et d'arrivée sont dans 'endpoints'
    arcs_filtres = arcs_df[arcs_df['point_debut'].isin(endpoints) & arcs_df['point_fin'].isin(endpoints)]

    # Pour chaque arc filtré, ajouter le point de fin à la liste des points connectés du point de départ, et vice versa
    for point_debut, point_fin in zip(arcs_filtres['point_debut'], arcs_filtres['point_fin']):
        if point_debut in graphe and point_fin in graphe:
            graphe[point_debut].append(point_fin)
            graphe[point_fin].append(point_debut)  # Pour un graphe non dirigé

    # Suppression des doublons dans les listes de connexion
    for point_id in graphe:
        graphe[point_id] = list(set(graphe[point_id]))

    return graphe
graphe_filtre = construire_graphe_filtre(arcs, points, endpoints)
