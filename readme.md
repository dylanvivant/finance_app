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
│   ├── budget.py
│   └── stock.py
│
├── services/               # Services métier
│   ├── finance_manager.py
│   ├── budget_manager.py
│   ├── stock_market.py
│   └── forecasting.py
│
├── gui/                    # Interface graphique
│   ├── main_window.py
│   ├── finance_view.py
│   └── stock_view.py
│
└── data/                   # Stockage des données
    ├── user_data.json
    └── stock_data.json
```

## Fonctionnalités Principales

1. Gestion des finances personnelles

   - Suivi des revenus et dépenses
   - Catégorisation des transactions
   - Budgétisation et objectifs financiers
   - Rapports et prévisions

2. Simulation du marché boursier

   - Achat et vente d'actions simulés
   - Suivi du portefeuille
   - Historique des transactions

3. Interface graphique utilisateur
   - Tableau de bord financier
   - Visualisation des données et graphiques
   - Interface de trading simulé

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

Voir `requirements.txt` pour la liste complète des dépendances.
