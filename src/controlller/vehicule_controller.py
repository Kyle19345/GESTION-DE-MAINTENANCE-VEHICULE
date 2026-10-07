import logging
import customtkinter as ctk

from typing import List, Dict
from datetime import date

from src.view.add_vehicule import addvehicule
from src.view.list_vehicule import ListVehicule
from src.view.message_view import MessageBox, ConfirmationBox
from src.models.vehicule import Vehicule
from src.models.intervention import Intervention
from src.models.bdd import BaseDeDonne
from src.config.tool import compute_rule_status


logger = logging.getLogger(__name__)


class VehiculeController:
    def __init__(
        self,
        master: ctk.CTk,
        database: BaseDeDonne
    ):
        self.master = master
        self.database = database
        self.list_vehicule = ListVehicule(
            self.master,
            on_add=self.show_add,
            on_select=self.show_update
        )
    
    def show_add(self) -> None:
        self.add_vehicule = addvehicule(
            self.master,
            on_add=self.ajouter_vehicule
        )
    
    def show_update(self,vehicule) -> None:
        self.update_vehicule = addvehicule(
            self.master,
            on_add=self.enregistrer_maj,
            on_suppr=self.suppr_vehicule
        )
        self.update_vehicule.afficher(vehicule)
    
    def ajouter_vehicule(self) -> None:
        donne = self.add_vehicule.get_entre()

        for entry in donne.values():
            if not entry:
                MessageBox(
                    self.master,
                    "Veuillez remplir tous les champs",
                    type="error"
                )
                return

        try:
            km = int(donne["kilometrage"])   

        except (TypeError, ValueError):
            MessageBox(
                self.master,
                "Le kilométrage doit etre un nombre entier",
                type="error"
            )
            return
        
        vehicule = Vehicule(
            ID=donne["id"],
            matricule=donne[ "matricule"],
            marque=donne["marque"],
            modele=donne["modele"],
            annee=donne["anne"],
            kilometrage=km
        )

        try:
            logger.info("Vehicule %s", vehicule)
            self.database.add_vehicule(vehicule)
            MessageBox(
                self.master,
                f"Vehicule Enregistrer",
                type="success"
            )
            self.afficher_vehicule()

        except Exception:
            MessageBox(
                self.master,
                f"L'ID saisie est invalide",
                type="error"
            )
    
    def enregistrer_maj(self) -> None:
        donne = self.update_vehicule.get_entre()
        for entry in donne.values():
            if not entry:
                MessageBox(
                    self.master,
                    "Veuillez remplir tous les champs",
                    type="error"
                )
                return

        try:
            km = int(donne["kilometrage"])

        except (TypeError, ValueError):
            MessageBox(
                self.master,
                "Le kilométrage doit etre un nombre entier",
                type="error"
            )
            return

        vehicule = Vehicule(
            ID=donne["id"],
            matricule=donne["matricule"],
            marque=donne["marque"],
            modele=donne["modele"],
            annee=donne["anne"],
            kilometrage=km
        )

        logger.info("Vehicule %s", vehicule)
        self.database.update_vehicule(vehicule)

        MessageBox(
            self.master,
            "Mise à jour du vehicule effectué",
            type="success"
        )
        self.afficher_vehicule()

        rules = self.verify_mileage_rules(donne["id"], km)

        reminders = []
        created = [] 

        for r in rules:
            status = r.get("status") or r.get("statuts")
            create_auto = int(r.get("create_automatically", 0))
            rule_id = r.get("rule_id")
            rule_name = r.get("rule_name", "Règle inconnue")

           
            if status == "soon":
                next_due = r.get("next_due_km") or r.get("next_due") or "n/a"
                reminders.append(
                    f"{rule_name} (règle {rule_id}) — échéance ~ {next_due} km"
                )
                logger.info(
                    "Rappel (soon) pour véhicule %s règle %s (next_due=%s)",
                    donne["id"],
                    rule_id,
                    next_due
                )
                continue
          
            if status == "due" and create_auto == 1:
                ref = f"AUTO-{donne['id']}-{rule_id}"
                inter = Intervention(
                    ref=ref,
                    description=f"Intervention automatique: {rule_name} — déclenchée par km {km} (status=due)",
                    type_intervention=rule_name,
                    date_intervention=date.today().isoformat(),
                    vehicule=donne["id"],
                    dure=None,
                    technicien="Système",
                    statut="Planifiée"
                )

                try:
                    res = None
                    if hasattr(self.database, "insert_intervention_if_not_existts"):
                        
                        res = self.database.insert_intervention_if_not_existts(inter, donne["id"], rule_id)
                        if res:
                            logger.info("Intervention automatique insérée (transaction) : %s", ref)
                    else:
                        if hasattr(self.database, "find_intervention_by_ref"):
                            if not self.database.find_intervention_by_ref(ref):
                                if hasattr(self.database, "add_intervention"):
                                    self.database.add_intervention(inter)
                                    res = {"ref": ref, "vehicule": donne["id"], "rule_id": rule_id}
                                    logger.info("Intervention automatique (fallback) ajoutée : %s", ref)

                            else:
                                logger.info("Intervention %s déjà existante — skip", ref)

                        else:
                            if hasattr(self.database, "add_intervention"):
                                self.database.add_intervention(inter)
                                res = {"ref": ref, "vehicule": donne["id"], "rule_id": rule_id}
                                logger.warning("Fallback sans vérification : intervention ajoutée (risque doublon) : %s", ref)

                    if res:
                        created.append(res)

                except Exception:
                    logger.exception("Erreur création auto pour véhicule %s règle %s", donne["id"], rule_id)
                   
        if reminders:
            msg = "Rappel(s) de maintenance prochain(s) :\n" + "\n".join(reminders)
            MessageBox(
                self.master,
                msg,
                type="info"
            )

        if created:
            lines = [f"{len(created)} intervention(s) automatique(s) créée(s):"]

            for c in created[:8]:
                lines.append(f"- {c.get('ref', c.get('description', ''))}")
            if len(created) > 8:
                lines.append("...et d'autres")

            MessageBox(
                self.master,
                "\n".join(lines),
                type="success"
            )

    def afficher_vehicule(self) -> None:
         donne = self.database.get_all_vehicule()
         self.list_vehicule.afficher(donne)
    
    def verify_mileage_rules(
        self,
        vehicle_id,
        current_km: int
    ) -> List[Dict]:
        rows = self.database.get_rules_for_vehicule(vehicle_id)

        results = []
        for row in rows:
            rule_id, name, interval_km, notify_before_km, create_auto, last_km = row

            status_info = compute_rule_status(
                current_km=current_km,
                last_service_km=last_km,
                interval_km=interval_km,
                notify_before_km=notify_before_km
            )

            results.append({
                "rule_id": rule_id,
                "rule_name": name,
                "last_km": last_km,
                "interval_km": interval_km,
                "next_due_km": status_info["next_due_km"],
                "notify_before_km": notify_before_km or 0,
                "create_automatically": int(create_auto or 0),
                "status": status_info["status"],
                "current_km": current_km
            })

        return results
    
    def suppr_vehicule(self) -> None:
        ConfirmationBox(
            self.master,
            on_valid=self.confirm_suppr
        )
        
    def confirm_suppr(self) -> None:
        vehicule = self.update_vehicule.get_vehicule_delete()
        self.database.delete_vehicule(vehicule)
        self.update_vehicule.destroy()
        self.afficher_vehicule()
