from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QMessageBox, QLineEdit
from gui.finance_view import FinanceView
from services.app_controller import AppController

class MainWindow(QMainWindow):
    def __init__(self, app_controller):
        """
        Initialise la fenêtre principale de l'application.
        
        :param app_controller: Le contrôleur de l'application
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

        btn_login = QPushButton("Se connecter", self)
        btn_login.clicked.connect(self.show_login_dialog)
        layout.addWidget(btn_login)

        btn_create_account = QPushButton("Créer un compte", self)
        btn_create_account.clicked.connect(self.show_create_account_dialog)
        layout.addWidget(btn_create_account)

        btn_finances = QPushButton("Voir finances personnelles", self)
        btn_finances.clicked.connect(self.show_finance_view)
        layout.addWidget(btn_finances)

        btn_set_seuil = QPushButton("Définir le seuil bas", self)
        btn_set_seuil.clicked.connect(self.definir_seuil_bas)
        layout.addWidget(btn_set_seuil)

        btn_logout = QPushButton("Se déconnecter", self)
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)

        # Créer un widget central pour contenir les boutons
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_login_dialog(self):
        """
        Affiche une boîte de dialogue pour la connexion de l'utilisateur.
        """
        username, ok1 = QInputDialog.getText(self, "Connexion", "Nom d'utilisateur:")
        if ok1:
            password, ok2 = QInputDialog.getText(self, "Connexion", "Mot de passe:", QLineEdit.Password)
            if ok2:
                if self.app_controller.login(username, password):
                    QMessageBox.information(self, "Connexion réussie", "Vous êtes maintenant connecté.")
                    self.show_finance_view()
                else:
                    QMessageBox.warning(self, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

    def show_create_account_dialog(self):
        """
        Affiche une boîte de dialogue pour la création d'un nouveau compte utilisateur.
        """
        username, ok1 = QInputDialog.getText(self, "Création de compte", "Choisissez un nom d'utilisateur:")
        if ok1:
            email, ok2 = QInputDialog.getText(self, "Création de compte", "Entrez votre email:")
            if ok2:
                password, ok3 = QInputDialog.getText(self, "Création de compte", "Choisissez un mot de passe:", QLineEdit.Password)
                if ok3:
                    if self.app_controller.create_account(username, email, password):
                        QMessageBox.information(self, "Compte créé", "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
                    else:
                        QMessageBox.warning(self, "Erreur", "Ce nom d'utilisateur existe déjà.")

    def show_finance_view(self):
        """
        Affiche la vue des finances personnelles.
        """
        if self.app_controller.current_user:
            self.setCentralWidget(self.finance_view)
        else:
            QMessageBox.warning(self, "Non connecté", "Veuillez vous connecter pour accéder à vos finances.")

    def definir_seuil_bas(self):
        """
        Ouvre une boîte de dialogue pour définir le seuil bas du solde.
        Le seuil est ensuite enregistré dans le contrôleur de l'application.
        """
        if self.app_controller.current_user:
            current_threshold = self.app_controller.get_low_threshold()
            seuil, ok = QInputDialog.getDouble(self, "Définir le seuil bas", 
                                               f"Seuil actuel : {current_threshold}\nEntrez le nouveau montant du seuil bas:", 
                                               value=current_threshold, 
                                               decimals=2)
            if ok:
                self.app_controller.set_low_threshold(seuil)
                QMessageBox.information(self, "Seuil bas défini", f"Le seuil bas a été défini à {seuil}")
        else:
            QMessageBox.warning(self, "Non connecté", "Veuillez vous connecter pour définir un seuil.")

    def logout(self):
        """
        Déconnecte l'utilisateur actuel.
        """
        if self.app_controller.current_user:
            self.app_controller.logout()
            QMessageBox.information(self, "Déconnexion", "Vous avez été déconnecté.")
            self.initUI()  # Réinitialise l'interface utilisateur
        else:
            QMessageBox.warning(self, "Non connecté", "Aucun utilisateur n'est actuellement connecté.")