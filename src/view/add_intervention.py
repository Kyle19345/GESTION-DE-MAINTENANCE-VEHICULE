import customtkinter as ctk
from typing import Callable


class InterventionView(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        ajouter: Callable = None,
        on_suppr: Callable = None
    ):
        super().__init__(master)
        self.title("Editer Intervention")
        self.on_suppr = on_suppr
        self.resizable(False, False)   
        self.transient(master)
        self.grab_set()    

        self.frame_container = ctk.CTkFrame(
            self,
            corner_radius=12,
            border_width=1
        )
        self.frame_container.pack(
            expand="True",
            fill="both",
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            self.frame_container,
            text="Intervention",
            font=("Poppins", 18, "bold")).grid(row=0,column=0,pady=10
        )

        self.labels = [
            "Référence",
            "Type d'intervention",
            "Date d'intervention",
            "Durée",
            "Vehicule",
            "Technicien"
        ]
        placeholder = [
            "Ex: INT-2025-001",
            "Ex: Vidange moteur",
            "Ex: 2025-10-18",
            "Ex: 2h",
            "Ex: ABC-1234",
            "Ex: Jean Dupont"
        ]
        self.entries = {}

        for i,label in enumerate(self.labels):
            ctk.CTkLabel(
                self.frame_container,
                text=label,
                font=("Poppins", 13)
            ).grid(
                row=i+1,
                column=0,
                pady=8,
                padx=30,
                sticky="e"
            )
            entry = ctk.CTkEntry(
                self.frame_container,
                width=300,
                placeholder_text=placeholder[i]
            )
            entry.grid(
                row=i+1,
                column=1,
                pady=8,
                padx=30
            )
            self.entries[label.replace(" ","_")] = entry

        ctk.CTkLabel(
            self.frame_container,
            text="Description",
            font=("Poppins", 13)
        ).grid(
            row=len(self.labels)+3,
            column=0,
            padx=30,
            sticky="e"
        )
        self.description = ctk.CTkTextbox(
            self.frame_container,
            height=75,
            width=300
        )
        self.description.grid(
            row=len(self.labels)+3,
            column=1,
            padx=30,
            pady=8
        )

        ctk.CTkButton(
            self.frame_container,
            text="💾 Enregistrer",
            command=ajouter,
            width=170,
            height=35,
            font=("Poppins", 14)
        ).grid(
            row=len(self.labels)+4,
            column=1,
            pady=20,
            padx=20,
            sticky="e"
        )

    def afficher(self, intervention) -> None:
        lbl_statut = ctk.CTkLabel(
            self.frame_container,
            text="Statut",
            font=("Poppins", 13)
        )
        lbl_statut.grid(
            row=len(self.labels)+2, 
            column=0,
            padx=30,
            pady=8,
            sticky="e"
        )

        self.statut = ctk.CTkComboBox(
            self.frame_container,
            width=300,
            values=["Planifié", "En cours", "Réalisé"],
            state="readonly"
        )
        self.statut.set("planifié")
        self.statut.grid(
            row=len(self.labels)+2,
            column=1,
            padx=30,
            pady=8
        )

        ctk.CTkButton(
            self.frame_container,
            text="🗑️ Supprimer",
            fg_color="#a74a4a",
            hover_color="#b85b5b",
            command=self.on_suppr,
            width=170,
            height=35,
            font=("Poppins" ,14)
        ).grid(
            row=len(self.labels)+4,
            column=0,
            pady=20,
            padx=20
        )

        self.suppression_champ()
        self.entries["Référence"].insert(0,intervention.ref)
        self.entries["Référence"].configure(state="readonly")
        self.entries["Date_d'intervention"].insert(0,intervention.date_intervention)
        self.entries["Type_d'intervention"].insert(0,intervention.type_intervention)
        self.entries["Durée"].insert(0,intervention.dure)
        self.entries["Vehicule"].insert(0,intervention.vehicule)
        self.entries["Vehicule"].configure(state="readonly")
        self.entries["Technicien"].insert(0, intervention.technicien)
        self.description.insert("1.0", intervention.description)
    
    def get_entre_with_statut(self) -> None:
        return{
            'ref': self.entries["Référence"].get().strip(),
            "date": self.entries["Date_d'intervention"].get().strip(),
            "type":self.entries["Type_d'intervention"].get().strip(),
            "dure": self.entries["Durée"].get().strip(),
            "vehicule": self.entries["Vehicule"].get().strip(),
            "technicien": self.entries["Technicien"].get().strip(),
            "description": self.description.get("1.0","end").strip(),
            "statut": self.statut.get()
        }
    
    def get_entre(self) -> None :
        return{
            'ref': self.entries["Référence"].get().strip(),
            "date": self.entries["Date_d'intervention"].get().strip(),
            "type":self.entries["Type_d'intervention"].get().strip(),
            "dure": self.entries["Durée"].get().strip(),
            "vehicule": self.entries["Vehicule"].get().strip(),
            "technicien": self.entries["Technicien"].get().strip(),
            "description": self.description.get("1.0","end").strip(),
            }

    def suppression_champ(self) -> None:
        self.entries["Référence"].delete("0", "end")
        self.entries["Date_d'intervention"].delete("0", "end")
        self.entries["Type_d'intervention"].delete("0", "end")
        self.entries["Durée"].delete("0", "end")
        self.entries["Vehicule"].delete("0", "end")
        self.entries["Technicien"].delete("0", "end")
        self.description.delete("1.0", "end")
    
    def suppr_selected(self):
        return self.entries["Référence"].get()


if __name__ == "__main__":
    root = ctk.CTk()
    app = InterventionView(root)
    root.mainloop()
            