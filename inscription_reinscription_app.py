import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from config_db import obtenir_connexion
from database_manager import enregistrer_etudiant

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class GesProInscriptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Inscriptions & Réinscriptions")
        self.geometry("620x700")
        self.resizable(False, False)
        
        self.titre = ctk.CTkLabel(self, text="MODULE INCRIPTION / RÉINSCRIPTION", font=("Helvetica", 18, "bold"), text_color="#1A365D")
        self.titre.pack(pady=15)
        
        self.form_frame = ctk.CTkFrame(self, width=560)
        self.form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.creer_champs_formulaire()

    def creer_champs_formulaire(self):
        # BLOC DE RECHERCHE / IDENTIFICATION
        ctk.CTkLabel(self.form_frame, text="Identification (Saisir Matricule pour une Réinscription)", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=40, pady=(15, 5))
        
        # Frame / le bouton Rechercher
        mat_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        mat_frame.pack(fill="x", padx=40, pady=5)
        
        self.ent_matricule = ctk.CTkEntry(mat_frame, placeholder_text="Matricule (ex: 2026-001)", width=310)
        self.ent_matricule.pack(side="left", padx=(0, 10))
        
        # Bouton pour la RÉINSCRIPTION
        self.btn_rechercher = ctk.CTkButton(mat_frame, text="🔍 Trouver", width=110, fg_color="#4A5568", hover_color="#718096", command=self.rechercher_etudiant_pour_reinscription)
        self.btn_rechercher.pack(side="left")
        
        #  CHAMPS CLASSIQUE
        self.ent_nom = ctk.CTkEntry(self.form_frame, placeholder_text="Nom de famille", width=450)
        self.ent_nom.pack(pady=5)
        
        self.ent_prenom = ctk.CTkEntry(self.form_frame, placeholder_text="Prénom", width=450)
        self.ent_prenom.pack(pady=5)
        
        self.sexe_var = ctk.StringVar(value="M")
        sexe_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        sexe_frame.pack(fill="x", padx=40, pady=5)
        ctk.CTkLabel(sexe_frame, text="Sexe : ").pack(side="left")
        ctk.CTkRadioButton(sexe_frame, text="Masculin", variable=self.sexe_var, value="M").pack(side="left", padx=20)
        ctk.CTkRadioButton(sexe_frame, text="Féminin", variable=self.sexe_var, value="F").pack(side="left", padx=20)

        ctk.CTkLabel(self.form_frame, text="Parcours Académique", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=40, pady=(10, 5))
        
        self.ent_filiere = ctk.CTkEntry(self.form_frame, placeholder_text="Filière (ex: Génie Logiciel...)", width=450)
        self.ent_filiere.pack(pady=5)
        
        self.combo_cycle = ctk.CTkComboBox(self.form_frame, values=["Premier Cycle", "Second Cycle"], width=450)
        self.combo_cycle.pack(pady=5)
        
        ctk.CTkLabel(self.form_frame, text="Coordonnées & Contacts", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=40, pady=(10, 5))
        
        self.ent_adresse = ctk.CTkEntry(self.form_frame, placeholder_text="Adresse de résidence", width=450)
        self.ent_adresse.pack(pady=5)
        
        self.ent_telephone = ctk.CTkEntry(self.form_frame, placeholder_text="Numéro de Téléphone", width=450)
        self.ent_telephone.pack(pady=5)
        
        self.ent_email = ctk.CTkEntry(self.form_frame, placeholder_text="Adresse Email", width=450)
        self.ent_email.pack(pady=5)

        # Bouton d'action principal
        self.btn_valider = ctk.CTkButton(
            self.form_frame, 
            text="VALIDER L'INSCRIPTION / RÉINSCRIPTION", 
            font=("Helvetica", 13, "bold"),
            fg_color="#1A365D", hover_color="#2A4D7C",
            command=self.executer_liaison_bdd,
            width=450, height=40
        )
        self.btn_valider.pack(pady=20)

    def rechercher_etudiant_pour_reinscription(self):
        """Action spécifique de réinscription : Cherche l'élève et pré-remplit les champs."""
        mat = self.ent_matricule.get().strip()
        if not mat:
            messagebox.showwarning("Matricule requis", "Veuillez entrer un matricule pour lancer la recherche.")
            return
            
        try:
            conn = obtenir_connexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM etudiants WHERE matricule = %s", (mat,))
            etudiant = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if etudiant:
                # On efface les anciennes saisies de l'interface
                self.ent_nom.delete(0, "end")
                self.ent_prenom.delete(0, "end")
                self.ent_filiere.delete(0, "end")
                self.ent_adresse.delete(0, "end")
                self.ent_telephone.delete(0, "end")
                self.ent_email.delete(0, "end")
                
                # On pré-remplit automatiquement avec les données trouvées dans MySQL
                self.ent_nom.insert(0, etudiant['nom'])
                self.ent_prenom.insert(0, etudiant['prenom'])
                self.sexe_var.set(etudiant['sexe'])
                self.ent_filiere.insert(0, etudiant['filiere'])
                self.combo_cycle.set(etudiant['cycle'])
                self.ent_adresse.insert(0, etudiant['adresse'])
                self.ent_telephone.insert(0, etudiant['telephone'])
                self.ent_email.insert(0, etudiant['email'])
                
                messagebox.showinfo("Étudiant Trouvé", f"Données de {etudiant['nom'].upper()} chargées. Vous pouvez modifier sa filière/classe pour valider sa réinscription.")
            else:
                messagebox.showwarning("Introuvable", f"Aucun étudiant enregistré avec le matricule '{mat}'. C'est donc une nouvelle inscription.")
        except Exception as e:
            messagebox.showerror("Erreur de Recherche", f"Impossible d'interroger la base de données : {e}")

    def executer_liaison_bdd(self):
        """Enregistre ou met à jour l'étudiant."""
        mat = self.ent_matricule.get().strip()
        nom = self.ent_nom.get().strip()
        prenom = self.ent_prenom.get().strip()
        sexe = self.sexe_var.get()
        filiere = self.ent_filiere.get().strip()
        cycle = self.combo_cycle.get()
        adresse = self.ent_adresse.get().strip()
        tel = self.ent_telephone.get().strip()
        email = self.ent_email.get().strip()

        if not mat or not nom or not prenom or not filiere:
            messagebox.showwarning("Champs obligatoires", "Veuillez remplir le matricule, le nom, le prénom et la filière.")
            return

        try:
            # Code d'insertion  (pour l'inscription ou la réinscription)
            enregistrer_etudiant(
                matricule=mat, nom=nom, prenom=prenom, sexe=sexe,
                filiere=filiere, cycle=cycle, adresse=adresse,
                telephone=tel, email=email, id_niveau=1, statut="Inscrit"
            )
            messagebox.showinfo("Succès", f"Opération réussie pour l'étudiant {nom.upper()} !")
            self.reinitialiser_champs()
        except mysql.connector.Error as err:
            # Gestion de la mise à jour si doublon (cas de la réinscription directe)
            if err.errno == 1062:
                
                messagebox.showinfo("Information Réinscription", f"Le matricule '{mat}' existe déjà. La logique de mise à jour (UPDATE) sera finalisée lors de la synchronisation de samedi.")
            else:
                messagebox.showerror("Erreur SQL", f"Détail : {err}")

    def reinitialiser_champs(self):
        self.ent_matricule.delete(0, "end")
        self.ent_nom.delete(0, "end")
        self.ent_prenom.delete(0, "end")
        self.ent_filiere.delete(0, "end")
        self.ent_adresse.delete(0, "end")
        self.ent_telephone.delete(0, "end")
        self.ent_email.delete(0, "end")

if __name__ == "__main__":
    app = GesProInscriptionApp()
    app.mainloop()