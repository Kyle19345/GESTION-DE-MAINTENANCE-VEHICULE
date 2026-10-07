import customtkinter as ctk

from tkinter import ttk, font
from typing import Callable


def ellipsize_for_width(text, avail_px, tkfont):
    if tkfont.measure(text) <= avail_px:
        return text
    ell = "…"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi) // 2
        candidate = text[:mid].rstrip() + ell
        if tkfont.measure(candidate) <= avail_px:
            lo = mid + 1
        else:
            hi = mid
    return text[:max(0, lo-1)].rstrip() + ell


class ListIntervention(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_add: Callable=None,
        on_select: Callable=None,
        imprimer: Callable=None,
        width: int=1000,
        height: int=600
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=8
        )
        self.width = width
        self.height = height
        self.on_select = on_select

        self.column_headers = [
            "Référence",
            "Description",
            "Type d'intervention",
            "Date d'intervention",
            "Vehicule",
            "Durée",
            "Technicien",
            "Statut"
        ]

        self.column_attrs = [
            "ref",
            "description",
            "type_intervention",
            "date_intervention",
            "vehicule",
            "dure",
            "technicien",
            "statut"
        ]

        self.head_font = font.Font(family="Poppins", size=11, weight="bold")
        self.cell_font = font.Font(family="Poppins", size=10)

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, pady=20, padx=20)
        lbl = ctk.CTkLabel(
            frame,
            text="📋 Liste des interventions",
            font=("Poppins", 18, "bold")
        )
        lbl.grid(row=0, column=0, pady=20, padx=20)

        bouton_ajouter = ctk.CTkButton(
            frame,
            text="➕ Ajouter intervention",
            command=on_add,
            width=170,
            height=35,
            font=("Poppins", 14)
        )
        bouton_ajouter.grid(
            row=1,
            column=0,
            pady=20,
            padx=20
        )

        bouton_imprimer = ctk.CTkButton(
            frame,
            text="Imprimer CSV",
            command=imprimer,
            width=170,
            height=35,
            font=("Poppins", 14)
        )
        bouton_imprimer.grid(
            row=1,
            column=2,
            pady=20,
            padx=20
        )

        container = ctk.CTkScrollableFrame(self, width=950, height=370)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        bg_color = "#2b2b2b"
        even_color = "#333333"
        odd_color = "#3a3a3a"
        text_color = "#f2f2f2"
        select_bg = "dark_blue"
        hover_color = "dark_blue"
        
        container.configure(fg_color=bg_color)

        style = ttk.Style()
        try:
            style.theme_use('clam')

        except Exception:
            pass

        tree_style_name = "Custom.Treeview"
       
        style.configure(
            tree_style_name,
            background=bg_color,
            fieldbackground=bg_color,
            foreground=text_color,
            rowheight=26,
            font=self.cell_font,
            borderwidth=0,
            relief="flat",
            lightcolor=bg_color,
            darkcolor=bg_color,
            bordercolor=bg_color
        )
        
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        style.configure(
            tree_style_name + ".Heading",
            font=self.head_font,
            foreground=text_color,
            background=even_color,
            bordercolor=bg_color,
            relief="flat"
        )

        style.map(
            "Treeview.Heading",
            background=[("active", hover_color)],  
            relief=[("active", "flat")],          
            foreground=[("active", text_color)]  
        )

        self.tree = ttk.Treeview(
            container,
            columns=self.column_attrs,
            show="headings",
            height=13,
            style=tree_style_name
        )
        self.tree.pack(
            fill="both",
            expand=True,
            pady=5,
            padx=5
        )

        total = self.width - 60
        weights = [13, 20, 20, 20, 12, 12, 12, 12]
        s = sum(weights[:len(self.column_attrs)])
        pix = [max(60, int(total * w / s)) for w in weights[:len(self.column_attrs)]]

        for header, attr, w in zip(self.column_headers, self.column_attrs, pix):
            self.tree.heading(attr, text=header, anchor="w")
            self.tree.column(attr, width=w, anchor="w", stretch=False)

        # tags pour alternance de lignes
        self.tree.tag_configure("odd", background=odd_color)
        self.tree.tag_configure("even", background=even_color)

        self.tree.bind("<Double-1>", self._on_double_click)
        self._donnees = []

    def _normalize_row(self, machine) -> None:
        return [getattr(machine, attr, "") for attr in self.column_attrs]

    def afficher(self, donne) -> None:
        self._donnees = donne
        for i in self.tree.get_children():
            self.tree.delete(i)

        col_px = {attr: self.tree.column(attr, option="width") for attr in self.column_attrs}

        for i, machine in enumerate(donne):
            row = self._normalize_row(machine)
            disp = []
            for attr, cell in zip(self.column_attrs, row):
                text = str(cell)
                avail = max(30, col_px[attr] - 12)
                short = ellipsize_for_width(text, avail, self.cell_font)
                disp.append(short)
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=disp, tags=(tag,))

    def _on_double_click(self, event) -> None:
        item_id = self.tree.identify_row(event.y)
        if item_id:
            index = self.tree.index(item_id)
            if 0 <= index < len(self._donnees) and self.on_select:
                self.on_select(self._donnees[index])


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1100x700")
    app = ListIntervention(root)
    app.pack(fill="both", expand=True)

    class M:
        def __init__(self, **kw):
            for k, v in kw.items():
                setattr(self, k, v)

    sample = [
        M(ID=1, nom="Machine A très longue", categorie="Type 1", date_service="2025-01-01", fabricant="X", etat="OK",
          compteur=123),
        M(ID=2, nom="Machine B", categorie="Type 2", date_service="2024-05-10", fabricant="Y", etat="En panne",
          compteur=456),
        M(ID=3, nom="Machine C", categorie="Type 3", date_service="2023-11-02", fabricant="Z", etat="OK", compteur=789),
    ]
    
    root.mainloop()
