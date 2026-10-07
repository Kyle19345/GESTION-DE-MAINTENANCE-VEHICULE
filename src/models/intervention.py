from dataclasses import dataclass


@dataclass
class Intervention:
    ref : str
    description : str 
    type_intervention : str
    date_intervention : str
    vehicule : str
    dure : int
    technicien : str = "-"   
    statut : str = "Planifié" #/Réalisé / En cours
    rule_id : str = None

    def return_dico(self):
        return{
            "ref": self.ref,
            "description": self.description,
            "type_intervention": self.type_intervention,
            "date_intervention": self.date_intervention,
            "vehicule": self.vehicule,
            "dure": self.dure,
            "Technicien": self.technicien,
            "statut": self.technicien
        }

