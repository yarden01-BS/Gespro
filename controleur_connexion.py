"""
controleur_connexion.py
========================

Contient la logique d'authentification : lecture des champs, vérification
des identifiants en base de données, et redirection vers le menu principal.

Le fichier de vue (vue_connexion.py) ne fait qu'appeler
`valider_connexion(app)` en lui passant l'instance de la fenêtre. Toute la
logique (lecture des champs, requête BDD, message d'erreur, redirection)
est à implémenter ici.

-------------------------------------------------------------------------
Widgets disponibles sur `app` (définis dans vue_connexion.py) :
-------------------------------------------------------------------------
    app.ent_username : CTkEntry -> identifiant ou email saisi
    app.ent_password : CTkEntry -> mot de passe saisi

`app` est une instance de tkinter/customtkinter (ConnexionApp), donc
`app.destroy()` ferme la fenêtre de connexion.
-------------------------------------------------------------------------
"""


def valider_connexion(app):
    """
    Déclenchée par le bouton "SE CONNECTER" (et par la touche Entrée).

    À faire ici :
      1. Lire app.ent_username.get().strip() et app.ent_password.get().strip()
      2. Si l'un des deux est vide :
             messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
             return
      3. Vérifier les identifiants en base de données (table Utilisateur :
         colonnes username, email, mot_de_passe, nom, prenom).
      4. Si l'utilisateur est trouvé :
             - construire nom_complet = f"{prenom} {nom.upper()}"
             - app.destroy()
             - from menu_app import MenuPrincipalApp
             - MenuPrincipalApp(nom_gestionnaire=nom_complet).mainloop()
         Sinon :
             - messagebox.showerror("Authentification échouée", "Identifiant ou mot de passe incorrect.")
      5. En cas d'erreur BDD (connexion impossible, etc.) :
             - messagebox.showerror("Erreur de Connexion", "Impossible de se connecter à la base de données.")
           (à toi de voir avec ton collègue si un mode de secours/dev est
           encore nécessaire une fois la BDD en place)

    Requête de référence (à adapter à l'implémentation BDD choisie) :

        SELECT nom, prenom
        FROM Utilisateur
        WHERE (username = %s OR email = %s) AND mot_de_passe = %s
    """
    raise NotImplementedError("À implémenter : authentification + BDD + redirection")
