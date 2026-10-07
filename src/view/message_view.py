import customtkinter as ctk
from typing import Optional, Callable


class MessageBox(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        msg: str,
        type="info"
    ):
        super().__init__(master)
        self.title("Notification")
        self.geometry("350x180")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.focus_force()

        if type == "success":
            color = "#4CAF50"   
            hover_color = "#66BB6A"
            icon = "✅"
            title = "Succès"

        elif type == "error":
            color = "#E53935"   
            hover_color = "#EF5350"
            icon = "❌"
            title = "Erreur"

        else:
            color = "#2C47DD"
            hover_color = "#2C47DD"
            icon = "ℹ️"
            title = "Information"

        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2 - 175)
        y = master.winfo_y() + (master.winfo_height() // 2 - 90)
        self.geometry(f"+{x}+{y}")

        frame = ctk.CTkFrame(
            self,
            corner_radius=ctk.ThemeManager.theme["CTkFrame"]["corner_radius"]
        )
        frame.pack(
            expand=True,
            fill="both",
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            frame,
            text=f"{icon} {title}",
            text_color=color,
            font=("Poppins", 14, "bold"),
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            frame,
            text=msg,
            wraplength=300,
            justify="center",
            font=("Poppins", 12),
            text_color=color
        ).pack(pady=(5, 15))

        ok_button = ctk.CTkButton(
            frame,
            text="OK",
            width=100,
            fg_color=color,
            hover_color=hover_color,
            text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"][0],
            corner_radius=ctk.ThemeManager.theme["CTkButton"]["corner_radius"],
            command=self.destroy
        )
        ok_button.pack(pady=5)
        
        self.bind("<Return>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())

class ConfirmationBox(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        on_valid: Optional[Callable[[], None]] = None,
        title: str="Confirmation",
        message: str="Voulez-vous vraiment supprimer cet élément ?"
    ):
        super().__init__(master)
        self.title(title)
        self.geometry("350x180")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.focus_force()

        self._on_valid = on_valid

        frame = ctk.CTkFrame(self, corner_radius=6)
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        ctk.CTkLabel(
            frame,
            text=message,
            wraplength=320,
            font=("Poppins", 12)
        ).grid(row=0, columnspan=2, pady=10, padx=10)

        validation_bouton = ctk.CTkButton(
            frame,
            text="Valider",
            fg_color="#94CF8F",
            hover_color="#116109",
            command=self._on_confirm
        )
        validation_bouton.grid(row=1, column=1, padx=10, pady=10)

        cancel_bouton = ctk.CTkButton(
            frame,
            text="Annuler",
            fg_color='#BE7272',
            hover_color="#8A1111",
            command=self._on_cancel
        )
        cancel_bouton.grid(row=1, column=0, padx=10, pady=10)
        
        self.bind("<Return>", lambda e: self._on_confirm())
        self.bind("<Escape>", lambda e: self._on_cancel())

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _on_confirm(self) -> None:
        """
        Relâche le grab, masque la boîte (pour éviter que d'autres focus callbacks
        essayent d'agir sur elle), exécute la callback en sécurité, puis détruit.
        """
        try:
            try:
                self.grab_release()
            except Exception:
                pass

            try:
                self.withdraw()
            except Exception:
                pass

            if callable(self._on_valid):
                try:
                    self._on_valid()
                except Exception as exc:
                    print("Erreur dans on_valid:", exc)
        finally:
            try:
                self.destroy()
            except Exception:
                pass

    def _on_cancel(self) -> None:
        try:
            self.grab_release()

        except Exception:
            pass

        try:
            self.destroy()
        except Exception:
            pass

 
if __name__ == "__main__":
    root = ctk.CTk()
    app = ConfirmationBox(root)
    root.mainloop()
