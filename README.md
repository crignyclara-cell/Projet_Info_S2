# Projet_Info_S2

## Informations du groupe
* **Groupe de TD :** L1 BI TD4
* **Étudiants :**  Clara CRIGNY 
    * Zahra-Nancy AMGHAR 
    * Fériel DOUAIRI 3
    * Arsham ALIHARED 4
* **URL du dépôt :** https://github.com/crignyclara-cell/Projet_Info_S2/edit/main/README.md

## Sources 
* **Sources externes :**
-Le widget Entry (les cases) 
-Documentation officielle (Python.org) : Explique les options comme width, justify ou state.
-La méthode .grid() (le placement) :Guide Tkinter - Grid : Explique comment fonctionnent row, column, padx et pady.
-Les messagebox (alertes) : Effbot - Tkinter Messagebox : Liste les différences entre showerror, showwarning et showinfo.
-Tutoriel simplifié pour débutants : Cours-Python.com - Tkinter 
* **Utilisation externe :** Nous avons utilisé Gemini pour comprendre comment créer et utiliser un fichier README 

## Code pour le sudoku (détaillé) 

import tkinter as tk  # Importation de la bibliothèque pour créer des fenêtres
from tkinter import messagebox  # Importation pour afficher des messages d'alerte (Pop-up)
grille_jeu = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

solution = [
    [4, 3, 5, 2, 6, 9, 7, 8, 1],
    [6, 8, 2, 5, 7, 1, 4, 9, 3],
    [1, 9, 7, 8, 3, 4, 5, 6, 2],
    [8, 2, 6, 1, 9, 5, 3, 4, 7],
    [3, 7, 4, 6, 8, 2, 9, 1, 5],
    [9, 5, 1, 7, 4, 3, 6, 2, 8],
    [5, 1, 9, 3, 2, 6, 8, 7, 4],
    [2, 4, 8, 9, 5, 7, 1, 3, 6],
    [7, 6, 3, 4, 1, 8, 2, 5, 9]
]

Liste globale pour stocker les objets 'Entry' et y accéder plus tard
toutes_les_cases = []


Cette fonction est appelée quand on clique sur le bouton
def verifier_la_grille():
    nombre_erreurs = 0  # On initialise un compteur d'erreurs à 0
    nombre_cases_vides = 0  # On initialise un compteur de cases vides
    
    # On parcourt chaque ligne (i) et chaque colonne (j)
    for i in range(9):
        for j in range(9):
            case_actuelle = toutes_les_cases[i][j]  # On récupère la case graphique
            valeur_saisie = case_actuelle.get()  # On lit ce qui est écrit dedans
            
            # Étape A : Vérifier si la case est vide
            if valeur_saisie == "":
                nombre_cases_vides = nombre_cases_vides + 1
                case_actuelle.config(bg="white")  # On laisse le fond blanc
            else:
                # Étape B : Comparaison avec la solution
                # int() transforme le texte en nombre pour comparer
                if int(valeur_saisie) == solution[i][j]:
                    # Si c'est juste et que c'était une case vide au début
                    if grille_jeu[i][j] == 0:
                        case_actuelle.config(bg="#c2f0c2")  # Fond vert clair
                else:
                    # Si c'est faux, on colorie en rouge
                    case_actuelle.config(bg="#ffcccc")  # Fond rouge clair
                    nombre_erreurs = nombre_erreurs + 1

    # Étape C : Affichage du message final
    # Source : https://docs.python.org/3/library/tkinter.messagebox.html
    if nombre_cases_vides > 0:
        messagebox.showwarning("Attention", "La grille n'est pas terminée !")
    elif nombre_erreurs > 0:
        messagebox.showerror("Erreur", "Il y a des fautes dans la grille.")
    else:
        messagebox.showinfo("Succès", "Bravo ! Tout est correct.")

fenetre = tk.Tk()  # Initialisation de la fenêtre principale
fenetre.title("Projet Sudoku L1 Bio-Info")

for i in range(9):
    liste_ligne = []  # Liste temporaire pour stocker les cases d'une ligne
    for j in range(9):
        # Création de la case de saisie (Entry)
        # Source : https://tkdocs.com/tutorial/widgets.html#entry
        case = tk.Entry(fenetre, width=2, font=('Arial', 20), justify='center', bd=1, relief="solid")
        
        # Gestion des marges (padx, pady) pour dessiner les blocs 3x3
        # On ajoute plus d'espace à gauche si c'est la 1ère, 4ème ou 7ème colonne
        marge_x = 1
        if j % 3 == 0: marge_x = 5
        
        marge_y = 1
        if i % 3 == 0: marge_y = 5
        
        # Placement de la case dans la grille logicielle
        # Source : https://tkdocs.com/tutorial/grid.html
        case.grid(row=i, column=j, padx=(marge_x, 1), pady=(marge_y, 1))
        
        # Si la grille de départ contient un chiffre, on l'affiche et on bloque la case
        valeur_depart = grille_jeu[i][j]
        if valeur_depart != 0:
            case.insert(0, str(valeur_depart))
            case.config(state='readonly', readonlybackground='#dfe6e9')
            
        liste_ligne.append(case)  # On ajoute la case à la ligne
    toutes_les_cases.append(liste_ligne)  # On ajoute la ligne à la liste globale

Création et placement du bouton de validation
bouton = tk.Button(fenetre, text="Vérifier ma solution", command=verifier_la_grille)
bouton.grid(row=9, column=0, columnspan=9, pady=20)

fenetre.mainloop()  # Lancement du programme
