import matplotlib.pyplot as plt
from noeud import *
from graphe import *

colors = ["red", "green", "blue", "purple", "pink", "orange"]
img = plt.imread("coupé.png")


def aff_k_moy(g, k_moy, carte=False):
  """
  In : Un graphe g [Graphe]
       Une liste de listes de sommets [list x list x Noeud]
       Un booleen carte, par defaut a False [bool]
  Out : None
  Goal : Affiche le decoupage de la zone a couvrir selon l'algorithme des k-moyennes
  """
  fig, ax = plt.subplots()

  ## Affiche la carte de France contenant les villes choisies en jeu de test
  if carte:
    ax.imshow(img, extent=[560, 8850, 690, 9450])

## Affichage des barycentres
  for j in range(len(k_moy[0])):
    s_j = k_moy[0][j]
    x_j = s_j.get_x()
    y_j = s_j.get_y()
    ax.plot(x_j, y_j, marker="x", color=colors[j])


## Affichage des villes, coloriees selon le barycentre qui leur est associe
  for i in range(1, len(k_moy)):
    for j in range(len(k_moy[i])):
      s_j = k_moy[i][j]
      x_j = s_j.get_x()
      y_j = s_j.get_y()
      ax.plot(x_j, y_j, marker="o", color=colors[i - 1])

  plt.show()
