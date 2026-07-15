import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import messagebox
from datetime import date

# ReportLab pour le reçu de caisse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from config_db import obtenir_connexion
import theme

# Configuration globale de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class GesProInscriptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Inscription Administrative")
        self.geometry("1150x760")
        self.minsize(1050, 700)
        self.resizable(True, True)
        self.configure(fg_color=theme.BG_FENETRE)

        # Centrer la fenêtre
        self.eval('tk::PlaceWindow . center')

        # Grille principale
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Contenu principal
        self.grid_rowconfigure(0, weight=1)

        
        # 1. BARRE LATÉRALE (SIDEBAR)
        
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=theme.BG_CARTE)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(2, weight=1)

        self.lbl_logo = ctk.CTkLabel(
            self.sidebar, 
            text="🎓  GesPro", 
            font=("Helvetica", 22, "bold"), 
            text_color=theme.TEXTE_TITRE
        )
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(30, 5), sticky="w")

        self.lbl_module = ctk.CTkLabel(
            self.sidebar, 
            text="ADMISSIONS & INSCRIPTIONS", 
            font=("Helvetica", 10, "bold"), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_module.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")

        self.btn_active = ctk.CTkButton(
            self.nav_frame,
            text="📝  Dossier Inscription",
            font=("Helvetica", 13, "bold"),
            fg_color=theme.BG_FENETRE,
            text_color=theme.TEXTE_TITRE,
            height=40,
            anchor="w",
            corner_radius=8,
            state="disabled"
        )
        self.btn_active.pack(fill="x", pady=5)

        self.btn_retour = ctk.CTkButton(
            self.sidebar,
            text="🏠  Menu Principal",
            font=("Helvetica", 12, "bold"),
            fg_color=theme.BOUTON_PRIMARY,
            hover_color=theme.BOUTON_PRIMARY_HOVER,
            text_color="white",
            height=38,
            command=self.retour_menu
        )
        self.btn_retour.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.btn_deco = ctk.CTkButton(
            self.sidebar,
            text="🚪  Se déconnecter",
            font=("Helvetica", 12, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            height=38,
            command=self.deconnexion
        )
        self.btn_deco.grid(row=4, column=0, padx=20, pady=(0, 30), sticky="ew")

        
        # 2. CONTENU PRINCIPAL
        
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=0)
        self.main_content.grid_rowconfigure(1, weight=1)

        self.lbl_titre = ctk.CTkLabel(
            self.main_content, 
            text="Saisie des Inscriptions & Réinscriptions", 
            font=("Helvetica", 24, "bold"), 
            text_color=theme.TEXTE_TITRE
        )
        self.lbl_titre.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.lbl_soustitre = ctk.CTkLabel(
            self.main_content, 
            text="Formulaire d'enregistrement synchronisé avec la base de données relationnelle de l'établissement.", 
            font=("Helvetica", 12), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_soustitre.grid(row=0, column=0, sticky="w", pady=(25, 20))

        # Carte du Formulaire
        self.card = ctk.CTkFrame(
            self.main_content, 
            fg_color=theme.BG_CARTE, 
            border_width=1, 
            border_color=theme.BORDURE_CARTE,
            corner_radius=12
        )
        self.card.grid(row=1, column=0, sticky="nsew")
        
        self.card.grid_columnconfigure(0, weight=1, uniform="form")
        self.card.grid_columnconfigure(1, weight=1, uniform="form")
        self.card.grid_rowconfigure(0, weight=1)

        self.creer_formulaire()

    def creer_formulaire(self):
        
        #  Profil personnel de l'Élève 
       
        self.col_gauche = ctk.CTkFrame(self.card, fg_color="transparent")
        self.col_gauche.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")

        self.lbl_section_perso = ctk.CTkLabel(
            self.col_gauche, text="COORDONNÉES DE L'ÉLÈVE", 
            font=("Helvetica", 12, "bold"), text_color=theme.BOUTON_PRIMARY
        )
        self.lbl_section_perso.pack(anchor="w", pady=(0, 10))

        # Type d'opération
        ctk.CTkLabel(self.col_gauche, text="Type d'Opération :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.combo_type = ctk.CTkComboBox(
            self.col_gauche, 
            values=["Nouvelle Inscription", "Réinscription"], 
            height=36, 
            fg_color=theme.BG_CHAMP,
            command=self.ajuster_champs_selon_type
        )
        self.combo_type.pack(fill="x", pady=(0, 10))

        # ID Unique de l'Élève (pour recherche lors d'une réinscription)
        ctk.CTkLabel(self.col_gauche, text="ID Unique de l'Élève :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.search_frame = ctk.CTkFrame(self.col_gauche, fg_color="transparent")
        self.search_frame.pack(fill="x", pady=(0, 10))
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=0)

        self.ent_id_eleve = ctk.CTkEntry(self.search_frame, placeholder_text="Généré automatiquement à la validation", height=36, fg_color=theme.BG_CHAMP, state="disabled")
        self.ent_id_eleve.grid(row=0, column=0, sticky="ew")

        self.btn_recherche = ctk.CTkButton(
            self.search_frame, 
            text="🔍 Charger", 
            width=80, 
            height=36, 
            fg_color=theme.BOUTON_PRIMARY, 
            hover_color=theme.BOUTON_PRIMARY_HOVER,
            command=self.rechercher_et_remplir_eleve,
            state="disabled"
        )
        self.btn_recherche.grid(row=0, column=1, padx=(10, 0), sticky="e")

        # Nom
        ctk.CTkLabel(self.col_gauche, text="Nom :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_nom = ctk.CTkEntry(self.col_gauche, placeholder_text="Ex: MBOUNGOU", height=36, fg_color=theme.BG_CHAMP)
        self.ent_nom.pack(fill="x", pady=(0, 10))

        # Prénom
        ctk.CTkLabel(self.col_gauche, text="Prénom :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_prenom = ctk.CTkEntry(self.col_gauche, placeholder_text="Ex: Pierre-Marie", height=36, fg_color=theme.BG_CHAMP)
        self.ent_prenom.pack(fill="x", pady=(0, 10))

        # Âge
        ctk.CTkLabel(self.col_gauche, text="Âge :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_age = ctk.CTkEntry(self.col_gauche, placeholder_text="Ex: 21", height=36, fg_color=theme.BG_CHAMP)
        self.ent_age.pack(fill="x", pady=(0, 10))

        # COLONNE DROITE : Coordonnées, Cursus & Encaissement
    
        self.col_droite = ctk.CTkFrame(self.card, fg_color="transparent")
        self.col_droite.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")

        self.lbl_section_admin = ctk.CTkLabel(
            self.col_droite, text="ADRESSE, ORIENTATION & PAIEMENT", 
            font=("Helvetica", 12, "bold"), text_color=theme.BOUTON_PRIMARY
        )
        self.lbl_section_admin.pack(anchor="w", pady=(0, 10))

        # Email
        ctk.CTkLabel(self.col_droite, text="Adresse Email :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_email = ctk.CTkEntry(self.col_droite, placeholder_text="Ex: p.mboungou@gmail.com", height=36, fg_color=theme.BG_CHAMP)
        self.ent_email.pack(fill="x", pady=(0, 10))

        # Adresse (Mappe avec 'addresse' dans la table Eleve)
        ctk.CTkLabel(self.col_droite, text="Adresse Physique :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_adresse = ctk.CTkEntry(self.col_droite, placeholder_text="Ex: 14 Rue des Écoles, Oyo", height=36, fg_color=theme.BG_CHAMP)
        self.ent_adresse.pack(fill="x", pady=(0, 10))

        # Filière
        ctk.CTkLabel(self.col_droite, text="Filière d'étude :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.combo_filiere = ctk.CTkComboBox(self.col_droite, values=["Génie Civil & Projets (GCP)", "Réseaux & Télécoms (RT)", "Génie Logiciel (GL)", "Management des Projets (MP)"], height=36, fg_color=theme.BG_CHAMP)
        self.combo_filiere.pack(fill="x", pady=(0, 10))

        # Niveau
        ctk.CTkLabel(self.col_droite, text="Niveau d'Étude :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.combo_niveau = ctk.CTkComboBox(self.col_droite, values=["Licence 1 (L1)", "Licence 2 (L2)", "Licence 3 (L3)", "BTS 1", "BTS 2"], height=36, fg_color=theme.BG_CHAMP)
        self.combo_niveau.pack(fill="x", pady=(0, 10))

        # Mode de paiement
        ctk.CTkLabel(self.col_droite, text="Mode de Paiement :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.combo_mode = ctk.CTkComboBox(self.col_droite, values=["Espèces", "Chèque", "Virement Bancaire", "Mobile Money"], height=36, fg_color=theme.BG_CHAMP)
        self.combo_mode.pack(fill="x", pady=(0, 10))

        # Badge Financier (Frais fixés à 10 000 FCFA)
        self.frais_frame = ctk.CTkFrame(self.col_droite, fg_color="#F0FDF4", border_width=1, border_color="#DCFCE7", height=40)
        self.frais_frame.pack(fill="x", pady=(5, 10))
        
        self.lbl_montant_indicatif = ctk.CTkLabel(
            self.frais_frame, 
            text="Frais obligatoires : 10 000 FCFA", 
            font=("Helvetica", 12, "bold"), 
            text_color="#15803D"
        )
        self.lbl_montant_indicatif.pack(expand=True, pady=8)

        # Bouton d'action principal
        self.btn_valider = ctk.CTkButton(
            self.col_droite,
            text="VALIDER L'OPÉRATION & GÉNÉRER LE REÇU",
            font=("Helvetica", 12, "bold"),
            fg_color=theme.BOUTON_PRIMARY,
            hover_color=theme.BOUTON_PRIMARY_HOVER,
            height=42,
            command=self.effectuer_inscription
        )
        self.btn_valider.pack(fill="x", pady=(10, 0))

        # ACTIONS DU FORMULAIRE ET DE LA RECHERCHE
   
    def ajuster_champs_selon_type(self, type_op):
        """Active ou désactive la recherche par ID."""
        if type_op == "Nouvelle Inscription":
            self.ent_id_eleve.configure(state="disabled", placeholder_text="Généré automatiquement à la validation")
            self.ent_id_eleve.delete(0, "end")
            self.btn_recherche.configure(state="disabled")
            self.vider_formulaire()
        else: # Réinscription
            self.ent_id_eleve.configure(state="normal", placeholder_text="Entrer l'ID de l'élève")
            self.btn_recherche.configure(state="normal")
            self.vider_formulaire()

    def vider_formulaire(self):
        self.ent_nom.delete(0, "end")
        self.ent_prenom.delete(0, "end")
        self.ent_age.delete(0, "end")
        self.ent_email.delete(0, "end")
        self.ent_adresse.delete(0, "end")

    def rechercher_et_remplir_eleve(self):
        """Lit l'ID élève et pré-remplit les champs de la BDD."""
        id_eleve = self.ent_id_eleve.get().strip()
        if not id_eleve:
            messagebox.showwarning("Recherche vide", "Veuillez spécifier un ID unique d'élève à charger.")
            return

        try:
            conn = obtenir_connexion()
            cursor = conn.cursor()

            # Note : On utilise 'addresse' avec deux 's' pour correspondre exactement à ta BDD
            query = """
                SELECT e.nom, e.prenom, e.age, e.email, e.addresse, f.nom, n.niveau 
                FROM Eleve e
                LEFT JOIN Inscription i ON e.id = i.etudiant_id
                LEFT JOIN Programme p ON i.programme_id = p.id
                LEFT JOIN Filiere f ON p.filiere_id = f.id
                LEFT JOIN Niveau n ON p.niveau_id = n.id
                WHERE e.id = %s
                ORDER BY i.id DESC LIMIT 1
            """
            cursor.execute(query, (id_eleve,))
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                self.vider_formulaire()
                self.ent_nom.insert(0, result[0] or "")
                self.ent_prenom.insert(0, result[1] or "")
                self.ent_age.insert(0, str(result[2]) if result[2] is not None else "")
                self.ent_email.insert(0, result[3] or "")
                self.ent_adresse.insert(0, result[4] or "") # Mappe 'addresse' de la BDD

                if result[5]:
                    self.combo_filiere.set(result[5])
                if result[6]:
                    self.combo_niveau.set(result[6])

                messagebox.showinfo("Élève Chargé", f"Données de {result[0]} {result[1]} importées.")
            else:
                messagebox.showerror("Non trouvé", f"Aucun élève trouvé avec l'ID unique : {id_eleve}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur SQL : {e}")

    # =====================================================================
    # LOGIQUE D'INSCRIPTION & VALIDATION BDD
    # =====================================================================
    def effectuer_inscription(self):
        type_op = self.combo_type.get()
        id_eleve_saisi = self.ent_id_eleve.get().strip()
        nom = self.ent_nom.get().strip().upper()
        prenom = self.ent_prenom.get().strip()
        age = self.ent_age.get().strip()
        email = self.ent_email.get().strip()
        addresse = self.ent_adresse.get().strip() # Variable addresse
        filiere = self.combo_filiere.get()
        niveau = self.combo_niveau.get()
        mode_paiement = self.combo_mode.get()

        # Validation de saisie obligatoire
        if not nom or not prenom or not age or not email or not addresse:
            messagebox.showwarning("Saisie incomplète", "Veuillez remplir toutes les informations personnelles requises pour l'élève.")
            return

        try:
            conn = obtenir_connexion()
            cursor = conn.cursor()

            # 1. Gestion de la table 'Eleve' (Création ou Mise à jour)
            if type_op == "Nouvelle Inscription":
                query_eleve = """
                    INSERT INTO Eleve (nom, prenom, age, email, addresse) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_eleve, (nom, prenom, age, email, addresse))
                eleve_id = cursor.lastrowid
            else:
                if not id_eleve_saisi:
                    messagebox.showerror("Erreur", "L'ID Unique de l'élève est requis pour effectuer une réinscription.")
                    cursor.close()
                    conn.close()
                    return
                eleve_id = int(id_eleve_saisi)
                query_update = """
                    UPDATE Eleve SET nom=%s, prenom=%s, age=%s, email=%s, addresse=%s 
                    WHERE id=%s
                """
                cursor.execute(query_update, (nom, prenom, age, email, addresse, eleve_id))

            # 2. Récupérer l'identifiant du programme académique choisi
            query_prog = """
                SELECT p.id FROM Programme p
                JOIN Filiere f ON p.filiere_id = f.id
                JOIN Niveau n ON p.niveau_id = n.id
                WHERE f.nom = %s AND n.niveau = %s
            """
            cursor.execute(query_prog, (filiere, niveau))
            result_prog = cursor.fetchone()
            
            if not result_prog:
                messagebox.showerror("Erreur Programme", f"La configuration académique {filiere} en {niveau} n'existe pas.")
                cursor.close()
                conn.close()
                return
            programme_id = result_prog[0]

            # 3. Récupérer l'Année Académique Active
            cursor.execute("SELECT id, libelle FROM Annee_academique WHERE statut = 'Active'")
            result_annee = cursor.fetchone()
            if not result_annee:
                messagebox.showerror("Erreur Système", "Aucune année académique active n'est paramétrée.")
                cursor.close()
                conn.close()
                return
            annee_id, annee_libelle = result_annee[0], result_annee[1]

            # 4. Enregistrer l'Inscription administrative
            query_ins = """
                INSERT INTO Inscription (etudiant_id, programme_id, annee_academique_id, date_inscription, type_inscription)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_ins, (eleve_id, programme_id, annee_id, date.today().strftime('%Y-%m-%d'), type_op))
            inscription_id = cursor.lastrowid

            # 5. Enregistrer le Paiement (Frais uniques de caisse : 10 000 FCFA)
            query_pay = """
                INSERT INTO Paiement (inscription_id, montant, datePaiement, modePaiement)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_pay, (inscription_id, 10000, date.today().strftime('%Y-%m-%d'), mode_paiement))

            conn.commit()
            cursor.close()
            conn.close()

            # Préparation et ouverture du document de reçu PDF
            infos_recu = {
                'id_eleve': str(eleve_id),
                'nom': nom,
                'prenom': prenom,
                'age': age,
                'email': email,
                'adresse': addresse,
                'filiere': filiere,
                'niveau': niveau,
                'annee': annee_libelle,
                'type': type_op,
                'mode': mode_paiement,
                'montant': "10 000 FCFA",
                'date': date.today().strftime('%d/%m/%Y')
            }
            
            self.generer_pdf_fiche_inscription(infos_recu)
            messagebox.showinfo("Succès", f"Opération validée !\nID Unique Élève : {eleve_id}")
            
            # Nettoyage des champs
            self.vider_formulaire()
            if type_op == "Réinscription":
                self.ent_id_eleve.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Erreur Base de Données", f"Échec de l'enregistrement : {e}")

    
    # IMPRESSION DU REÇU 
   
    def generer_pdf_fiche_inscription(self, infos):
        nom_fichier = f"Recu_Caisse_Eleve_{infos['id_eleve']}.pdf"
        doc = SimpleDocTemplate(nom_fichier, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        
        style_entete = ParagraphStyle('Entete', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#1E3A8A'), alignment=1)
        style_devise = ParagraphStyle('Devise', fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#475569'), alignment=1)
        style_titre = ParagraphStyle('TitreFiche', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=5)
        style_meta = ParagraphStyle('Meta', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#475569'), alignment=1, spaceAfter=15)
        
        style_label = ParagraphStyle('LabelStyle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#475569'))
        style_valeur = ParagraphStyle('ValueStyle', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#1E293B'))
        
        story = []
        
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_entete))
        story.append(Paragraph("ISPSLO - Agrément Ministériel N° 0418/MESRST-CAB", style_devise))
        story.append(Paragraph('"Savoir - Rigueur - Excellence"', style_devise))
        story.append(Spacer(1, 15))
        
        style_badge = ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#065F46'), alignment=1, spaceAfter=10)
        story.append(Paragraph("<b>[ RÈGLEMENT EFFECTUÉ ]</b>", style_badge))
        
        story.append(Paragraph("REÇU DE CAISSE ET DE SCOLARITÉ", style_titre))
        story.append(Paragraph(f"Nº Reçu: REC-2026-INS-{infos['id_eleve']} | Date: {infos['date']}", style_meta))
        
        donnees = [
            [Paragraph("ID Unique Élève :", style_label), Paragraph(f"<b>{infos['id_eleve']}</b>", style_valeur)],
            [Paragraph("Nom & Prénom :", style_label), Paragraph(f"{infos['nom']} {infos['prenom']}", style_valeur)],
            [Paragraph("Âge & Email :", style_label), Paragraph(f"{infos['age']} ans  -  {infos['email']}", style_valeur)],
            [Paragraph("Adresse Physique :", style_label), Paragraph(infos['adresse'], style_valeur)],
            [Paragraph("Filière & Spécialité :", style_label), Paragraph(infos['filiere'], style_valeur)],
            [Paragraph("Niveau d'Étude :", style_label), Paragraph(infos['niveau'], style_valeur)],
            [Paragraph("Année Académique :", style_label), Paragraph(infos['annee'], style_valeur)],
            [Paragraph("Nature de l'Opération :", style_label), Paragraph(f"<b>{infos['type']}</b>", style_valeur)],
            [Paragraph("Mode de Paiement :", style_label), Paragraph(infos['mode'], style_valeur)],
            [Paragraph("TOTAL ENCAISSÉ :", style_label), Paragraph(f"<b>{infos['montant']}</b>", ParagraphStyle('Tot', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#1E3A8A')))]
        ]
        
        tableau = Table(donnees, colWidths=[200, 300])
        tableau.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(tableau)
        story.append(Spacer(1, 20))
        
        sig_data = [
            [Paragraph("<b>L'Étudiant / Le Déposant</b><br/><br/><br/>Signature", style_label),
             Paragraph("<b>Pour l'Administration (Caisse)</b><br/><br/><br/>Signature et Cachet", ParagraphStyle('SigR', parent=style_label, alignment=2))]
        ]
        sig_table = Table(sig_data, colWidths=[250, 250])
        story.append(sig_table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("<i>Note: Les droits d'inscription et de réinscription sont réglementairement non remboursables.</i>", ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#64748B'))))
        
        doc.build(story)
        self.ouvrir_pdf(nom_fichier)

    def ouvrir_pdf(self, nom_fichier):
        if sys.platform.startswith('darwin'): subprocess.call(('open', nom_fichier))
        elif os.name == 'nt': os.startfile(nom_fichier)
        elif os.name == 'posix': subprocess.call(('xdg-open', nom_fichier))

    
    # NAVIGATION
    
    def retour_menu(self):
        self.destroy()
        from menu_app import MenuPrincipalApp
        app = MenuPrincipalApp()
        app.mainloop()

    def deconnexion(self):
        self.destroy()
        from vue_connexion import ConnexionApp
        app = ConnexionApp()
        app.mainloop()

if __name__ == "__main__":
    app = GesProInscriptionApp()
    app.mainloop()