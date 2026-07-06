import customtkinter as ctk
from tkinter import messagebox
from database_manager import verifier_connexion

# Configuration du style global de CustomTkinter
ctk.set_appearance_mode("System")  # S'adapte automatiquement au mode Sombre/Clair du PC
ctk.set_default_color_theme("blue") # Thème bleu professionnel

def tenter_connexion():
    email = entree_email.get()
    mdp = entree_mdp.get()
    
    gestionnaire = verifier_connexion(email)
    
    if gestionnaire:
        if gestionnaire['mot_de_passe'] == mdp: 
            messagebox.showinfo("Succès", f"Bienvenue {gestionnaire['nom_complet']} !")
            fenetre_connexion.destroy()
            # Logique pour ouvrir l'interface suivante ici
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
    else:
        messagebox.showerror("Erreur", "Gestionnaire introuvable.")

# Création de la fenêtre principale
fenetre_connexion = ctk.CTk()
fenetre_connexion.title("GesPro — Connexion")
fenetre_connexion.geometry("400x350")
fenetre_connexion.resizable(False, False)

# Titre de l'interface
titre = ctk.CTkLabel(fenetre_connexion, text="Gespro", font=("Helvetica", 20, "bold"))
titre.pack(pady=25)

# Champ Email
ctk.CTkLabel(fenetre_connexion, text="Identifiant (Email) :", font=("Helvetica", 12)).pack(pady=2)
entree_email = ctk.CTkEntry(fenetre_connexion, width=280, placeholder_text="exemple@domaine.com")
entree_email.pack(pady=5)

# Champ Mot de passe
ctk.CTkLabel(fenetre_connexion, text="Mot de passe :", font=("Helvetica", 12)).pack(pady=2)
entree_mdp = ctk.CTkEntry(fenetre_connexion, show="*", width=280, placeholder_text="••••••••")
entree_mdp.pack(pady=5)

# Bouton de connexion
bouton_connexion = ctk.CTkButton(fenetre_connexion, text="Se connecter", command=tenter_connexion, width=200, font=("Helvetica", 13, "bold"))
bouton_connexion.pack(pady=30)

fenetre_connexion.mainloop()