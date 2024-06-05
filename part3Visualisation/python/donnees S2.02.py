        ###########################################################################
        ##  Initialisation des variables et fonction n√©cessaire aux algorithmes  ##
        ###########################################################################
#Initialisation des variables et des fonctions n‚àö¬©cessaires au bon fonctionnement des algos
import json
import pandas as pd
import numpy as np
import os
import sys
import random as r
sys.path.append('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\part3Visualisation\\python')
os.chdir('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\part2RechercheDeplusCourtChemin\\donnees')
import graphics as g 
chemin_image = ("C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.02\\part3Visualisation\\python\\CaptureOpenStreetMap2024.PNG")
# import dicsucc.json et dicsuccdist.json (--> dictionnaire)
with open("dicsucc.json", "r") as fichier:
    dicsucc = json.load(fichier)
with open("dicsuccdist.json", "r") as fichier:
    dicsuccdist = json.load(fichier)

# import aretes.csv (--> dataframe) et transformation de lstpoints (cha‚àö√Üne-->liste)
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
#Fonction pour avoir 2 points al√©atoire du graphe
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




        ##########################################
        ##  Algorithmes de recherche de chemin  ##
        ##########################################




                ################
                ##  Dijkstra  ##
                ################
                
                
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
            break  # On a trouvé le chemin le plus court
        
        for voisin, poids in graphe[sommet_courant].items():  # Utiliser .items() pour iterer sur les voisins
            # Calculer la nouvelle distance
            nouvelle_distance = distances[sommet_courant] + poids
            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                pred[voisin] = sommet_courant
                #tracer le chemin qui a √©t√© parcouru
                traceChemin(sommet_courant, voisin, color="orange", width=2)
                
    chemin = reconstruire_chemin(sommet_depart, sommet_arrivee, pred)
    #Tracer le plus court chemin trouv√©
    for i in range(len(chemin) - 1):
        traceChemin(chemin[i], chemin[i + 1], color="purple", width=4)
    distance_totale = distances[sommet_arrivee]
    return chemin, round(distance_totale)



                ###############
                ##  Bellman  ##
                ###############
                
                
def bellman_ford(graphe, sommet_depart):
 # Initialisation
 distances = {sommet: float('inf') for sommet in graphe}
 distances[sommet_depart] = 0
 pred = {sommet: None for sommet in graphe}

 # Rel‚àö¬¢cher chaque arete (V-1) fois
 for _ in range(len(graphe) - 1):
     for sommet in graphe:
         for voisin, poids in graphe[sommet].items():
             #tracer le chemin qui a √©t√© parcouru
             traceChemin(sommet, voisin, color="red", width=2)
             if distances[sommet] + poids < distances[voisin]:
                 distances[voisin] = distances[sommet] + poids
                 pred[voisin] = sommet
                 

 return distances, pred





                #############################
                ##  Visualisation Bellman  ##
                #############################



# Variables pour la transformation des coordonnées
longitudeGauche = -1.48768
echelle_longitude = 1411 / 0.0303
echelle_latitude = 912 / 0.01422
latHauteur = 43.4990
 
# Cr√©er la fenetre et l'image
win = g.GraphWin("Carte de Bayonne", 1412, 912)
image = g.Image(g.Point(705, 456), chemin_image)
image.draw(win)

# représenter les sommet par un point de couleur rouge sur la carte
for i in range(1884):
    lat = sommets.iloc[i, 0]
    lon = sommets.iloc[i, 1]
    x = (lon - longitudeGauche) * echelle_longitude
    y = (latHauteur - lat) * echelle_latitude
    cercle = g.Circle(g.Point(x, y), 2)
    cercle.setFill("red")
    cercle.draw(win)

# Fonction pour créer les chemins entre les points
def traceChemin(point1, point2, color="black", width=1):
    lat1 = sommets.loc[point1, 'lat']
    lon1 = sommets.loc[point1, 'lon']
    lat2 = sommets.loc[point2, 'lat']
    lon2 = sommets.loc[point2, 'lon']
    
    ptn1 = g.Point((lon1 - longitudeGauche) * echelle_longitude, 
                  (latHauteur - lat1) * echelle_latitude)
    ptn2 = g.Point((lon2 - longitudeGauche) * echelle_longitude, 
                  (latHauteur - lat2) * echelle_latitude)
    
    arc = g.Line(ptn1, ptn2)
    arc.setFill(color)
    arc.setWidth(width)
    arc.draw(win)

# Dessiner tout les arcs entre les points
for arc in aretes.index:
    listePoints = aretes.loc[arc, 'lstpoints']
    depart = listePoints[0]
    arrive = listePoints[-1]
    traceChemin(depart, arrive)

#Ex√©cuter l'algorithme sur 2 points aléatoires du graphe 
point1Bell, point2Bell = point_alea(dicsuccdistInt)
distances, pred = bellman_ford(dicsuccdistInt, point1Bell)
chemin = reconstruire_chemin( point1Bell, point2Bell, pred)

#Tracer le plus court chemin trouvé
for i in range(len(chemin) - 1):
        traceChemin(chemin[i], chemin[i + 1], color="green", width=3)
        
#Afficher la fenetre qui se fermera sur un clic souris
win.getMouse()  
win.close()




                ##############################
                ##  Visualisation Dijkstra  ##
                ##############################



# Variables pour la transformation des coordonnées
longitudeGauche = -1.48768
echelle_longitude = 1411 / 0.0303
echelle_latitude = 912 / 0.01422
latHauteur = 43.4990
 
# Créer la fenetre et l'image
win = g.GraphWin("Carte de Bayonne", 1412, 912)
image = g.Image(g.Point(705, 456), chemin_image)
image.draw(win)

# représenter les sommet par un point de couleur rouge sur la carte
for i in range(1884):
    lat = sommets.iloc[i, 0]
    lon = sommets.iloc[i, 1]
    x = (lon - longitudeGauche) * echelle_longitude
    y = (latHauteur - lat) * echelle_latitude
    cercle = g.Circle(g.Point(x, y), 2)
    cercle.setFill("red")
    cercle.draw(win)

# Fonction pour créer les chemins entre les points
def traceChemin(point1, point2, color="black", width=1):
    lat1 = sommets.loc[point1, 'lat']
    lon1 = sommets.loc[point1, 'lon']
    lat2 = sommets.loc[point2, 'lat']
    lon2 = sommets.loc[point2, 'lon']
    
    ptn1 = g.Point((lon1 - longitudeGauche) * echelle_longitude, 
                  (latHauteur - lat1) * echelle_latitude)
    ptn2 = g.Point((lon2 - longitudeGauche) * echelle_longitude, 
                  (latHauteur - lat2) * echelle_latitude)
    
    arc = g.Line(ptn1, ptn2)
    arc.setFill(color)
    arc.setWidth(width)
    arc.draw(win)

# Dessiner tout les arcs entre les points
for arc in aretes.index:
    listePoints = aretes.loc[arc, 'lstpoints']
    depart = listePoints[0]
    arrive = listePoints[-1]
    traceChemin(depart, arrive)

#Ex√©cuter l'algorithme sur 2 points al√©atoires du graphe 
point1Dij, point2Dij = point_alea(dicsuccdistInt)
chemin, distance = dijkstra(dicsuccdistInt, point1Dij, point2Dij)
del point1Dij, point2Dij, chemin, distance

#Afficher la fenetre qui se fermera sur un clic souris
win.getMouse()  
win.close()


        




