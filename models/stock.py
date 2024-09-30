# stock.py

from datetime import datetime

class Stock:
    """
    Classe représentant une action détenue par un utilisateur.
    """

    def __init__(self, stock_id, user_id, symbol, company_name, quantity, purchase_price, purchase_date=None):
        """
        Initialise une nouvelle action.

        :param stock_id: Identifiant unique de l'action
        :param user_id: Identifiant de l'utilisateur qui possède cette action
        :param symbol: Symbole boursier de l'action (par exemple, "AAPL" pour Apple)
        :param company_name: Nom de l'entreprise
        :param quantity: Quantité d'actions détenues
        :param purchase_price: Prix d'achat par action
        :param purchase_date: Date d'achat (par défaut à la date actuelle si non spécifiée)
        """
        self.stock_id = stock_id
        self.user_id = user_id
        self.symbol = symbol
        self.company_name = company_name
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date if purchase_date else datetime.now()
        self.current_price = purchase_price  # Initialisé au prix d'achat, à mettre à jour régulièrement

    def update_current_price(self, new_price):
        """
        Met à jour le prix actuel de l'action.

        :param new_price: Nouveau prix de l'action
        """
        self.current_price = new_price

    def get_total_value(self):
        """
        Calcule la valeur totale actuelle de l'investissement.

        :return: La valeur totale actuelle
        """
        return self.quantity * self.current_price

    def get_profit_loss(self):
        """
        Calcule le profit ou la perte actuelle sur l'investissement.

        :return: Le profit (positif) ou la perte (négatif)
        """
        return (self.current_price - self.purchase_price) * self.quantity

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'action.

        :return: Chaîne de caractères représentant l'action
        """
        return f"{self.company_name} ({self.symbol}): {self.quantity} actions à {self.current_price}€ (Achat: {self.purchase_price}€)"