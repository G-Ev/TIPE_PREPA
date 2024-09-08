class Drone():

  def __init__(self, graphe, l_client=[], autonomie=1800):  # Autonomie en s
    self.graphe = graphe
    self.autonomie = autonomie
    self.liste_client = l_client
    self.nombre_client = len(l_client)
    self.speed = 3  # speed en m/s
    self.noeud_courant = graphe.noms_som["Base"]


## Getter/Setter :

  def get_autonomie(self):
    return self.autonomie

  def get_liste_client(self):
    return self.liste_client

  def get_speed(self):
    return self.speed

  def get_noeud_courant(self):
    return self.noeud_courant

  def _set_speed(self, new_speed):
    self.speed = new_speed

  def _set_autonomie(self, new_auto):
    self.autonomie = new_auto   
    
## Affichage :    
    
  def print_etat(self):
    """
    In : None
    Out : None
    Goal : informe par effet de bord de l'etat global du drone (nb de clients et autonomie restante ainsi que sa position actuelle)
    """
    print(
      "{} client(s) restant a livrer.\nPosition du drone : {}. \nAutonomie restante: {} minutes.\n"
      .format(len(self.get_liste_client()),
              self.get_noeud_courant().get_nom(),
              round(self.get_autonomie() / 60, 1)))

## Autres méthodes :
   
  def deplacement(self, n):
    """
    In : un sommet n [Noeud]
    Out : None
    Goal : determine si le drone courant peut se déplacer du sommet ou il est a celui pris en parametre en fonction de son autonomie restante; si oui effectue le deplacement, sinon previent l'utilisateur
    """
    d = self.graphe.get_arcs()[self.noeud_courant.get_nom()][n.get_nom()]

    assert self.autonomie >= d / self.speed, (
      "Batterie restante dans le drone insuffisante")

    self.autonomie -= d / self.speed
    self.noeud_courant = n
    print("Destination atteinte")

  def trajet(self):
    """
    In : None
    Out : None
    Goal : lance la mission du drone : il va livrer les clients dans l'ordre donne par la liste
    """
    for i in range(len(self.liste_client)):
      self.print_etat()
      self.deplacement(self.liste_client.pop(0))