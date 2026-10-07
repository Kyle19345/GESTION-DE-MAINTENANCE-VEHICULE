import logging
import customtkinter as ctk

from src.view.add_intervention import InterventionView
from src.view.list_intervention import ListIntervention
from src.view.message_view import ConfirmationBox
from src.view.message_view import MessageBox

from src.models.intervention import Intervention
from src.models.bdd import BaseDeDonne
from src.config.tool import est_date_valide, write_csv


logger = logging.getLogger(__name__)


class InterventionController:
    def __init__(
        self,
        master: ctk.CTk,
        database: BaseDeDonne
    ):
        self.master = master
        self.database = database
        self.list_intervention = ListIntervention(
            self.master,
            on_add=self.show_add,
            on_select=self.show_update,
            imprimer=self.imprimer_csv
        )

    def show_add(self) -> None:
        self.add_intervention = InterventionView(
            self.master,
            ajouter=self.ajouter_intervention
        )

    def show_update(self, intervention: Intervention) -> None:
        self.update_intervention = InterventionView(
            self.master,
            ajouter=self.enregistrer_maj,
            on_suppr=self.suppr_intervention
        )
        self.update_intervention.afficher(intervention)

    def ajouter_intervention(self) -> None:
        donne = self.add_intervention.get_entre()

        for entry in donne.values():
            if not entry:
                MessageBox(
                    self.master,
                    "Veuillez remplir tous les champs",
                    type="error"
                )
                return

        try:
            dure = int(donne.get("dure", 0))

        except (TypeError,ValueError):
            MessageBox(
                self.master,
                "La dure doit etre un nombre entier",
                type="error"
            )
            return

        valide = est_date_valide(donne["date"])
        if not valide:
            MessageBox(
                self.master,
                "La date saisie est invalide",
                type="error"
            )
            return

        intervention = Intervention(
            ref= donne["ref"],
            description= donne["description"],
            type_intervention=donne["type"],
            date_intervention=donne["date"],
            vehicule=donne["vehicule"],
            dure=dure,
            technicien=donne["technicien"]
        )
        try:
            logger.info("Intervention: %s", intervention)
            self.database.add_intervention(intervention)
            MessageBox(
                self.master,
                f"Intervention enregistrée",
                type="success"
            )
            self.add_intervention.suppression_champ()
            self.afficher_intervention()

        except Exception:
            MessageBox(
                self.master,
                f"Référence ou machine invalide",
                type="error"
            )

    def enregistrer_maj(self) -> None:
        donne = self.update_intervention.get_entre_with_statut()

        for entry in donne.values():
            if not entry:
                MessageBox(
                    self.master,
                    "Veuillez remplir tous les champs",
                    type="error"
                )
                return

        try:
            dure = int(donne.get("dure", 0))

        except (TypeError, ValueError):
            MessageBox(
                self.master,
                "La dure doit etre un nombre entier",
                type="error"
            )
            return

        valide = est_date_valide(donne["date"])

        if not valide:
            MessageBox(
                self.master,
                "La date saisie est invalide",
                type="error"
            )
            return

        intervention = Intervention(
            ref= donne["ref"],
            description= donne["description"],
            type_intervention=donne["type"],
            date_intervention=donne["date"],
            vehicule=donne["vehicule"],
            dure=dure,
            technicien=donne["technicien"],
            statut=donne["statut"]
        )

        try : 
            logger.info("Intervention: %s", intervention)
            self.database.update_intervention(intervention)
            MessageBox(
                self.master,
                "Intervention mise à jour",
                type="success"
            )
            self.afficher_intervention()

        except Exception as e:
            MessageBox(
                self.master,
                f"Erreur {e}",
                type="error"
            )

    def afficher_intervention(self) -> None:
        donne = self.database.get_all_intervention()
        self.list_intervention.afficher(donne)

    def suppr_intervention(self) -> None:
        ConfirmationBox(
            self.master,
            on_valid=self.confirm_delete
        )

    def imprimer_csv(self) -> None:
        donnes = self.database.get_all_intervention_for_csv()
        write_csv(donnes)
        MessageBox(
            self.master,
            "Fichier csv crée",
            type = "success"
        )

    def confirm_delete(self) -> None:
        intervention = self.update_intervention.suppr_selected()
        self.database.delete_intervention(intervention)
        self.update_intervention.destroy()
        self.afficher_intervention()
