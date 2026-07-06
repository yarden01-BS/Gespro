import mysql.connector

def obtenir_connexion():
    """Établit et retourne la connexion à la base de données Gespro."""
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Utilisateur par défaut
        password="",          # Laissez vide puisqu'il n'y a pas de mot de passe
        database="Gespro"     # Le nom exact de votre BD
    )