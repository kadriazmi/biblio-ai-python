import json
import os
import ollama


class LibraryManager:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    self.books = json.load(f)
                except json.JSONDecodeError:
                    self.books = []
        else:
            self.books = []
            self.init_fake_data()

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.books, f, indent=4, ensure_ascii=False)

    def _next_id(self):
        return max((b["id"] for b in self.books), default=100) + 1

    def init_fake_data(self):
        data = [
            (102, "Le Petit Prince",             "Antoine de Saint-Exupéry",
             "Roman",            1943, 3, "disponible", ""),
            (103, "Les Misérables",               "Victor Hugo",
             "Roman",            1862, 0, "emprunté",   "15/03/2026"),
            (104, "Notre-Dame de Paris",          "Victor Hugo",
             "Roman",            1831, 2, "disponible", ""),
            (105, "Orgueil et Préjugés",          "Jane Austen",
             "Roman romantique", 1813, 1, "disponible", ""),
            (106, "Jane Eyre",                    "Charlotte Brontë",
             "Roman romantique", 1847, 2, "disponible", ""),
            (107, "Clean Code",                   "Robert C. Martin",
             "Informatique",     2008, 1, "disponible", ""),
            (108, "Python Crash Course",          "Eric Matthes",
             "Informatique",     2015, 2, "disponible", ""),
            (109, "Automate the Boring Stuff",    "Al Sweigart",
             "Informatique",     2015, 1, "disponible", ""),
            (110, "Le Rouge et le Noir",          "Stendhal",
             "Roman",            1830, 1, "emprunté",   "20/04/2026"),
            (111, "1984",                         "George Orwell",
             "Science-Fiction",  1949, 2, "disponible", ""),
            (112, "Brave New World",              "Aldous Huxley",
             "Science-Fiction",  1932, 1, "disponible", ""),
            (113, "Sapiens",                      "Yuval Noah Harari",
             "Histoire",         2011, 3, "disponible", ""),
            (114, "Une brève histoire du temps",  "Stephen Hawking",
             "Science",          1988, 1, "réservé",    ""),
            (115, "Les Contemplations",           "Victor Hugo",
             "Poésie",           1856, 1, "disponible", ""),
            (116, "L'Étranger",                   "Albert Camus",
             "Roman",            1942, 2, "disponible", ""),
            (117, "Le Comte de Monte-Cristo",     "Alexandre Dumas",
             "Roman",            1844, 2, "disponible", ""),
            (118, "Don Quichotte",                "Cervantes",
             "Roman",            1605, 1, "disponible", ""),
            (119, "Introduction aux algorithmes", "Cormen et al.",
             "Informatique",     2009, 1, "emprunté",   "10/06/2026"),
            (120, "Deep Learning",                "Ian Goodfellow",
             "Informatique",     2016, 1, "disponible", ""),
            (121, "Fluent Python",                "Luciano Ramalho",
             "Informatique",     2015, 2, "disponible", ""),
        ]
        for d in data:
            self.books.append({
                "id":                  int(d[0]),
                "titre":               d[1],
                "auteur":              d[2],
                "categorie":           d[3],
                "annee_publication":   int(d[4]),
                "quantite_disponible": int(d[5]),
                "statut":              d[6],
                "date_retour":         d[7]
            })
        self.save_books()

    def ajouter_livre(self, titre, auteur, categorie, annee, quantite, statut, date_retour=""):
        self.books.append({
            "id":                  self._next_id(),
            "titre":               titre,
            "auteur":              auteur,
            "categorie":           categorie,
            "annee_publication":   int(annee),
            "quantite_disponible": int(quantite),
            "statut":              statut,
            "date_retour":         date_retour
        })
        self.save_books()

    def afficher_livres(self):
        return self.books

    def get_by_id(self, book_id):
        return next((b for b in self.books if b["id"] == int(book_id)), None)

    def modifier_livre(self, book_id, titre, auteur, categorie, annee, quantite, statut, date_retour):
        for b in self.books:
            if b["id"] == int(book_id):
                b["titre"] = titre
                b["auteur"] = auteur
                b["categorie"] = categorie
                b["annee_publication"] = int(annee)
                b["quantite_disponible"] = int(quantite)
                b["statut"] = statut
                b["date_retour"] = date_retour
                self.save_books()
                return True
        return False

    def supprimer_livre(self, book_id):
        self.books = [b for b in self.books if b["id"] != int(book_id)]
        self.save_books()

    def rechercher_livre(self, query):
        q = query.strip().lower()
        return [
            b for b in self.books
            if q in b["titre"].lower()
            or q in b["auteur"].lower()
            or q == str(b["id"])
        ]

    def poser_question_chatbot(self, question):
        contexte = "Voici les livres de la bibliothèque :\n"
        for b in self.books:
            contexte += (
                f"- ID:{b['id']} | {b['titre']} | {b['auteur']} | "
                f"{b['categorie']} | {b['annee_publication']} | "
                f"Qté:{b['quantite_disponible']} | Statut:{b['statut']}"
                + (f" | Retour:{b['date_retour']}" if b["date_retour"] else "")
                + "\n"
            )

        prompt = f"""Tu es un assistant bibliothécaire intelligent. Réponds TOUJOURS en français avec ce format exact selon le type de question :

TYPE 1 — Question par ID (ex: "livre avec l'ID 102"):
Oui, ce livre existe dans la bibliothèque.
📖 Titre : [titre]
✍️ Auteur : [auteur]
📊 Statut : [statut] ([quantite] exemplaires)

TYPE 2 — Question de disponibilité (ex: "Les Misérables est-il disponible"):
Si disponible:
Oui, ce livre est disponible.
📖 Titre : [titre]
✍️ Auteur : [auteur]
📊 Statut : Disponible ([quantite] exemplaires)

Si emprunté:
Non, ce roman est actuellement emprunté.
📖 Titre : [titre]
✍️ Auteur : [auteur]
📊 Statut : Emprunté
📅 Retour prévu le : [date_retour]

TYPE 3 — Recommandation (ex: "roman romantique", "livre de science"):
Bien sûr ! Voici mes recommandations :
1. [titre] — [auteur] — [statut]
2. [titre] — [auteur] — [statut]
3. [titre] — [auteur] — [statut]

TYPE 4 — Recherche par auteur (ex: "livre de Victor Hugo"):
[auteur] est dans notre catalogue. Voici ses œuvres :
1. [titre] — [statut] (retour le [date] si emprunté) ([quantite] exemplaires si disponible)
2. ...

DONNÉES DE LA BIBLIOTHÈQUE :
{contexte}

RÈGLES STRICTES :
- Utilise UNIQUEMENT les données ci-dessus, n'invente rien.
- Respecte EXACTEMENT le format demandé selon le type de question.
- Ne rajoute pas d'explications supplémentaires.

Question : {question}
Réponse :"""

        try:
            response = ollama.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            return f"Erreur Ollama : {e}\n(Vérifiez qu'Ollama est lancé: ollama serve)"
