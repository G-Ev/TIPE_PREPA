from random import *
from math import floor, sqrt
from copy import deepcopy

from graphe import *
from noeud import *
from drone import *
from decoupage_zones import *
from data import *
from tasmin import *
from unionfind import *
from affichage import *
from main_glouton import *
from analyse_resultat import *


def const_tasmin_aretes_sommet(g, som):
  """
  In : Un graphe g [Graphe]
       Un sommet som du graphe [string]
  Out : Une file de priorite min [TasMin]
  Goal : Construit la file de priorite min contenant toutes les aretes incidentes au sommet entre en parametre
  """
  t = TasMin()
  for s in g.get_arcs()[som].keys():
    t.push((som, s), g.get_arcs()[som][s])

  return t


def cmp_aretes(a1, a2):
  """
  In : 2 aretes [Noeud*Noeud]
  Out : True si les aretes sont les memes, False sinon [Bool]
  Goal : Regarde si les 2 aretes donnees en parametres sont les memes (dans un graphe non oriente)
  """
  x1, y1 = a1
  x2, y2 = a2

  return ((x1 == x2 and y2 == y1) or (x1 == y2 and y1 == x2))


def approx_cout_aux(g, n, sommets_requis=[]):
  """
  In : Un graphe g [Graphe]
       Un entier n correspondant au nombre de sommets à parcourir au départ [int]
       Une liste de noms de sommets, par defaut vide [list x string]
  Out : Un flottant [float]
  Goal : Determine le cout d'acces maximal de chaque sommet, en differenciant ceux requis et les autres -> somme des deux aretes de plus bas cout de chaque sommet non requis + cout des aretes reliant les sommets requis le tout divise par 2
  """
  c = 2 * poids_chemin(g, sommets_requis)
  nb_som = len(sommets_requis)

  ## Si le drone ne doit parcourir qu'un sommet, le résultat est immediat
  if n == 1:
    return c

  l_utilises = []
  for i in range(nb_som - 1):
    l_utilises.append((sommets_requis[i], sommets_requis[i + 1]))

  ## Si tous les sommets du graphe sont deja "requis", il ne reste plus qu'a ajouter le cout de l'arete permettant de fermer le tour au poids total du chemin :
  if nb_som == n:
    return (c + g.get_arcs()[sommets_requis[0]][sommets_requis[-1]]) / 2

  premier_tasmin = const_tasmin_aretes_sommet(g, sommets_requis[0])
  a = premier_tasmin.pop()  # Arete de poids minimal du premier sommet requis

  if nb_som == 1:
    b = premier_tasmin.pop(
    )  # Arete de poids minimal du dernier sommet requis (le même que le premier)

  else:
    dernier_tasmin = const_tasmin_aretes_sommet(g, sommets_requis[-1])
    b = dernier_tasmin.pop()  # Arete de poids minimal du dernier sommet requis

    ## Verifie que l'arete de poids minimal du premier sommet requis n'est pas deja empruntee pour aller au second sommet requis, sinon tire la seconde arete de plus petit cout :
    if cmp_aretes(a, (sommets_requis[0], sommets_requis[1])):
      a = premier_tasmin.pop()

    ## Verifie que l'arete de poids minimal du dernier sommet requis n'est pas deja emprunte pour fermer le tour, sinon tire la seconde arete de plus petit cout :
    if cmp_aretes(b, (sommets_requis[-1], sommets_requis[-2])):
      b = dernier_tasmin.pop()

    c += g.get_arcs()[b[0]][b[1]]

  l_utilises.append(a)
  l_utilises.append(b)

  c += g.get_arcs()[a[0]][a[1]]
  som_restants = list(
    g.get_arcs().keys())  # Liste des sommets du graphe non requis

  for s in sommets_requis:
    som_restants.remove(s)


## Derniere etape : calcul le cout d'acces aux sommets non requis (tire leurs 2 aretes de plus bas cout) :
  for s in som_restants:
    t = const_tasmin_aretes_sommet(g, s)
    x1, y1 = t.pop()
    x2, y2 = t.pop()
    l_utilises.append((x1, y1))
    l_utilises.append((x2, y2))
    c += g.get_arcs()[x1][y1] + g.get_arcs()[x2][y2]

  return c / 2


def approx_cout(g, som_dep, restants, n, l=[]):
  """
  In : Un graphe g [Graphe]
       Le nom du sommet de depart du tour som_dep (doit être dans restant) [string]
       Une liste restants des noms des sommets non encore requis [list x string]
       Un entier n correspondant au nombre de sommets à parcourir au départ [int]
       Une liste l des noms des sommets requis, par defaut vide, sert d'accumulateur [list x string]
  Out : Une liste de noms de sommets [list x string]
  Goal : Calcule le poids maximal de maniere optimale pour un tour dans le graphe donne
          (sert de borne superieure a l'algorithme de Branch and Bound)
  """
  ## Condition de depart :
  if l == []:
    assert som_dep in restants, "Le sommet de départ doit faire partie de la liste restants"
    l = [som_dep]
    restants.remove(som_dep)


## Condition de fin :
  if len(l) == n:
    return l + [l[0]]

  m = float('inf')  # Va servir de borne sup
  res = ""  # Sert a stocker le meilleur sommet a prendre pour minimiser
  #                     le cout total

  ## Calcul le cout du chemin requis a tous les sommets encore disponibles puis ajoute le sommet minimisant ce cout :
  for s in restants:
    c = approx_cout_aux(g, n, l + [s])

    if c < m:
      m = c
      res = s

  restants.remove(res)
  l.append(res)

  return approx_cout(g, som_dep, restants, n, l)


