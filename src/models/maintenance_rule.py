from dataclasses import dataclass


@dataclass
class MaintenanceRule:
    description : str
    intervalle_km : int
    notify_before : int
    create_auto : int = 0
   