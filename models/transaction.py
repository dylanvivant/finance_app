from datetime import datetime

class Transaction:
    """
    Classe représentant une transaction financière.
    """

    def __init__(self, transaction_id, user_id, amount, category, description="", date=None):
        """
        Initialise une nouvelle transaction.

        :param transaction_id: Identifiant unique de la transaction
        :param user_id: Identifiant de l'utilisateur associé à cette transaction
        :param amount: Montant de la transaction (positif pour les revenus, négatif pour les dépenses)
        :param category: Catégorie de la transaction (par exemple, "Alimentation", "Loisirs", etc.)
        :param description: Description optionnelle de la transaction
        :param date: Date de la transaction (par défaut à la date actuelle si non spécifiée)
        """
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else datetime.now()

    def is_expense(self):
        """
        Détermine si la transaction est une dépense.

        :return: True si c'est une dépense, False sinon
        """
        return self.amount < 0

    def is_income(self):
        """
        Détermine si la transaction est un revenu.

        :return: True si c'est un revenu, False sinon
        """
        return self.amount > 0

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la transaction.

        :return: Chaîne de caractères représentant la transaction
        """
        transaction_type = "Dépense" if self.is_expense() else "Revenu"
        return f"{transaction_type}: {abs(self.amount)}€ - {self.category} - {self.date.strftime('%Y-%m-%d')}"