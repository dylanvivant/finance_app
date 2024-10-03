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
        # Modification: Gestion améliorée de la date
        if isinstance(date, datetime):
            self.date = date
        elif isinstance(date, str):
            self.date = datetime.fromisoformat(date)
        else:
            self.date = datetime.now()

    # Les méthodes suivantes restent inchangées
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

    def to_dict(self):
        """
        Convertit l'objet Transaction en dictionnaire pour la sérialisation.

        :return: Un dictionnaire représentant la transaction
        """
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée une instance de Transaction à partir d'un dictionnaire.

        :param data: Dictionnaire contenant les données de la transaction
        :return: Une nouvelle instance de Transaction
        """
        if isinstance(data['date'], str):
            data['date'] = datetime.fromisoformat(data['date'])
        return cls(**data)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la transaction.

        :return: Chaîne de caractères représentant la transaction
        """
        transaction_type = "Dépense" if self.is_expense() else "Revenu"
        return f"{transaction_type}: {abs(self.amount)}€ - {self.category} - {self.date.strftime('%Y-%m-%d')}"