from dataclasses import dataclass


@dataclass
class Vehicule:
    ID : str
    matricule : str
    marque : str
    modele : str
    annee : int
    kilometrage : int
    

