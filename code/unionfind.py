class UnionFind():

  def __init__(self, lien={}, rang={}):
    self.liens = lien  # lien[i] sera le representant de i
    self.rangs = rang  # rang[i] est la hauteur de i dans son arbre

## Getter / Setter

  def _set_liens(self, nv_liens):
    self.liens = nv_liens

  def _set_rangs(self, nv_rangs):
    self.rangs = nv_rangs

  def get_liens(self):
    return self.liens

  def get_rangs(self):
    return self.rangs

## Affichage

  def __str__(self):
    return "{}\n{}\n".format(self.liens, self.rangs)

  def __repr__(self):
    return "{}\n{}\n".format(self.liens, self.rangs)


## Methodes

  def partitionner(self, n):
    """
    In : Un entier n [int]
    Out : None
    Goal : Creer un nombre voulu de groupes
    """
    self._set_liens([i for i in range(n)])
    self._set_rangs([0 for i in range(n)])

  def trouver(self, i):
    """
    In : Un element i contenu dans la structure [beta]
    Out : Le representant de cet element [beta]
    Goal : Sert a donner le representant de l'element donne (pour savoir son groupe) de maniere optimisee
    """
    if self.liens[i] == i:
      return i

    else:
      p = self.trouver(self.liens[i])
      self.liens[i] = p
      return p

  def union(self, i, j):
    """
    In  : Deux elements i et j contenu dans la structure [beta]
    Out : None
    Goal : Effectue l'union des 2 groupes contenant les deux elements de maniere optimisee
    """
    rep_i = self.trouver(i)
    rep_j = self.trouver(j)

    if rep_i != rep_j:  ## Le representant de plus haut rang englobe celui de rang le plus bas
      if self.rangs[rep_i] > self.rangs[rep_j]: self.liens[rep_j] = rep_i
      elif self.rangs[rep_i] < self.rangs[rep_j]: self.liens[rep_i] = rep_j
      else:
        self.liens[rep_j] = rep_i
        self.rangs[rep_i] += 1
