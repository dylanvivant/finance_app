from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QMessageBox
from gui.finance_view import FinanceView  # na- Import de la vue des finances

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # na- Initialisation de la vue des finances
        self.finance_view = FinanceView()
        self.initUI()

    def initUI(self):
        # na- Définir le titre de la fenêtre
        self.setWindowTitle("Application de Gestion des Finances")
        self.setGeometry(100, 100, 800, 600)

        # na- Créer des boutons pour accéder aux différentes vues
        layout = QVBoxLayout()

        btn_finances = QPushButton("Voir finances personnelles", self)
        btn_finances.clicked.connect(self.show_finance_view)
        layout.addWidget(btn_finances)

        btn_set_seuil = QPushButton("Définir le seuil bas", self)
        btn_set_seuil.clicked.connect(self.definir_seuil_bas)
        layout.addWidget(btn_set_seuil)

        # na- Créer un widget central pour contenir les boutons
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # na- Fonction pour afficher la vue des finances
    def show_finance_view(self):
        self.setCentralWidget(self.finance_view)

    # na- Fonction pour définir le seuil bas
    def definir_seuil_bas(self):
        seuil, ok = QInputDialog.getDouble(self, "Définir le seuil bas", "Entrez le montant du seuil bas:", decimals=2)
        if ok:
            self.finance_view.seuil_bas = seuil
            QMessageBox.information(self, "Seuil bas défini", f"Le seuil bas a été défini à {seuil}")
