import customtkinter as ctk
import logging

from src.view.add_rule import addRule
from src.view.message_view import ConfirmationBox,MessageBox
from src.models.maintenance_rule import MaintenanceRule
from src.models.bdd import BaseDeDonne


logger = logging.getLogger(__name__)


class MaintenanceRuleController:
    def __init__(
        self,
        master: ctk.CTk,
        database: BaseDeDonne
    ):
        self.master = master
        self.database = database

    def show_add(self) -> None:
        self.addrule = addRule(
            self.master,
            on_add=self.ajouter_rule,
            on_suppr=self.suppr_rule
        )
        self.afficher_rule()
    
    def ajouter_rule(self) -> None:
        donne = self.addrule.get_entre()
        entry = [
            donne["Description"],
            donne["Intervalle_Km"],
            donne["Notify_before_Km"]
        ]
        for e in entry:
            if not e:
                MessageBox(
                    self.master,
                    "Veuillez remplir tous les champs",
                    type="error"
                )
                return
        
        try:
            intervalle = int(donne["Intervalle_Km"])
            notify = int(donne["Notify_before_Km"])

        except (TypeError, ValueError):
            MessageBox(
                self.master,
                "L'intervalle et la notofication doit etre un nombre entier",
                type="error"
            )
            return

        rule = MaintenanceRule(
            description=donne["Description"],
            intervalle_km=intervalle,
            notify_before=notify,
            create_auto=donne["Active"]
        )
       
        logger.info("Rule %s", rule)
        self.database.add_maintenance_rule(rule)

        MessageBox(
            self.master,
            f"Regle Enregistrer",
            type="success"
        )
        self.afficher_rule()
    
    def afficher_rule(self) -> None:
        donne = self.database.get_rule()
        self.addrule.afficher(donne)

    def suppr_rule(self) -> None:
        ConfirmationBox(
            self.master,
            on_valid=self.confirm_delete
        )
    
    def confirm_delete(self) -> None:
        rule = self.addrule.get_suppr_selected()
        self.database.delete_maintenance_rule(rule)
        self.addrule.destroy()
        self.afficher_rule()

    def afficher_rule(self) -> None:
        donne = self.database.get_rule()
        self.addrule.afficher(donne)

                