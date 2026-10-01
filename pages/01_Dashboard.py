
"""
VolyTrack — Dashboard
=====================

Tableau de bord principal de l'exploitation agricole.

Les données sont récupérées directement depuis SQLite
via les services métier :

    - ParcelleService
    - CultureService
    - DepenseService
    - RevenuService

Le Dashboard affiche notamment :

    - nombre de parcelles ;
    - nombre de cultures ;
    - total des dépenses ;
    - total des revenus ;
    - marge actuelle ;
    - superficie totale ;
    - résumé des parcelles ;
    - résumé des cultures.
"""

import streamlit as st
import pandas as pd

from core.services.parcelle_service import ParcelleService
from core.services.culture_service import CultureService
from core.services.depense_service import DepenseService
from core.services.revenu_service import RevenuService


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dashboard — VolyTrack",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# TITRE
# ============================================================

st.title("📊 Dashboard")

st.markdown(
    """
    Vue générale de l'exploitation agricole.

    Les indicateurs présentés ci-dessous sont calculés
    à partir des données réelles enregistrées dans SQLite.
    """
)

st.divider()


# ============================================================
# SERVICES
# ============================================================

parcelle_service = ParcelleService()
culture_service = CultureService()
depense_service = DepenseService()
revenu_service = RevenuService()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

try:

    parcelles = (
        parcelle_service.get_all_parcelles()
    )

    cultures = (
        culture_service.get_all_cultures()
    )

    depenses = (
        depense_service.get_all_depenses()
    )

    revenus = (
        revenu_service.get_all_revenus()
    )

except Exception as exc:

    st.error(
        f"""
        ❌ Impossible de charger les données du Dashboard.

        Erreur : {exc}
        """
    )

    st.stop()


# ============================================================
# CALCUL DES INDICATEURS
# ============================================================

# ------------------------------------------------------------
# PARCELLES
# ------------------------------------------------------------

total_parcelles = len(parcelles)


# ------------------------------------------------------------
# CULTURES
# ------------------------------------------------------------

total_cultures = len(cultures)


# ------------------------------------------------------------
# DÉPENSES
# ------------------------------------------------------------

total_depenses = sum(
    float(depense.montant)
    for depense in depenses
)


# ------------------------------------------------------------
# REVENUS
# ------------------------------------------------------------

total_revenus = sum(
    float(revenu.montant)
    for revenu in revenus
)


# ------------------------------------------------------------
# MARGE
# ------------------------------------------------------------

marge = (
    total_revenus
    - total_depenses
)


# ------------------------------------------------------------
# SUPERFICIE
# ------------------------------------------------------------

# Les superficies sont regroupées par unité afin de ne pas
# additionner directement des hectares et des mètres carrés.

superficie_ha = sum(
    float(parcelle.superficie)
    for parcelle in parcelles
    if parcelle.unite_superficie == "ha"
)

superficie_m2 = sum(
    float(parcelle.superficie)
    for parcelle in parcelles
    if parcelle.unite_superficie == "m²"
)


# ============================================================
# INDICATEURS PRINCIPAUX
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌾 Parcelles",
        total_parcelles,
    )


with col2:

    st.metric(
        "🌱 Cultures",
        total_cultures,
    )


with col3:

    st.metric(
        "💰 Dépenses",
        f"{total_depenses:,.0f} Ar",
    )


with col4:

    st.metric(
        "📈 Revenus",
        f"{total_revenus:,.0f} Ar",
    )


st.divider()


# ============================================================
# INDICATEURS FINANCIERS
# ============================================================

st.subheader("💰 Situation financière")


financial_col1, financial_col2, financial_col3 = st.columns(3)


with financial_col1:

    st.metric(
        "💸 Total des dépenses",
        f"{total_depenses:,.0f} Ar",
    )


with financial_col2:

    st.metric(
        "📈 Total des revenus",
        f"{total_revenus:,.0f} Ar",
    )


with financial_col3:

    st.metric(
        "💵 Marge",
        f"{marge:,.0f} Ar",
    )


st.caption(
    "Marge = Revenus − Dépenses"
)


st.divider()


# ============================================================
# SUPERFICIE
# ============================================================

st.subheader("📐 Superficie agricole")


surface_col1, surface_col2, surface_col3 = st.columns(3)


with surface_col1:

    st.metric(
        "🌾 Parcelles",
        total_parcelles,
    )


with surface_col2:

    st.metric(
        "📏 Superficie en hectares",
        f"{superficie_ha:.2f} ha",
    )


with surface_col3:

    st.metric(
        "📏 Superficie en m²",
        f"{superficie_m2:.2f} m²",
    )


st.divider()


# ============================================================
# RÉSUMÉ DE L'EXPLOITATION
# ============================================================

st.markdown(
    "## 📋 Résumé de l'exploitation"
)


col1, col2 = st.columns(2)


# ============================================================
# PARCELLES
# ============================================================

