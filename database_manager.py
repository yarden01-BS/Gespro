import mysql.connector
from config_db import obtenir_connexion

def verifier_connexion(email):
    """Vérifie si le gestionnaire existe et retourne ses infos."""
    conn = obtenir_connexion()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id_gestionnaire, nom_complet, mot_de_passe FROM gestionnaires WHERE email = %s"
    cursor.execute(query, (email,))
    resultat = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultat

def enregistrer_etudiant(matricule, nom, prenom, sexe, filiere, cycle, adresse, telephone, email, id_niveau, statut):
    """Inscrit un nouvel étudiant en base de données."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    query = """
        INSERT INTO etudiants (matricule, nom, prenom, sexe, filiere, cycle, adresse, telephone, email, id_niveau, statut_inscription)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valeurs = (matricule, nom, prenom, sexe, filiere, cycle, adresse, telephone, email, id_niveau, statut)
    cursor.execute(query, valeurs)
    conn.commit()
    cursor.close()
    conn.close()

def enregistrer_paiement(numero_recu, id_etudiant, id_gestionnaire, type_frais, mois, montant, montant_lettres, date_paiement):
    """Enregistre une transaction financière basée sur le modèle du reçu."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    query = """
        INSERT INTO paiements (numero_recu, id_etudiant, id_gestionnaire, type_frais, mois_concerne, montant, montant_lettres, date_paiement)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valeurs = (numero_recu, id_etudiant, id_gestionnaire, type_frais, mois, montant, montant_lettres, date_paiement)
    cursor.execute(query, valeurs)
    conn.commit()
    cursor.close()
    conn.close()