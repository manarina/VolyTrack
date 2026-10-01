import streamlit as st


# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="VolyTrack",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# EN-TÊTE
# ============================================================

st.title("🌱 VolyTrack")

st.subheader(
    "Agricultural Management & Tracking"
)

st.markdown(
    """
    **VolyTrack** est une application de gestion et de suivi
    d'une exploitation agricole.

    Elle permettra de centraliser les informations concernant
    les parcelles, les cultures, les travaux, les dépenses,
    les revenus et les récoltes.
    """
)

st.divider()


# ============================================================
# PRÉSENTATION DES MODULES
# ============================================================

st.markdown("## 📋 Modules de l'application")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌾 Parcelles",
        "0",
    )

with col2:
    st.metric(
        "🌱 Cultures",
        "0",
    )

with col3:
    st.metric(
        "💰 Dépenses",
        "0 Ar",
    )

with col4:
    st.metric(
        "📈 Revenus",
        "0 Ar",
    )


st.divider()


# ============================================================
# MODULES
# ============================================================

modules = [
    ("📊", "Dashboard", "Vue générale de l'exploitation"),
    ("🌾", "Parcelles", "Gestion des parcelles agricoles"),
    ("🌱", "Cultures", "Suivi des cultures"),
    ("🔧", "Travaux", "Suivi des travaux agricoles"),
    ("💰", "Dépenses", "Gestion des dépenses"),
    ("📈", "Revenus", "Gestion des revenus"),
    ("🧺", "Récoltes", "Suivi de la production"),
    ("📊", "Analytics", "Analyse des performances"),
]

for icon, name, description in modules:
    st.markdown(
        f"**{icon} {name}** — {description}"
    )


st.divider()


# ============================================================
# ÉTAT DU PROJET
# ============================================================

st.markdown("## 🚧 État du projet")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Modules",
        "8",
    )

with col2:
    st.metric(
        "Base de données",
        "En préparation",
    )

with col3:
    st.metric(
        "Version",
        "v0.1",
    )


st.info(
    """
    🌱 **VolyTrack est actuellement en phase d'initialisation.**

    Les prochaines étapes permettront d'ajouter la base de données,
    les modèles, les opérations CRUD, les indicateurs agricoles
    et les analyses financières.
    """
)