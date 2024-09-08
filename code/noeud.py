from math import sqrt

class Noeud():

  def __init__(self, nom, x, y):
    self.nom = nom
    self.x = x
    self.y = y
    self.pos = (x, y)

## Getter/Setter :

  def get_nom(self):
    return self.nom

  def get_pos(self):
    return self.pos

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def _set_nom(self, new_name):
    self.nom = new_name

  def _set_x(self, new_x):
    self.x = new_x
    self.pos = (self.x, self.y)

  def _set_y(self, new_y):
    self.y = new_y
    self.pos = (self.x, self.y)

  def _set_pos(self, new_pos):
    new_x, new_y = new_pos
    self.x = new_x
    self.y = new_y
    self.pos = new_pos


## Autres méthodes :

  def distance(self, som):
    """
    In : un sommet som [Noeud]
    Out : la distance euclidienne entre 2 sommets [float]
    Goal : etablir la distance euclidienne entre les 2 sommets par leurs coordonnées 
    """
    return sqrt((self.x - som.x)**2 + (self.y - som.y)**2)

def to_str (l):
  """
  In : une liste de sommets l [list x Noeud]
  Out : une liste de string [list x str]
  Goal : donne la liste contenant le noms, dans l'ordre, des sommets contenus dans l
  """
  return [s.get_nom() for s in l]