import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import io

# na- Initialisation des données
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

if 'solde' not in st.session_state:
    st.session_state.solde = 0

if 'seuil_bas' not in st.session_state:
    st.session_state.seuil_bas = -100  # na- Définir le seuil bas

# na- Fonction pour ajouter une transaction
def ajouter_transaction(montant, categorie, transaction_date, est_planifiee=False):
    # na- Vérification si la date est antérieure à aujourd'hui
    if est_planifiee and transaction_date < date.today():
        st.error("Erreur : Vous ne pouvez pas planifier une transaction dans le passé.")
        return False

    # na- Formatage de la transaction
    transaction = {
        'Date': transaction_date.strftime('%Y-%m-%d'),
        'Montant': montant,  # na- On garde le montant comme un nombre pour les calculs
        'Catégorie': categorie
    }

    # na- Statut de la transaction
    if est_planifiee:
        transaction['Statut'] = 'Planifiée'
    else:
        transaction['Statut'] = 'Effectuée'
        st.session_state.solde += montant  # na- Mise à jour du solde pour les transactions effectuées

    st.session_state.transactions.append(transaction)

    # na- Vérification du seuil bas si la transaction est effectuée
    if not est_planifiee and st.session_state.solde < st.session_state.seuil_bas:
        st.warning(f"Attention : Votre solde est inférieur au seuil bas de {st.session_state.seuil_bas} !")
    
    return True

# na- Titre de l'application
st.title("Gestion des Finances Personnelles")

# na- Formulaire pour ajouter une transaction
st.header("Ajouter une nouvelle transaction")
montant = st.number_input("Montant de la transaction (€)", min_value=0.0)
categorie = st.selectbox("Catégorie", ["Courses", "Divertissement", "Voyage", "Restaurants", 
                                       "Virements", "Transport", "Santé", "Achat", "Services", "Autre"])

# na- Ajout d'une date pour la transaction (aujourd'hui par défaut)
transaction_date = st.date_input("Date de la transaction", value=date.today())
transaction_planifiee = st.checkbox("Transaction planifiée ?")  # na- Case à cocher pour une transaction planifiée

# na- Bouton pour ajouter la transaction
if st.button("Ajouter transaction"):
    if ajouter_transaction(montant, categorie, transaction_date, transaction_planifiee):
        st.success("Transaction ajoutée avec succès!")

# na- Affichage du tableau des transactions
st.header("Transactions récentes")
if len(st.session_state.transactions) > 0:
    df = pd.DataFrame(st.session_state.transactions)
    
    # na- Format d'affichage : Ajout du symbole "€" pour l'affichage, sans modifier les montants dans les calculs
    df_display = df.copy()
    df_display['Montant (€)'] = df_display['Montant'].apply(lambda x: f"{x:.2f}€")
    
    st.write(df_display[['Date', 'Montant (€)', 'Catégorie', 'Statut']])
else:
    st.write("Aucune transaction pour l'instant.")

# na- Visualisation des données avec Matplotlib
st.header("Visualisation des Dépenses")
if len(st.session_state.transactions) > 0:
    df_effectuees = df[df['Statut'] == 'Effectuée']  # na- Visualiser uniquement les transactions effectuées
    if len(df_effectuees) > 0:
        fig, ax = plt.subplots()
        df_effectuees.groupby('Catégorie')['Montant'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
else:
    st.write("Aucune transaction pour générer un graphique.")

# na- Génération du rapport CSV avec bordures et colonnes séparées (Date, Montant, Catégorie)
st.header("Génération de rapport")
if len(st.session_state.transactions) > 0:
    # na- Sélectionner uniquement les colonnes utiles pour le rapport
    df_report = df[['Date', 'Montant', 'Catégorie']]

    # na- Création du fichier CSV propre avec les bordures pour Excel
    csv_buffer = io.StringIO()
    df_report['Montant'] = df_report['Montant'].apply(lambda x: f"{x:.2f}€")  # Ajouter € aux montants dans le CSV
    df_report.to_csv(csv_buffer, index=False, sep=',')

    st.download_button(
        label="Télécharger rapport CSV",
        data=csv_buffer.getvalue(),
        file_name=f"rapport_financier_{datetime.now().strftime('%Y_%m')}.csv",
        mime='text/csv',
    )
else:
    st.write("Aucune transaction pour générer un rapport.")