def calcul_borne_inf(g, som_dep, som_req=[], som_lib=[]):
  """
  In : Un graphe g [Graphe]
       Le nom du sommet de depart du tour som_dep [string]
       Une liste de noms de sommets som_req [list x string]
       Une liste de noms de sommets som_lib [list x string]
  Out : Un flottant [float]
  Goal : Determine le cout d'accès minimal de chaque sommet, en differenciant ceux requis 
                             et les autres 
  """
  if som_req == []:
    som_req = [som_dep]

  if som_lib == []:
    som_lib = to_str(g.get_sommets())

    if som_dep in som_lib:
      som_lib.remove(som_dep)

  cout = 0
  ## Applique l'algorithme de Kruskal au graphe induit par les sommets libres
  g_induit_lib = g.graphe_induit(som_lib)
  acm_lib = kruskal(g_induit_lib)

  ## Somme les poids des aretes dans l'ACM
  for a in acm_lib:
    x, y = a[0], a[1]
    cout += g.get_arcs()[x][y]


## Rajoute les poids des aretes deja requises
  cout += poids_chemin(g, som_req)

  return cout


def branch_and_bound_aux(g,
                         som_dep,
                         som_lib, num_drone,
                         som_req=[]):
  """
  In : Un graphe g [Graphe]
       Un sommet som_dep [Noeud]
       Une liste de noms de sommet som_lib [list x string]
       Un entier num_drone [int]
  Out : None
  Goal : Applique le principe de Branch and Bound au graphe donne pour y trouver le 
                             tour de cout minimal
  """
  global bornes_sup
  global parcours_bb
                           
  n = g.get_taille()

  if len(som_req) == g.get_taille():
    poids = poids_chemin(g, som_req + [som_dep.get_nom()])
    if poids < bornes_sup[num_drone]:
      bornes_sup[num_drone] = poids
      parcours_bb[num_drone] = som_req + [som_dep.get_nom()]

  else:
    
    file_prio = TasMin()

    for s in som_lib:

      cout = approx_cout_aux(g, n, som_req + [s])
      if cout < bornes_sup[num_drone]:
        file_prio.push(s, cout)
  
    parcours_possibles = TasMin()
  
    while not file_prio.est_vide():
  
      s = file_prio.pop()
      new_som_lib = list(som_lib)
      new_som_lib.remove(s)
      
      branch_and_bound_aux(g,som_dep,new_som_lib,num_drone,som_req+[s])
    
def branch_and_bound(g, som_dep, num_drone):
  """
  In : Un graphe g [Graphe]
       Un sommet som_dep [Noeud]
       Un entier num_drone [int]
  Out : Une liste de sommet [list x string]
  Goal : Calcule le parcours optimal pour le drone numéro num_drone
  """
  global bornes_sup
  global parcours_bb
  
  bornes_sup[num_drone]=float('inf')

  a_parcourir = list(g.get_sommets())
  a_parcourir.remove(som_dep)
  a_parcourir = to_str(a_parcourir)
  
  branch_and_bound_aux(g,som_dep,a_parcourir,num_drone,[som_dep.get_nom()])

  return parcours_bb[num_drone]


def test_k_moy():
  k_moy_fr = k_moyennes(g_fr, 6)
  k_moy_16 = k_moyennes(g_16, 3)
  return (k_moy_fr, k_moy_16)


g_16 = creer_graphe(alentours_Janson)
g_fr = creer_graphe(villes_france)

bornes_sup = [float('inf')]*100
parcours_bb = [[]]*100

"""
## TEST K-MOYENNES
k_moy_fr, k_moy_16 = test_k_moy()

l_fr = list(g_fr.get_arcs().keys())
l_16 = list(g_16.get_arcs().keys())


## TEST GLOUTON
g_16_special_glouglou = creer_graphe(alentours_Janson)
g_fr_special_glouglou = creer_graphe(villes_france)

pg_fr = glouton(g_fr, g_fr.noms_som["Paris"])
pg_16 = glouton(g_16, g_16.noms_som["Lycée"])

poids_pg_fr = poids_chemin(g_fr, pg_fr)
poids_pg_16 = poids_chemin(g_16, pg_16)

## TEST B&B 
pb_16 = branch_and_bound(g_16, g_16.noms_som["Lycée"], 0)
pb_fr = branch_and_bound(g_fr, g_fr.noms_som["Paris"], 0)

poids_pb_16 = poids_chemin(g_16, pb_16)
poids_pb_fr = poids_chemin(g_fr, pb_fr)


## TEST TOTAL

print("b&b : {} \nde poids {}\n".format(pb_fr, 
print("glouton : {} \nde poids : {}\n".format(pg_16, poids_pg_16))
"""

scores = calcul_score_moyen(g_fr, branch_and_bound, g_fr.noms_som["Paris"], 3)
print("scores : {} \ntaille totale : {}\n".format(scores, len(scores)))

aff_efficacité(scores)



## TEST B&B


#print(branch_and_bound_aux(g_fr, g_fr.noms_som["Paris"], a_parcourir, ["Paris"]))


print(borne_sup)

