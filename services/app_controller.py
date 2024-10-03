from models.user import User
from services.finance_manager import FinanceManager
from services.budget_manager import BudgetManager
from datetime import datetime, timedelta

class AppController:
    """
    Classe centrale qui gère la communication entre l'interface utilisateur et la logique métier.
    Elle coordonne les actions entre FinanceManager et BudgetManager.
    """

    def __init__(self):
        """
        Initialise le contrôleur de l'application avec un utilisateur par défaut
        et les gestionnaires de finances et de budget.
        """
        self.user = User(user_id=1, username="Default User", email="user@example.com")
        self.finance_manager = FinanceManager(self.user)
        self.budget_manager = BudgetManager(self.user)
        self.low_threshold = 0  # Initialisation du seuil bas à 0


    def set_low_threshold(self, threshold):
        """
        Définit le seuil bas pour le solde de l'utilisateur.

        :param threshold: Le nouveau seuil bas
        """
        self.low_threshold = threshold

    def get_low_threshold(self):
        """
        Récupère le seuil bas actuel pour le solde de l'utilisateur.

        :return: Le seuil bas actuel
        """
        return self.low_threshold

    def check_low_balance(self):
        """
        Vérifie si le solde actuel est inférieur au seuil bas.

        :return: True si le solde est inférieur au seuil bas, False sinon
        """
        current_balance = self.get_balance()
        return current_balance < self.low_threshold

    def add_transaction(self, amount, category, description="", date=None, is_planned=False):
        """
        Ajoute une nouvelle transaction et met à jour le budget si nécessaire.
        """
        transaction = self.finance_manager.add_transaction(amount, category, description)
        if not is_planned:
            self.budget_manager.update_budget_spent(category, amount)
        return transaction

    def get_balance(self):
        """
        Récupère le solde actuel de l'utilisateur.
        """
        return self.finance_manager.get_balance()

    def get_budget_status(self):
        """
        Récupère le statut actuel des budgets.
        """
        return self.budget_manager.get_budget_status()

    def get_transactions(self):
        """
        Récupère toutes les transactions de l'utilisateur.
        """
        return self.user.transactions

    def delete_last_transaction(self):
        """
        Supprime la dernière transaction et met à jour le solde et le budget.
        """
        if self.user.transactions:
            last_transaction = self.user.transactions[-1]
            deleted_transaction = self.finance_manager.delete_transaction(last_transaction.transaction_id)
            if deleted_transaction:
                self.budget_manager.handle_transaction_deletion(deleted_transaction)
            return deleted_transaction
        return None

    def set_budget(self, category, amount, period_start=None, period_end=None):
        """
        Définit ou met à jour le budget pour une catégorie donnée.
        """
        if period_start is None:
            period_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if period_end is None:
            period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        return self.budget_manager.create_budget(category, amount, period_start, period_end)

    def get_budgets(self):
        """
        Récupère tous les budgets de l'utilisateur.
        """
        return self.user.budgets

    def update_transaction(self, transaction_id, amount, category, description):
        """
        Met à jour une transaction existante.
        """
        old_transaction = next((t for t in self.user.transactions if t.transaction_id == transaction_id), None)
        if old_transaction:
            new_transaction = self.finance_manager.update_transaction(transaction_id, amount, category, description)
            if new_transaction:
                self.budget_manager.handle_transaction_update(old_transaction, new_transaction)
            return new_transaction
        return None

    def get_transactions_by_category(self, category):
        """
        Récupère toutes les transactions d'une catégorie spécifique.
        """
        return self.finance_manager.get_transactions_by_category(category)

    def get_total_by_category(self):
        """
        Calcule le total des dépenses/revenus pour chaque catégorie.
        """
        return self.finance_manager.get_total_by_category()

    def get_transactions_for_period(self, start_date, end_date):
        """
        Récupère toutes les transactions dans une période donnée.
        """
        return self.finance_manager.get_transactions_for_period(start_date, end_date)