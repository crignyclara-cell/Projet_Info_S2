import tkinter as tk
from tkinter import messagebox
import random
import time
import json

TAILLE_GRILLE = 600
COULEUR_ERREUR = "red"
COULEUR_CONTR = "#F0F0F0"
FONTS = ("Arial", 16)

class SudokuL1:# utilisation de gemini pour l'utilisation de class
    def _init_(self, root):
        self.root = root
        
        self.grille = [[None]*9 for _ in range(9)]
        self.solution = [[None]*9 for _ in range(9)]
        self.modifiable = [[False]*9 for _ in range(9)]
        
        self.selection = None
        self.chiffre_aide = None
        self.erreurs = 0
        self.temps_debut = 0
        self.en_cours = False
        
        # Pile pour l'annulation (undo)
        self.historique = []
        
        self.cadre_boutons = tk.Frame(self.root)
        self.cadre_boutons.pack(pady=10)
        
        self.label_score = tk.Label(self.root, text="Initialisation...", font=("Arial", 12))
        self.label_score.pack()
        
        self.canvas = tk.Canvas(self.root, width=TAILLE_GRILLE, height=TAILLE_GRILLE, bg="white")
        self.canvas.pack(padx=20, pady=20)

    # ---------- Arsham - Vérification et génération ----------
    def verifier_regles(self, ligne, col, num):
        for i in range(9):
            if (self.grille[ligne][i] == num and i != col) or (self.grille[i][col] == num and i != ligne):
                return False
        r_dep, c_dep = 3 * (ligne // 3), 3 * (col // 3)
        for i in range(r_dep, r_dep+3):
            for j in range(c_dep, c_dep+3):
                if self.grille[i][j] == num and (i != ligne or j != col):
                    return False
        return True

    def nouvelle_partie(self, diff="Facile"):
        base = [1,2,3,4,5,6,7,8,9]
        random.shuffle(base)
        for r in range(9):
            dec = (r * 3 + r // 3) % 9
            for c in range(9):
                v = str(base[(c + dec) % 9])
                self.solution[r][c] = v 
                self.grille[r][c] = v
                self.modifiable[r][c] = False
        nb_vides = {"Facile": 35, "Moyen": 48, "Difficile": 58}[diff]
        indices = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(indices)
        for i in range(nb_vides):
            r, c = indices[i]
            self.grille[r][c] = None
            self.modifiable[r][c] = True
        self.erreurs = 0
        self.temps_debut = time.time()
        self.en_cours = True
        self.historique.clear()   # Vider la pile undo
        self.maj_chrono()
        self.dessiner_grille()

    # ---------- Zahra Nancy - Affichage et événements ----------
    def dessiner_grille(self):
        self.canvas.delete("all")
        pas = TAILLE_GRILLE / 9
        for r in range(9):
            for c in range(9):
                x1, y1 = c * pas, r * pas
                x2, y2 = x1 + pas, y1 + pas
                if self.selection:# recherche google pour l'utilisation de self ( a partir d'un code deja crée ) 
                    sr, sc = self.selection
                    if r == sr or c == sc or (r//3 == sr//3 and c//3 == sc//3):
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=COULEUR_CONTR, outline="")
                if self.chiffre_aide and self.grille[r][c] == self.chiffre_aide:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="")
                val = self.grille[r][c]
                if val:
                    if not self.verifier_regles(r, c, val):
                        couleur = COULEUR_ERREUR
                    elif self.modifiable[r][c]:
                        couleur = "blue"
                    else:
                        couleur = "black"
                    self.canvas.create_text(x1+pas/2, y1+pas/2, text=val, font=FONTS, fill=couleur)
        for i in range(10):
            w = 3 if i % 3 == 0 else 1
            self.canvas.create_line(i*pas, 0, i*pas, TAILLE_GRILLE, width=w)
            self.canvas.create_line(0, i*pas, TAILLE_GRILLE, i*pas, width=w)

    def _sauvegarder_etat(self):
        """Sauvegarde l'état actuel (grille + erreurs) dans la pile historique."""
        copie_grille = [[self.grille[i][j] for j in range(9)] for i in range(9)]
        self.historique.append((copie_grille, self.erreurs))

    def annuler(self):
        """Annule la dernière action (retour à l'état précédent)."""
        if self.historique:
            ancienne_grille, anciennes_erreurs = self.historique.pop()
            for i in range(9):
                for j in range(9):
                    self.grille[i][j] = ancienne_grille[i][j]
            self.erreurs = anciennes_erreurs
            self.dessiner_grille()
        else:
            messagebox.showinfo("Annuler", "Rien à annuler.")

    def gerer_entree(self, event):
        if self.selection and self.en_cours:
            r, c = self.selection
            if self.modifiable[r][c] and event.char in "123456789":
                self._sauvegarder_etat()   # Sauvegarde avant modification
                self.grille[r][c] = event.char
                if not self.verifier_regles(r, c, event.char):
                    self.erreurs += 1
                self.dessiner_grille()

    # ---------- Feriel - Persistance et utilitaires ----------
    def sauvegarder_partie(self):
        data = {
            "grille": self.grille, "sol": self.solution, "mod": self.modifiable,
            "err": self.erreurs, "t": time.time() - self.temps_debut
        }
        with open("partie_sudoku.json", "w") as f:
            json.dump(data, f)
        messagebox.showinfo("INFO", "Partie sauvegardée dans partie_sudoku.json")

    def charger_partie(self):
        try:
            with open("partie_sudoku.json", "r") as f:
                d = json.load(f)
            self.grille, self.solution, self.modifiable = d["grille"], d["sol"], d["mod"]
            self.erreurs, self.temps_debut = d["err"], time.time() - d["t"]
            self.en_cours = True
            self.historique.clear()   # On vide l'historique après chargement
            self.dessiner_grille()
        except FileNotFoundError:
            messagebox.showerror("Oups", "Aucun fichier de sauvegarde trouvé.")

    def maj_chrono(self):
        if self.en_cours:
            sec = int(time.time() - self.temps_debut)
            minutes, secondes = divmod(sec, 60)
            self.label_score.config(text=f"Fautes: {self.erreurs} | Temps: {minutes:02d}:{secondes:02d}")
            self.root.after(1000, self.maj_chrono)

    def aide_visuelle(self):
        if self.selection:
            r, c = self.selection
            self.chiffre_aide = self.grille[r][c]
            self.dessiner_grille()

    def effacer_case(self):
        if self.selection:
            r, c = self.selection
            if self.modifiable[r][c] and self.grille[r][c] is not None:
                self._sauvegarder_etat()   # Sauvegarde avant effacement
                self.grille[r][c] = None
                self.dessiner_grille()

if _name_ == "_main_":
    fenetre = tk.Tk()
    app = SudokuL1(fenetre)

    app.canvas.bind("<Button-1>", lambda e: (
        setattr(app, 'selection', (int(e.y//(TAILLE_GRILLE/9)), int(e.x//(TAILLE_GRILLE/9)))),
        setattr(app, 'chiffre_aide', None),
        app.dessiner_grille()
    ))
    fenetre.bind("<Key>", app.gerer_entree)

    tk.Button(app.cadre_boutons, text="Nouveau", command=lambda: app.nouvelle_partie(app.menu_diff_var.get())).pack(side=tk.LEFT, padx=2)
    tk.Button(app.cadre_boutons, text="Sauver", command=app.sauvegarder_partie).pack(side=tk.LEFT, padx=2)
    tk.Button(app.cadre_boutons, text="Charger", command=app.charger_partie).pack(side=tk.LEFT, padx=2)
    tk.Button(app.cadre_boutons, text="Aide Chiffre", command=app.aide_visuelle).pack(side=tk.LEFT, padx=2)
    tk.Button(app.cadre_boutons, text="Effacer", command=app.effacer_case).pack(side=tk.LEFT, padx=2)
    tk.Button(app.cadre_boutons, text="Annuler", command=app.annuler).pack(side=tk.LEFT, padx=2)   # Bouton Annuler

    app.menu_diff_var = tk.StringVar(value="Facile")
    tk.OptionMenu(app.cadre_boutons, app.menu_diff_var, "Facile", "Moyen", "Difficile").pack(side=tk.LEFT)

    fenetre.mainloop()
