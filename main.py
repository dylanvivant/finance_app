import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from services.app_controller import AppController

def main():
    """
    Fonction principale qui initialise et lance l'application.
    """
    # Créer l'application Qt
    app = QApplication(sys.argv)

    # Initialiser le contrôleur de l'application
    app_controller = AppController()

    # Créer la fenêtre principale en lui passant le contrôleur
    main_window = MainWindow(app_controller)

    # Afficher la fenêtre principale
    main_window.show()

    # Exécuter la boucle principale de l'application
    sys.exit(app.exec_())

# Point d'entrée du programme
if __name__ == "__main__":
    main()