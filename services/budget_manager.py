from models.budget import Budget
from models.user import User
from typing import List, Dict
from datetime import datetime

class BudgetManager:
    """
    Gère les budgets de l'utilisateur par catégorie.
    """

    def __init__(self, user: User):
        """
        Initialise le gestionnaire de budget pour un utilisateur donné.
        
        :param user: L'utilisateur dont les budgets sont gérés
        """
        self.user = user

    def create_budget(self, category: str, amount: float, period_start: datetime, period_end: datetime) -> Budget:
        """
        Crée un nouveau budget pour une catégorie spécifique.
        
        :param category: La catégorie du budget
        :param amount: Le montant alloué pour ce budget
        :param period_start: La date de début de la période du budget
        :param period_end: La date de fin de la période du budget
        :return: Le budget créé
        """
        budget = Budget(
            budget_id=len(self.user.budgets) + 1,
            user_id=self.user.user_id,
            category=category,
            amount=amount,
            period_start=period_start,
            period_end=period_end
        )
        self.user.add_budget(budget)
        return budget

    def get_budget_by_category(self, category: str) -> List[Budget]:
        """
        Retourne tous les budgets pour une catégorie spécifique.
        
        :param category: La catégorie à filtrer
        :return: Une liste des budgets de la catégorie spécifiée
        """
        return [b for b in self.user.budgets if b.category == category]

    def update_budget_spent(self, category: str, amount: float):
        """
        Met à jour le montant dépensé pour tous les budgets actifs d'une catégorie.
        
        :param category: La catégorie du budget à mettre à jour
        :param amount: Le montant à ajouter aux dépenses
        """
        now = datetime.now()
        for budget in self.user.budgets:
            if budget.category == category and budget.period_start <= now <= budget.period_end:
                budget.add_expense(amount)

    def get_budget_status(self) -> Dict[str, Dict[str, float]]:
        """
        Retourne le statut de tous les budgets actifs.
        
        :return: Un dictionnaire avec les catégories comme clés et les statuts de budget comme valeurs
        """
        status = {}
        now = datetime.now()
        for budget in self.user.budgets:
            if budget.period_start <= now <= budget.period_end:
                status[budget.category] = {
                    "allocated": budget.amount,
                    "spent": budget.spent,
                    "remaining": budget.get_remaining()
                }
        return status