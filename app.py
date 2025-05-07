import streamlit as st
import pandas as pd
from utils import load_and_clean_data
from viz import (
    show_type_distribution,
    show_niveau_distribution,
    show_formations_by_region,
    show_top_domains,
    show_domain_heatmap,
    show_type_vs_statut,
    show_duration_distribution,
    show_recent_updates,
)

# Configuration de la page
st.set_page_config(layout="wide", page_title="Explorer les formations ONISEP")
st.title("Explorer les formations en France")

# Chargement des données
@st.cache_data
def load_data():
    return load_and_clean_data("data/formations.csv")

df = load_data()

# Menu de navigation
menu = st.sidebar.radio("Navigation", [
    "Vue d'ensemble",
    "Répartition géographique",
    "Formations par domaine",
    "Statut & durée"
])

# Filtres dynamiques
st.sidebar.subheader("Filtres")
region = st.sidebar.selectbox("Région", ["Toutes"] + sorted(df["ENS région"].unique()))
niveau = st.sidebar.selectbox("Niveau de sortie", ["Tous"] + sorted(df["FOR niveau de sortie"].unique()))

if region != "Toutes":
    df = df[df["ENS région"] == region]
if niveau != "Tous":
    df= df[df["FOR niveau de sortie"] == niveau]

# Barre de recherche
st.sidebar.subheader("Recherche libre")
search_query = st.sidebar.text_input("Entrez un mot-clé (ex : BTS, santé, lycée...)").lower()

# Colonnes à filtrer pour la recherche
search_cols = [
    "FOR type", 
    "FOR indexation domaine web Onisep", 
    "FOR niveau de sortie",
    "Lieu d'enseignement (ENS) libellé", 
    "ENS région", 
    "ENS statut"
]

if search_query:
    mask = df[search_cols].apply(lambda row: row.astype(str).str.lower().str.contains(search_query)).any(axis=1)
    df = df[mask]

#desired_cols = [
#   "FOR type", 
#   "FOR indexation domaine web Onisep", 
#   "FOR niveau de sortie",
#  "Établissement formateur nom",   # le vrai nom trouvé
#   "ENS région", 
#  "ENS statut"
#]
#search_cols = [col for col in desired_cols if col in df.columns]

#if search_query and search_cols:
#    mask = df[search_cols].apply(lambda row: row.astype(str).str.lower().str.contains(search_query)).any(axis=1)
#    df = df[mask]


# Affichage des pages
if menu == "Vue d'ensemble":
    st.subheader("Répartition des formations")
    show_type_distribution(df)
    show_niveau_distribution(df)

elif menu == "Répartition géographique":
    st.subheader("Formations par région")
    show_formations_by_region(df)

elif menu == "Formations par domaine":
    st.subheader("Domaines les plus fréquents")
    show_top_domains(df)
    show_domain_heatmap(df)

elif menu == "Statut & durée":
    st.subheader("Type de formation et statut")
    show_type_vs_statut(df)
    st.subheader("Durée des formations")
    show_duration_distribution(df)
