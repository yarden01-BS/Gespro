"""
controleur_autres_paiements.py
================================

Contient tout ce qui touche au stockage des paiements ponctuels : frais de
bibliothèque et frais d'examen. Séparé de controleur_paiement.py (qui ne
gère que la scolarité mensuelle) et de controleur_inscription.py (frais
d'inscription/réinscription).

Le fichier de vue (vue_autres_paiements.py) ne lit/écrit jamais le
stockage directement : il délègue tout ici.

-------------------------------------------------------------------------
Widgets et données disponibles sur `app` (définis dans vue_autres_paiements.py) :
-------------------------------------------------------------------------
    app.var_matricule      : StringVar -> matricule saisi
    app.var_nom             : StringVar -> nom & prénom(s)
    app.var_type_frais      : StringVar -> "Frais de Bibliothèque" / "Frais d'Examen"
    app.var_montant         : StringVar -> montant saisi (chaîne)
    app.var_mode_paiement   : StringVar -> mode de règlement choisi

Méthodes disponibles sur `app` (définies dans vue_autres_paiements.py, ne
touchent pas le stockage) :
    app.generer_pdf_recu(infos)   -> construit et ouvre le reçu PDF.
        `infos` attendu :
        {
            "matricule": str, "nom": str, "type_frais": str,
            "mode_paye": str, "montant_verse": float,
            "date_str": str, "nom_fichier": str
        }
    app.ouvrir_pdf(nom_fichier)    -> ouvre un PDF déjà généré

-------------------------------------------------------------------------
"""

FICHIER_SUIVI = "autres_paiements.json"


def initialiser_stockage():
    """
    Appelée une fois au démarrage de l'application (voir vue_autres_paiements.py,
    dans __init__).

    À faire ici : s'assurer que le support de stockage existe et est prêt à
    l'emploi (fichier JSON vide {} aujourd'hui, table(s) BDD demain).
    """
    raise NotImplementedError("À implémenter : initialisation du stockage des autres paiements")


def valider_et_generer_recu(app):
    """
    Déclenchée par le bouton de validation.

    À faire ici :
      1. Lire matricule, nom, type de frais, montant (chaîne), mode de paiement.
      2. Valider :
           - matricule/nom/montant non vides -> sinon messagebox.showwarning(...)
           - montant convertible en float et > 0 -> sinon messagebox.showerror(...)
      3. Enregistrer l'opération dans le stockage (matricule, nom, type de
         frais, montant, mode de paiement, date). Contrairement à la
         scolarité mensuelle, il n'y a pas de cumul/reste à suivre ici :
         chaque paiement est indépendant (un enregistrement par versement).
      4. Construire `infos` (voir format en tête de fichier, y compris
         "date_str" = date.today().strftime('%d/%m/%Y')) avec un nom de
         fichier du type f"Recu_{type_frais}_{matricule}_{date_du_jour}.pdf",
         puis appeler app.generer_pdf_recu(infos).
      5. messagebox.showinfo("Paiement Enregistré",
         "Opération enregistrée avec succès !\\nLe reçu '<nom_fichier>' a été généré.")
    """
    raise NotImplementedError("À implémenter : enregistrement du paiement + reçu")
