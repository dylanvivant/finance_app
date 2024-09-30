from datetime import datetime

class Budget:
    """
    Classe représentant un budget pour une catégorie spécifique.
    """

    def __init__(self, budget_id, user_id, category, amount, period_start, period_end):
        """
        Initialise un nouveau budget.

        :param budget_id: Identifiant unique du budget
        :param user_id: Identifiant de l'utilisateur associé à ce budget
        :param category: Catégorie du budget (par exemple, "Alimentation", "Loisirs", etc.)
        :param amount: Montant alloué pour ce budget
        :param period_start: Date de début de la période du budget
        :param period_end: Date de fin de la période du budget
        """
        self.budget_id = budget_id
        self.user_id = user_id
        self.category = category
        self.amount = amount
        self.period_start = period_start
        self.period_end = period_end
        self.spent = 0  # Montant dépensé, initialisé à 0

    def add_expense(self, amount):
        """
        Ajoute une dépense au budget.

        :param amount: Montant de la dépense à ajouter
        """
        self.spent += amount

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

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du budget.

        :return: Chaîne de caractères représentant le budget
        """
        return f"Budget pour {self.category}: {self.amount}€ (Dépensé: {self.spent}€, Restant: {self.get_remaining()}€)"