with col1:

    with st.expander(
        f"🌾 Parcelles ({total_parcelles})",
        expanded=True,
    ):

        if not parcelles:

            st.info(
                "Aucune parcelle enregistrée pour le moment."
            )

        else:

            parcelle_rows = []

            for parcelle in parcelles:

                parcelle_rows.append(
                    {
                        "ID": parcelle.id,
                        "Nom": parcelle.nom,
                        "Superficie": (
                            parcelle.superficie
                        ),
                        "Unité": (
                            parcelle.unite_superficie
                        ),
                        "Localisation": (
                            parcelle.localisation
                            or ""
                        ),
                    }
                )

            parcelle_df = pd.DataFrame(
                parcelle_rows
            )

            st.dataframe(
                parcelle_df,
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# CULTURES
# ============================================================

with col2:

    with st.expander(
        f"🌱 Cultures ({total_cultures})",
        expanded=True,
    ):

        if not cultures:

            st.info(
                "Aucune culture enregistrée pour le moment."
            )

        else:

            culture_rows = []

            for culture in cultures:

                culture_rows.append(
                    {
                        "ID": culture.id,
                        "Nom": culture.nom,
                        "Variété": (
                            culture.variete
                            or ""
                        ),
                        "Parcelle": (
                            culture.parcelle_id
                        ),
                        "Statut": (
                            culture.statut
                        ),
                    }
                )

            culture_df = pd.DataFrame(
                culture_rows
            )

            st.dataframe(
                culture_df,
                use_container_width=True,
                hide_index=True,
            )


st.divider()


# ============================================================
# DERNIÈRES DÉPENSES
# ============================================================

st.subheader("💸 Dépenses")


if not depenses:

    st.info(
        "Aucune dépense enregistrée pour le moment."
    )

else:

    depense_rows = []

    # Les dépenses retournées par le service sont affichées
    # dans l'ordre fourni par le repository.

    for depense in depenses[:10]:

        depense_rows.append(
            {
                "ID": depense.id,
                "Catégorie": depense.categorie,
                "Montant": (
                    f"{float(depense.montant):,.0f} Ar"
                ),
                "Date": depense.date_depense,
                "Parcelle": (
                    depense.parcelle_id
                    if depense.parcelle_id is not None
                    else ""
                ),
                "Culture": (
                    depense.culture_id
                    if depense.culture_id is not None
                    else ""
                ),
            }
        )

    depense_df = pd.DataFrame(
        depense_rows
    )

    st.dataframe(
        depense_df,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# ============================================================
# REVENUS
# ============================================================

st.subheader("📈 Revenus")


if not revenus:

    st.info(
        "Aucun revenu enregistré pour le moment."
    )

else:

    revenu_rows = []

    for revenu in revenus[:10]:

        revenu_rows.append(
            {
                "ID": revenu.id,
                "Produit": revenu.produit,
                "Quantité": revenu.quantite,
                "Prix unitaire": (
                    f"{float(revenu.prix_unitaire):,.0f} Ar"
                ),
                "Montant": (
                    f"{float(revenu.montant):,.0f} Ar"
                ),
                "Date": revenu.date_revenu,
            }
        )

    revenu_df = pd.DataFrame(
        revenu_rows
    )

    st.dataframe(
        revenu_df,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# ============================================================
# RÉSUMÉ GLOBAL
# ============================================================

st.subheader("📊 Résumé global")


summary_df = pd.DataFrame(
    {
        "Indicateur": [
            "Nombre de parcelles",
            "Nombre de cultures",
            "Nombre de dépenses",
            "Nombre de revenus",
            "Total dépenses",
            "Total revenus",
            "Marge",
        ],
        "Valeur": [
            total_parcelles,
            total_cultures,
            len(depenses),
            len(revenus),
            f"{total_depenses:,.0f} Ar",
            f"{total_revenus:,.0f} Ar",
            f"{marge:,.0f} Ar",
        ],
    }
)


st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# ÉTAT DU DASHBOARD
# ============================================================

st.divider()

st.markdown(
    "## ✅ État du Dashboard"
)

st.success(
    """
    Le Dashboard est maintenant connecté à la base de données
    SQLite via les services métier de VolyTrack.

    Les indicateurs sont calculés automatiquement à partir
    des données enregistrées dans l'application.
    """
)


# ============================================================
# INFORMATIONS TECHNIQUES
# ============================================================

with st.expander(
    "🔧 Informations techniques"
):

    st.markdown(
        """
        ### Sources des données

        Le Dashboard utilise les services suivants :

        - `ParcelleService`
        - `CultureService`
        - `DepenseService`
        - `RevenuService`

        Les services utilisent eux-mêmes les repositories
        et la base de données SQLite.

        ### Architecture

        ```text
        Streamlit Dashboard
                ↓
        Services métier
                ↓
        Repositories
                ↓
        SQLite
        ```

        Cette séparation permet de conserver la logique métier
        indépendante de l'interface Streamlit.
        """
    )

