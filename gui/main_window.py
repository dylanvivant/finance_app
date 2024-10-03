from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QMessageBox
from gui.finance_view import FinanceView
from services.app_controller import AppController

class MainWindow(QMainWindow):
    def __init__(self,  app_controller):
        """
        Initialise la fenêtre principale de l'application.
        """
        super().__init__()

        # Initialisation du contrôleur de l'application
        self.app_controller = app_controller

        # Initialisation de la vue des finances avec le contrôleur
        self.finance_view = FinanceView(self.app_controller)

        # Initialisation de l'interface utilisateur
        self.initUI()

    def initUI(self):
        """
        Configure l'interface utilisateur de la fenêtre principale.
        """
        # Définir le titre de la fenêtre
        self.setWindowTitle("Application de Gestion des Finances")
        self.setGeometry(100, 100, 800, 600)

        # Créer des boutons pour accéder aux différentes vues
        layout = QVBoxLayout()

        btn_finances = QPushButton("Voir finances personnelles", self)
        btn_finances.clicked.connect(self.show_finance_view)
        layout.addWidget(btn_finances)

        btn_set_seuil = QPushButton("Définir le seuil bas", self)
        btn_set_seuil.clicked.connect(self.definir_seuil_bas)
        layout.addWidget(btn_set_seuil)

        # Créer un widget central pour contenir les boutons
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_finance_view(self):
        """
        Affiche la vue des finances personnelles.
        """
        self.setCentralWidget(self.finance_view)

    def definir_seuil_bas(self):
        """
        Ouvre une boîte de dialogue pour définir le seuil bas du solde.
        Le seuil est ensuite enregistré dans le contrôleur de l'application.
        """
        seuil, ok = QInputDialog.getDouble(self, "Définir le seuil bas", "Entrez le montant du seuil bas:", decimals=2)
        if ok:
            # Ici, nous supposons que AppController a une méthode set_low_threshold
            # Si ce n'est pas le cas, il faudra l'ajouter à AppController
            self.app_controller.set_low_threshold(seuil)
            QMessageBox.information(self, "Seuil bas défini", f"Le seuil bas a été défini à {seuil}")