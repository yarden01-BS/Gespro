import mysql.connector

try:
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    if connexion.is_connected():
        print("Bravo, connexion à Mysql réussie.")
        connexion.close()
except Exception as e:
    print(f" Erreur de connexion : {e}")