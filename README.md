# 📚 Bibliothèque Intelligente avec Chatbot IA

Projet Semestriel Python — iTeam University | AU 2025-2026  
**Étudiant :** Kadri Azmi

---

## 🎯 Description

Application Python de gestion de bibliothèque avec un chatbot IA intégré.  
Le chatbot répond aux questions en langage naturel en se basant sur les données réelles de la bibliothèque.

---

## ✅ Fonctionnalités

- **CRUD complet** : Ajouter, Afficher, Modifier, Supprimer, Rechercher des livres
- **Chatbot IA** : Assistant intelligent basé sur Ollama + LLaMA 3.2 (local, gratuit, sans Internet)
- **Interface graphique** : Tkinter avec 2 onglets (CRUD + Chatbot)
- **Stockage** : Fichier JSON (books.json) — auto-créé au premier lancement avec 20 livres

---

## 🛠️ Technologies utilisées

| Composant | Technologie |
|---|---|
| Langage | Python 3 |
| Interface graphique | Tkinter (inclus avec Python) |
| Base de données | JSON |
| Chatbot IA | Ollama + LLaMA 3.2 (local) |
| Backend | Python pur (classe LibraryManager) |

---

## ⚙️ Installation et Lancement

### Prérequis
- Python 3.10+
- [Ollama](https://ollama.com/download) installé

### Étape 1 — Cloner le projet
```bash
git clone https://github.com/kadriazmi/bibliotheque-intelligente-chatbot-ia
cd bibliotheque-intelligente-chatbot-ia
```

### Étape 2 — Installer Ollama
Télécharger depuis : https://ollama.com/download/windows  
Puis télécharger le modèle LLaMA 3.2 :
```bash
ollama pull llama3.2
```

### Étape 3 — Installer la dépendance Python
```bash
pip install ollama
```

### Étape 4 — Lancer l'application
```bash
python main.py
```

> ⚠️ **Important :** Ollama se lance automatiquement en arrière-plan après installation.  
> Si le chatbot retourne une erreur, lancer manuellement dans un terminal séparé :
> ```bash
> ollama serve
> ```
> Puis relancer `python main.py`.

---

## 📁 Structure du projet

```
bibliotheque-intelligente-chatbot-ia/
├── main.py       # Interface graphique Tkinter
├── backend.py    # Gestion JSON + Chatbot Ollama (classe LibraryManager)
└── books.json    # Base de données (auto-générée au premier lancement)
```

---

## 💬 Exemples de dialogues avec le Chatbot

**Recherche par ID :**
> 👤 Est-ce que le livre avec l'ID 102 existe ?  
> 🤖 Oui. 📖 Titre : Le Petit Prince | ✍️ Auteur : Antoine de Saint-Exupéry | 📊 Statut : Disponible (3 exemplaires)

**Disponibilité :**
> 👤 Le roman Les Misérables est-il disponible ?  
> 🤖 Non, il est emprunté. 📅 Retour prévu le : 15/03/2026

**Recommandation :**
> 👤 Je veux un roman romantique facile à lire.  
> 🤖 Voici mes recommandations : 1. Orgueil et Préjugés — Jane Austen — disponible ...

**Recherche par auteur :**
> 👤 Je cherche un livre de Victor Hugo.  
> 🤖 Victor Hugo est dans notre catalogue. Voici ses œuvres : ...

---
