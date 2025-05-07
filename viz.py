import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def show_type_distribution(df):
    counts = df['FOR type'].value_counts().reset_index()
    counts.columns = ['Type', 'Nombre']
    fig = px.bar(counts, x='Type', y='Nombre', labels={'Type': 'Type de formation', 'Nombre': 'Nombre'})
    st.plotly_chart(fig, use_container_width=True)

def show_niveau_distribution(df):
    counts = df['FOR niveau de sortie'].value_counts().reset_index()
    counts.columns = ['Niveau', 'Nombre']
    fig = px.pie(counts, names='Niveau', values='Nombre', title='Répartition par niveau de sortie')
    st.plotly_chart(fig, use_container_width=True)

def show_formations_by_region(df):
    counts = df['ENS région'].value_counts().reset_index()
    counts.columns = ['Région', 'Nombre']
    fig = px.bar(counts, x='Région', y='Nombre', title="Nombre de formations par région")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def show_top_domains(df):
    top_domains = df['FOR indexation domaine web Onisep'].value_counts().head(10).reset_index()
    top_domains.columns = ['Domaine', 'Nombre']
    fig = px.bar(top_domains, x='Domaine', y='Nombre', title='Top 10 des domaines les plus fréquents')
    st.plotly_chart(fig, use_container_width=True)

def show_domain_heatmap(df):
    pivot = pd.crosstab(df['FOR indexation domaine web Onisep'], df['FOR niveau de sortie'])
    fig = px.imshow(
        pivot,
        labels=dict(x="Niveau de sortie", y="Domaine", color="Nombre"),
        title="Carte thermique Domaine vs Niveau"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_type_vs_statut(df):
    cross = pd.crosstab(df['FOR type'], df['ENS statut']).reset_index()
    fig = px.bar(
        cross, 
        x='FOR type', 
        y=cross.columns[1:], 
        title='Répartition des types de formations par statut', 
        labels={'value': 'Nombre', 'FOR type': 'Type'},
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)

def show_duration_distribution(df):
    duration = df['AF durée cycle standard'].dropna()
    fig = px.histogram(duration, nbins=20, title="Distribution des durées de formation")
    st.plotly_chart(fig, use_container_width=True)

def show_recent_updates(df):
    if 'FOR date de mise à jour' in df.columns:
        df['FOR date de mise à jour'] = pd.to_datetime(df['FOR date de mise à jour'], errors='coerce')
        recent = df.sort_values('FOR date de mise à jour', ascending=False).head(20)
        st.dataframe(recent[['FOR nom', 'ENS nom', 'FOR date de mise à jour']])
    else:
        st.warning("La colonne 'FOR date de mise à jour' est absente du fichier.")
