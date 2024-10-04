# Application de Gestion des Finances Personnelles

## Description du Projet

Cette application Python est conçue pour la gestion des finances personnelles. Elle permet aux utilisateurs de suivre leurs revenus, dépenses et de gérer leurs budgets. L'application offre une interface utilisateur intuitive construite avec Streamlit.

## Architecture du Projet

```
finance_app/
│
├── app.py                  # Interface utilisateur Streamlit
├── main.py                 # Point d'entrée de l'application
├── config.py               # Configuration globale
│
├── utils/                  # Utilitaires
│   ├── file_handlers.py
│   └── data_processing.py
│
├── models/                 # Modèles de données
│   ├── user.py
│   ├── transaction.py
│   └── budget.py
│
├── services/               # Services métier
│   ├── app_controller.py
│   ├── finance_manager.py
│   ├── budget_manager.py
│   └── user_manager.py
│
└── data/                   # Stockage des données
    └── user_data.json
```

## Fonctionnalités Principales

1. Gestion des utilisateurs
   - Création de compte
   - Connexion/Déconnexion
   - Persistance de session

2. Gestion des finances personnelles
   - Ajout de transactions (revenus et dépenses)
   - Catégorisation des transactions
   - Affichage du solde actuel

3. Visualisation des données
   - Affichage des transactions récentes
   - Graphiques de répartition des dépenses et revenus

4. Génération de rapports
   - Export des données financières au format CSV

## Installation

1. Clonez le repository
2. Créez un environnement virtuel : `python -m venv venv`
3. Activez l'environnement virtuel :
   - Windows : `venv\Scripts\activate`
   - Unix ou MacOS : `source venv/bin/activate`
4. Installez les dépendances : `pip install -r requirements.txt`
5. Lancez l'application : `streamlit run app.py`

## Dépendances

Les principales dépendances du projet sont :

- Streamlit : Interface utilisateur web
- Pandas : Manipulation et analyse de données
- Matplotlib : Création de graphiques
- Python-dateutil : Manipulation avancée des dates

Voir `requirements.txt` pour la liste complète et les versions spécifiques des dépendances.

## Utilisation

1. Lancez l'application avec `streamlit run app.py`
2. Créez un compte ou connectez-vous
3. Utilisez l'interface pour ajouter des transactions, visualiser vos finances, et générer des rapports

## Développement Futur

## Roadmap du Projet

```mermaid
gantt
    title Roadmap du Projet de Gestion des Finances Personnelles
    dateFormat  YYYY-MM-DD
    section Phase 1 : Fondations
    Architecture de base             :done,    des1, 2023-01-01, 30d
    Gestion des utilisateurs         :done,    des2, after des1, 30d
    Interface utilisateur Streamlit  :done,    des3, after des2, 30d
    Transactions de base             :done,    des4, after des3, 30d
    Visualisation simple             :done,    des5, after des4, 30d
    Rapports CSV basiques            :done,    des6, after des5, 30d

    section Phase 2 : Amélioration
    Catégories personnalisables      :active,  des7, 2023-07-01, 45d
    Budgétisation par catégorie      :         des8, after des7, 45d
    Alertes de dépassement           :         des9, after des8, 30d
    Graphiques interactifs           :         des10, after des9, 45d
    Tableau de bord personnalisable  :         des11, after des10, 45d

    section Phase 3 : Analyses Avancées
    Analyse de tendances             :         des12, 2024-01-01, 60d
    Prévisions financières           :         des13, after des12, 60d
    Objectifs financiers             :         des14, after des13, 45d
    Rapports détaillés               :         des15, after des14, 45d
    Calendrier financier             :         des16, after des15, 45d

    section Phase 4 : Intégration
    Développement API                :         des17, 2024-07-01, 60d
    Import auto transactions         :         des18, after des17, 60d
    Synchro multi-appareils          :         des19, after des18, 45d
    Intégration cryptomonnaies       :         des20, after des19, 60d

    section Phase 5 : Fonctions Avancées
    Simulation d'investissements     :         des21, 2025-01-01, 60d
    Conseils IA                      :         des22, after des21, 75d
    Version mobile                   :         des23, after des22, 90d
    Planification retraite           :         des24, after des23, 60d
    Gestion des dettes               :         des25, after des24, 60d

    section Phase 6 : Optimisation
    Optimisation performances        :         des26, 2025-07-01, 2026-12-31
    Amélioration UX                  :         des27, 2025-07-01, 2026-12-31
    Tests automatisés                :         des28, 2025-07-01, 2026-12-31
    Sécurité avancée                 :         des29, 2025-07-01, 2026-12-31
    Scaling infrastructure           :         des30, 2025-07-01, 2026-12-31

```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à forker le projet, créer une branche, et soumettre une pull request.
