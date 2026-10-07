import csv

from typing import Dict
from datetime import datetime


def est_date_valide(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True

    except Exception:
        return False
    
def compute_rule_status(
    current_km: int,
    last_service_km: int | None,
    interval_km: int | None,
    notify_before_km: int | None
    ) -> dict:
    """
    Retourne dict contenant next_due_km et status ('due'|'soon'|None).
    Pure function -> facile à unit tester.
    """
    if interval_km is None:
        return {"next_due_km": None, "status": None}

    last_km = last_service_km if last_service_km is not None else 0
    next_due_km = last_km + interval_km
    notify_before = notify_before_km or 0

    if current_km >= next_due_km:
        status = "due"
    
    elif current_km >= (next_due_km - notify_before):
        status = "soon"

    else:
        status = None

    return {"next_due_km": next_due_km, "status": status}

def write_csv(donne: Dict[str, str]) -> None:
    champs = [
        "ref",
        "description",
        "type_intervention",
        "date_intervention",
        "vehicule",
        "dure",
        "Technicien",
        "statut"
    ]
    
    with open(
        "intervention.csv",
        "w",
        encoding="utf-8",
        newline=""
    ) as csvfile:
        data = csv.DictWriter(csvfile, fieldnames=champs)
        data.writeheader()
        data.writerows(donne)
