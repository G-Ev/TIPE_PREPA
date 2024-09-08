from random import *
from noeud import *


def plus_proche(s, l):
  """
  In : Un sommet s [Noeud]
       Une liste l de noeuds [list x Noeud]
  Out : Le nom d'un sommet [string]
  Goal : Determine le sommet le plus proche du sommet entre en parametre parmi ceux contenu dans la liste
  """
  min = float('inf')
  res = None
  for p in l:
    d = p.distance(s)

    if d < min:
      min = d
      res = p

  return res.get_nom()


def pos_moyenne(l):
  """
  In : Une liste de sommets [Noeud]
  Out : Un tuple de flottant [float*float]
  Goal : Calcul la position moyenne des sommets contenus dans la liste
  """
  x = [s.get_x() for s in l]
  y = [s.get_y() for s in l]

  moy_x = sum(x) / len(x)
  moy_y = sum(y) / len(y)

  return (moy_x, moy_y)


def k_moyennes(g, k, iter=5):
  """
  In : Un graphe g [Graphe]
       Un entier k (correspond au nombre de drones) [integer]
       Un entier iter (nombre de fois a recalculer la position du barycentre), par defaut a 5 [Integer]
  Out : Une liste de listes de noeuds [list x list x Noeud]
  Goal : Determine k zones distinctes (sous forme de liste de listes) du graphe a la maniere de l'algorithme des k-moyennes
  """
  x = [s.get_x() for s in g.get_sommets()]
  y = [s.get_y() for s in g.get_sommets()]
  min_x = min(x)
  max_x = max(x)
  min_y = min(y)
  max_y = max(y)

  barycentres = []
  couleur = {}

  ## Determine la position aleatoire des k barycentres :
  for i in range(k):
    x_rd = randint(int(min_x), int(max_x))
    y_rd = randint(int(min_y), int(max_y))

    barycentres.append(Noeud(i, x_rd, y_rd))
    couleur[i] = []

## Affecte a chaque sommet une le barycentre le plus proche
  for s in g.get_sommets():
    spp = plus_proche(s, barycentres)
    couleur[spp].append(s)

## Reapplique les etapes precedentes pour ameliorer la precision des barycentres
  for i in range(iter):
    for j in range(k):
      if couleur[j] != []:
        barycentres[j]._set_pos(pos_moyenne(couleur[j]))
        couleur[j] = []

    for s in g.get_sommets():
      couleur[plus_proche(s, barycentres)].append(s)


## Affecte a chaque barycentre les sommets les plus proches d'eux
  res = [barycentres]
  for j in range(k):
    res.append([s for s in couleur[j]])

  return res
