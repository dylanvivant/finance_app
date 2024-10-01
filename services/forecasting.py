from typing import List, Dict
from datetime import datetime, timedelta
from models.transaction import Transaction
from models.user import User

class ForecastingService:
    """
    Service pour effectuer des prévisions financières basées sur l'historique des transactions.
    """

    def __init__(self, user: User):
        """
        Initialise le service de prévision pour un utilisateur donné.
        
        :param user: L'utilisateur pour lequel les prévisions sont faites
        """
        self.user = user

    def predict_future_balance(self, days: int) -> float:
        """
        Prédit le solde futur basé sur les tendances des transactions passées.
        
        :param days: Nombre de jours dans le futur pour la prévision
        :return: Le solde prévu
        """
        current_balance = sum(t.amount for t in self.user.transactions)
        daily_average = self._calculate_daily_average()
        predicted_change = daily_average * days
        return current_balance + predicted_change

    def _calculate_daily_average(self) -> float:
        """
        Calcule la moyenne quotidienne des transactions sur les 30 derniers jours.
        
        :return: La moyenne quotidienne des transactions
        """
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_transactions = [t for t in self.user.transactions if t.date >= thirty_days_ago]
        if not recent_transactions:
            return 0
        total_amount = sum(t.amount for t in recent_transactions)
        return total_amount / 30

    def predict_category_spending(self, category: str, days: int) -> float:
        """
        Prédit les dépenses futures pour une catégorie spécifique.
        
        :param category: La catégorie pour laquelle faire la prévision
        :param days: Nombre de jours dans le futur pour la prévision
        :return: Les dépenses prévues pour la catégorie
        """
        category_transactions = [t for t in self.user.transactions if t.category == category]
        if not category_transactions:
            return 0
        total_spent = sum(t.amount for t in category_transactions if t.amount < 0)
        days_since_first_transaction = (datetime.now() - min(t.date for t in category_transactions)).days
        daily_average = abs(total_spent) / max(days_since_first_transaction, 1)
        return daily_average * days

    def suggest_savings_goal(self) -> float:
        """
        Suggère un objectif d'épargne basé sur les habitudes de dépenses.
        
        :return: Le montant suggéré pour l'épargne mensuelle
        """
        monthly_income = sum(t.amount for t in self.user.transactions if t.amount > 0 and t.date >= datetime.now() - timedelta(days=30))
        monthly_expenses = abs(sum(t.amount for t in self.user.transactions if t.amount < 0 and t.date >= datetime.now() - timedelta(days=30)))
        
        if monthly_income > monthly_expenses:
            return (monthly_income - monthly_expenses) * 0.2  # Suggère d'épargner 20% du surplus
        else:
            return 0  # Pas de suggestion d'épargne si les dépenses dépassent les revenus