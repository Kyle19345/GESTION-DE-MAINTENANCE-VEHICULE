import customtkinter as ctk
import tkinter as tk

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

class addRule(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        on_add: Callable=None,
        on_suppr: Callable=None
    ):
        super().__init__(master)
        self.title("Configuration maintenance")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.config(padx=12, pady=12)
        CARD_PADX = 14
        CARD_PADY = 12
        LABEL_FONT = ("Poppins", 13)
        TITLE_FONT = ("Poppins", 18, "bold")
        SMALL_FONT = ("Poppins", 11)

        self.container = ctk.CTkFrame(
            self,
            corner_radius=14,
            border_width=1,
            width=820
        )
        self.container.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=6,
            pady=6
        )
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=CARD_PADX,
            pady=(CARD_PADY, 8)
        )
        header.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            header,
            text="Règle de Maintenance",
            font=TITLE_FONT
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Définissez les intervalles et options d'intervention automatique",
            font=SMALL_FONT,
            text_color="#bfc1c3"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 0)
        )

        form_frame = ctk.CTkFrame(self.container, corner_radius=10)
        form_frame.grid(
            row=1,
            column=0,
            padx=(CARD_PADX, 8),
            pady=(6, CARD_PADY),
            sticky="nsew"
        )
        form_frame.grid_columnconfigure(1, weight=1)

        self.labels = ["Description", "Intervalle Km", "Notify before Km"]
        self.entries = {}
        for i, label in enumerate(self.labels):
            ctk.CTkLabel(
                form_frame,
                text=label,
                font=LABEL_FONT,
                anchor="e"
            ).grid(
                row=i,
                column=0,
                padx=(12, 6),
                pady=(10 if i == 0 else 6, 6),
                sticky="e"
            )

            entry = ctk.CTkEntry(
                form_frame,
                placeholder_text="" if hasattr(ctk.CTkEntry, "placeholder_text") else None
            )
            entry.grid(
                row=i,
                column=1,
                padx=(6, 12),
                pady=(10 if i == 0 else 6, 6),
                sticky="ew"
            )
            self.entries[label.replace(" ","_")] = entry

        self.active_var = tk.IntVar(value=1)
        switch_row = len(self.labels) + 1
        ctk.CTkLabel(
            form_frame,
            text="Intervention automatique",
            font=LABEL_FONT
        ).grid(
            row=switch_row,
            column=0,
            padx=(12, 6),
            pady=(6, 8),
            sticky="e"
        )

        self.switch_active = ctk.CTkSwitch(
            form_frame,
            text="",
            variable=self.active_var,
            onvalue=1,
            offvalue=0
        )
        self.switch_active.grid(
            row=switch_row,
            column=1,
            padx=(6, 12),
            pady=(6, 8),
            sticky="w"
        )

        buttons_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        buttons_frame.grid(
            row=switch_row + 1,
            column=0,
            columnspan=2,
            pady=(10, 6),
            padx=8,
            sticky="ew"
        )
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
       
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Enregistrer",
            command=on_add,
            width=160,
            height=38,
            corner_radius=10
        )
        save_btn.grid(row=0, column=1, padx=(6, 12), sticky="e")

        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Supprimer",
            fg_color="#a74a4a",
            hover_color="#b85b5b",
            command=on_suppr,
            width=160,
            height=38,
            corner_radius=10
        )
        delete_btn.grid(row=0, column=0, padx=(12, 6), sticky="w")
   
        tree_bg = "#2c2f31" 

        colonnes = ["Déscription", "Intervalle", "Notify", "Create_auto"]
        self.column_attrs = ["description","intervalle_km",'notify_before','create_auto']

        self.head_font = font.Font(family="Poppins", size=11, weight="bold")
        self.cell_font = font.Font(family="Poppins", size=10)

        width=600
        tree_container = ctk.CTkScrollableFrame(
            self.container,
            corner_radius=10,
            width=width,
            height=420,
            fg_color=tree_bg
        )
        tree_container.grid(
            row=1,
            column=1,
            padx=(8, CARD_PADX),
            pady=(6, CARD_PADY),
            sticky="nsew"
        )

        self.tree = ttk.Treeview(
            tree_container,
            columns=colonnes,
            show="headings",
            height=14
        )
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        for col in colonnes:
            width = 240 if col == "Déscription" else 120
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center", stretch=True)

        # --- Style sombre ---
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "Treeview",
            background="#2c2f31",
            foreground="#e6e6e6",
            fieldbackground=tree_bg,
            rowheight=26,
            font=("Arial", 10),
            bordercolor=tree_bg,
            relief="flat"
        )
        
        style.configure(
            "Treeview.Heading",
            background="#181a1b",
            foreground="#e7e7e7",
            font=("Poppins", 11, "bold"),
            relief="flat",
            bordercolor="#181a1b"
        )
        
        style.map("Treeview.Heading", background=[("active", "#2f3436")])

        style.configure("Treeview", borderwidth=0)
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        style.map("Treeview", background=[("selected", "#3a3d3f")])
        self.tree.tag_configure("odd", background="#2b2d2e")
        self.tree.tag_configure("even", background="#262728")

        self.tree.bind("<Double-1>",self._on_tree_double_click)
        self.focus()

    def _on_tree_double_click(self, event) -> None:
        item = self.tree.identify_row(event.y)
        if not item:
            return
        values = self.tree.item(item, "values")
        if not values:
            return
        try:
            if "Description" in self.entries and len(values) >= 1:
                self.entries["Description"].delete(0, "end")
                self.entries["Description"].insert(0, values[0])

            if "Intervalle_Km" in self.entries and len(values) >= 2:
                self.entries["Intervalle_Km"].delete(0, "end")
                self.entries["Intervalle_Km"].insert(0, values[1])

            if "Notify_before_Km" in self.entries and len(values) >= 3:
                self.entries["Notify_before_Km"].delete(0, "end")
                self.entries["Notify_before_Km"].insert(0, values[2])

            if len(values) >= 4:
                create_auto = str(values[3]).lower()
                active_val = 1 if create_auto in ("yes", "oui", "1", "true", "on") else 0
                self.active_var.set(active_val)

        except Exception:
            pass

    def get_entre(self) -> None:
        return {
            "Description": self.entries["Description"].get().strip(),
            "Intervalle_Km": self.entries["Intervalle_Km"].get().strip(),
            "Notify_before_Km": self.entries["Notify_before_Km"].get().strip(),
            "Active": bool(self.active_var.get())
        }
    def get_suppr_selected(self) -> None:
        return self.entries["Description"].get().strip()
    
    def _normalize_row(self, intervention) -> None:
        """
        Retourne une liste de valeurs (strings) dans l'ordre self.column_attrs.
        Supporte :
         - objets (getattr)
         - dicts (key lookup)
         - sequences (list/tuple) : on ramène en list et on lit par index si possible
        """
        out = []
        if intervention is None:
            return ["" for _ in self.column_attrs]
        
        if isinstance(intervention, dict):
            for attr in self.column_attrs:
                out.append(intervention.get(attr, ""))
            return out

        try:
            seq = list(intervention)
    
            if len(seq) >= len(self.column_attrs):
                return [seq[i] if i < len(seq) else "" for i in range(len(self.column_attrs))]

        except Exception:
            seq = None

        for i, attr in enumerate(self.column_attrs):
            val = ""
            if seq is not None and i < len(seq):
                val = seq[i]
            else:
                val = getattr(intervention, attr, "")
            out.append(val)

        return out

    def afficher(self, donne) -> None:
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        if not donne:
            return 0

        tree_cols = list(self.tree["columns"])
        ncols = min(len(tree_cols), len(self.column_attrs))

        col_px = {}
        for col in tree_cols[:ncols]:
            try:
                col_px[col] = int(self.tree.column(col, option="width"))
            except Exception:
                # fallback si impossible de lire
                col_px[col] = 120

        inserted = 0
        seen = set()
        for idx, intervention in enumerate(donne):
            row_vals = self._normalize_row(intervention)

            disp = []
            for col_index in range(ncols):
                col_name = tree_cols[col_index]
                attr_val = row_vals[col_index] if col_index < len(row_vals) else ""
                text = "" if attr_val is None else str(attr_val)
                avail = max(30, col_px.get(col_name, 120) - 12)
                short = ellipsize_for_width(text, avail, self.cell_font)
                disp.append(short)


            key = tuple(x.strip() for x in disp)
            if key in seen:
                continue
            seen.add(key)

            tag = "even" if inserted % 2 == 0 else "odd"
            self.tree.insert("", "end", values=tuple(disp), tags=(tag,))
            inserted += 1

        return inserted


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("960x560")
    app = addRule(root)
    root.mainloop()
