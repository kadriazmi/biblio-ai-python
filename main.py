import tkinter as tk
from tkinter import ttk, messagebox
import threading
from backend import LibraryManager


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Bibliothèque Intelligente avec Chatbot IA — iTeam University")
        self.root.geometry("950x620")
        self.root.resizable(True, True)

        self.manager = LibraryManager()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_crud = ttk.Frame(self.notebook)
        self.tab_chat = ttk.Frame(self.notebook)

        self.notebook.add(
            self.tab_crud, text="  📚 Gestion des Livres (CRUD)  ")
        self.notebook.add(self.tab_chat, text="  🤖 Chatbot Intelligent  ")

        self._setup_crud_tab()
        self._setup_chat_tab()

    def _setup_crud_tab(self):
        frm = ttk.LabelFrame(self.tab_crud, text=" Informations du Livre ")
        frm.pack(fill="x", padx=10, pady=6)

        labels = ["Titre", "Auteur", "Catégorie",
                  "Année", "Quantité", "Date retour"]
        self.entries = {}
        positions = [(0, 0), (0, 2), (0, 4), (1, 0), (1, 2), (1, 4)]

        for (r, c), lbl in zip(positions, labels):
            ttk.Label(frm, text=f"{lbl} :").grid(
                row=r, column=c, padx=6, pady=6, sticky="e")
            e = ttk.Entry(frm, width=20)
            e.grid(row=r, column=c+1, padx=6, pady=6)
            self.entries[lbl] = e

        ttk.Label(frm, text="Statut :").grid(
            row=2, column=0, padx=6, pady=6, sticky="e")
        self.combo_statut = ttk.Combobox(
            frm, values=["disponible", "emprunté", "réservé"], width=14, state="readonly"
        )
        self.combo_statut.set("disponible")
        self.combo_statut.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        frm_btn = ttk.Frame(self.tab_crud)
        frm_btn.pack(fill="x", padx=10, pady=4)

        ttk.Button(frm_btn, text="➕ Ajouter",
                   command=self._add).pack(side="left", padx=4)
        ttk.Button(frm_btn, text="💾 Modifier",
                   command=self._edit).pack(side="left", padx=4)
        ttk.Button(frm_btn, text="🗑️ Supprimer",
                   command=self._delete).pack(side="left", padx=4)
        ttk.Button(frm_btn, text="🔄 Actualiser",
                   command=self._refresh).pack(side="left", padx=4)

        ttk.Separator(frm_btn, orient="vertical").pack(
            side="left", fill="y", padx=10)

        ttk.Label(frm_btn, text="🔍 Recherche :").pack(side="left")
        self.ent_search = ttk.Entry(frm_btn, width=22)
        self.ent_search.pack(side="left", padx=4)
        self.ent_search.bind("<Return>", lambda e: self._search())
        ttk.Button(frm_btn, text="Chercher",
                   command=self._search).pack(side="left")

        cols = ("id", "titre", "auteur", "categorie",
                "annee", "qte", "statut", "retour")
        self.tree = ttk.Treeview(
            self.tab_crud, columns=cols, show="headings", selectmode="browse")

        headers = ("ID", "Titre", "Auteur", "Catégorie",
                   "Année", "Qté", "Statut", "Date Retour")
        widths = (45,   180,    140,       110,
                  55,     45,    90,        90)
        for col, hdr, w in zip(cols, headers, widths):
            self.tree.heading(col, text=hdr)
            self.tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(self.tab_crud, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both",
                       expand=True, padx=(10, 0), pady=6)
        sb.pack(side="left", fill="y", pady=6, padx=(0, 10))

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._refresh()

    def _refresh(self, data=None):
        self.tree.delete(*self.tree.get_children())
        for b in (data or self.manager.afficher_livres()):
            self.tree.insert("", "end", values=(
                b["id"], b["titre"], b["auteur"], b["categorie"],
                b["annee_publication"], b["quantite_disponible"],
                b["statut"], b["date_retour"]
            ))

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        keys = ["Titre", "Auteur", "Catégorie",
                "Année", "Quantité", "Date retour"]
        data = [vals[1], vals[2], vals[3], vals[4], vals[5], vals[7]]
        for k, v in zip(keys, data):
            self.entries[k].delete(0, "end")
            self.entries[k].insert(0, str(v))
        self.combo_statut.set(vals[6])
        self._selected_id = vals[0]

    def _get_fields(self):
        return (
            self.entries["Titre"].get().strip(),
            self.entries["Auteur"].get().strip(),
            self.entries["Catégorie"].get().strip(),
            self.entries["Année"].get().strip(),
            self.entries["Quantité"].get().strip(),
            self.combo_statut.get(),
            self.entries["Date retour"].get().strip(),
        )

    def _clear_form(self):
        for e in self.entries.values():
            e.delete(0, "end")
        self.combo_statut.set("disponible")
        self._selected_id = None

    def _add(self):
        titre, auteur, cat, annee, qte, statut, retour = self._get_fields()
        if not titre or not auteur:
            messagebox.showwarning(
                "Champs manquants", "Titre et Auteur sont obligatoires.")
            return
        try:
            self.manager.ajouter_livre(
                titre, auteur, cat, annee, qte, statut, retour)
            messagebox.showinfo(
                "✅ Succès", f"« {titre} » ajouté avec succès !")
            self._refresh()
            self._clear_form()
        except Exception as ex:
            messagebox.showerror("Erreur", str(ex))

    def _edit(self):
        if not getattr(self, "_selected_id", None):
            messagebox.showwarning(
                "Sélection", "Cliquez d'abord sur un livre dans le tableau.")
            return
        titre, auteur, cat, annee, qte, statut, retour = self._get_fields()
        try:
            self.manager.modifier_livre(
                self._selected_id, titre, auteur, cat, annee, qte, statut, retour
            )
            messagebox.showinfo("✅ Succès", "Livre modifié avec succès !")
            self._refresh()
            self._clear_form()
        except Exception as ex:
            messagebox.showerror("Erreur", str(ex))

    def _delete(self):
        if not getattr(self, "_selected_id", None):
            messagebox.showwarning(
                "Sélection", "Cliquez d'abord sur un livre dans le tableau.")
            return
        book = self.manager.get_by_id(self._selected_id)
        if messagebox.askyesno(
            "Confirmer suppression",
            f"Supprimer « {book['titre']} » ?\nCette action est irréversible."
        ):
            self.manager.supprimer_livre(self._selected_id)
            messagebox.showinfo("✅ Supprimé", "Livre supprimé avec succès !")
            self._refresh()
            self._clear_form()

    def _search(self):
        q = self.ent_search.get().strip()
        self._refresh(self.manager.rechercher_livre(q) if q else None)

    def _setup_chat_tab(self):
        self.txt_chat = tk.Text(
            self.tab_chat, state="disabled", wrap="word",
            bg="#f4f4f6", font=("Arial", 11), padx=10, pady=8
        )
        self.txt_chat.pack(fill="both", expand=True, padx=10, pady=(10, 4))

        frm = ttk.Frame(self.tab_chat)
        frm.pack(fill="x", padx=10, pady=8)

        self.ent_msg = ttk.Entry(frm, font=("Arial", 11))
        self.ent_msg.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.ent_msg.bind("<Return>", lambda e: self._send())

        ttk.Button(frm, text="Envoyer 🚀",
                   command=self._send).pack(side="right")

    def _append_chat(self, text):
        self.txt_chat.configure(state="normal")
        self.txt_chat.insert("end", text)
        self.txt_chat.configure(state="disabled")
        self.txt_chat.see("end")

    def _send(self):
        msg = self.ent_msg.get().strip()
        if not msg:
            return
        self.ent_msg.delete(0, "end")
        self._append_chat(f"👤 Vous : {msg}\n\n")
        self._append_chat("🤖 Chatbot : ⏳ En cours...\n")

        def fetch():
            resp = self.manager.poser_question_chatbot(msg)

            def update():
                self.txt_chat.configure(state="normal")
                content = self.txt_chat.get("1.0", "end-1c")
                idx = content.rfind("🤖 Chatbot : ⏳ En cours...")
                self.txt_chat.delete(f"1.0+{idx}c", "end")
                self.txt_chat.insert("end", f"🤖 Chatbot : {resp}\n")
                self.txt_chat.insert("end", "─" * 60 + "\n\n")
                self.txt_chat.configure(state="disabled")
                self.txt_chat.see("end")
            self.root.after(0, update)

        threading.Thread(target=fetch, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
