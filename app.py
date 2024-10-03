import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import io
from services.app_controller import AppController

# Initialisation de l'AppController
if 'app_controller' not in st.session_state:
    st.session_state.app_controller = AppController()

def ajouter_transaction(montant, categorie, transaction_date, est_depense, est_planifiee=False):
    """
    Ajoute une nouvelle transaction en utilisant l'AppController.
    
    :param montant: Le montant de la transaction
    :param categorie: La catégorie de la transaction
    :param transaction_date: La date de la transaction
    :param est_depense: Indique si la transaction est une dépense
    :param est_planifiee: Indique si la transaction est planifiée ou non
    :return: True si la transaction a été ajoutée avec succès, False sinon
    """
    # Vérification de la date pour les transactions planifiées
    if est_planifiee and transaction_date < date.today():
        st.error("Erreur : Vous ne pouvez pas planifier une transaction dans le passé.")
        return False

    # Conversion de la date en objet datetime
    if not isinstance(transaction_date, datetime):
        transaction_date = datetime.combine(transaction_date, datetime.min.time())

    # Si c'est une dépense, on rend le montant négatif
    if est_depense:
        montant = -abs(montant)

    transaction = st.session_state.app_controller.add_transaction(
        amount=montant,
        category=categorie,
        date=transaction_date,
        description="Transaction ajoutée via l'interface utilisateur"
    )

    if transaction:
        if not est_planifiee and st.session_state.app_controller.check_low_balance():
            st.warning(f"Attention : Votre solde est inférieur au seuil bas de {st.session_state.app_controller.get_low_threshold()} !")
        return True
    return False

# Titre de l'application
st.title("Gestion des Finances Personnelles")

# Gestion de la connexion utilisateur
if not st.session_state.app_controller.current_user:
    # Affichage du formulaire de connexion si l'utilisateur n'est pas connecté
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if st.session_state.app_controller.login(username, password):
            st.success("Connexion réussie!")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    # Affichage des informations de l'utilisateur connecté et option de déconnexion
    st.write(f"Connecté en tant que : {st.session_state.app_controller.current_user.username}")
    if st.button("Se déconnecter"):
        st.session_state.app_controller.logout()
        st.experimental_rerun()

# Le reste du code ne s'exécute que si l'utilisateur est connecté
if st.session_state.app_controller.current_user:
    # Formulaire pour ajouter une nouvelle transaction
    st.header("Ajouter une nouvelle transaction")
    montant = st.number_input("Montant de la transaction (€)", min_value=0.0)
    categorie = st.selectbox("Catégorie", ["Courses", "Divertissement", "Voyage", "Restaurants", 
                                           "Virements", "Transport", "Santé", "Achat", "Services", "Autre"])
    transaction_date = st.date_input("Date de la transaction", value=date.today())
    transaction_planifiee = st.checkbox("Transaction planifiée ?")

    if st.button("Ajouter transaction"):
        if ajouter_transaction(montant, categorie, transaction_date, transaction_planifiee):
            st.success("Transaction ajoutée avec succès!")

    # Affichage du tableau des transactions récentes
    st.header("Transactions récentes")
    transactions = st.session_state.app_controller.get_transactions()
    if transactions:
        # Création d'un DataFrame à partir des transactions
        df = pd.DataFrame([t.to_dict() for t in transactions])
        df['Montant (€)'] = df['amount'].apply(lambda x: f"{x:.2f}€")
        st.write(df[['date', 'Montant (€)', 'category']])
    else:
        st.write("Aucune transaction pour l'instant.")

    # Visualisation des données avec Matplotlib
    st.header("Visualisation des Dépenses et Revenus")
    if transactions:
        df = pd.DataFrame([t.to_dict() for t in transactions])
        
        # Séparation des dépenses et des revenus
        expenses = df[df['amount'] < 0].copy()
        incomes = df[df['amount'] > 0].copy()
        
        # Conversion des dépenses en valeurs positives pour la visualisation
        expenses['amount'] = expenses['amount'].abs()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # Graphique des dépenses
        if not expenses.empty:
            expenses.groupby('category')['amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax1, title='Répartition des Dépenses')
        else:
            ax1.text(0.5, 0.5, 'Pas de dépenses', ha='center', va='center')
        ax1.set_ylabel('')
        
        # Graphique des revenus
        if not incomes.empty:
            incomes.groupby('category')['amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax2, title='Répartition des Revenus')
        else:
            ax2.text(0.5, 0.5, 'Pas de revenus', ha='center', va='center')
        ax2.set_ylabel('')
        
        st.pyplot(fig)
    else:
        st.write("Aucune transaction pour générer un graphique.")

    # Génération et téléchargement du rapport CSV
    st.header("Génération de rapport")
    if transactions:
        df_report = df[['date', 'amount', 'category']]
        csv_buffer = io.StringIO()
        df_report['amount'] = df_report['amount'].apply(lambda x: f"{x:.2f}€")
        df_report.to_csv(csv_buffer, index=False, sep=',')

        st.download_button(
            label="Télécharger rapport CSV",
            data=csv_buffer.getvalue(),
            file_name=f"rapport_financier_{datetime.now().strftime('%Y_%m')}.csv",
            mime='text/csv',
        )
    else:
        st.write("Aucune transaction pour générer un rapport.")