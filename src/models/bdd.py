import sqlite3
import logging

from datetime import date,datetime
from typing import List

from src.models.vehicule import Vehicule
from src.models.intervention import Intervention
from src.models.maintenance_rule import MaintenanceRule


logger = logging.getLogger(__name__)


class BaseDeDonne:
    def __init__(
        self,
        path="config/Database.db"
    ):
        self.com = sqlite3.connect(path)
        self.cur = self.com.cursor()
        
        self.cur.execute("PRAGMA foreign_keys=ON")

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS table_vehicule(
                ID TEXT UNIQUE,
                matricule TEXT UNIQUE NOT NULL,
                marque TEXT NOT NULL,
                modele TEXT NOT NULL,
                anne INTEGER NOT NULL,
                kilometrage INTEGER NOT NULL
                )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS intervention (
                ref TEXT UNIQUE,
                description TEXT NOT NULL,
                type TEXT NOT NULL,
                date_intervention TEXT NOT NULL,
                vehicule TEXT NOT NULL,
                dure INTEGER,
                technicien TEXT NOT NULL,
                statut TEXT NOT NULL,
                rule_id INTEGER DEFAULT 0,
                FOREIGN KEY (vehicule) REFERENCES table_vehicule (ID) ON DELETE CASCADE
                )
            """
            )   

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS maintenance_rule(
                id INTEGER PRIMARY KEY AUTOINCREMENT,   
                description TEXT NOT NULL,
                intervall_km INTEGER,
                notify_before_km INTEGER DEFAULT 500,
                create_automatically INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1
                )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vehicule_maintenance(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicule_id INTEGER NOT NULL,
                rule_id INTEGER NOT NULL,
                last_service_km INTEGER,
                UNIQUE(vehicule_id,rule_id),
                FOREIGN KEY(vehicule_id) REFERENCES table_vehicule (ID) ON DELETE CASCADE,
                FOREIGN KEY(rule_id) REFERENCES maintenance_rule (id) ON DELETE CASCADE
                )
            """
        )
        
        self.com.commit()
        logger.info("Base de données initialisée") 

    def add_intervention(self, intervention: Intervention) -> None:
        try:
            self.cur.execute(
                """
                INSERT INTO intervention(
                ref,
                description,
                type,
                date_intervention,
                vehicule,
                dure,
                technicien,
                statut
                ) VALUES(?,?,?,?,?,?,?,?)""",
                (
                    intervention.ref,
                    intervention.description,
                    intervention.type_intervention,
                    intervention.date_intervention,
                    intervention.vehicule,
                    intervention.dure,
                    intervention.technicien,
                    intervention.statut
                )
            )
            self.com.commit()
            logger.info("Intervention ajouter")

        except Exception:
            logger.exception("Erreur lors de l'ajout")
            raise
    
    def add_vehicule(self, vehicule: Vehicule) -> None:
        try:
            self.cur.execute(
                """
                INSERT INTO table_vehicule(
                    ID,
                    matricule,
                    marque,modele,
                    anne,
                    kilometrage
                ) VALUES(?,?,?,?,?,?)""",
                (
                    vehicule.ID,
                    vehicule.matricule,
                    vehicule.marque,
                    vehicule.modele,
                    vehicule.annee,
                    vehicule.kilometrage
                )
            )
            vehicule_id = vehicule.ID

            self.cur.execute(
                """
                INSERT INTO vehicule_maintenance(
                    vehicule_id,
                    rule_id,
                    last_service_km
                ) SELECT ?, id, NULL FROM maintenance_rule WHERE active = 1
                """, (vehicule_id, )
            )
            self.com.commit()
            logger.info("Vehicule ajouter")
            return vehicule_id

        except Exception:
            logger.exception("Erreur lors de l'ajout")
            raise
    
    def add_maintenance_rule(self, maintenance_rule) -> None:
        try:
            self.cur.execute(
                """
                INSERT INTO maintenance_rule(
                    description,
                    intervall_km,
                    notify_before_km,
                    create_automatically
                ) VALUES(?, ?, ?, ?)
                """,
                (
                    maintenance_rule.description,
                    maintenance_rule.intervalle_km,
                    maintenance_rule.notify_before,
                    maintenance_rule.create_auto
                )
            )
            self.com.commit()
            logger.info("Regle ajouté")

        except:
            logger.exception("Erreur lors de l'ajout)")
            raise

    def get_all_intervention(self) -> List[Intervention]:
        self.cur.execute(
            """
            SELECT * FROM intervention ORDER BY date_intervention ASC
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction intervention effectué depuis la Bdd")
        return [Intervention(*row) for row in rows]

    def get_all_intervention_for_csv(self) -> List[Intervention]:
        self.cur.execute("SELECT * FROM intervention")
        rows = self.cur.fetchall()
        return[Intervention(*row).return_dico() for row in rows]

    def get_all_vehicule(self) -> List[Vehicule]:
        self.cur.execute("SELECT * FROM table_vehicule ")
        rows = self.cur.fetchall()

        logger.info("Extraction vehicule effectué depuis la Bdd")
        return [Vehicule(*row) for row in rows]
    
    def get_rule(self) -> List[MaintenanceRule]:
        self.cur.execute(
            """
            SELECT description, intervall_km, notify_before_km,create_automatically FROM maintenance_rule
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction regle effectué")

        return[MaintenanceRule(*row) for row in rows]

    def update_intervention(
        self,
        intervention: Intervention
    ) -> None:
        try:
            self.cur.execute(
                """ UPDATE intervention
                        SET description = ?,
                        type = ?,
                        date_intervention = ?,
                        dure = ?,
                        technicien = ?,
                        statut = ?
                        WHERE ref = ?
                """,
                (
                    intervention.description,
                    intervention.type_intervention,
                    intervention.date_intervention,
                    intervention.dure,
                    intervention.technicien,
                    intervention.statut,
                    intervention.ref
                )
            )
            
            if intervention.statut == "Réalisé":
                self.cur.execute(
                    """
                    SELECT vehicule,rule_id FROM intervention WHERE ref = ? 
                    """,
                    (intervention.ref, )
                )
                row = self.cur.fetchone()

                if row : 
                    vehicule_id, rule_id = row
                    self.cur.execute(
                        """
                        SELECT kilometrage FROM table_vehicule WHERE ID = ?
                        """,
                        (vehicule_id, )
                    )

                    km_row = self.cur.fetchone()
                    current_km = km_row[0] if km_row else None

                    if current_km is not None:
                        self.cur.execute(
                            """
                            UPDATE vehicule_maintenance
                            SET last_service_km = ?
                            WHERE vehicule_id = ? AND rule_id = ?
                            """, 
                            (current_km, vehicule_id, rule_id)
                        )
            
            self.com.commit()
            logger.info("Mise à jour intervention effectuée et last_service_km mis à jour si applicable")
        
        except:
            try:
                self.com.rollback()

            except:
                logger.exception("Erreur dans la mise à jour des données")
        
    def update_vehicule(
        self,
        vehicule: Vehicule
    ) -> None:
        try:
            self.cur.execute(
                """
                UPDATE table_vehicule
                    SET kilometrage = ?
                    WHERE ID = ?
                """,
                (vehicule.kilometrage, vehicule.ID)
            )
            self.com.commit()
            logger.info("Mise à jour effectué")

        except:
            try:
                self.com.rollback()

            except:
                logger.exception("Erreur dans la mise à jour des données")
    
    def delete_intervention(
        self,
        intervention: Intervention
    ) -> None:
        try:
            self.cur.execute(
                """
                DELETE FROM intervention WHERE ref = ?
                """,
                (intervention, )
            )
            self.com.commit()
            logger.info("Suppression intervention effectué")

        except Exception as e:
            logger.info(
                f"""
                Erreur lors de la suppression de l'intervention {intervention} : {e}
                """
            )

    def delete_vehicule(
        self,
        vehicule: Vehicule
    ) -> None:
        try:
            self.cur.execute(
                """
                DELETE FROM table_vehicule WHERE ID = ?
                """,
                (vehicule, )
            )
            self.com.commit()
            logger.info("Suppression vehicule effectué")

        except Exception as e:
            logger.error(
                f"""
                Erreur lors de la suppression du véhicule {vehicule} : {e}
                """
            )
        
    def delete_maintenance_rule(self, rule) -> None:
        try:
            self.cur.execute(
                """
                DELETE FROM maintenance_rule WHERE description = ?
                """,
                (rule, )
            )
            self.com.commit()
            logger.info("Suppression règle effectué")

        except Exception as e: 
            logger.info(
                f"""Erreur lors de la suppression de l'élement {rule} : {e}"""
            )

    def get_rules_for_vehicule(self, vehicule_id) -> None:
        """
        Vérifie toutes les règles actives pour le véhicule et renvoie
        une liste d'entrées décrivant l'état (due/soon/ok) pour chaque règle.
        Ne crée pas d'intervention : juste vérification.
        """
        self.cur.execute(
            """
            SELECT 
                r.id, 
                r.description,
                r.intervall_km,
                r.notify_before_km,
                r.create_automatically,
                vm.last_service_km
                FROM maintenance_rule r
                JOIN vehicule_maintenance vm ON vm.rule_id = r.id
                WHERE vm.vehicule_id = ? AND r.active = 1
                """,
                (vehicule_id, )
        )
        return self.cur.fetchall()
    
    def insert_intervention_if_not_existts(
        self,
        intervention,
        vehicule_id,
        rule_id
    ) -> None:
        try:
            self.cur.execute("BEGIN IMMEDIATE")
            self.cur.execute(
                """
                SELECT COUNT(*) FROM intervention
                WHERE vehicule = ? AND rule_id = ? AND statut = 'Planifié'
                """,
                (vehicule_id,rule_id)
            )

            row = self.cur.fetchone()
            if row and row[0] > 0:
                try:
                    self.cur.execute("COMMIT")

                except Exception:
                    pass

                logger.debug(
                    """
                    Intervention existante trouvée pour vehicule = %s rule = %s
                    """,
                    vehicule_id,rule_id
                )
                return None
    
            ts_iso = date.today().strftime("%d/%m/%Y")
            ts = int(datetime.utcnow().timestamp())
            ref = f"Auto-{vehicule_id}-{rule_id}--{ts}"
            
            date_int = ts_iso
            type_inter = getattr(
                intervention,
                "type_intervention", 
                None
            ) or getattr(intervention, "type", None) or f"Rule-{rule_id}"

            desc = getattr(
                intervention,
                "description",
                ""
            ) or f"Intervention automatique (règle {rule_id})"

            dure_val = getattr(intervention, "dure", None) or 0
            tech = getattr(intervention, "technicien", None) or "Système"
            statut_val = getattr(intervention, "statut", None) or "Planifiée"

            self.cur.execute(
                """
                INSERT INTO intervention (
                    ref, description, type, date_intervention, vehicule, dure, technicien, statut, rule_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (ref, desc, type_inter, date_int, vehicule_id, dure_val, tech, statut_val, rule_id)
            )

            self.com.commit()
            logger.info(
                """
                Auto-created intervention %s for vehicule %s rule %s
                """,
                ref,
                vehicule_id,
                rule_id
            )

            return {
                "ref": ref,
                "vehicule_id": vehicule_id,
                "rule_id": rule_id,
                "description": desc,
                "date_intervention": date_int,
                "dure": dure_val,
                "technicien": tech,
                "statut": statut_val
            }

        except Exception:
            try:
                self.com.rollback()

            except Exception:
                pass
            logger.exception("Erreur lors de la création d'intervention")

    def close(self) -> None:
        try :
            self.com.commit()

        except:
            pass

        try:
            self.com.close()
            logger.info("Bdd fermé ")

        except Exception as e:
            logger.exception(f"Erreur {e} dans la fermeture de la Bdd")
        
