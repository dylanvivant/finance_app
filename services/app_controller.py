from models.user import User
from models.transaction import Transaction
from models.budget import Budget
from services.finance_manager import FinanceManager
from services.budget_manager import BudgetManager
from services.user_manager import UserManager
from datetime import datetime, timedelta

class AppController:
    """
    Classe centrale qui gère la communication entre l'interface utilisateur et la logique métier.
    Elle coordonne les actions entre UserManager, FinanceManager et BudgetManager.
    """

    def __init__(self):
        """
        Initialise le contrôleur de l'application avec un gestionnaire d'utilisateurs,
        et prépare les gestionnaires de finances et de budget.
        """
        self.user_manager = UserManager()
        self.current_user = None
        self.finance_manager = None
        self.budget_manager = None
        self.low_threshold = 0

    def create_account(self, username, email, password):
        """
        Crée un nouveau compte utilisateur.

        :param username: Nom d'utilisateur
        :param email: Adresse email de l'utilisateur
        :param password: Mot de passe de l'utilisateur
        :return: True si le compte a été créé, False sinon
        """
        return self.user_manager.create_user(username, email, password)

    def login(self, username, password):
        """
        Authentifie un utilisateur et charge ses données.

        :param username: Nom d'utilisateur
        :param password: Mot de passe de l'utilisateur
        :return: True si l'authentification réussit, False sinon
        """
        if self.user_manager.authenticate(username, password):
            user_data = self.user_manager.get_user_data(username)
            if user_data:
                self.current_user = User(user_id=user_data.get('user_id', 1), username=username, email=user_data['email'])
                self.finance_manager = FinanceManager(self.current_user)
                self.budget_manager = BudgetManager(self.current_user)
                self.load_user_data(user_data)
                return True
        return False

    def load_user_data(self, user_data):
        """
        Charge les données de l'utilisateur (transactions et budgets).

        :param user_data: Dictionnaire contenant les données de l'utilisateur
        """
        for transaction_data in user_data.get('transactions', []):
            transaction = Transaction.from_dict(transaction_data)
            self.current_user.add_transaction(transaction)
        for budget_data in user_data.get('budgets', []):
            budget = Budget(**budget_data)
            self.current_user.add_budget(budget)

    def save_user_data(self):
        """
        Sauvegarde les données de l'utilisateur courant.
        """
        if self.current_user:
            transactions = [t.to_dict() for t in self.current_user.transactions]
            budgets = [b.__dict__ for b in self.current_user.budgets]
            self.user_manager.update_user_data(self.current_user.username, transactions, budgets)

    def logout(self):
        """
        Déconnecte l'utilisateur actuel et sauvegarde ses données.
        """
        if self.current_user:
            self.save_user_data()
            self.current_user = None
            self.finance_manager = None
            self.budget_manager = None

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

    def add_transaction(self, amount, category, description="", date=None):
        """
        Ajoute une nouvelle transaction et met à jour le budget si nécessaire.

        :param amount: Montant de la transaction
        :param category: Catégorie de la transaction
        :param description: Description de la transaction (optionnel)
        :param date: Date de la transaction (optionnel)
        :return: La transaction créée
        """
        transaction = self.finance_manager.add_transaction(amount, category, description, date)
        self.budget_manager.update_budget_spent(category, amount)
        self.save_user_data()
        return transaction

    def get_balance(self):
        """
        Récupère le solde actuel de l'utilisateur.

        :return: Le solde actuel
        """
        return self.finance_manager.get_balance()

    def get_budget_status(self):
        """
        Récupère le statut actuel des budgets.

        :return: Un dictionnaire avec le statut des budgets
        """
        return self.budget_manager.get_budget_status()

    def get_transactions(self):
        """
        Récupère toutes les transactions de l'utilisateur.

        :return: Une liste de toutes les transactions
        """
        return self.current_user.transactions

    def delete_last_transaction(self):
        """
        Supprime la dernière transaction et met à jour le solde et le budget.

        :return: La transaction supprimée ou None si aucune transaction n'existe
        """
        if self.current_user.transactions:
            last_transaction = self.current_user.transactions[-1]
            deleted_transaction = self.finance_manager.delete_transaction(last_transaction.transaction_id)
            if deleted_transaction:
                self.budget_manager.handle_transaction_deletion(deleted_transaction)
                self.save_user_data()
            return deleted_transaction
        return None

    def set_budget(self, category, amount, period_start=None, period_end=None):
        """
        Définit ou met à jour le budget pour une catégorie donnée.

        :param category: La catégorie du budget
        :param amount: Le montant du budget
        :param period_start: Date de début de la période (optionnel)
        :param period_end: Date de fin de la période (optionnel)
        :return: Le budget créé ou mis à jour
        """
        if period_start is None:
            period_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if period_end is None:
            period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        budget = self.budget_manager.create_budget(category, amount, period_start, period_end)
        self.save_user_data()
        return budget

    def get_budgets(self):
        """
        Récupère tous les budgets de l'utilisateur.

        :return: Une liste de tous les budgets
        """
        return self.current_user.budgets

    def update_transaction(self, transaction_id, amount, category, description):
        """
        Met à jour une transaction existante.

        :param transaction_id: L'ID de la transaction à mettre à jour
        :param amount: Le nouveau montant
        :param category: La nouvelle catégorie
        :param description: La nouvelle description
        :return: La transaction mise à jour ou None si non trouvée
        """
        old_transaction = next((t for t in self.current_user.transactions if t.transaction_id == transaction_id), None)
        if old_transaction:
            new_transaction = self.finance_manager.update_transaction(transaction_id, amount, category, description)
            if new_transaction:
                self.budget_manager.handle_transaction_update(old_transaction, new_transaction)
                self.save_user_data()
            return new_transaction
        return None

    def get_transactions_by_category(self, category):
        """
        Récupère toutes les transactions d'une catégorie spécifique.

        :param category: La catégorie des transactions à récupérer
        :return: Une liste des transactions de la catégorie spécifiée
        """
        return self.finance_manager.get_transactions_by_category(category)

    def get_total_by_category(self):
        """
        Calcule le total des dépenses/revenus pour chaque catégorie.

        :return: Un dictionnaire avec les catégories comme clés et les totaux comme valeurs
        """
        return self.finance_manager.get_total_by_category()

    def get_transactions_for_period(self, start_date, end_date):
        """
        Récupère toutes les transactions dans une période donnée.

        :param start_date: Date de début de la période
        :param end_date: Date de fin de la période
        :return: Une liste des transactions dans la période spécifiée
        """
        return self.finance_manager.get_transactions_for_period(start_date, end_date)