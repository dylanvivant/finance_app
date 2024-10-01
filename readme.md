# Application de Gestion des Finances Personnelles et Simulation Boursière

## Description du Projet

Cette application Python combine la gestion des finances personnelles avec un simulateur de marché boursier. Elle permet aux utilisateurs de suivre leurs revenus, dépenses, économies et investissements, tout en offrant la possibilité de simuler des transactions boursières.

## Architecture du Projet

```
finance_app/
│
├── main.py                 # Point d'entrée de l'application
├── config.py               # Configuration globale
├── utils/                  # Utilitaires
│   ├── file_handlers.py
│   └── data_processing.py
│
├── models/                 # Modèles de données
│   ├── user.py
│   ├── transaction.py
│   └── budget.py
│
│
├── services/               # Services métier
│   ├── finance_manager.py
│   ├── budget_manager.py
│   ├── stock_market.py
│   └── forecasting.py
│
├── gui/                    # Interface graphique
│   ├── main_window.py
│   └── finance_view.py
│
│
└── data/                   # Stockage des données
    └── user_data.json
```

## Fonctionnalités Principales

1. Gestion des finances personnelles

   - Suivi détaillé des revenus et dépenses
   - Catégorisation flexible des transactions
   - Ajout, modification et suppression de transactions

2. Budgétisation

   - Création et gestion de budgets par catégorie
   - Suivi en temps réel des dépenses par rapport aux budgets fixés
   - Alertes de dépassement de budget

3. Analyse Financière

   - Génération de rapports financiers
   - Visualisation des tendances de dépenses et revenus
   - Prévisions financières basées sur l'historique

4. Interface graphique utilisateur
   - Tableau de bord financier intuitif
   - Graphiques et visualisations des données financières
   - Vue d'ensemble rapide de la santé financière

## Workflow Git et Nomenclature des Branches

Nous utilisons une adaptation du modèle GitFlow pour notre workflow de développement.

### Branches Principales

- `main` : Code de production stable
- `develop` : Branche d'intégration pour le développement

### Branches de Fonctionnalités

- Format : `feature/nom-de-la-fonctionnalite`
- Exemple : `feature/budget-tracking`

### Branches de Correction

- Format : `hotfix/description-du-probleme`
- Exemple : `hotfix/fix-calculation-bug`

### Branches de Version

- Format : `release/x.y.z`
- Exemple : `release/1.0.0`

## Guide de Contribution

1. Clonez le repository
2. Créez une nouvelle branche à partir de `develop` pour votre fonctionnalité
3. Committez vos changements avec des messages clairs
4. Poussez votre branche et créez une Pull Request vers `develop`
5. Attendez la revue de code et l'approbation avant de merger

## Installation

1. Clonez le repository
2. Créez un environnement virtuel : `python -m venv venv`
3. Activez l'environnement virtuel :
   - Windows : `venv\Scripts\activate`
   - Unix ou MacOS : `source venv/bin/activate`
4. Installez les dépendances : `pip install -r requirements.txt`
5. Lancez l'application : `python main.py`

## Dépendances

Les principales dépendances du projet sont les suivantes :

1. **PyQt5** : Interface graphique

   - `pip install PyQt5`

2. **pandas** : Manipulation et analyse de données

   - `pip install pandas`

3. **matplotlib** : Création de graphiques statiques

   - `pip install matplotlib`

4. **seaborn** : Amélioration des visualisations

   - `pip install seaborn`

5. **python-dateutil** : Manipulation avancée des dates

   - `pip install python-dateutil`

6. **numpy** : Calculs numériques

   - `pip install numpy`

7. **simplejson** : Manipulation avancée de JSON

   - `pip install simplejson`

8. **yfinance** (optionnel) : Données boursières réelles

   - `pip install yfinance`

9. **pytest** : Tests unitaires et d'intégration

   - `pip install pytest`

10. **black** : Formatage du code

    - `pip install black`

11. **flake8** : Linting du code

    - `pip install flake8`

12. **python-dotenv** : Gestion des variables d'environnement
    - `pip install python-dotenv`

Pour installer toutes les dépendances en une seule commande, utilisez :

```
pip install -r requirements.txt
```

Voir `requirements.txt` pour la liste complète et les versions spécifiques des dépendances.
