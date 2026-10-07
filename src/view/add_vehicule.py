import customtkinter as ctk
from src.models.vehicule import Vehicule


class addvehicule(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        on_add: callable = None,
        on_suppr: callable = None
    ):
        super().__init__(master)   
        self.title("Editer vehicule")
        self.on_suppr = on_suppr
        self.resizable(False, False)   
        self.transient(master)
        self.grab_set()    

        self.container = ctk.CTkFrame(
            self,
            corner_radius=12,
            border_width=1
        )
        self.container.grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="nsew"
        )
        ctk.CTkLabel(
            self.container,
            text="Editer vehicule",
            font=("Poppins", 18, "bold")
        ).grid(padx=20, pady=10)

        self.labels = ["ID","Matricule","Marque","Modele","Année","Kilométrage"]
        placeholder = ["Ex: 1","Ex: ABC-1234","Ex: Toyota","Ex: Corolla","Ex: 2015", "Ex: 85000"]

        self.entries = {}

        for i,label in enumerate(self.labels):
            ctk.CTkLabel(
                self.container,
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
                self.container,
                width=300,
                placeholder_text=placeholder[i]
            )
            entry.grid(
                row=i+1,
                column=1,
                pady=8,
                padx=50
            )
            self.entries[label.replace(" ","_")] = entry
        
        ctk.CTkButton(
            self.container,
            text="💾 Enregistrer",
            command=on_add,
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
    
    def afficher(self, vehicule: Vehicule) -> None:
        ctk.CTkButton(
            self.container,
            text="🗑️ Supprimer",
            fg_color="#a74a4a",
            hover_color="#b85b5b",
            command=self.on_suppr,
            width=170,
            height=35,
            font=("Poppins", 14)
        ).grid(
            row=len(self.labels)+4,
            column=0,
            pady=20,
            padx=20,
            sticky="e"
        )
            
        self.entries["ID"].insert(0,vehicule.ID)
        self.entries["ID"].configure(state = "readonly")
        self.entries["Matricule"].insert(0,vehicule.matricule)
        self.entries["Matricule"].configure(state = "readonly")
        self.entries["Marque"].insert(0,vehicule.marque)
        self.entries["Marque"].configure(state = "readonly")
        self.entries["Modele"].insert(0,vehicule.modele)
        self.entries["Modele"].configure(state = "readonly")
        self.entries["Année"].insert(0,vehicule.annee)
        self.entries["Année"].configure(state = "readonly")
        self.entries["Kilométrage"].insert(0,vehicule.kilometrage)
        
    def get_entre(self) -> None:
        return {
            "id": self.entries["ID"].get().strip(),
            "matricule": self.entries["Matricule"].get().strip(),
            "marque": self.entries["Marque"].get().strip(),
            "modele": self.entries["Modele"].get().strip(),
            "anne": self.entries["Année"].get().strip(),
            "kilometrage": self.entries["Kilométrage"].get().strip()
        }
        
    def delete_champ(self) -> None:
        self.entries["ID"].delete(0,"end")
        self.entries["Matricule"].delete(0,"end")
        self.entries["Marque"].delete(0,"end")
        self.entries["Modele"].delete(0,"end")
        self.entries["Année"].delete(0,"end")
        self.entries["Kilométrage"].delete(0,"end")

    def get_vehicule_delete(self)-> None:
        return self.entries["ID"].get()


if __name__ == "__main__":
    root = ctk.CTk()
    app = addvehicule(root)
    root.mainloop()    

