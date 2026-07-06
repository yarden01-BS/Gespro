import mysql.connector
from database_manager import verifier_connexion, enregistrer_etudiant

def lancer_tests():
    print(" DEMARRAGE DU TEST D'INTEGRATION (PONT PYTHON -> MYSQL) \n")
    
    # Vérification de la lecture 
    print("🔍 Test 1 : Vérification des identifiants de connexion...")
    email_test = "emmanuelle@gespro.com"
    
    try:
        gestionnaire = verifier_connexion(email_test)
        if gestionnaire:
            print(" SUCCÈS : Connexion établie et base de données interrogée !")
            print(f"Nom du gestionnaire trouvé : {gestionnaire['nom_complet']}")
            print(f" Mot de passe extrait : {gestionnaire['mot_de_passe']}")
        else:
            print("ATTENTION : La requête a fonctionné mais le gestionnaire n'existe pas dans la table.")
            print("   As-tu bien exécuté le script SQL d'insertion des données hier ?")
    except Exception as e:
        print(f" ERREUR sur le Test 1 : {e}")
        return

    print("\n" + "-"*50 + "\n")

    
    #  Vérification de l'écriture, le formulaire d'inscription     
    print(" Test 2 : Tentative d'insertion d'un nouvel étudiant...")
    
    # Données d'un étudiant fictif pour le test
    matricule_test = "2026-TEST"
    nom_test = "KAMBA"
    prenom_test = "Merveille"
    
    try:
        # On appelle ta fonction CRUD
        enregistrer_etudiant(
            matricule=matricule_test,
            nom=nom_test,
            prenom=prenom_test,
            sexe="F",
            filiere="Génie Logiciel",
            cycle="Premier Cycle",
            adresse="Ouenzé, Brazzaville",
            telephone="+242 06 999 8877",
            email="merveille.kamba@test.com",
            id_niveau=1,  # ID correspondant à Licence 1
            statut="Inscrit"
        )
        print(f" SUCCÈS : L'étudiante {nom_test} {prenom_test} a été inscrite en base de données !")
        print(f"   -> dans phpMyAdmin (table 'etudiants') : le matricule '{matricule_test}'  y est.")
        
    except mysql.connector.Error as err:
        # Si on relance le test, le matricule existe déjà (Clé primaire), c'est géré ici
        if err.errno == 1062:
            print(f" NOTE : L'étudiant avec le matricule '{matricule_test}' existe déjà en base de données.")
            print("L'écriture fonctionne, le test est validé !")
        else:
            print(f" ERREUR SQL sur le Test 2 : {err}")
    except Exception as e:
        print(f" ERREUR générale sur le Test 2 : {e}")

    print("\nFIN DES TESTS  — ")

if __name__ == "__main__":
    lancer_tests()