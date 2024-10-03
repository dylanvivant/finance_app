from models.transaction import Transaction
from models.user import User
from typing import List, Dict, Optional
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

    def add_transaction(self, amount, category, description="", date=None):
        """
        Ajoute une nouvelle transaction pour l'utilisateur.
        
        :param amount: Le montant de la transaction
        :param category: La catégorie de la transaction
        :param description: Une description optionnelle de la transaction
        :param date: La date de la transaction (optionnel)
        :return: La transaction créée
        """
        transaction_id = len(self.user.transactions) + 1
        transaction = Transaction(
            transaction_id=transaction_id,
            user_id=self.user.user_id,
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        self.user.add_transaction(transaction)
        self.categories.add(category)  # Ajout de la catégorie à l'ensemble des catégories
        return transaction

    # Les méthodes suivantes restent inchangées

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
    
    def delete_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """
        Supprime une transaction de l'utilisateur.
        
        :param transaction_id: L'ID de la transaction à supprimer
        :return: La transaction supprimée ou None si non trouvée
        """
        for i, transaction in enumerate(self.user.transactions):
            if transaction.transaction_id == transaction_id:
                deleted_transaction = self.user.transactions.pop(i)
                
                # Mise à jour des catégories si nécessaire
                if not any(t.category == deleted_transaction.category for t in self.user.transactions):
                    self.categories.remove(deleted_transaction.category)
                
                return deleted_transaction
        return None

    def update_transaction(self, transaction_id: int, amount: float, category: str, description: str) -> Optional[Transaction]:
        """
        Met à jour une transaction existante.
        
        :param transaction_id: L'ID de la transaction à mettre à jour
        :param amount: Le nouveau montant
        :param category: La nouvelle catégorie
        :param description: La nouvelle description
        :return: La transaction mise à jour ou None si non trouvée
        """
        for transaction in self.user.transactions:
            if transaction.transaction_id == transaction_id:
                old_category = transaction.category
                transaction.amount = amount
                transaction.category = category
                transaction.description = description
                
                # Mise à jour des catégories si nécessaire
                self.categories.add(category)
                if not any(t.category == old_category for t in self.user.transactions):
                    self.categories.remove(old_category)
                
                return transaction
        return None