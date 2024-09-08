from noeud import *
from unionfind import *
from tasmin import *


class Graphe():

  def __init__(self):
    self.sommets = []
    self.noms_som = {}
    self.taille = 0
    self.arcs = {}
## Rq : les arcs sont sous forme de dico dont les clefs sont les NOMS des sommets [str] et les clefs sont des dicos stockant les voisins (clefs) et leur distance (valeurs associees).

## Getter/Setter :

  def get_sommets(self):
    return self.sommets

  def get_taille(self):
    return self.taille

  def get_arcs(self):
    return self.arcs


## Autres méthodes :

  def ajout_sommet(self, som):
    """
    In : un sommet som [Noeud]
    Out : None
    Goal : rajoute par effet de bord le sommet en parametre dans le graphe courant (i.e. creer des arcs pondérés par la distance avec tous les autres sommets du graphe)
    """
    self.arcs[som.get_nom()] = {}
    for i in range(self.taille):
      d = som.distance(self.sommets[i])
      self.arcs[som.get_nom()][self.sommets[i].get_nom()] = d
      self.arcs[self.sommets[i].get_nom()][som.get_nom()] = d

    self.sommets.append(som)
    self.noms_som[som.nom] = som
    self.taille += 1

  def graphe_induit(self, l):
    """
      In : Une liste de noeuds l [list x string]
      Out : Un graphe res [Graphe] 
      Goal : Construire le graphe induit dans self par les sommets de l
    """
    res = Graphe()
    res.taille = len(l)
    
    for s in l:
      res.arcs[s] = {}
      res.sommets.append(self.noms_som[s])
      res.noms_som[s] = self.noms_som[s]
      
    for s in l:
      for vois in self.get_arcs()[s].keys():
        
        if vois in l:
          d = self.get_arcs()[s][vois]
          res.arcs[s][vois] = d
          res.arcs[vois][s] = d
          
    return res


def creer_graphe(l):
  """
  In : Une liste l de triplets contenant le nom et les coordonnées de sommets [list x string*float*float]
  Out : Un graphe contenant autant de sommets que de triplets dans la liste ayant les caractéristiques contenues dans chaque triplet [Graphe]
  Goal : Creer un graphe contenant les "points strategiques"
  """
  g = Graphe()
  for i in l:
    n = Noeud(i[0], i[1], i[2])
    g.ajout_sommet(n)

  return g


def recense_aretes(g):
  """
  In : Un graphe g [Graphe]
  Out : Une liste d'aretes et leur poids [list x (string*string)*float]
  Goal : Creer une liste contenant toutes les aretes du graphe avec leur poids (distance euclidienne entre les 2 extremites)
  """
  res = []
  for k in g.get_arcs().keys():
    for i in g.get_arcs()[k].keys():
      if k < i:
        res.append(((k, i), g.get_arcs()[k][i]))

  return res


def kruskal(g):
  """
  In : Un graphe g [Graphe]
  Out : Une liste d'aretes [list x string*string]
  Goal : Applique l'algorithme de Kruskal pour determiner un arbre couvrant de cout minimal du graphe entre
  """
  n = g.get_taille()
  l = {}
  r = {}

  for i in g.get_arcs().keys():
    l[i] = i
    r[i] = 0

  uf = UnionFind(l, r)
  tasmin = TasMin()
  aretes = recense_aretes(g)
  
  for e in aretes:
    tasmin.push(e[0], e[1])

  acm = []
  taille = 0

  while taille < n - 1:
    (x, y) = tasmin.pop()
    rep_x = uf.trouver(x)
    rep_y = uf.trouver(y)

    if rep_x != rep_y:
      uf.union(x, y)
      acm.append((x, y))
      taille += 1
  
  return acm


def poids_chemin(g, sommets):
  """
  In : Un graphe g [Graphe] 
       Une liste de sommets [list x string]
  Out : Un flottant [float]
  Goal : Calcule le poids du chemin décrit par la liste
  """
  c = 0
  for i in range(len(sommets) - 1):
    c += g.get_arcs()[sommets[i]][sommets[i + 1]]
  return c
