from models.transaction import Transaction
from models.user import User
from typing import List, Dict
from datetime import datetime

class FinanceManager:
    """
    Gère les opérations financières de l'utilisateur, y compris les transactions et les catégories.
    """

    def __init__(self, user: User):
        """
        Initialise le gestionnaire financier pour un utilisateur donné.
        
        :param user: L'utilisateur dont les finances sont gérées
        """
        self.user = user
        self.categories = set()  # Ensemble pour stocker les catégories uniques

    def add_transaction(self, amount: float, category: str, description: str = "") -> Transaction:
        """
        Ajoute une nouvelle transaction pour l'utilisateur.
        
        :param amount: Le montant de la transaction (positif pour les revenus, négatif pour les dépenses)
        :param category: La catégorie de la transaction
        :param description: Une description optionnelle de la transaction
        :return: La transaction créée
        """
        transaction = Transaction(
            transaction_id=len(self.user.transactions) + 1,
            user_id=self.user.user_id,
            amount=amount,
            category=category,
            description=description
        )
        self.user.add_transaction(transaction)
        self.categories.add(category)
        return transaction

    def get_balance(self) -> float:
        """
        Calcule et retourne le solde actuel de l'utilisateur.
        
        :return: Le solde actuel
        """
        return sum(transaction.amount for transaction in self.user.transactions)

    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """
        Retourne toutes les transactions d'une catégorie spécifique.
        
        :param category: La catégorie à filtrer
        :return: Une liste des transactions de la catégorie spécifiée
        """
        return [t for t in self.user.transactions if t.category == category]

    def get_total_by_category(self) -> Dict[str, float]:
        """
        Calcule le total des dépenses/revenus pour chaque catégorie.
        
        :return: Un dictionnaire avec les catégories comme clés et les totaux comme valeurs
        """
        totals = {}
        for category in self.categories:
            total = sum(t.amount for t in self.user.transactions if t.category == category)
            totals[category] = total
        return totals

    def get_transactions_for_period(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        """
        Retourne toutes les transactions dans une période donnée.
        
        :param start_date: La date de début de la période
        :param end_date: La date de fin de la période
        :return: Une liste des transactions dans la période spécifiée
        """
        return [t for t in self.user.transactions if start_date <= t.date <= end_date]