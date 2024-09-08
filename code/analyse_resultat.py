import matplotlib.pyplot as plt
import numpy as np

from noeud import *
from graphe import *
from decoupage_zones import *


def const_jeu_test(g, n=10):
  """
    In : Un graphe g [Graphe]
         Un entier n [int]
    Out : Une liste de listes de listes de listes de noms de sommet 
              [list x list x list x list x string]
    Goal : Pour k allant de 1 au nombre de sommets du graphe, crée n découpages 
              de la zone a couvrir par la methode des k-moyennes du graphe
              
      Construction du jeu de test (les imbrications) :
      -> jeu[i] : jeu de test pour i+1 drones ;
      -> jeu[i][j] : test n°j pour i+1 drones ;
      -> jeu[i][j][k] : sommets a parcourir par le k-ieme drone du j-ieme test pour i+1 drones
  """
  taille = g.get_taille()
  jeu = [[] for i in range(taille)]

  for k in range(1, taille + 1):
    for i in range(n):
      jeu[k - 1].append(k_moyennes(
        g, k)[1:])  # k_moyennes()[0] donne les barycentres inutiles ici

  return jeu


def aff_jeu_test(jeu):
  """
    In : Une liste de listes de listes de listes de noms de sommet 
              [list x list x list x list x Noeud]
    Out : None
    Goal : Affiche le jeu de test créé par la fonction const_jeu_test
  """
  for i in range(len(jeu)):
    print("\nTest pour {} drones :\n".format(i + 1))

    for j in range(len(jeu[i])):
      print("\tTest n° {} :\n".format(j + 1))

      for k in range(i + 1):
        print("\tParcours du drone n° {} : {}\n".format(
          k + 1, to_str(jeu[i][j][k])))


def calcul_score_moyen(g, fonction_res, som_dep, n=10):
  """
  In : Un graphe g [Graphe]
       Une fonction fonction_res [fun]
       Un noeud som_dep [Noeud]
       Un entier n [int]
  Out : Une liste de flottants [list x float]
  Goal : Determine le score moyen (sur n simulations) de tours determines par la methode implentee avec la fonction_res pour tous nombre de drones possible ([|1 ; nb_sommets-1|])
  """

  a_parcourir = g.get_sommets()
  a_parcourir.remove(som_dep)
  g_a_parcourir = g.graphe_induit(to_str(a_parcourir))

  taille = g_a_parcourir.get_taille()

  jeu_test = const_jeu_test(g_a_parcourir, n)

  scores_moyens = []

  ## Le but est de faire varier le nombre de drone de 1 au nombre de sommets
  for i in range(taille):

    scores_i_drones = []

    for test_j in range(len(jeu_test[i])):

      poids_test_j = []

      ## Permet d'obtenir le trajet du k-ieme drone
      for drone_k in range(len(jeu_test[i][test_j])):

        ## Ne s'interesse qu'aux drones ayant au moins 1 sommet attribue
        if len(jeu_test[i][test_j][drone_k]) > 0:
          g_induit = g.graphe_induit(
            to_str(jeu_test[i][test_j][drone_k]) + [som_dep.get_nom()])

          acm_induit = kruskal(g_induit)
          poids_acm = 0

          ## Determine le cout total de l'ACM, servant de cout ideal pour le tour
          for a in acm_induit:
            x, y = a[0], a[1]
            poids_acm += g.get_arcs()[x][y]
        ## Determine le cout du tour trouve pour le k-ieme drone
          parcours_drone_k = fonction_res(g_induit, som_dep, drone_k)
          poids_test_j.append(
            (poids_chemin(g, parcours_drone_k), poids_acm
             ))  # le 2e element servira a effectuer des calculs plus tard

          #print("Pour {} drones, test n° {}, drone n° {} ok,\nparcours : {}  \n".format(i+1,j,k,parcours_k))

      max_poids = 0

      ## Determine le drone ayant le parcours le plus long
      ## Etant le dernier a terminer son tour, sert de representant pour les autres drones du meme test
      pire_parcours = None
      for a in poids_test_j:
        if a[0] > max_poids:
          max_poids = a[0]
          pire_parcours = a

    ## Le score d'un test est determiner tel que :
    ## s(test) = (valeur_atteinte - valeur_ideale) * (1 + cout(test)) > 0
    ## Ici le cout est le nombre de drones utilise.
    ## Le but est de reduire son impact pour ameliorer le visuel des graphiques
      scores_i_drones.append(
        (pire_parcours[0] - pire_parcours[1]) * (1 + (i + 1)**0.5))

  ## Stocke toutes les moyennes des tests faits pour chaque nombre de drones
  ## (n = simulations faites pour chaque nombre de drones)
    scores_moyens.append(sum(scores_i_drones) / n)

  return scores_moyens


def aff_efficacité(scores):
  """
  In : Une liste de flottants [list x float]
  Out : None
  Goal : Affiche le score moyen de la methode de resolution du probleme selon le nombre de drones utilises 
  """
  fig, ax = plt.subplots()

  nb_drones = range(1, len(scores) + 1)

  ax.bar(nb_drones, scores)

  ax.set_ylabel('Coût')
  ax.set_xlabel('Nombre de drones')

  plt.show()
