import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow  # na- Import de la fenêtre principale

# na- Point d'entrée du programme
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # na- Créer et afficher la fenêtre principale
    main_window = MainWindow()
    main_window.show()

    # na- Boucle principale de l'application (nécessaire pour exécuter l'application Qt)
    sys.exit(app.exec_())

