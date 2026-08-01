import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import messagebox

# Importations ReportLab pour le reçu PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

import controleur_autres_paiements

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

TYPES_FRAIS = ["Frais de Bibliothèque", "Frais d'Examen"]


class AutresPaiementsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Autres Paiements (Bibliothèque & Examen)")
        self.geometry("700x560")
        self.resizable(False, False)

        # Initialisation du support de stockage (géré par le contrôleur)
        controleur_autres_paiements.initialiser_stockage()

        # Variables de contrôle
        self.var_matricule = ctk.StringVar()
        self.var_nom = ctk.StringVar()
        self.var_type_frais = ctk.StringVar(value=TYPES_FRAIS[0])
        self.var_montant = ctk.StringVar()

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
            text="AUTRES PAIEMENTS (BIBLIOTHÈQUE & EXAMEN)",
            font=("Helvetica", 16, "bold"),
            text_color="#1E3A8A"
        )
        self.lbl_titre.pack()

        self.lbl_desc = ctk.CTkLabel(
            self.head_frame,
            text="Encaissement des frais annexes non liés à la scolarité mensuelle.",
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

        self.lbl_nom = ctk.CTkLabel(self.form_frame, text="Nom & Prénom(s) :", font=("Helvetica", 11, "bold"))
        self.lbl_nom.grid(row=0, column=1, padx=20, pady=(15, 5), sticky="w")
        self.ent_nom = ctk.CTkEntry(self.form_frame, textvariable=self.var_nom, width=240, placeholder_text="Nom complet")
        self.ent_nom.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="w")

        # Ligne 2 : Type de frais & Montant
        self.lbl_type = ctk.CTkLabel(self.form_frame, text="Type de Frais :", font=("Helvetica", 11, "bold"))
        self.lbl_type.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.combo_type = ctk.CTkComboBox(
            self.form_frame,
            values=TYPES_FRAIS,
            textvariable=self.var_type_frais,
            width=240
        )
        self.combo_type.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        self.lbl_montant = ctk.CTkLabel(self.form_frame, text="Montant à Encaisser (FCFA) :", font=("Helvetica", 11, "bold"))
        self.lbl_montant.grid(row=2, column=1, padx=20, pady=5, sticky="w")
        self.ent_montant = ctk.CTkEntry(self.form_frame, textvariable=self.var_montant, width=240)
        self.ent_montant.grid(row=3, column=1, padx=20, pady=(0, 10), sticky="w")

        # Ligne 3 : Mode de règlement
        self.lbl_mode = ctk.CTkLabel(self.form_frame, text="Mode de Règlement :", font=("Helvetica", 11, "bold"))
        self.lbl_mode.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.combo_mode = ctk.CTkComboBox(self.form_frame, values=self.modes_paiement, textvariable=self.var_mode_paiement, width=240)
        self.combo_mode.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="w")

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
        self.btn_valider.pack(side="left", padx=(90, 10))

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

        # --- RETOUR VERS LA CAISSE SCOLARITÉ MENSUELLE ---
        self.btn_retour = ctk.CTkButton(
            self,
            text="← Retour à la Caisse Scolarité Mensuelle",
            font=("Helvetica", 11, "bold"),
            fg_color="#64748B",
            hover_color="#475569",
            height=34,
            command=self.retour_paiement
        )
        self.btn_retour.pack(pady=(0, 20))

    # =====================================================================
    # LOGIQUE D'AFFICHAGE PURE (ne touche pas le stockage)
    # =====================================================================
    def reinitialiser_champs(self):
        self.var_matricule.set("")
        self.var_nom.set("")
        self.var_type_frais.set(TYPES_FRAIS[0])
        self.var_montant.set("")
        self.var_mode_paiement.set(self.modes_paiement[0])

    # =====================================================================
    # ACTION DÉLÉGUÉE AU CONTRÔLEUR (lecture/écriture du stockage)
    # =====================================================================
    def valider_et_generer_recu(self):
        controleur_autres_paiements.valider_et_generer_recu(self)

    # =====================================================================
    # NAVIGATION
    # =====================================================================
    def retour_paiement(self):
        self.destroy()
        from vue_paiement import GesProPaiementApp
        app = GesProPaiementApp()
        app.mainloop()

    # =====================================================================
    # GÉNÉRATION DU REÇU PDF (mise en forme uniquement, pas de stockage)
    # =====================================================================
    def generer_pdf_recu(self, infos):
        """
        `infos` doit contenir : matricule, nom, type_frais, mode_paye,
        montant_verse, date_str, nom_fichier
        (voir le docstring de controleur_autres_paiements.valider_et_generer_recu)
        """
        nom_fichier = infos["nom_fichier"]
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
                Paragraph(f"<b>REÇU OFFICIEL DE VERSEMENT</b><br/><font size=8 color='#64748B'>{infos['type_frais']}</font>", style_grand_titre),
                Paragraph("STATUT : VALIDÉ", style_status)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[260, 260])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(header_table)

        # Ligne de séparation
        sep_table = Table([[""]], colWidths=[520])
        sep_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 1, couleur_ligne),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(sep_table)
        story.append(Spacer(1, 5))

        # Données de l'étudiant et du paiement
        col_gauche_data = [
            [Paragraph("INFORMATIONS ÉTUDIANT", style_h2)],
            [Paragraph("Matricule", style_label)],
            [Paragraph(infos['matricule'], style_value)],
            [Spacer(1, 4)],
            [Paragraph("Nom & Prénom(s)", style_label)],
            [Paragraph(infos['nom'], style_value_normal)],
        ]

        col_droite_data = [
            [Paragraph("DÉTAILS DU RÈGLEMENT", style_h2)],
            [Paragraph("Nature du Versement", style_label)],
            [Paragraph(infos['type_frais'], style_value)],
            [Spacer(1, 4)],
            [Paragraph("Mode de Paiement utilisé", style_label)],
            [Paragraph(infos['mode_paye'], style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Date d'émission", style_label)],
            [Paragraph(infos['date_str'], style_value_normal)],
        ]

        table_gauche = Table(col_gauche_data, colWidths=[240])
        table_gauche.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))

        table_droite = Table(col_droite_data, colWidths=[240])
        table_droite.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))

        corps_table = Table([[table_gauche, table_droite]], colWidths=[260, 260])
        corps_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 15)]))
        story.append(corps_table)
        story.append(sep_table)
        story.append(Spacer(1, 10))

        # Montant encaissé, mis en valeur
        montant_data = [
            [
                Paragraph("<b>MONTANT ENCAISSÉ</b>", style_label),
                Paragraph(f"<b>{infos['montant_verse']:,.0f} FCFA</b>".replace(",", " "),
                          ParagraphStyle('Mnt', fontName='Helvetica-Bold', fontSize=16, textColor=couleur_succes, alignment=2))
            ]
        ]
        montant_table = Table(montant_data, colWidths=[280, 220])
        montant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ]))
        story.append(montant_table)
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


if __name__ == "__main__":
    app = AutresPaiementsApp()
    app.mainloop()
