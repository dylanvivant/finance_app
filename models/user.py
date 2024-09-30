# user.py

from datetime import datetime

class User:
    """
    Classe représentant un utilisateur de l'application de finances personnelles.
    """

    def __init__(self, user_id, username, email, created_at=None):
        """
        Initialise un nouvel utilisateur.

        :param user_id: Identifiant unique de l'utilisateur (peut être un UUID ou un entier)
        :param username: Nom d'utilisateur
        :param email: Adresse email de l'utilisateur
        :param created_at: Date de création du compte (par défaut à la date actuelle si non spécifiée)
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = created_at if created_at else datetime.now()
        self.transactions = []  # Liste pour stocker les transactions de l'utilisateur
        self.budgets = []  # Liste pour stocker les budgets de l'utilisateur
        self.stocks = []  # Liste pour stocker les actions de l'utilisateur

    def add_transaction(self, transaction):
        """
        Ajoute une transaction à la liste des transactions de l'utilisateur.

        :param transaction: Objet Transaction à ajouter
        """
        self.transactions.append(transaction)

    def add_budget(self, budget):
        """
        Ajoute un budget à la liste des budgets de l'utilisateur.

        :param budget: Objet Budget à ajouter
        """
        self.budgets.append(budget)

    def add_stock(self, stock):
        """
        Ajoute une action à la liste des actions de l'utilisateur.

        :param stock: Objet Stock à ajouter
        """
        self.stocks.append(stock)

    def get_balance(self):
        """
        Calcule et retourne le solde actuel de l'utilisateur basé sur ses transactions.

        :return: Le solde actuel
        """
        return sum(transaction.amount for transaction in self.transactions)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'utilisateur.

        :return: Chaîne de caractères représentant l'utilisateur
        """
        return f"User(id={self.user_id}, username={self.username}, email={self.email})"