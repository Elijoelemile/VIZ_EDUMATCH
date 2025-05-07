import pandas as pd

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)

    # Nettoyage de base
    df['AF date de modification'] = pd.to_datetime(df['AF date de modification'], errors='coerce')
    df['FOR indexation domaine web Onisep'] = df['FOR indexation domaine web Onisep'].fillna('Inconnu')
    df['ENS région'] = df['ENS région'].fillna('Inconnu')
    df['FOR niveau de sortie'] = df['FOR niveau de sortie'].fillna('Inconnu')
    df['FOR type'] = df['FOR type'].fillna('Autre')
    df['ENS statut'] = df['ENS statut'].fillna('Non précisé')

    df = df.drop_duplicates()

    return df