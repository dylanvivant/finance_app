import csv
from datetime import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QWidget, QMessageBox, QCheckBox, QDateEdit
import matplotlib.pyplot as plt

class FinanceView(QWidget):
    def __init__(self):
        super().__init__()

        # na- Création d'un layout vertical pour l'interface
        layout = QVBoxLayout()

        # na- Label pour le titre de la section
        label = QLabel("Gestion des Transactions", self)
        layout.addWidget(label)

        # na- Champ de saisie pour entrer le montant de la transaction
        self.montant_input = QLineEdit(self)
        self.montant_input.setPlaceholderText("Montant de la transaction")
        layout.addWidget(self.montant_input)

        # na- Menu déroulant pour sélectionner la catégorie de la transaction
        self.categorie_input = QComboBox(self)
        # na- Liste des catégories modifiées
        self.categorie_input.addItems([
            "Courses", "Divertissement", "Voyage", "Restaurants", 
            "Virements", "Transport", "Santé", "Achat", "Services", "Autre"
        ])
        layout.addWidget(self.categorie_input)

        # na- Case à cocher pour une transaction planifiée
        self.planification_input = QCheckBox("Transaction planifiée ?", self)
        layout.addWidget(self.planification_input)

        # na- Champ pour entrer la date de la prochaine transaction
        self.date_planification = QDateEdit(self)
        layout.addWidget(self.date_planification)

        # na- Bouton pour ajouter la transaction
        self.btn_ajouter = QPushButton("Ajouter transaction", self)
        self.btn_ajouter.clicked.connect(self.ajouter_transaction)  # na- Connecter le clic à la fonction d'ajout
        layout.addWidget(self.btn_ajouter)

        # na- Label pour afficher le solde actuel
        self.solde_label = QLabel("Solde actuel: 0", self)
        layout.addWidget(self.solde_label)

        # na- Bouton pour supprimer la dernière transaction
        self.btn_supprimer = QPushButton("Supprimer dernière transaction", self)
        self.btn_supprimer.clicked.connect(self.supprimer_transaction)
        layout.addWidget(self.btn_supprimer)

        # na- Bouton pour générer le rapport mensuel en CSV
        self.btn_generer_rapport = QPushButton("Générer rapport mensuel (CSV)", self)
        self.btn_generer_rapport.clicked.connect(self.generer_rapport_csv)
        layout.addWidget(self.btn_generer_rapport)

        # na- Bouton pour visualiser la répartition des dépenses
        self.btn_visualiser_graphique = QPushButton("Visualiser répartition des dépenses", self)
        self.btn_visualiser_graphique.clicked.connect(self.visualiser_repartition_depenses)
        layout.addWidget(self.btn_visualiser_graphique)

        # na- Appliquer le layout à la vue
        self.setLayout(layout)

        # na- Initialisation du solde à 0
        self.solde = 0

        # na- Initialisation des transactions et des transactions planifiées
        self.transactions = []
        self.transactions_planifiees = []

        # na- Initialisation des budgets par catégorie
        self.budgets = {
            "Courses": 500,
            "Divertissement": 300,
            "Voyage": 1000,
            "Restaurants": 200,
            "Virements": 500,
            "Transport": 300,
            "Santé": 200,
            "Achat": 400,
            "Services": 250,
            "Autre": 100
        }

    # na- Fonction pour ajouter une transaction
    def ajouter_transaction(self):
        try:
            montant = float(self.montant_input.text())
            categorie = self.categorie_input.currentText()

            # na- Vérification si la transaction est planifiée
            if self.planification_input.isChecked():
                date_planification = self.date_planification.date().toPyDate()
                self.transactions_planifiees.append((montant, categorie, date_planification))
                QMessageBox.information(self, "Transaction planifiée", f"Transaction planifiée pour le {date_planification}")
            else:
                # Ajouter la transaction dans la liste si elle n'est pas planifiée
                self.transactions.append((montant, categorie))
                self.solde += montant
                self.solde_label.setText(f"Solde actuel: {self.solde}")
                self.montant_input.clear()  # Réinitialiser le champ montant après ajout

        except ValueError:
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez entrer un montant valide.")

    # na- Fonction pour supprimer la dernière transaction
    def supprimer_transaction(self):
        if self.transactions:
            derniere_transaction = self.transactions.pop()
            montant = derniere_transaction[0]
            self.solde -= montant
            self.solde_label.setText(f"Solde actuel: {self.solde}")
        else:
            QMessageBox.information(self, "Suppression impossible", "Aucune transaction à supprimer.")

    # na- Fonction pour générer un rapport mensuel en CSV
    def generer_rapport_csv(self):
        nom_fichier = f"rapport_finances_{datetime.now().strftime('%Y_%m')}.csv"
        
        # Vérifier si des transactions existent avant de générer le rapport
        if not self.transactions:
            QMessageBox.warning(self, "Aucune transaction", "Il n'y a aucune transaction à inclure dans le rapport.")
            return

        # Écriture du fichier CSV
        with open(nom_fichier, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Montant", "Catégorie"])
            
            # Ajouter chaque transaction dans le fichier CSV
            for transaction in self.transactions:
                montant, categorie = transaction
                writer.writerow([datetime.now().strftime('%Y-%m-%d'), montant, categorie])
        
        QMessageBox.information(self, "Rapport généré", f"Le rapport a été sauvegardé sous le nom {nom_fichier}")

    # na- Fonction pour visualiser la répartition des dépenses avec matplotlib
    def visualiser_repartition_depenses(self):
        categories = {}
        for transaction in self.transactions:
            montant, categorie = transaction
            if categorie in categories:
                categories[categorie] += montant
            else:
                categories[categorie] = montant

        labels = list(categories.keys())
        sizes = list(categories.values())

        # na- Création du graphique circulaire
        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Répartition des dépenses par catégorie")
        plt.show()
