class TasMin():

  def __init__(self):
    self.val = []
    self.size = 0

## Getter / Setter

  def get_val(self):
    return self.val

  def get_size(self):
    return self.size

  def _set_val(self, new_val):
    self.val = new_val

  def _set_size(self, new_size):
    self.size = new_size

## Affichage

  def __str__(self):
    return str(self.val)

  def __repr__(self):
    return str(self.val)


## Methodes
  def est_vide(self):
    return (self.get_size() == 0)

  def push(self, x, p):
    """
    In : Un element x [alpha] et son poids p [float]
    Out : None
    Goal : Insere un element dans la file de priorite avec son poids
    """
    i = 0
    while i < self.size and self.val[i][1] < p:
      i += 1
    self.val = self.val[:i] + [(x, p)] + self.val[i:]
    self.size += 1

  def pop(self):
    """
    In : None
    Out : Un element de la liste [alpha]
    Goal : Sort l'element de priorite minimale de la file de priorite 
    """
    assert self.size != 0, "Tas vide"
    v = self.val.pop(0)[0]
    self.size -= 1
    return v
