import json
import os

class UserManager:
    """
    Gère les opérations liées aux utilisateurs, y compris la création,
    l'authentification, le chargement et la sauvegarde des données utilisateur.
    """

    def __init__(self, file_path='data/user_data.json'):
        """
        Initialise le gestionnaire d'utilisateurs.

        :param file_path: Chemin du fichier JSON pour stocker les données utilisateur
        """
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        """
        Charge les données utilisateur à partir du fichier JSON.

        :return: Dictionnaire contenant les données utilisateur
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def save_users(self):
        """
        Sauvegarde les données utilisateur dans le fichier JSON.
        Crée le répertoire parent si nécessaire.
        """
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(self.users, f)

    def create_user(self, username, email, password):
        """
        Crée un nouvel utilisateur.

        :param username: Nom d'utilisateur
        :param email: Adresse email de l'utilisateur
        :param password: Mot de passe de l'utilisateur
        :return: True si l'utilisateur a été créé, False si le nom d'utilisateur existe déjà
        """
        if username in self.users:
            return False
        self.users[username] = {
            'email': email,
            'password': password,  # Note: Dans une application réelle, il faudrait hasher le mot de passe
            'transactions': [],
            'budgets': []
        }
        self.save_users()
        return True

    def authenticate(self, username, password):
        """
        Authentifie un utilisateur.

        :param username: Nom d'utilisateur
        :param password: Mot de passe
        :return: True si l'authentification réussit, False sinon
        """
        if username in self.users and self.users[username]['password'] == password:
            return True
        return False

    def get_user_data(self, username):
        """
        Récupère les données d'un utilisateur.

        :param username: Nom d'utilisateur
        :return: Dictionnaire contenant les données de l'utilisateur, ou None si l'utilisateur n'existe pas
        """
        return self.users.get(username)

    def update_user_data(self, username, transactions, budgets):
        """
        Met à jour les données d'un utilisateur.

        :param username: Nom d'utilisateur
        :param transactions: Liste des transactions de l'utilisateur
        :param budgets: Liste des budgets de l'utilisateur
        """
        if username in self.users:
            self.users[username]['transactions'] = transactions
            self.users[username]['budgets'] = budgets
            self.save_users()

    def delete_user(self, username):
        """
        Supprime un utilisateur.

        :param username: Nom d'utilisateur à supprimer
        :return: True si l'utilisateur a été supprimé, False s'il n'existait pas
        """
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True
        return False