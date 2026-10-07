import logging
import customtkinter as ctk

from src.models.bdd import BaseDeDonne
from src.controlller.vehicule_controller import VehiculeController
from src.controlller.intervention_controller import InterventionController
from src.controlller.rule_controller import MaintenanceRuleController

from src.view.sidebar_view import Sidebar,Header


logger = logging.getLogger(__name__)


class MainController:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.database = BaseDeDonne()
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        side = Sidebar(self.master, self)
        side.grid(
            row=1,
            column=0,
            pady=(0, 10),
            padx=(10, 0),
            sticky="nsew"
        )

        head = Header(self.master)
        head.grid(
            row=0,
            columnspan=2,
            padx=10,
            pady=(10, 0),
            sticky="nsew"
        )

        self.intervention = InterventionController(self.master, self.database)
        self.vehicule = VehiculeController(self.master, self.database)
        self.rule = MaintenanceRuleController(self.master, self.database)
        self.show_vehicule()

    def show_vehicule(self) -> None:
        self.intervention.list_intervention.grid_forget()
        self.vehicule.list_vehicule.grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew"
        )
        self.vehicule.afficher_vehicule()
    
    def show_intervention(self) -> None:
        self.vehicule.list_vehicule.grid_forget()
        self.intervention.list_intervention.grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew"
        )
        self.intervention.afficher_intervention()

    def show_rule(self)  -> None:
        self.rule.show_add()

    def on_close(self) -> None:
        try :
            self.database.close()

        except:
            logger.exception("Erreur lors de la fermeture de la DB")

        self.master.destroy()