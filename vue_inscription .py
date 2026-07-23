import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import date, datetime

# ReportLab pour la génération du reçu moderne
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

import controleur_inscription
import theme

# Configuration globale de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class GesProInscriptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Gestion des Inscriptions Universitaires")
        self.geometry("1280x820")
        self.minsize(1150, 750)
        self.resizable(True, True)
        self.configure(fg_color=theme.BG_FENETRE)

        # Centrer la fenêtre
        self.eval('tk::PlaceWindow . center')

        # Grille principale
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Contenu
        self.grid_rowconfigure(0, weight=1)

        
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
            text="PORTAIL DES INSCRIPTIONS", 
            font=("Helvetica", 10, "bold"), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_module.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")

        self.btn_active = ctk.CTkButton(
            self.nav_frame,
            text="📝  Dossier Étudiant",
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

        
        
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=0)
        self.main_content.grid_rowconfigure(1, weight=1)

        self.lbl_titre = ctk.CTkLabel(
            self.main_content, 
            text="Saisie & Gestion des Inscriptions Universitaires", 
            font=("Helvetica", 22, "bold"), 
            text_color=theme.TEXTE_TITRE
        )
        self.lbl_titre.grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.lbl_soustitre = ctk.CTkLabel(
            self.main_content, 
            text="Enregistrement des dossiers administratifs, paiements initiaux et suivi des promotions.", 
            font=("Helvetica", 11), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_soustitre.grid(row=0, column=0, sticky="w", pady=(20, 15))

        # Conteneur défilable
        self.scrollable_container = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        self.scrollable_container.grid(row=1, column=0, sticky="nsew")
        self.scrollable_container.grid_columnconfigure(0, weight=1)

        # -- SECTION 1 : FORMULAIRE D'INSCRIPTION --
        self.card_form = ctk.CTkFrame(
            self.scrollable_container, 
            fg_color=theme.BG_CARTE, 
            border_width=1, 
            border_color=theme.BORDURE_CARTE,
            corner_radius=12
        )
        self.card_form.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.card_form.grid_columnconfigure(0, weight=1, uniform="form")
        self.card_form.grid_columnconfigure(1, weight=1, uniform="form")

        self.creer_formulaire()

        # -- SECTION 2 : RECHERCHE & ADMINISTRATION --
        self.card_admin = ctk.CTkFrame(
            self.scrollable_container, 
            fg_color=theme.BG_CARTE, 
            border_width=1, 
            border_color=theme.BORDURE_CARTE,
            corner_radius=12
        )
        self.card_admin.grid(row=1, column=0, sticky="ew")
        self.card_admin.grid_columnconfigure(0, weight=1)

        self.creer_panneau_administration()

    # =====================================================================
    # CREATION DES COMPOSANTS GRAPHIQUES
    # =====================================================================
    def creer_formulaire(self):
        # COLONNE GAUCHE
        self.col_gauche = ctk.CTkFrame(self.card_form, fg_color="transparent")
        self.col_gauche.grid(row=0, column=0, padx=25, pady=20, sticky="nsew")

        self.lbl_section_perso = ctk.CTkLabel(
            self.col_gauche, text="COORDONNÉES DE L'ÉTUDIANT", 
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

        # Matricule
        ctk.CTkLabel(self.col_gauche, text="Matricule de l'Étudiant :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.search_frame = ctk.CTkFrame(self.col_gauche, fg_color="transparent")
        self.search_frame.pack(fill="x", pady=(0, 10))
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=0)

        self.ent_matricule = ctk.CTkEntry(self.search_frame, placeholder_text="Généré automatiquement à la validation", height=36, fg_color=theme.BG_CHAMP, state="disabled")
        self.ent_matricule.grid(row=0, column=0, sticky="ew")

        self.btn_recherche = ctk.CTkButton(
            self.search_frame, 
            text="🔍 Charger", 
            width=80, 
            height=36, 
            fg_color=theme.BOUTON_PRIMARY, 
            hover_color=theme.BOUTON_PRIMARY_HOVER,
            command=self.rechercher_et_remplir_etudiant,
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

        # Date de naissance
        ctk.CTkLabel(self.col_gauche, text="Date de naissance (JJ/MM/AAAA) :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_date_naiss = ctk.CTkEntry(self.col_gauche, placeholder_text="Ex: 15/04/2005", height=36, fg_color=theme.BG_CHAMP)
        self.ent_date_naiss.pack(fill="x", pady=(0, 10))

        # COLONNE DROITE
        self.col_droite = ctk.CTkFrame(self.card_form, fg_color="transparent")
        self.col_droite.grid(row=0, column=1, padx=25, pady=20, sticky="nsew")

        self.lbl_section_admin = ctk.CTkLabel(
            self.col_droite, text="ADRESSE, ORIENTATION & INTEGRATION", 
            font=("Helvetica", 12, "bold"), text_color=theme.BOUTON_PRIMARY
        )
        self.lbl_section_admin.pack(anchor="w", pady=(0, 10))

        # Email
        ctk.CTkLabel(self.col_droite, text="Adresse Email :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_email = ctk.CTkEntry(self.col_droite, placeholder_text="Ex: p.mboungou@gmail.com", height=36, fg_color=theme.BG_CHAMP)
        self.ent_email.pack(fill="x", pady=(0, 10))

        # Adresse
        ctk.CTkLabel(self.col_droite, text="Adresse Physique :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.ent_adresse = ctk.CTkEntry(self.col_droite, placeholder_text="Ex: 14 Rue des Écoles, Oyo", height=36, fg_color=theme.BG_CHAMP)
        self.ent_adresse.pack(fill="x", pady=(0, 10))

        # Filière
        ctk.CTkLabel(self.col_droite, text="Filière d'étude :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.combo_filiere = ctk.CTkComboBox(self.col_droite, values=["Gestion Comptable et du Personnel (GCP)", "Transport et Logistique(TL)", "Economie Numérique (EN)"], height=36, fg_color=theme.BG_CHAMP)
        self.combo_filiere.pack(fill="x", pady=(0, 10))

        # Niveau
        ctk.CTkLabel(self.col_droite, text="Niveau d'Étude :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.combo_niveau = ctk.CTkComboBox(self.col_droite, values=["Licence 1 (L1)", "Licence 2 (L2)", "Licence 3 (L3)", "BTS 1", "BTS 2"], height=36, fg_color=theme.BG_CHAMP)
        self.combo_niveau.pack(fill="x", pady=(0, 10))

        # Mode de paiement
        ctk.CTkLabel(self.col_droite, text="Mode de Paiement des Frais :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", pady=(2, 2))
        self.combo_mode = ctk.CTkComboBox(self.col_droite, values=["Espèces", "Chèque", "Virement Bancaire", "Mobile Money"], height=36, fg_color=theme.BG_CHAMP)
        self.combo_mode.pack(fill="x", pady=(0, 10))

        # Badge Financier
        self.frais_frame = ctk.CTkFrame(self.col_droite, fg_color="#F0FDF4", border_width=1, border_color="#DCFCE7")
        self.frais_frame.pack(fill="x", pady=(5, 10))
        
        self.lbl_montant_indicatif = ctk.CTkLabel(
            self.frais_frame, 
            text="Frais d'inscription/réinscription (Hors scolarité) : 10 000 FCFA", 
            font=("Helvetica", 11, "bold"), 
            text_color="#15803D"
        )
        self.lbl_montant_indicatif.pack(expand=True, pady=8)

        # Bouton principal
        self.btn_valider = ctk.CTkButton(
            self.col_droite,
            text="VALIDER L'OPÉRATION & GENERER LE REÇU",
            font=("Helvetica", 12, "bold"),
            fg_color=theme.BOUTON_PRIMARY,
            hover_color=theme.BOUTON_PRIMARY_HOVER,
            height=42,
            command=self.effectuer_inscription
        )
        self.btn_valider.pack(fill="x", pady=(10, 0))

    def creer_panneau_administration(self):
        self.admin_frame = ctk.CTkFrame(self.card_admin, fg_color="transparent")
        self.admin_frame.pack(fill="both", expand=True, padx=25, pady=20)

        self.lbl_admin_title = ctk.CTkLabel(
            self.admin_frame, 
            text="LISTE DES ÉTUDIANTS INSCRITS ET RÉINSCRITS", 
            font=("Helvetica", 12, "bold"), 
            text_color=theme.BOUTON_PRIMARY
        )
        self.lbl_admin_title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        # Filtres
        ctk.CTkLabel(self.admin_frame, text="Filière :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.filter_filiere = ctk.CTkComboBox(self.admin_frame, values=["Toutes", "Gestion Comptable et du Personnel (GCP)", "Transport et Logistique(TL)", "Economie Numérique (EN)"], width=230, height=32, fg_color=theme.BG_CHAMP)
        self.filter_filiere.grid(row=1, column=1, sticky="w", padx=(0, 20))

        ctk.CTkLabel(self.admin_frame, text="Niveau :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).grid(row=1, column=2, sticky="w", padx=(0, 10))
        self.filter_niveau = ctk.CTkComboBox(self.admin_frame, values=["Tous", "Licence 1 (L1)", "Licence 2 (L2)", "Licence 3 (L3)", "BTS 1", "BTS 2"], width=150, height=32, fg_color=theme.BG_CHAMP)
        self.filter_niveau.grid(row=1, column=3, sticky="w", padx=(0, 20))

        self.btn_charger_liste = ctk.CTkButton(
            self.admin_frame,
            text="🔄 Filtrer la Liste",
            font=("Helvetica", 12, "bold"),
            fg_color=theme.BOUTON_PRIMARY,
            hover_color=theme.BOUTON_PRIMARY_HOVER,
            width=130,
            height=32,
            command=self.charger_etudiants_table
        )
        self.btn_charger_liste.grid(row=1, column=4, sticky="w")

        # Table Treeview
        self.tree_frame = ctk.CTkFrame(self.admin_frame, fg_color="transparent")
        self.tree_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", pady=(15, 15))
        self.admin_frame.grid_rowconfigure(2, weight=1)

        colonnes = ("matricule", "nom", "prenom", "date_naiss", "email", "adresse", "filiere", "niveau", "type")
        self.tree = ttk.Treeview(self.tree_frame, columns=colonnes, show="headings", height=8)
        
        self.tree.heading("matricule", text="Matricule")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("prenom", text="Prénom")
        self.tree.heading("date_naiss", text="Date Naissance")
        self.tree.heading("email", text="Email")
        self.tree.heading("adresse", text="Adresse")
        self.tree.heading("filiere", text="Filière")
        self.tree.heading("niveau", text="Niveau")
        self.tree.heading("type", text="Type")

        self.tree.column("matricule", width=80, anchor="center")
        self.tree.column("nom", width=110, anchor="w")
        self.tree.column("prenom", width=110, anchor="w")
        self.tree.column("date_naiss", width=110, anchor="center")
        self.tree.column("email", width=140, anchor="w")
        self.tree.column("adresse", width=140, anchor="w")
        self.tree.column("filiere", width=150, anchor="w")
        self.tree.column("niveau", width=90, anchor="center")
        self.tree.column("type", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Barre d'actions basse
        self.actions_bar = ctk.CTkFrame(self.admin_frame, fg_color="transparent")
        self.actions_bar.grid(row=3, column=0, columnspan=5, sticky="ew")

        self.btn_export_pdf = ctk.CTkButton(
            self.actions_bar,
            text="🖨️  Imprimer la Liste (PDF)",
            font=("Helvetica", 12, "bold"),
            fg_color="#0F766E",
            hover_color="#0D9488",
            height=36,
            command=self.exporter_liste_pdf
        )
        self.btn_export_pdf.pack(side="left", padx=(0, 15))

        self.btn_supprimer = ctk.CTkButton(
            self.actions_bar,
            text="🗑️  Retirer l'Étudiant sélectionné",
            font=("Helvetica", 12, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            height=36,
            command=self.retirer_inscription
        )
        self.btn_supprimer.pack(side="left")

        self.charger_etudiants_table()

    # =====================================================================
    # LOGIQUE DE NAVIGATION ET DE RECHERCHE
    # =====================================================================
    def ajuster_champs_selon_type(self, type_op):
        if type_op == "Nouvelle Inscription":
            self.ent_matricule.configure(state="disabled", placeholder_text="Généré automatiquement")
            self.ent_matricule.delete(0, "end")
            self.btn_recherche.configure(state="disabled")
            self.vider_formulaire()
        else:
            self.ent_matricule.configure(state="normal", placeholder_text="Matricule de l'étudiant")
            self.btn_recherche.configure(state="normal")
            self.vider_formulaire()

    def vider_formulaire(self):
        self.ent_nom.delete(0, "end")
        self.ent_prenom.delete(0, "end")
        self.ent_date_naiss.delete(0, "end")
        self.ent_email.delete(0, "end")
        self.ent_adresse.delete(0, "end")

    # =====================================================================
    # ACTIONS DÉLÉGUÉES AU CONTRÔLEUR (logique métier + BDD + mise à jour UI)
    # Ces 4 méthodes ne font que transmettre l'instance de la fenêtre : toute
    # la logique (lecture des champs, calculs, accès BDD, messages, mise à
    # jour du tableau/formulaire) est implémentée dans controleur_inscription.py
    # =====================================================================
    def rechercher_et_remplir_etudiant(self):
        controleur_inscription.rechercher_et_remplir_etudiant(self)

    def effectuer_inscription(self):
        controleur_inscription.effectuer_inscription(self)

    def charger_etudiants_table(self):
        controleur_inscription.charger_etudiants_table(self)

    def retirer_inscription(self):
        controleur_inscription.retirer_inscription(self)

    # =====================================================================
    # CONCEPTION DU REÇU : LOOK MODERNE & FINTECH (HUMAIN ET PRO)
    # =====================================================================
    def generer_pdf_fiche_inscription(self, infos):
        nom_fichier = f"Recu_Caisse_Matricule_{infos['matricule']}.pdf"
        
        # Dimensions standard A4, marges confortables pour un rendu "Facture Moderne"
        doc = SimpleDocTemplate(
            nom_fichier, 
            pagesize=letter, 
            rightMargin=45, 
            leftMargin=45, 
            topMargin=45, 
            bottomMargin=40
        )
        
        # Définition des couleurs de la charte
        couleur_primaire = colors.HexColor('#1E3A8A')    # Bleu nuit académique
        couleur_valide = colors.HexColor('#059669')      # Émeraude de transaction
        couleur_texte = colors.HexColor('#1E293B')       # Slate 800 pour le texte
        couleur_mutile = colors.HexColor('#64748B')      # Slate 500 pour les libellés secondaires
        couleur_ligne = colors.HexColor('#F1F5F9')       # Slate 100 pour les lignes de séparation
        
        # Styles typographiques
        style_universite = ParagraphStyle('Univ', fontName='Helvetica-Bold', fontSize=12, textColor=couleur_primaire, alignment=1)
        style_agrement = ParagraphStyle('Agre', fontName='Helvetica-Oblique', fontSize=8, textColor=couleur_mutile, alignment=1, leading=10)
        style_devise = ParagraphStyle('Devise', fontName='Helvetica-Bold', fontSize=8, textColor=couleur_primaire, alignment=1, spaceAfter=20)
        
        style_grand_titre = ParagraphStyle('GTitre', fontName='Helvetica-Bold', fontSize=16, textColor=couleur_texte, alignment=0)
        style_reference = ParagraphStyle('Ref', fontName='Helvetica', fontSize=9, textColor=couleur_mutile, alignment=0)
        style_status = ParagraphStyle('Status', fontName='Helvetica-Bold', fontSize=10, textColor=couleur_valide, alignment=2)
        
        style_h2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, textColor=couleur_primaire, spaceBefore=10, spaceAfter=8)
        
        style_label = ParagraphStyle('Lbl', fontName='Helvetica', fontSize=9.5, textColor=couleur_mutile)
        style_value = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=9.5, textColor=couleur_texte)
        style_value_normal = ParagraphStyle('ValNorm', fontName='Helvetica', fontSize=9.5, textColor=couleur_texte)
        
        style_montant_principal = ParagraphStyle('MntPrin', fontName='Helvetica-Bold', fontSize=20, textColor=couleur_valide, alignment=2)
        style_montant_label = ParagraphStyle('MntLbl', fontName='Helvetica-Bold', fontSize=9, textColor=couleur_mutile, alignment=2)

        story = []
        
        # 1. EN-TÊTE ACADÉMIQUE PROFESSIONNEL
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_universite))
        story.append(Paragraph("Etablissement agréé sous l'arrêté n°7061/MESRSIT/CAB", style_agrement))
        story.append(Paragraph('"Rigueur - Réussite - Innovation"', style_devise))
        
        # 2. BLOC DE TRANSACTION (MODERNE - STYLE FINTECH)
        header_table_data = [
            [
                Paragraph(f"<b>REÇU DE SCOLARITÉ</b><br/><font size=9 color='#64748B'>N° {infos['matricule']}-{date.today().year}</font>", style_grand_titre),
                Paragraph("STATUT : TRANSACTION EFFECTUÉE", style_status)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[260, 260])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(header_table)
        
        # Ligne de séparation épurée
        sep_table = Table([[""]], colWidths=[520])
        sep_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, couleur_ligne),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ]))
        story.append(sep_table)
        story.append(Spacer(1, 5))
        
        # 3. CONTENU DOUBLE COLONNE : Profil Étudiant (Gauche) vs Fiche de Caisse (Droite)
        col_gauche_data = [
            [Paragraph("INFORMATIONS ÉTUDIANT", style_h2)],
            [Paragraph("Matricule", style_label)],
            [Paragraph(f"#{infos['matricule']}", style_value)],
            [Spacer(1, 4)],
            [Paragraph("Nom & Prénom", style_label)],
            [Paragraph(f"{infos['nom']} {infos['prenom']}", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Parcours Académique", style_label)],
            [Paragraph(f"<b>{infos['niveau']}</b><br/>{infos['filiere']}", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Coordonnées & Adresse", style_label)],
            [Paragraph(f"{infos['email']}<br/>{infos['adresse']}", style_value_normal)],
        ]
        
        col_droite_data = [
            [Paragraph("DÉTAIL DU RÈGLEMENT", style_h2)],
            [Paragraph("Nature de l'opération", style_label)],
            [Paragraph(f"Frais de {infos['type']}", style_value)],
            [Spacer(1, 4)],
            [Paragraph("Mode de versement", style_label)],
            [Paragraph(f"{infos['mode']}", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Date comptable", style_label)],
            [Paragraph(f"{infos['date']}", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Année académique", style_label)],
            [Paragraph(f"{infos['annee']}", style_value_normal)],
        ]
        
        table_gauche = Table(col_gauche_data, colWidths=[240])
        table_gauche.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        
        table_droite = Table(col_droite_data, colWidths=[240])
        table_droite.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        
        corps_table = Table([[table_gauche, table_droite]], colWidths=[260, 260])
        corps_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ]))
        story.append(corps_table)
        
        # Autre ligne de séparation
        story.append(sep_table)
        story.append(Spacer(1, 5))
        
        # 4. CARTE FINANCIÈRE DE SYNTHÈSE (MODERNE ET VISUELLE)
        carte_financiere_data = [
            [
                Paragraph("<b>FRAIS D'INSCRIPTION ACQUITTÉS</b><br/><font size=8 color='#64748B'>Hors scolarité annuelle</font>", style_label),
                Paragraph(f"{infos['montant']}", style_montant_principal)
            ],
            [
                Paragraph("Coût Annuel de la Formation", style_label),
                Paragraph(f"<b>{infos['total_scolarite']}</b>", ParagraphStyle('SubM', fontName='Helvetica', fontSize=10, textColor=couleur_texte, alignment=2))
            ],
            [
                Paragraph("<font color='#EF4444'><b>RESTE À PAYER SUR LA SCOLARITÉ</b></font>", style_label),
                Paragraph(f"<b>{infos['reste']}</b>", ParagraphStyle('SubM2', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#EF4444'), alignment=2))
            ]
        ]
        
        carte_financiere = Table(carte_financiere_data, colWidths=[280, 220])
        carte_financiere.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
            ('RIGHTPADDING', (0,0), (-1,-1), 15),
            ('LINEBELOW', (0,0), (-1,-2), 0.5, couleur_ligne),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ]))
        story.append(carte_financiere)
        story.append(Spacer(1, 25))
        
        # 5. CODE DE SIGNATURES COMPATIBLES
        sig_data = [
            [
                Paragraph("<b>Le Déposant / L'Étudiant</b><br/><font size=7.5 color='#64748B'>Signature précédée de la mention 'Lu et approuvé'</font><br/><br/><br/>", style_label),
                Paragraph("<b>Pour le Service Financier</b><br/><font size=7.5 color='#64748B'>Visa, Date et Cachet d'Oyo</font><br/><br/><br/>", ParagraphStyle('SigR', parent=style_label, alignment=2))
            ]
        ]
        sig_table = Table(sig_data, colWidths=[260, 260])
        story.append(sig_table)
        story.append(Spacer(1, 15))
        
        # 6. MENTIONS LEGALES ÉPURÉES
        story.append(Paragraph(
            "<i>Note importante : Conformément aux règlements intérieurs de l'ISPSLO, les frais d'inscription et de réinscription sont définitivement acquis à l'établissement et ne peuvent faire l'objet d'aucun remboursement. Le solde restant dû de la scolarité devra être régularisé selon l'échéancier convenu.</i>", 
            ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=7, textColor=couleur_mutile, leading=9)
        ))
        
        doc.build(story)
        self.ouvrir_pdf(nom_fichier)

    # =====================================================================
    # EXPORTATION DE LA LISTE DE LA PROMOTION (PAYSAGE)
    # =====================================================================
    def exporter_liste_pdf(self):
        filiere_doc = self.filter_filiere.get()
        niveau_doc = self.filter_niveau.get()
        date_generation = date.today().strftime('%d/%m/%Y')

        nom_fichier_liste = f"Liste_Etudiants_{filiere_doc.replace(' ', '_')}_{niveau_doc.replace(' ', '_')}.pdf"
        
        doc = SimpleDocTemplate(nom_fichier_liste, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        
        styles = getSampleStyleSheet()
        style_titre_liste = ParagraphStyle('TitreL', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#1E3A8A'), alignment=1, spaceAfter=8)
        style_stitre_liste = ParagraphStyle('STitreL', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#475569'), alignment=1, spaceAfter=15)
        style_th = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=1)
        style_td = ParagraphStyle('TD', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#1E293B'))
        style_td_center = ParagraphStyle('TDC', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#1E293B'), alignment=1)

        story = []
        
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", ParagraphStyle('HeaderU', fontName='Helvetica-Bold', fontSize=11, alignment=1)))
        story.append(Paragraph("<b>REGISTRE ACADÉMIQUE DES PROMOTIONS</b>", style_titre_liste))
        story.append(Paragraph(f"Filière : {filiere_doc}  |  Niveau : {niveau_doc}  |  Date d'Édition : {date_generation}", style_stitre_liste))

        data_table = [[
            Paragraph("Matricule", style_th),
            Paragraph("Nom & Prénom", style_th),
            Paragraph("Né(e) le", style_th),
            Paragraph("Email", style_th),
            Paragraph("Adresse", style_th),
            Paragraph("Filière", style_th),
            Paragraph("Niveau", style_th),
            Paragraph("Type", style_th)
        ]]

        for child in self.tree.get_children():
            row_vals = self.tree.item(child, 'values')
            data_table.append([
                Paragraph(str(row_vals[0]), style_td_center),
                Paragraph(f"{row_vals[1]} {row_vals[2]}", style_td),
                Paragraph(str(row_vals[3]), style_td_center),
                Paragraph(str(row_vals[4]), style_td),
                Paragraph(str(row_vals[5]), style_td),
                Paragraph(str(row_vals[6]), style_td),
                Paragraph(str(row_vals[7]), style_td_center),
                Paragraph(str(row_vals[8]), style_td_center)
            ])

        col_widths = [55, 120, 65, 110, 110, 140, 60, 70]
        
        t = Table(data_table, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ]))
        
        story.append(t)
        story.append(Spacer(1, 20))
        
        sig_data = [
            [Paragraph("", style_td), Paragraph("<b>Fait à Oyo, le " + date_generation + "<br/>Le Secrétariat Académique</b>", ParagraphStyle('FaitA', fontName='Helvetica-Bold', fontSize=9, alignment=2))]
        ]
        sig_table = Table(sig_data, colWidths=[450, 280])
        story.append(sig_table)

        doc.build(story)
        self.ouvrir_pdf(nom_fichier_liste)

    def ouvrir_pdf(self, nom_fichier):
        if sys.platform.startswith('darwin'): 
            subprocess.call(('open', nom_fichier))
        elif os.name == 'nt': 
            os.startfile(nom_fichier)
        elif os.name == 'posix': 
            subprocess.call(('xdg-open', nom_fichier))

    # =====================================================================
    # NAVIGATION & CYCLES DE VIE
    # =====================================================================
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
