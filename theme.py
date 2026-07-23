# theme.py

# --- COULEURS D'ARRIÈRE-PLAN ---
from paiement_app import FICHIER_SUIVI, FRAIS_INSCRIPTION_MONTANT, GRILLE_TARIFAIRE


import customtkinter as ctk
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


import json
import os
import subprocess
import sys
from datetime import date
from tkinter import messagebox


BG_FENETRE = ("#F1F5F9", "#0F172A")  # Blanc cassé épuré / Bleu nuit moderne
BG_CARTE = ("#FFFFFF", "#1E293B")     # Blanc pur / Gris ardoise (Slate 800)

# --- COULEURS DES BORDURES ---
BORDURE_CARTE = ("#E2E8F0", "#334155") # Gris clair / Gris bleuté subtil

# --- COULEURS DE TEXTE ---
TEXTE_TITRE = ("#1A365D", "#60A5FA")   # Bleu marine royal / Bleu électrique
TEXTE_SECONDAIRE = ("#64748B", "#94A3B8") # Gris ardoise clair / Gris moyen

# --- COULEURS DES COMPOSANTS (Champs de saisie, etc.) ---
BG_CHAMP = ("#F8FAFC", "#0F172A")      # Blanc bleuté très clair / Bleu nuit profond

# --- COULEURS DES BOUTONS (Thème Principal) ---
BOUTON_PRIMARY = ("#1A365D", "#3B82F6") # Bleu foncé / Bleu brillant
BOUTON_PRIMARY_HOVER = ("#2A4D7C", "#2563EB") # Légère variation au survol

# --- BOUTONS SECONDAIRES OU ACTIONS SPÉCIFIQUES ---
BOUTON_SUCCESS = ("#10B981", "#059669") # Vert émeraude (idéal pour les paiements en S2)
BOUTON_SUCCESS_HOVER = ("#059669", "#047857")


class GesProPaiementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Caisse, Scolarité & Inscription")
        self.geometry("740x620")
        self.resizable(False, False)

        # Initialisation du fichier de données local
        if not os.path.exists(FICHIER_SUIVI):
            with open(FICHIER_SUIVI, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)

        # Variables de contrôle
        self.var_matricule = ctk.StringVar()
        self.var_nom = ctk.StringVar()
        self.var_niveau = ctk.StringVar(value=list(GRILLE_TARIFAIRE.keys())[0])
        self.var_montant = ctk.StringVar()
        self.var_type_frais = ctk.StringVar(value="Mensualité")

        # Ordre des modes de paiement :
        # 1. Espèces en premier | 2. Banques spécifiques | 3. Les restants en dernier
        self.modes_paiement = [
            "Espèces",
            "Virement - BGFI BANK",
            "Virement - MUCODEC",
            "Virement - BANK OF AFRICA",
            "Mobile Money (MTN MoMo)",
            "Airtel Money",
            "Chèque"
        ]
        self.var_mode_paiement = ctk.StringVar(value=self.modes_paiement[0])

        # --- CONCEPTION DE L'INTERFACE GRAPHIQUE ---

        # En-tête
        self.head_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.head_frame.pack(fill="x", pady=(15, 5))

        self.lbl_titre = ctk.CTkLabel(
            self.head_frame,
            text="PORTAIL DE CAISSE SCOLAIRE (BTS & LICENCE)",
            font=("Helvetica", 16, "bold"),
            text_color="#1E3A8A"
        )
        self.lbl_titre.pack()

        self.lbl_desc = ctk.CTkLabel(
            self.head_frame,
            text="Suivi automatisé du reste à payer annuel après déduction des mensualités.",
            font=("Helvetica", 11),
            text_color="#64748B"
        )
        self.lbl_desc.pack(pady=2)

        # Formulaire principal
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="both", expand=True, padx=45, pady=10)

        # Ligne 1 : Matricule & Nom Complet
        self.lbl_mat = ctk.CTkLabel(self.form_frame, text="Matricule Étudiant :", font=("Helvetica", 11, "bold"))
        self.lbl_mat.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        self.ent_mat = ctk.CTkEntry(self.form_frame, textvariable=self.var_matricule, width=240, placeholder_text="Ex: 2026-GCP-0042")
        self.ent_mat.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
        # Déclenchement automatique dès que l'utilisateur clique ailleurs ou appuie sur Entrée
        self.ent_mat.bind("<FocusOut>", self.charger_infos_etudiant)
        self.ent_mat.bind("<Return>", self.charger_infos_etudiant)

        self.lbl_nom = ctk.CTkLabel(self.form_frame, text="Nom & Prénom(s) :", font=("Helvetica", 11, "bold"))
        self.lbl_nom.grid(row=0, column=1, padx=20, pady=(15, 5), sticky="w")
        self.ent_nom = ctk.CTkEntry(self.form_frame, textvariable=self.var_nom, width=240, placeholder_text="Nom complet")
        self.ent_nom.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="w")

        # Ligne 2 : Année d'études & Type de Versement
        self.lbl_niveau = ctk.CTkLabel(self.form_frame, text="Année d'études (BTS/Licence) :", font=("Helvetica", 11, "bold"))
        self.lbl_niveau.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        # OptionMenu ou ComboBox pour l'année d'études avec callback sur changement
        self.combo_niveau = ctk.CTkComboBox(
            self.form_frame,
            values=list(GRILLE_TARIFAIRE.keys()),
            textvariable=self.var_niveau,
            width=240,
            command=self.mettre_a_jour_montant_conseille
        )
        self.combo_niveau.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        self.lbl_type = ctk.CTkLabel(self.form_frame, text="Type de Versement :", font=("Helvetica", 11, "bold"))
        self.lbl_type.grid(row=2, column=1, padx=20, pady=5, sticky="w")
        self.combo_type = ctk.CTkComboBox(
            self.form_frame,
            values=["Mensualité", "Inscription / Réinscription"],
            textvariable=self.var_type_frais,
            width=240,
            command=self.mettre_a_jour_montant_conseille
        )
        self.combo_type.grid(row=3, column=1, padx=20, pady=(0, 10), sticky="w")

        # Ligne 3 : Montant à encaisser & Mode de Règlement (Ordre Configuré)
        self.lbl_montant = ctk.CTkLabel(self.form_frame, text="Montant à Encaisser (FCFA) :", font=("Helvetica", 11, "bold"))
        self.lbl_montant.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.ent_montant = ctk.CTkEntry(self.form_frame, textvariable=self.var_montant, width=240)
        self.ent_montant.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="w")

        self.lbl_mode = ctk.CTkLabel(self.form_frame, text="Mode de Règlement :", font=("Helvetica", 11, "bold"))
        self.lbl_mode.grid(row=4, column=1, padx=20, pady=5, sticky="w")
        self.combo_mode = ctk.CTkComboBox(self.form_frame, values=self.modes_paiement, textvariable=self.var_mode_paiement, width=240)
        self.combo_mode.grid(row=5, column=1, padx=20, pady=(0, 15), sticky="w")

        # Zone d'information dynamique
        self.lbl_info_solde = ctk.CTkLabel(
            self.form_frame,
            text="Saisissez un Matricule pour évaluer son historique comptable.",
            font=("Helvetica", 10.5, "italic"),
            text_color="#2563EB"
        )
        self.lbl_info_solde.grid(row=6, column=0, columnspan=2, pady=(10, 10))

        # Initialisation du montant conseillé par défaut
        self.mettre_a_jour_montant_conseille()

        # --- ACTIONS ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(fill="x", pady=15)

        self.btn_valider = ctk.CTkButton(
            self.action_frame,
            text="💾 Valider & Émettre Reçu",
            font=("Helvetica", 12, "bold"),
            fg_color="#059669",
            hover_color="#047857",
            height=45,
            width=280,
            command=self.valider_et_generer_recu
        )
        self.btn_valider.pack(side="left", padx=(120, 10))

        self.btn_reset = ctk.CTkButton(
            self.action_frame,
            text="🔄 Annuler",
            font=("Helvetica", 12, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            height=45,
            width=140,
            command=self.reinitialiser_champs
        )
        self.btn_reset.pack(side="left", padx=10)

    def mettre_a_jour_montant_conseille(self, event=None):
        """Affiche automatiquement la valeur par défaut recommandée selon l'année d'étude et le type de frais"""
        type_frais = self.var_type_frais.get()
        annee = self.var_niveau.get()

        if type_frais == "Inscription / Réinscription":
            self.var_montant.set(str(int(FRAIS_INSCRIPTION_MONTANT)))
        else:
            # Récupérer la mensualité de base associée à l'année d'études
            mensualite = GRILLE_TARIFAIRE.get(annee, {}).get("mensuel", 32000.0)
            self.var_montant.set(str(int(mensualite)))

    def charger_infos_etudiant(self, event=None):
        """Récupère l'historique complet de l'étudiant à partir du matricule"""
        mat = self.var_matricule.get().strip()
        if not mat:
            return

        try:
            with open(FICHIER_SUIVI, "r", encoding="utf-8") as f:
                data = json.load(f)

            if mat in data:
                etudiant = data[mat]
                self.var_nom.set(etudiant["nom"])
                self.var_niveau.set(etudiant["niveau"])
                self.var_type_frais.set("Mensualité")  # Par défaut sur mensualité lors d'un chargement

                # Récupération de l'historique financier
                cumul_scolarite = etudiant.get("cumul_mensualites", 0.0)
                tarif_annuel = GRILLE_TARIFAIRE.get(etudiant["niveau"], {}).get("annuel", 320000.0)
                reste = max(0.0, tarif_annuel - cumul_scolarite)

                inscription_statut = "Réglée" if etudiant.get("inscription_payee", False) else "Non réglée (10 000 FCFA dus)"

                self.lbl_info_solde.configure(
                    text=f"Étudiant : {etudiant['nom']} ({etudiant['niveau']}) | Déjà payé : {cumul_scolarite:,.0f} FCFA | Reste à payer : {reste:,.0f} FCFA | Inscription : {inscription_statut}".replace(",", " "),
                    text_color="#059669"
                )
                self.mettre_a_jour_montant_conseille()
            else:
                self.lbl_info_solde.configure(
                    text="Nouveau matricule détecté (création de compte étudiant automatique).",
                    text_color="#EA580C"
                )
        except Exception as e:
            print(f"Erreur de lecture du suivi: {e}")

    def reinitialiser_champs(self):
        self.var_matricule.set("")
        self.var_nom.set("")
        self.var_niveau.set(list(GRILLE_TARIFAIRE.keys())[0])
        self.var_type_frais.set("Mensualité")
        self.var_mode_paiement.set(self.modes_paiement[0])
        self.mettre_a_jour_montant_conseille()
        self.lbl_info_solde.configure(
            text="Saisissez un Matricule pour évaluer son historique comptable.",
            text_color="#2563EB"
        )

    def valider_et_generer_recu(self):
        mat = self.var_matricule.get().strip()
        nom = self.var_nom.get().strip()
        annee_etude = self.var_niveau.get()
        montant_str = self.var_montant.get().strip()
        type_frais = self.var_type_frais.get()
        mode_paye = self.var_mode_paiement.get()

        if not mat or not nom or not montant_str:
            messagebox.showwarning("Formulaire Incomplet", "Veuillez renseigner le matricule, le nom de l'étudiant et le montant.")
            return

        try:
            montant_verse = float(montant_str)
            if montant_verse <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir un montant d'encaissement numérique positif.")
            return

        # 1. MISE À JOUR DE LA COMPTABILITÉ ÉTUDIANT
        try:
            with open(FICHIER_SUIVI, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

        tarif_annuel = GRILLE_TARIFAIRE.get(annee_etude, {}).get("annuel", 320000.0)

        # Initialisation ou récupération du profil de l'étudiant
        if mat not in data:
            data[mat] = {
                "nom": nom,
                "niveau": annee_etude,
                "cumul_mensualites": 0.0,
                "inscription_payee": False
            }
        else:
            # Mise à jour des informations si elles ont changé lors de l'encaissement
            data[mat]["nom"] = nom
            data[mat]["niveau"] = annee_etude

        cumul_scolarite_avant = data[mat].get("cumul_mensualites", 0.0)
        inscription_deja_payee = data[mat].get("inscription_payee", False)

        # Traitement spécifique selon le type de règlement
        if type_frais == "Inscription / Réinscription":
            data[mat]["inscription_payee"] = True
            inscription_deja_payee = True
            # Les frais d'inscription sont hors scolarité annuelle : pas de modification du cumul des mensualités
            cumul_scolarite_apres = cumul_scolarite_avant
        else:
            # Règlement d'une mensualité
            data[mat]["cumul_mensualites"] += montant_verse
            cumul_scolarite_apres = data[mat]["cumul_mensualites"]

        # Enregistrement des données mises à jour
        with open(FICHIER_SUIVI, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Reste à payer sur la scolarité annuelle
        reste_a_payer_annuel = max(0.0, tarif_annuel - cumul_scolarite_apres)

        # 2. DESIGN DU REÇU PDF
        nom_fichier = f"Recu_{mat.replace('-', '_')}_{date.today().strftime('%d%m%Y')}.pdf"
        doc = SimpleDocTemplate(nom_fichier, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=40)
        story = []

        couleur_primaire = colors.HexColor('#1E3A8A')
        couleur_texte = colors.HexColor('#1E293B')
        couleur_mutile = colors.HexColor('#64748B')
        couleur_ligne = colors.HexColor('#E2E8F0')
        couleur_succes = colors.HexColor('#059669')

        style_universite = ParagraphStyle('Univ', fontName='Helvetica-Bold', fontSize=12, textColor=couleur_primaire, alignment=1)
        style_agrement = ParagraphStyle('Agre', fontName='Helvetica-Oblique', fontSize=8, textColor=couleur_mutile, alignment=1, leading=10)
        style_devise = ParagraphStyle('Devise', fontName='Helvetica-Bold', fontSize=8, textColor=couleur_primaire, alignment=1, spaceAfter=20)

        style_grand_titre = ParagraphStyle('GTitre', fontName='Helvetica-Bold', fontSize=14, textColor=couleur_texte, alignment=0)
        style_status = ParagraphStyle('Status', fontName='Helvetica-Bold', fontSize=9, textColor=couleur_succes, alignment=2)
        style_h2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, textColor=couleur_primaire, spaceBefore=8, spaceAfter=8)

        style_label = ParagraphStyle('Lbl', fontName='Helvetica', fontSize=9, textColor=couleur_mutile)
        style_value = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=9.5, textColor=couleur_texte)
        style_value_normal = ParagraphStyle('ValNorm', fontName='Helvetica', fontSize=9.5, textColor=couleur_texte)

        # En-tête de l'Institut
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_universite))
        story.append(Paragraph("Etablissement agréé sous l'arrêté n°7061/MESRSIT/CAB", style_agrement))
        story.append(Paragraph('"Rigueur - Réussite - Innovation"', style_devise))

        header_table_data = [
            [
                Paragraph(f"<b>REÇU OFFICIEL DE VERSEMENT</b><br/><font size=8 color='#64748B'>Paiement {type_frais}</font>", style_grand_titre),
                Paragraph("STATUT : VALIDÉ & INSCRIT", style_status)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[260, 260])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(header_table)

        # Ligne de séparation
        sep_table = Table([[""]], colWidths=[520])
        sep_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, couleur_ligne),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ]))
        story.append(sep_table)
        story.append(Spacer(1, 5))

        # Données de l'étudiant et du paiement
        col_gauche_data = [
            [Paragraph("INFORMATIONS ÉTUDIANT", style_h2)],
            [Paragraph("Matricule", style_label)],
            [Paragraph(mat, style_value)],
            [Spacer(1, 4)],
            [Paragraph("Nom & Prénom(s)", style_label)],
            [Paragraph(nom, style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Année d'études de référence", style_label)],
            [Paragraph(annee_etude, style_value_normal)],
        ]

        col_droite_data = [
            [Paragraph("DÉTAILS DU RÈGLEMENT", style_h2)],
            [Paragraph("Libellé du Versement", style_label)],
            [Paragraph(type_frais, style_value)],
            [Spacer(1, 4)],
            [Paragraph("Mode de Paiement utilisé", style_label)],
            [Paragraph(mode_paye, style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Date d'émission", style_label)],
            [Paragraph(f"{date.today().strftime('%d/%m/%Y')}", style_value_normal)],
        ]

        table_gauche = Table(col_gauche_data, colWidths=[240])
        table_gauche.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))

        table_droite = Table(col_droite_data, colWidths=[240])
        table_droite.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))

        corps_table = Table([[table_gauche, table_droite]], colWidths=[260, 260])
        corps_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 15)]))
        story.append(corps_table)
        story.append(sep_table)
        story.append(Spacer(1, 10))

        # 3. CONSTRUIRE LE TABLEAU FINANCIER SPÉCIFIQUE AVEC LES RÈGLES BTS / LICENCE
        style_cell_head = ParagraphStyle('CH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)
        style_cell_body = ParagraphStyle('CB', fontName='Helvetica', fontSize=8.5, textColor=couleur_texte)
        style_cell_body_bold = ParagraphStyle('CBB', fontName='Helvetica-Bold', fontSize=8.5, textColor=couleur_texte)

        recap_headers = [
            Paragraph("Scolarité Annuelle", style_cell_head),
            Paragraph("Cumul Précédent", style_cell_head),
            Paragraph("Versement du Jour", style_cell_head),
            Paragraph("Total Scolarité Versée", style_cell_head),
            Paragraph("Reste à Payer Scolarité", style_cell_head)
        ]

        recap_values = [
            Paragraph(f"{tarif_annuel:,.0f} FCFA".replace(",", " "), style_cell_body),
            Paragraph(f"{cumul_scolarite_avant:,.0f} FCFA".replace(",", " "), style_cell_body),
            # Met en valeur le type de versement effectué
            Paragraph(f"<b>{montant_verse:,.0f} FCFA</b><br/><font size=6.5 color='#64748B'>({type_frais})</font>", style_cell_body),
            Paragraph(f"{cumul_scolarite_apres:,.0f} FCFA".replace(",", " "), style_cell_body),
            Paragraph(f"<font color='#EF4444'><b>{reste_a_payer_annuel:,.0f} FCFA</b></font>".replace(",", " "), style_cell_body_bold)
        ]

        recap_table_data = [recap_headers, recap_values]
        recap_table = Table(recap_table_data, colWidths=[104, 104, 104, 104, 104])
        recap_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), couleur_primaire),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC')])
        ]))

        story.append(Paragraph("SITUATION SCOLAIRE GLOBALE (FCFA)", style_h2))
        story.append(recap_table)

        # Ajout d'une mention pour les frais d'inscription (les 10 000 FCFA hors scolarité)
        inscription_statut_reçu = "RÉGLÉS (10 000 FCFA hors scolarité)" if inscription_deja_payee else "NON RÉGLÉS (10 000 FCFA exigibles)"
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<b>Note administrative :</b> Droits d'inscription / Réinscription : <b>{inscription_statut_reçu}</b>.", ParagraphStyle('Note', fontName='Helvetica', fontSize=8, textColor=couleur_mutile)))
        story.append(Spacer(1, 20))

        # Signatures
        sig_data = [
            [
                Paragraph("<b>Signature de l'Étudiant</b><br/><font size=7 color='#64748B'>Fait à Oyo, pour acquit</font><br/><br/><br/><br/>", style_label),
                Paragraph("<b>La Caisse Centrale - ISPSLO</b><br/><font size=7 color='#64748B'>Signature et cachet du comptable</font><br/><br/><br/><br/>", ParagraphStyle('SigR', parent=style_label, alignment=2))
            ]
        ]
        sig_table = Table(sig_data, colWidths=[260, 260])
        story.append(sig_table)

        doc.build(story)

        # Mettre à jour l'écran avec les dernières données calculées
        self.lbl_info_solde.configure(
            text=f"Mise à jour réussie : Total Scolarité Payé = {cumul_scolarite_apres:,.0f} FCFA | Reste dû = {reste_a_payer_annuel:,.0f} FCFA".replace(",", " "),
            text_color="#059669"
        )

        messagebox.showinfo("Caisse Enregistrée", f"Opération enregistrée avec succès !\nLe reçu '{nom_fichier}' a été généré.")
        self.ouvrir_pdf(nom_fichier)

    def ouvrir_pdf(self, nom_fichier):
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', nom_fichier))
            elif os.name == 'nt':
                os.startfile(nom_fichier)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', nom_fichier))
        except Exception as e:
            messagebox.showerror("Visualisation", f"Impossible d'ouvrir le fichier PDF : {e}")