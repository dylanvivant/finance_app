from datetime import datetime
import logging

class Budget:
    """
    Classe représentant un budget pour une catégorie spécifique.
    """

    def __init__(self, budget_id, user_id, category, amount, period_start, period_end, spent=0):
        """
        Initialise un nouveau budget.

        :param budget_id: Identifiant unique du budget
        :param user_id: Identifiant de l'utilisateur associé à ce budget
        :param category: Catégorie du budget (par exemple, "Alimentation", "Loisirs", etc.)
        :param amount: Montant alloué pour ce budget
        :param period_start: Date de début de la période du budget
        :param period_end: Date de fin de la période du budget
        :param spent: Montant déjà dépensé (par défaut 0)
        """
        self.budget_id = budget_id
        self.user_id = user_id
        self.category = category
        self.amount = amount
        self.period_start = period_start
        self.period_end = period_end
        self.spent = spent
        logging.debug(f"Budget initialized: {self}")

    def add_expense(self, amount):
        """
        Ajoute une dépense au budget.

        :param amount: Montant de la dépense à ajouter (devrait être positif)
        """
        old_spent = self.spent
        self.spent += amount
        logging.debug(f"Expense added to budget {self.budget_id}: old_spent={old_spent}, amount={amount}, new_spent={self.spent}")

    def get_remaining(self):
        """
        Calcule le montant restant dans le budget.

        :return: Le montant restant
        """
        return self.amount - self.spent

    def is_overbudget(self):
        """
        Vérifie si le budget a été dépassé.

        :return: True si le budget est dépassé, False sinon
        """
        return self.spent > self.amount

    def to_dict(self):
        """
        Convertit l'objet Budget en dictionnaire pour la sérialisation.

        :return: Un dictionnaire représentant le budget
        """
        return {
            'budget_id': self.budget_id,
            'user_id': self.user_id,
            'category': self.category,
            'amount': self.amount,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'spent': self.spent
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée une instance de Budget à partir d'un dictionnaire.

        :param data: Dictionnaire contenant les données du budget
        :return: Une nouvelle instance de Budget
        """
        data['period_start'] = datetime.fromisoformat(data['period_start'])
        data['period_end'] = datetime.fromisoformat(data['period_end'])
        return cls(**data)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du budget.

        :return: Chaîne de caractères représentant le budget
        """
        return f"Budget pour {self.category}: {self.amount}€ (Dépensé: {self.spent}€, Restant: {self.get_remaining()}€)"