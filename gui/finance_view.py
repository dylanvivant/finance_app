import csv
from datetime import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QWidget, QMessageBox, QCheckBox, QDateEdit
import matplotlib.pyplot as plt
from services.app_controller import AppController

class FinanceView(QWidget):
    def __init__(self, app_controller):
        super().__init__()
        
        # Initialisation du contrôleur de l'application
        self.app_controller = app_controller

        # Création d'un layout vertical pour l'interface
        layout = QVBoxLayout()

        # Label pour le titre de la section
        label = QLabel("Gestion des Transactions", self)
        layout.addWidget(label)

        # Champ de saisie pour entrer le montant de la transaction
        self.montant_input = QLineEdit(self)
        self.montant_input.setPlaceholderText("Montant de la transaction")
        layout.addWidget(self.montant_input)

        # Menu déroulant pour sélectionner la catégorie de la transaction
        self.categorie_input = QComboBox(self)
        self.categorie_input.addItems([
            "Courses", "Divertissement", "Voyage", "Restaurants", 
            "Virements", "Transport", "Santé", "Achat", "Services", "Autre"
        ])
        layout.addWidget(self.categorie_input)

        # Case à cocher pour une transaction planifiée
        self.planification_input = QCheckBox("Transaction planifiée ?", self)
        layout.addWidget(self.planification_input)

        # Champ pour entrer la date de la prochaine transaction
        self.date_planification = QDateEdit(self)
        layout.addWidget(self.date_planification)

        # Bouton pour ajouter la transaction
        self.btn_ajouter = QPushButton("Ajouter transaction", self)
        self.btn_ajouter.clicked.connect(self.ajouter_transaction)
        layout.addWidget(self.btn_ajouter)

        # Label pour afficher le solde actuel
        self.solde_label = QLabel(f"Solde actuel: {self.app_controller.get_balance()}", self)
        layout.addWidget(self.solde_label)

        # Bouton pour supprimer la dernière transaction
        self.btn_supprimer = QPushButton("Supprimer dernière transaction", self)
        self.btn_supprimer.clicked.connect(self.supprimer_transaction)
        layout.addWidget(self.btn_supprimer)

        # Bouton pour générer le rapport mensuel en CSV
        self.btn_generer_rapport = QPushButton("Générer rapport mensuel (CSV)", self)
        self.btn_generer_rapport.clicked.connect(self.generer_rapport_csv)
        layout.addWidget(self.btn_generer_rapport)

        # Bouton pour visualiser la répartition des dépenses
        self.btn_visualiser_graphique = QPushButton("Visualiser répartition des dépenses", self)
        self.btn_visualiser_graphique.clicked.connect(self.visualiser_repartition_depenses)
        layout.addWidget(self.btn_visualiser_graphique)

        # Appliquer le layout à la vue
        self.setLayout(layout)

    def ajouter_transaction(self):
        """
        Fonction pour ajouter une nouvelle transaction.
        Elle récupère les données saisies par l'utilisateur et utilise AppController pour ajouter la transaction.
        """
        try:
            montant = float(self.montant_input.text())
            categorie = self.categorie_input.currentText()
            date = self.date_planification.date().toPyDate()
            is_planned = self.planification_input.isChecked()

            # Utilisation de AppController pour ajouter la transaction
            transaction = self.app_controller.add_transaction(montant, categorie, date=date, is_planned=is_planned)
            
            if is_planned:
                QMessageBox.information(self, "Transaction planifiée", f"Transaction planifiée pour le {date}")
            else:
                self.update_solde_display()
                self.montant_input.clear()  # Réinitialiser le champ montant après ajout

        except ValueError:
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez entrer un montant valide.")

    def supprimer_transaction(self):
        """
        Fonction pour supprimer la dernière transaction.
        Elle utilise AppController pour supprimer la dernière transaction et met à jour l'affichage du solde.
        """
        deleted_transaction = self.app_controller.delete_last_transaction()
        if deleted_transaction:
            self.update_solde_display()
        else:
            QMessageBox.information(self, "Suppression impossible", "Aucune transaction à supprimer.")

    def generer_rapport_csv(self):
        """
        Fonction pour générer un rapport mensuel en CSV.
        Elle récupère les transactions via AppController et les écrit dans un fichier CSV.
        """
        transactions = self.app_controller.get_transactions()
        if not transactions:
            QMessageBox.warning(self, "Aucune transaction", "Il n'y a aucune transaction à inclure dans le rapport.")
            return

        nom_fichier = f"rapport_finances_{datetime.now().strftime('%Y_%m')}.csv"
        
        with open(nom_fichier, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Montant", "Catégorie"])
            
            for transaction in transactions:
                writer.writerow([transaction.date.strftime('%Y-%m-%d'), transaction.amount, transaction.category])
        
        QMessageBox.information(self, "Rapport généré", f"Le rapport a été sauvegardé sous le nom {nom_fichier}")

    def visualiser_repartition_depenses(self):
        """
        Fonction pour visualiser la répartition des dépenses avec matplotlib.
        Elle récupère les totaux par catégorie via AppController et crée un graphique circulaire.
        """
        totals_by_category = self.app_controller.get_total_by_category()

        labels = list(totals_by_category.keys())
        sizes = list(totals_by_category.values())

        # Création du graphique circulaire
        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Répartition des dépenses par catégorie")
        plt.show()

    def update_solde_display(self):
        """
        Fonction pour mettre à jour l'affichage du solde.
        Elle récupère le solde actuel via AppController et met à jour le label correspondant.
        """
        solde = self.app_controller.get_balance()
        self.solde_label.setText(f"Solde actuel: {solde}")