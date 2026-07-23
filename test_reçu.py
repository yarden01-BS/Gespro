import os
import sys
import subprocess
from datetime import date
import customtkinter as ctk
from tkinter import messagebox

# Importations ReportLab requises pour la mise en page des PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TestRecuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Générateur de Tests de Reçus PDF")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # Titre Principal
        self.lbl_titre = ctk.CTkLabel(
            self, 
            text="LABORATOIRE DE TEST DES REÇUS (PDF)", 
            font=("Helvetica", 16, "bold"),
            text_color="#1E3A8A"
        )
        self.lbl_titre.pack(pady=(30, 10))
        
        self.lbl_soustitre = ctk.CTkLabel(
            self, 
            text="Cliquez sur un bouton pour générer et ouvrir le document PDF correspondant.", 
            font=("Helvetica", 11),
            text_color="#64748B"
        )
        self.lbl_soustitre.pack(pady=(0, 25))

        # Conteneur des boutons de test
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="both", expand=True, padx=50)

        # Bouton 1 : Reçu d'Inscription
        self.btn_recu_inscription = ctk.CTkButton(
            self.btn_frame,
            text="🎫 Générer : Reçu d'Inscription d'un Étudiant",
            font=("Helvetica", 12, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            height=45,
            command=self.tester_recu_inscription
        )
        self.btn_recu_inscription.pack(fill="x", pady=10)

        # Bouton 2 : Reçu Mensuel
        self.btn_recu_mensuel = ctk.CTkButton(
            self.btn_frame,
            text="💵 Générer : Reçu de Frais Mensuels (Mensualité)",
            font=("Helvetica", 12, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
            height=45,
            command=self.tester_recu_mensuel
        )
        self.btn_recu_mensuel.pack(fill="x", pady=10)

        # Bouton 3 : Rapport Global des Paiements
        self.btn_rapport_global = ctk.CTkButton(
            self.btn_frame,
            text="📋 Générer : Liste des Paiements de tous les Étudiants",
            font=("Helvetica", 12, "bold"),
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            height=45,
            command=self.tester_rapport_global
        )
        self.btn_rapport_global.pack(fill="x", pady=10)

    # ---------------------------------------------------------
    # 1. GÉNÉRATION DU REÇU D'INSCRIPTION (SIMULÉ)
    # ---------------------------------------------------------
    def tester_recu_inscription(self):
        nom_fichier = "Test_Recu_Inscription_Etudiant.pdf"
        doc = SimpleDocTemplate(nom_fichier, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=40)
        
        # Charte graphique
        couleur_primaire = colors.HexColor('#1E3A8A')    # Bleu nuit
        couleur_valide = colors.HexColor('#3B82F6')      # Bleu azur pour l'inscription
        couleur_texte = colors.HexColor('#1E293B')
        couleur_mutile = colors.HexColor('#64748B')
        couleur_ligne = colors.HexColor('#F1F5F9')

        style_universite = ParagraphStyle('Univ', fontName='Helvetica-Bold', fontSize=12, textColor=couleur_primaire, alignment=1)
        style_agrement = ParagraphStyle('Agre', fontName='Helvetica-Oblique', fontSize=8, textColor=couleur_mutile, alignment=1, leading=10)
        style_devise = ParagraphStyle('Devise', fontName='Helvetica-Bold', fontSize=8, textColor=couleur_primaire, alignment=1, spaceAfter=20)
        
        style_grand_titre = ParagraphStyle('GTitre', fontName='Helvetica-Bold', fontSize=16, textColor=couleur_texte, alignment=0)
        style_status = ParagraphStyle('Status', fontName='Helvetica-Bold', fontSize=10, textColor=couleur_valide, alignment=2)
        
        style_h2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, textColor=couleur_primaire, spaceBefore=10, spaceAfter=8)
        
        style_label = ParagraphStyle('Lbl', fontName='Helvetica', fontSize=9.5, textColor=couleur_mutile)
        style_value = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=9.5, textColor=couleur_texte)
        style_value_normal = ParagraphStyle('ValNorm', fontName='Helvetica', fontSize=9.5, textColor=couleur_texte)
        
        style_montant_principal = ParagraphStyle('MntPrin', fontName='Helvetica-Bold', fontSize=20, textColor=couleur_valide, alignment=2)

        story = []
        
        # En-tête académique
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_universite))
        story.append(Paragraph("Etablissement agréé sous l'arrêté n°7061/MESRSIT/CAB", style_agrement))
        story.append(Paragraph('"Rigueur - Réussite - Innovation"', style_devise))
        
        # En-tête transaction
        header_table_data = [
            [
                Paragraph("<b>REÇU D'INSCRIPTION & DOSSIER</b><br/><font size=9 color='#64748B'>Frais d'admission académique</font>", style_grand_titre),
                Paragraph("STATUT : DOSSIER VALIDÉ", style_status)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[260, 260])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(header_table)
        
        # Séparateur
        sep_table = Table([[""]], colWidths=[520])
        sep_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, couleur_ligne),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ]))
        story.append(sep_table)
        story.append(Spacer(1, 5))
        
        # Double colonne d'informations
        col_gauche_data = [
            [Paragraph("INFORMATIONS ÉTUDIANT", style_h2)],
            [Paragraph("Matricule Affecté", style_label)],
            [Paragraph("#2026-GCP-0042", style_value)],
            [Spacer(1, 4)],
            [Paragraph("Nom & Prénom", style_label)],
            [Paragraph("MBOUNGOU Christian", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Filière de Formation", style_label)],
            [Paragraph("Génie Civil et Project (GCP) - Niveau 1", style_value_normal)],
        ]
        
        col_droite_data = [
            [Paragraph("DÉTAIL COMPTABLE", style_h2)],
            [Paragraph("Type d'Opération", style_label)],
            [Paragraph("Frais d'Inscription Administrative", style_value)],
            [Spacer(1, 4)],
            [Paragraph("Mode de Paiement", style_label)],
            [Paragraph("Espèces (Caisse Centrale)", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Date d'effet", style_label)],
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
        story.append(Spacer(1, 5))
        
        # Synthèse financière de l'inscription
        carte_financiere_data = [
            [
                Paragraph("<b>Frais d'inscription perçus</b><br/><font size=8 color='#64748B'>Droits administratifs non remboursables</font>", style_label),
                Paragraph("50 000 FCFA", style_montant_principal)
            ],
            [
                Paragraph("Statut financier annuel de l'étudiant", style_label),
                Paragraph("<b>Inscrit en règle (Caisse Ouverte)</b>", ParagraphStyle('SubM', fontName='Helvetica', fontSize=10, textColor=couleur_texte, alignment=2))
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
        story.append(Spacer(1, 30))
        
        # Signatures
        sig_data = [
            [
                Paragraph("<b>Signature de l'Étudiant</b><br/><br/><br/><br/>", style_label),
                Paragraph("<b>Le Chef du Service Financier</b><br/><font size=7.5 color='#64748B'>Visa et Cachet de l'Etablissement</font><br/><br/><br/>", ParagraphStyle('SigR', parent=style_label, alignment=2))
            ]
        ]
        sig_table = Table(sig_data, colWidths=[260, 260])
        story.append(sig_table)
        
        doc.build(story)
        self.ouvrir_pdf(nom_fichier)

    # ---------------------------------------------------------
    # 2. GÉNÉRATION DU REÇU MENSUEL (SIMULÉ)
    # ---------------------------------------------------------
    def tester_recu_mensuel(self):
        nom_fichier = "Test_Recu_Mensuel_Etudiant.pdf"
        doc = SimpleDocTemplate(nom_fichier, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=40)
        
        couleur_primaire = colors.HexColor('#1E3A8A')
        couleur_valide = colors.HexColor('#059669')      # Vert émeraude
        couleur_texte = colors.HexColor('#1E293B')
        couleur_mutile = colors.HexColor('#64748B')
        couleur_ligne = colors.HexColor('#F1F5F9')

        style_universite = ParagraphStyle('Univ', fontName='Helvetica-Bold', fontSize=12, textColor=couleur_primaire, alignment=1)
        style_agrement = ParagraphStyle('Agre', fontName='Helvetica-Oblique', fontSize=8, textColor=couleur_mutile, alignment=1, leading=10)
        style_devise = ParagraphStyle('Devise', fontName='Helvetica-Bold', fontSize=8, textColor=couleur_primaire, alignment=1, spaceAfter=20)
        
        style_grand_titre = ParagraphStyle('GTitre', fontName='Helvetica-Bold', fontSize=16, textColor=couleur_texte, alignment=0)
        style_status = ParagraphStyle('Status', fontName='Helvetica-Bold', fontSize=10, textColor=couleur_valide, alignment=2)
        
        style_h2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, textColor=couleur_primaire, spaceBefore=10, spaceAfter=8)
        
        style_label = ParagraphStyle('Lbl', fontName='Helvetica', fontSize=9.5, textColor=couleur_mutile)
        style_value = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=9.5, textColor=couleur_texte)
        style_value_normal = ParagraphStyle('ValNorm', fontName='Helvetica', fontSize=9.5, textColor=couleur_texte)
        
        style_montant_principal = ParagraphStyle('MntPrin', fontName='Helvetica-Bold', fontSize=20, textColor=couleur_valide, alignment=2)

        story = []
        
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_universite))
        story.append(Paragraph("Etablissement agréé sous l'arrêté n°7061/MESRSIT/CAB", style_agrement))
        story.append(Paragraph('"Rigueur - Réussite - Innovation"', style_devise))
        
        header_table_data = [
            [
                Paragraph("<b>REÇU DE SCOLARITÉ MENSUELLE</b><br/><font size=9 color='#64748B'>Mois de Règlement : Novembre</font>", style_grand_titre),
                Paragraph("STATUT : PAIEMENT EXÉCUTÉ", style_status)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[260, 260])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(header_table)
        
        sep_table = Table([[""]], colWidths=[520])
        sep_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, couleur_ligne),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ]))
        story.append(sep_table)
        story.append(Spacer(1, 5))
        
        col_gauche_data = [
            [Paragraph("INFORMATIONS ÉTUDIANT", style_h2)],
            [Paragraph("Matricule", style_label)],
            [Paragraph("#2026-GCP-0042", style_value)],
            [Spacer(1, 4)],
            [Paragraph("Nom & Prénom", style_label)],
            [Paragraph("MBOUNGOU Christian", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Parcours Académique", style_label)],
            [Paragraph("<b>Génie Civil (GCP) - Niveau 1</b>", style_value_normal)],
        ]
        
        col_droite_data = [
            [Paragraph("DÉTAIL DU RÈGLEMENT", style_h2)],
            [Paragraph("Nature de l'échéance", style_label)],
            [Paragraph("Frais Mensuels (Novembre)", style_value)],
            [Spacer(1, 4)],
            [Paragraph("Mode appliqué", style_label)],
            [Paragraph("Mobile Money (MTN MoMo)", style_value_normal)],
            [Spacer(1, 4)],
            [Paragraph("Date comptable", style_label)],
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
        story.append(Spacer(1, 5))
        
        carte_financiere_data = [
            [
                Paragraph("<b>MONTANT ACQUITTE CE JOUR</b><br/><font size=8 color='#64748B'>Versement mensuel régulier</font>", style_label),
                Paragraph("32 000 FCFA", style_montant_principal)
            ],
            [
                Paragraph("Échéance Mensuelle Fixée pour GCP L1", style_label),
                Paragraph("<b>32 000 FCFA</b>", ParagraphStyle('SubM', fontName='Helvetica', fontSize=10, textColor=couleur_texte, alignment=2))
            ],
            [
                Paragraph("<font color='#059669'><b>SOLDE RESTANT SUR CE MOIS</b></font>", style_label),
                Paragraph("<b>0 FCFA</b>", ParagraphStyle('SubM2', fontName='Helvetica-Bold', fontSize=11, textColor=couleur_valide, alignment=2))
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
        
        sig_data = [
            [
                Paragraph("<b>Le Déposant / L'Étudiant</b><br/><font size=7.5 color='#64748B'>Signature avec mention 'Lu et approuvé'</font><br/><br/><br/>", style_label),
                Paragraph("<b>Pour le Service Financier</b><br/><font size=7.5 color='#64748B'>Visa de la caisse centrale d'Oyo</font><br/><br/><br/>", ParagraphStyle('SigR', parent=style_label, alignment=2))
            ]
        ]
        sig_table = Table(sig_data, colWidths=[260, 260])
        story.append(sig_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(
            "<i>Note : Aucun versement pour un mois N ne peut être validé sans solde complet du mois N-1. Ce reçu est unique et obligatoire pour l'accès aux examens.</i>", 
            ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=7, textColor=couleur_mutile, leading=9)
        ))
        
        doc.build(story)
        self.ouvrir_pdf(nom_fichier)

    # ---------------------------------------------------------
    # 3. LISTE DE PAIEMENT DE TOUS LES ÉTUDIANTS (RAPPORT GLOBAL)
    # ---------------------------------------------------------
    def tester_rapport_global(self):
        nom_fichier = "Test_Rapport_Global_Paiements.pdf"
        doc = SimpleDocTemplate(nom_fichier, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        
        couleur_primaire = colors.HexColor('#1E3A8A')
        couleur_texte = colors.HexColor('#1E293B')
        
        style_titre = ParagraphStyle('TitreR', fontName='Helvetica-Bold', fontSize=14, textColor=couleur_primaire, spaceAfter=5, alignment=1)
        style_soustitre = ParagraphStyle('ST', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#475569'), spaceAfter=15, alignment=1)
        style_cell_head = ParagraphStyle('CH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)
        style_cell = ParagraphStyle('CC', fontName='Helvetica', fontSize=8, textColor=couleur_texte)
        style_cell_regle = ParagraphStyle('CR', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#059669'))
        style_cell_retard = ParagraphStyle('CD', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#EF4444'))
        
        story = []
        
        # En-tête académique d'Oyo
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", ParagraphStyle('Un', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=couleur_primaire)))
        story.append(Paragraph("ISPSLO - Enregistrement comptable de scolarités", ParagraphStyle('UnS', fontName='Helvetica', fontSize=8, alignment=1, textColor=colors.HexColor('#64748B'))))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("ÉTAT RECAPITULATIF DES ENCAISSEMENTS : NOVEMBRE", style_titre))
        story.append(Paragraph(f"Généré le {date.today().strftime('%d/%m/%Y')} | Trié par Niveau Académique (Données Simulées)", style_soustitre))
        
        # Tableau de suivi
        table_data = [[
            Paragraph("Niveau", style_cell_head),
            Paragraph("Matricule", style_cell_head),
            Paragraph("Nom & Prénom(s)", style_cell_head),
            Paragraph("Scolarité Mensuelle", style_cell_head),
            Paragraph("Déjà Versé (Mois)", style_cell_head),
            Paragraph("Statut de Caisse", style_cell_head)
        ]]

        # Simulation de données fictives représentatives pour le test
        donnees_simulees = [
            {"niveau": "Niveau 1", "mat": "2026-GCP-0042", "nom": "MBOUNGOU Christian", "frais": 32000, "verse": 32000, "statut": True},
            {"niveau": "Niveau 1", "mat": "2026-INFO-0010", "nom": "OKO Yvon", "frais": 32000, "verse": 15000, "statut": False},
            {"niveau": "Niveau 2", "mat": "2026-GCP-0152", "nom": "NGOLO Grâce", "frais": 37000, "verse": 37000, "statut": True},
            {"niveau": "Niveau 2", "mat": "2026-GEL-0201", "nom": "EBOULA Patrick", "frais": 37000, "verse": 0, "statut": False},
            {"niveau": "Niveau 3", "mat": "2026-INFO-0341", "nom": "LOUBASSOU Syntyche", "frais": 42000, "verse": 42000, "statut": True},
            {"niveau": "Niveau 3", "mat": "2026-GCP-0412", "nom": "MAKOSSO Jean-Daniel", "frais": 42000, "verse": 20000, "statut": False},
        ]

        for ds in donnees_simulees:
            status_p = Paragraph("En Règle ✅", style_cell_regle) if ds["statut"] else Paragraph("En Retard ❌", style_cell_retard)
            table_data.append([
                Paragraph(ds["niveau"], style_cell),
                Paragraph(ds["mat"], style_cell),
                Paragraph(ds["nom"], style_cell),
                Paragraph(f"{ds['frais']:,} F".replace(",", " "), style_cell),
                Paragraph(f"{ds['verse']:,} F".replace(",", " "), style_cell),
                status_p
            ])

        # Construction de la table ReportLab
        tableau = Table(table_data, colWidths=[80, 85, 175, 65, 65, 80])
        tableau.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), couleur_primaire),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        
        story.append(tableau)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("<i>Visa de Direction Générale : ________________________________</i>", ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#64748B'))))

        doc.build(story)
        self.ouvrir_pdf(nom_fichier)

    # Fonction utilitaire pour lancer le fichier PDF automatiquement sur l'OS
    def ouvrir_pdf(self, nom_fichier):
        try:
            if sys.platform.startswith('darwin'): 
                subprocess.call(('open', nom_fichier))
            elif os.name == 'nt': 
                os.startfile(nom_fichier)
            elif os.name == 'posix': 
                subprocess.call(('xdg-open', nom_fichier))
        except Exception as e:
            messagebox.showerror("Alerte", f"PDF généré avec succès ({nom_fichier}), mais impossible de l'ouvrir automatiquement : {e}")

if __name__ == "__main__":
    app = TestRecuApp()
    app.mainloop()