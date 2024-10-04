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

    def get_balance(self):
        """
        Calcule et retourne le solde actuel de l'utilisateur basé sur ses transactions.

        :return: Le solde actuel
        """
        return sum(transaction.amount for transaction in self.transactions)

    def to_dict(self):
        """
        Convertit l'objet User en dictionnaire pour la sérialisation.

        :return: Un dictionnaire représentant l'utilisateur et ses données
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'transactions': [t.to_dict() for t in self.transactions],
            'budgets': [b.to_dict() for b in self.budgets]
        }

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'utilisateur.

        :return: Chaîne de caractères représentant l'utilisateur
        """
        return f"User(id={self.user_id}, username={self.username}, email={self.email})"