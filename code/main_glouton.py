from graphe import *
from noeud import *
from drone import *
from math import floor, sqrt
from copy import deepcopy
from data import *


def glouton(g, som_dep, num_drone):
  """
    In : Un graphe g operationnel [Graphe]
         Un sommet de depart som_dep [Noeud]
    Out : Une liste de sommets [list x Noeud]
    Goal : Etablie la liste (par methode gloutonne : plus-proche-voisin) des sommets les plus proches pour effectuer le parcours le plus petit possible 
    """
  n = g.get_taille()

  a_parcourir = list(g.get_sommets())
  
  if som_dep in a_parcourir:
    a_parcourir.remove(som_dep)
    
  liste_parcours = [som_dep]

  for i in range(n - 1):
    sommet_courant = liste_parcours[i]
    m = n - 1 - i
    nmin = 0
    dmin = g.get_arcs()[a_parcourir[nmin].get_nom()][sommet_courant.get_nom()]  # distance du sommet courant à un sommet arbitrairement choisi

    for j in range(1, m):
      d = g.get_arcs()[a_parcourir[j].get_nom()][sommet_courant.get_nom()]  # distance de tous les autres sommets au sommet courant

      if d < dmin:  # mise a jour sommet plus proche du courant
        dmin = d
        nmin = j

    liste_parcours.append(a_parcourir.pop(nmin))

  liste_parcours.append(som_dep)

  return to_str(liste_parcours)


def multi_glouton(g, nb_drones):
  """
    In : Un graphe g operationnel [Graphe] 
         Un nombre de drones nb_drones [integer]
    Out : Une liste de listes de noeuds [list x list x Noeud]
    Goal : Ajoute, a tour de role le sommet le plus proche de chaque drone a sa liste de parcour
    """
  n = g.get_taille()
  liste_parcours = [[g.get_sommets()[0]] for i in range(nb_drones)]
  a_parcourir = g.get_sommets()[1:]

  for i in range(floor((n - 1) / nb_drones)):
    for x in range(nb_drones):
      sommet_courant = liste_parcours[x][-1]
      nmin = 0
      dmin = g.get_arcs()[a_parcourir[nmin].get_nom()][sommet_courant.get_nom(
      )]  # distance du sommet courant à un sommet arbitrairement choisi
      m = len(a_parcourir)

    for j in range(1, m):
      d = g.get_arcs()[a_parcourir[j].get_nom()][sommet_courant.get_nom(
      )]  # distance de tous les autres sommets au sommet courant

      if d < dmin:  # mise a jour sommet plus proche du courant
        dmin = d
        nmin = j

  liste_parcours[x].append(a_parcourir.pop(nmin))

  for i in range(floor((n - 1) / nb_drones) * nb_drones, n - 1):
    x = i - floor((n - 1) / nb_drones) * nb_drones
    sommet_courant = liste_parcours[x][-1]
    nmin = 0
    dmin = g.get_arcs()[a_parcourir[nmin].get_nom()][sommet_courant.get_nom(
    )]  # distance du sommet courant à un sommet arbitrairement choisi
    m = len(a_parcourir)

  for j in range(1, m):
    d = g.get_arcs()[a_parcourir[j].get_nom()][sommet_courant.get_nom(
    )]  # distance de tous les autres sommets au sommet courant

    if d < dmin:  # mise a jour sommet plus proche du courant
      dmin = d
      nmin = j

  liste_parcours[x].append(a_parcourir.pop(nmin))

  return liste_parcours


def print_parcours(l):
  """
    In : Une liste l de noeuds [list x Noeud]
    Out : None
    Goal : Affiche le parcours cree par l'algorithme glouton
    """
  for i in range(len(l)):
    print("{}\n".format(l[i].get_nom()))


def print_multi_parcours(l):
  """
    In : Une liste l de noeuds [list x Noeud]
    Out : None
    Goal : Affiche a la console le parcours effectue par chaque drone
    """
  for i in range(len(l)):
    print("Parcours du drone n°", i)
    for j in range(len(l[i])):
      print("  {} \n".format(l[i][j].get_nom()))


def creer_chemin(l, n):
  """
    In : Une liste l de noeuds [list x Noeud]
         Un entier n [integer]
    Out : Une liste de listes de triplets [list X list x string*float*float]
    Goal : Etablit les sommets les plus proches repartis en n sous-zones distinctes
    """
  liste_x = [s.get_x() for s in l]
  liste_y = [s.get_y() for s in l]
  bg = (min(liste_x), min(liste_y))  #coin bas gauche de la zone à quadriller
  hd = (max(liste_x), max(liste_y))  #coin haut droite de la zone à quadriller

  step_x = (hd[0] - bg[0]) / sqrt(n)
  step_y = (hd[1] - bg[1]) / sqrt(n)

  grid = [[] for i in range(n)]

  for i in range(len(l)):
    x = 0
    y = 0

    while (bg[0] + (x + 1) * step_x < l[i].get_x()):
      x += 1

    while (bg[1] + (y + 1) * step_y < l[i].get_y()):
      y += 1

    grid[x * int(sqrt(n)) + y].append(
      (l[i].get_nom(), l[i].get_x(), l[i].get_y()))

  return grid


def multi_chemin(g, n):
  """
    In : Un graphe g [Graphe]
         Un entier n [integer]
    Out : Une liste de listes de noeuds [list X list x Noeud]
    Goal : Applique l'algorithme glouton aux differents sommets de chaque sous-zones, etablissant le parcours que chaque drone prendra
    """
  grid = creer_chemin(g.get_sommets(), n)

  listes_parcours = [glouton(creer_graphe(l)) for l in grid]

  return listes_parcours
