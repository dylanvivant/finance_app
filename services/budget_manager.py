from models.budget import Budget
from models.user import User
from models.transaction import Transaction
from typing import List, Dict
from datetime import datetime
import logging


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
        logging.debug(f"BudgetManager initialized for user: {user.username}")


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
        logging.debug(f"Created new budget: {budget}")
        return budget

    def get_budget_by_category(self, category: str) -> List[Budget]:
        """
        Retourne tous les budgets pour une catégorie spécifique.
        
        :param category: La catégorie à filtrer
        :return: Une liste des budgets de la catégorie spécifiée
        """
        budgets = [b for b in self.user.budgets if b.category == category]
        logging.debug(f"Retrieved budgets for category {category}: {budgets}")
        return budgets
    
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
        

    def update_budget_spent(self, category: str, amount: float):
        """
        Met à jour le montant dépensé pour tous les budgets actifs d'une catégorie.
        
        :param category: La catégorie du budget à mettre à jour
        :param amount: Le montant à ajouter aux dépenses (négatif pour les dépenses)
        """
        now = datetime.now()
        logging.debug(f"Updating budget spent for category: {category}, amount: {amount}")
        for budget in self.user.budgets:
            if budget.category == category and budget.period_start <= now <= budget.period_end:
                old_spent = budget.spent
                budget.add_expense(amount)
                logging.debug(f"Budget updated: category={category}, old_spent={old_spent}, new_spent={budget.spent}")

    def handle_transaction_deletion(self, transaction: Transaction):
        """
        Met à jour les budgets suite à la suppression d'une transaction.
        
        :param transaction: La transaction supprimée
        """
        logging.debug(f"Handling deletion of transaction: {transaction}")
        if transaction.is_expense():
            self.update_budget_spent(transaction.category, -transaction.amount)
        logging.debug(f"After deletion, budget spent: {self.get_budget_by_category(transaction.category)[0].spent}")

    def handle_transaction_update(self, old_transaction: Transaction, new_transaction: Transaction):
        """
        Met à jour les budgets suite à la modification d'une transaction.
        
        :param old_transaction: L'ancienne version de la transaction
        :param new_transaction: La nouvelle version de la transaction
        """
        logging.debug(f"Handling update of transaction: Old={old_transaction}, New={new_transaction}")
        if old_transaction.is_expense():
            self.update_budget_spent(old_transaction.category, -old_transaction.amount)
        if new_transaction.is_expense():
            self.update_budget_spent(new_transaction.category, new_transaction.amount)
        logging.debug(f"After update, budget spent: {self.get_budget_by_category(new_transaction.category)[0].spent}")
