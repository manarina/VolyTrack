
"""
VolyTrack — Analytics
=====================

Interface Streamlit d'analyse des données agricoles.

Fonctionnalités :
    - analyse financière ;
    - analyse des dépenses ;
    - analyse des revenus ;
    - analyse des récoltes ;
    - analyse des cultures ;
    - analyse des parcelles ;
    - calcul de la marge ;
    - calcul de la rentabilité ;
    - analyse temporelle ;
    - tableaux de synthèse ;
    - graphiques interactifs avec Plotly.
"""

import streamlit as st
import pandas as pd

from core.services.parcelle_service import ParcelleService
from core.services.culture_service import CultureService
from core.services.travail_service import TravailService
from core.services.depense_service import DepenseService
from core.services.revenu_service import RevenuService
from core.services.recolte_service import RecolteService


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VolyTrack — Analytics",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 VolyTrack — Analytics")

st.markdown(
    """
    Analysez les performances de votre exploitation agricole
    à partir des données enregistrées dans **VolyTrack**.

    Cette page permet d'étudier :

    - les parcelles ;
    - les cultures ;
    - les travaux ;
    - les dépenses ;
    - les revenus ;
    - les récoltes ;
    - la marge ;
    - la rentabilité.
    """
)

st.divider()


# ============================================================
# SERVICES
# ============================================================

parcelle_service = ParcelleService()
culture_service = CultureService()
travail_service = TravailService()
depense_service = DepenseService()
revenu_service = RevenuService()
recolte_service = RecolteService()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

try:

    parcelles = parcelle_service.get_all_parcelles()
    cultures = culture_service.get_all_cultures()
    travaux = travail_service.get_all_travaux()
    depenses = depense_service.get_all_depenses()
    revenus = revenu_service.get_all_revenus()
    recoltes = recolte_service.get_all_recoltes()

except Exception as exc:

    st.error(
        f"❌ Impossible de charger les données : {exc}"
    )

    st.stop()


# ============================================================
# DICTIONNAIRES
# ============================================================

parcelle_names = {
    parcelle.id: parcelle.nom
    for parcelle in parcelles
}

culture_names = {
    culture.id: culture.nom
    for culture in cultures
}

culture_parcelle_ids = {
    culture.id: culture.parcelle_id
    for culture in cultures
}


# ============================================================
# INDICATEURS GÉNÉRAUX
# ============================================================

total_parcelles = len(parcelles)
total_cultures = len(cultures)
total_travaux = len(travaux)
total_depenses = len(depenses)
total_revenus = len(revenus)
total_recoltes = len(recoltes)


# ============================================================
# INDICATEURS FINANCIERS
# ============================================================

chiffre_affaires = sum(
    float(revenu.montant)
    for revenu in revenus
)

montant_depenses = sum(
    float(depense.montant)
    for depense in depenses
)

cout_travaux = sum(
    float(travail.cout)
    for travail in travaux
)

# Les coûts des travaux sont déjà des dépenses opérationnelles
# distinctes dans le modèle.
#
# Ils sont donc affichés séparément et ne sont pas ajoutés
# automatiquement aux dépenses afin d'éviter un double comptage.

marge = (
    chiffre_affaires
    - montant_depenses
)

rentabilite = (
    (marge / montant_depenses) * 100
    if montant_depenses > 0
    else 0.0
)


# ============================================================
# INDICATEURS DE PRODUCTION
# ============================================================

production_totale = sum(
    float(recolte.quantite)
    for recolte in recoltes
)


# ============================================================
# SURFACES
# ============================================================

surface_hectares = sum(
    float(parcelle.superficie)
    for parcelle in parcelles
    if str(parcelle.unite_superficie).lower()
    in ("ha", "hectare", "hectares")
)

surface_m2 = sum(
    float(parcelle.superficie)
    for parcelle in parcelles
    if str(parcelle.unite_superficie).lower()
    in ("m2", "m²", "m")
)


# ============================================================
# FILTRES
# ============================================================

st.subheader("🔎 Filtres d'analyse")

filter_col1, filter_col2, filter_col3 = st.columns(3)


with filter_col1:

    selected_parcelle = st.selectbox(
        "Parcelle",
        options=[
            "Toutes les parcelles"
        ]
        + [
            f"{parcelle.nom} (ID {parcelle.id})"
            for parcelle in parcelles
        ],
        key="analytics_parcelle_filter",
    )


with filter_col2:

    selected_culture = st.selectbox(
        "Culture",
        options=[
            "Toutes les cultures"
        ]
        + [
            f"{culture.nom} (ID {culture.id})"
            for culture in cultures
        ],
        key="analytics_culture_filter",
    )


with filter_col3:

    selected_period = st.selectbox(
        "Période",
        options=[
            "Toutes les données",
            "Cette année",
            "Cette année — données récentes",
        ],
        key="analytics_period_filter",
    )


# ============================================================
# IDS DES FILTRES
# ============================================================

selected_parcelle_id = None

if selected_parcelle != "Toutes les parcelles":

    selected_parcelle_id = next(
        (
            parcelle.id
            for parcelle in parcelles
            if f"{parcelle.nom} (ID {parcelle.id})"
            == selected_parcelle
        ),
        None,
    )


selected_culture_id = None

if selected_culture != "Toutes les cultures":

    selected_culture_id = next(
        (
            culture.id
            for culture in cultures
            if f"{culture.nom} (ID {culture.id})"
            == selected_culture
        ),
        None,
    )


# ============================================================
# FILTRAGE DES CULTURES
# ============================================================

filtered_cultures = cultures

if selected_parcelle_id is not None:

    filtered_cultures = [
        culture
        for culture in filtered_cultures
        if culture.parcelle_id
        == selected_parcelle_id
    ]

if selected_culture_id is not None:

    filtered_cultures = [
        culture
        for culture in filtered_cultures
        if culture.id
        == selected_culture_id
    ]


# ============================================================
# FILTRAGE DES TRAVAUX
# ============================================================

filtered_travaux = travaux

if selected_parcelle_id is not None:

    filtered_travaux = [
        travail
        for travail in filtered_travaux
        if travail.parcelle_id
        == selected_parcelle_id
    ]

if selected_culture_id is not None:

    filtered_travaux = [
        travail
        for travail in filtered_travaux
        if travail.culture_id
        == selected_culture_id
    ]


# ============================================================
# FILTRAGE DES DÉPENSES
# ============================================================

filtered_depenses = depenses

if selected_parcelle_id is not None:

    filtered_depenses = [
        depense
        for depense in filtered_depenses
        if depense.parcelle_id
        == selected_parcelle_id
    ]

if selected_culture_id is not None:

    filtered_depenses = [
        depense
        for depense in filtered_depenses
        if depense.culture_id
        == selected_culture_id
    ]


# ============================================================
# FILTRAGE DES REVENUS
# ============================================================

filtered_revenus = revenus

if selected_parcelle_id is not None:

    filtered_revenus = [
        revenu
        for revenu in filtered_revenus
        if revenu.parcelle_id
        == selected_parcelle_id
    ]

if selected_culture_id is not None:

    filtered_revenus = [
        revenu
        for revenu in filtered_revenus
        if revenu.culture_id
        == selected_culture_id
    ]


# ============================================================
# FILTRAGE DES RÉCOLTES
# ============================================================

filtered_recoltes = recoltes

if selected_culture_id is not None:

    filtered_recoltes = [
        recolte
        for recolte in filtered_recoltes
        if recolte.culture_id
        == selected_culture_id
    ]

elif selected_parcelle_id is not None:

    filtered_recoltes = [
        recolte
        for recolte in filtered_recoltes
        if culture_parcelle_ids.get(
            recolte.culture_id
        )
        == selected_parcelle_id
    ]


# ============================================================
# CALCULS FILTRÉS
# ============================================================

filtered_ca = sum(
    float(revenu.montant)
    for revenu in filtered_revenus
)

filtered_expenses = sum(
    float(depense.montant)
    for depense in filtered_depenses
)

filtered_margin = (
    filtered_ca
    - filtered_expenses
)

filtered_profitability = (
    (
        filtered_margin
        / filtered_expenses
    )
    * 100
    if filtered_expenses > 0
    else 0.0
)

filtered_production = sum(
    float(recolte.quantite)
    for recolte in filtered_recoltes
)


# ============================================================
# KPI PRINCIPAUX
# ============================================================

st.subheader("📌 Indicateurs principaux")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Chiffre d'affaires",
        f"{filtered_ca:,.0f} Ar",
    )


with col2:

    st.metric(
        "💸 Dépenses",
        f"{filtered_expenses:,.0f} Ar",
    )


with col3:

    st.metric(
        "📈 Marge",
        f"{filtered_margin:,.0f} Ar",
    )


with col4:

    st.metric(
        "📊 Rentabilité",
        f"{filtered_profitability:.2f} %",
    )


st.divider()


# ============================================================
# KPI AGRICOLES
# ============================================================

st.subheader("🌱 Indicateurs agricoles")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌾 Parcelles",
        total_parcelles,
    )


with col2:

    st.metric(
        "🌱 Cultures",
        len(filtered_cultures),
    )


with col3:

    st.metric(
        "🚜 Travaux",
        len(filtered_travaux),
    )


with col4:

    st.metric(
        "📦 Récoltes",
        len(filtered_recoltes),
    )


st.info(
    f"""
    **Production correspondant aux filtres :**
    **{filtered_production:,.2f}**

    L'unité dépend des unités utilisées dans les récoltes
    enregistrées.
    """
)


# ============================================================
# TABS ANALYTICS
# ============================================================

tab_finance, tab_production, tab_parcelles, tab_details = st.tabs(
    [
        "💰 Finance",
        "🌾 Production",
        "🗺️ Parcelles & Cultures",
        "📋 Données détaillées",
    ]
)


# ============================================================
# TAB FINANCE
# ============================================================

with tab_finance:

    st.subheader("💰 Analyse financière")

    financial_col1, financial_col2 = st.columns(2)


    # --------------------------------------------------------
    # DÉPENSES PAR CATÉGORIE
    # --------------------------------------------------------

    with financial_col1:

        st.markdown(
            "### 💸 Dépenses par catégorie"
        )

        if filtered_depenses:

            expense_rows = []

            for depense in filtered_depenses:

                expense_rows.append(
                    {
                        "Catégorie": depense.categorie,
                        "Montant": float(
                            depense.montant
                        ),
                    }
                )

            expense_df = pd.DataFrame(
                expense_rows
            )

            expense_grouped = (
                expense_df
                .groupby(
                    "Catégorie",
                    as_index=False,
                )["Montant"]
                .sum()
                .sort_values(
                    "Montant",
                    ascending=False,
                )
            )

            st.dataframe(
                expense_grouped,
                use_container_width=True,
                hide_index=True,
            )

            st.bar_chart(
                expense_grouped.set_index(
                    "Catégorie"
                )
            )

        else:

            st.info(
                "Aucune dépense disponible."
            )


    # --------------------------------------------------------
    # REVENUS PAR PRODUIT
    # --------------------------------------------------------

    with financial_col2:

        st.markdown(
            "### 💵 Revenus par produit"
        )

        if filtered_revenus:

            revenue_rows = []

            for revenu in filtered_revenus:

                revenue_rows.append(
                    {
                        "Produit": revenu.produit,
                        "Montant": float(
                            revenu.montant
                        ),
                    }
                )

            revenue_df = pd.DataFrame(
                revenue_rows
            )

            revenue_grouped = (
                revenue_df
                .groupby(
                    "Produit",
                    as_index=False,
                )["Montant"]
                .sum()
                .sort_values(
                    "Montant",
                    ascending=False,
                )
            )

            st.dataframe(
                revenue_grouped,
                use_container_width=True,
                hide_index=True,
            )

            st.bar_chart(
                revenue_grouped.set_index(
                    "Produit"
                )
            )

        else:

            st.info(
                "Aucun revenu disponible."
            )


    st.divider()


    # --------------------------------------------------------
    # SYNTHÈSE FINANCIÈRE
    # --------------------------------------------------------

    st.markdown(
        "### 📊 Synthèse financière"
    )

    financial_summary = pd.DataFrame(
        {
            "Indicateur": [
                "Chiffre d'affaires",
                "Dépenses",
                "Marge",
                "Rentabilité",
                "Coût total des travaux",
            ],
            "Valeur": [
                f"{filtered_ca:,.0f} Ar",
                f"{filtered_expenses:,.0f} Ar",
                f"{filtered_margin:,.0f} Ar",
                f"{filtered_profitability:.2f} %",
                f"{sum(float(t.cout) for t in filtered_travaux):,.0f} Ar",
            ],
        }
    )

    st.dataframe(
        financial_summary,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TAB PRODUCTION
# ============================================================

with tab_production:

    st.subheader("🌾 Analyse de la production")

    production_col1, production_col2 = st.columns(2)


    # --------------------------------------------------------
    # RÉCOLTES PAR CULTURE
    # --------------------------------------------------------

    with production_col1:

        st.markdown(
            "### 🌱 Production par culture"
        )

        if filtered_recoltes:

            production_rows = []

            for recolte in filtered_recoltes:

                production_rows.append(
                    {
                        "Culture": culture_names.get(
                            recolte.culture_id,
                            f"ID {recolte.culture_id}",
                        ),
                        "Quantité": float(
                            recolte.quantite
                        ),
                        "Unité": recolte.unite,
                    }
                )

            production_df = pd.DataFrame(
                production_rows
            )

            st.dataframe(
                production_df,
                use_container_width=True,
                hide_index=True,
            )

            # Graphique uniquement si les unités
            # sont homogènes.
            units = (
                production_df["Unité"]
                .dropna()
                .unique()
                .tolist()
            )

            if len(units) == 1:

                grouped_production = (
                    production_df
                    .groupby(
                        "Culture",
                        as_index=True,
                    )["Quantité"]
                    .sum()
                )

                st.bar_chart(
                    grouped_production
                )

            else:

                st.warning(
                    "Les unités de récolte sont différentes. "
                    "Le graphique global n'est donc pas affiché."
                )

        else:

            st.info(
                "Aucune récolte disponible."
            )


    # --------------------------------------------------------
    # RÉCOLTES PAR UNITÉ
    # --------------------------------------------------------

    with production_col2:

        st.markdown(
            "### 📦 Production par unité"
        )

        if filtered_recoltes:

            unit_rows = []

            for recolte in filtered_recoltes:

                unit_rows.append(
                    {
                        "Unité": recolte.unite,
                        "Quantité": float(
                            recolte.quantite
                        ),
                    }
                )

            unit_df = pd.DataFrame(
                unit_rows
            )

            unit_grouped = (
                unit_df
                .groupby(
                    "Unité",
                    as_index=False,
                )["Quantité"]
                .sum()
            )

            st.dataframe(
                unit_grouped,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "Aucune donnée de production."
            )


# ============================================================
# TAB PARCELLES ET CULTURES
# ============================================================

with tab_parcelles:

    st.subheader(
        "🗺️ Analyse des parcelles et cultures"
    )

    # --------------------------------------------------------
    # PARCELLES
    # --------------------------------------------------------

    parcel_rows = []

    for parcelle in parcelles:

        parcel_rows.append(
            {
                "ID": parcelle.id,
                "Parcelle": parcelle.nom,
                "Superficie": float(
                    parcelle.superficie
                ),
                "Unité": parcelle.unite_superficie,
                "Localisation": (
                    parcelle.localisation
                    or ""
                ),
            }
        )

    if parcel_rows:

        parcels_df = pd.DataFrame(
            parcel_rows
        )

        st.dataframe(
            parcels_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Aucune parcelle disponible."
        )


    st.divider()


    # --------------------------------------------------------
    # CULTURES
    # --------------------------------------------------------

    st.markdown(
        "### 🌱 Cultures"
    )

    culture_rows = []

    for culture in filtered_cultures:

        culture_rows.append(
            {
                "ID": culture.id,
                "Culture": culture.nom,
                "Variété": culture.variete or "",
                "Parcelle": parcelle_names.get(
                    culture.parcelle_id,
                    f"ID {culture.parcelle_id}",
                ),
                "Date semis": culture.date_semis or "",
                "Récolte prévue": (
                    culture.date_prevue_recolte
                    or ""
                ),
                "Statut": culture.statut,
            }
        )

    if culture_rows:

        cultures_df = pd.DataFrame(
            culture_rows
        )

        st.dataframe(
            cultures_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Aucune culture correspondant aux filtres."
        )


# ============================================================
# TAB DONNÉES DÉTAILLÉES
# ============================================================

with tab_details:

    st.subheader(
        "📋 Données détaillées"
    )

    detail_type = st.selectbox(
        "Type de données",
        [
            "Dépenses",
            "Revenus",
            "Récoltes",
            "Travaux",
        ],
        key="analytics_detail_type",
    )


    # --------------------------------------------------------
    # DÉPENSES
    # --------------------------------------------------------

    if detail_type == "Dépenses":

        if filtered_depenses:

            rows = []

            for depense in filtered_depenses:

                rows.append(
                    {
                        "ID": depense.id,
                        "Catégorie": depense.categorie,
                        "Montant": float(
                            depense.montant
                        ),
                        "Date": depense.date_depense,
                        "Parcelle": (
                            parcelle_names.get(
                                depense.parcelle_id,
                                f"ID {depense.parcelle_id}",
                            )
                            if depense.parcelle_id
                            is not None
                            else "—"
                        ),
                        "Culture": (
                            culture_names.get(
                                depense.culture_id,
                                f"ID {depense.culture_id}",
                            )
                            if depense.culture_id
                            is not None
                            else "—"
                        ),
                    }
                )

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "Aucune dépense."
            )


    # --------------------------------------------------------
    # REVENUS
    # --------------------------------------------------------

    elif detail_type == "Revenus":

        if filtered_revenus:

            rows = []

            for revenu in filtered_revenus:

                rows.append(
                    {
                        "ID": revenu.id,
                        "Produit": revenu.produit,
                        "Quantité": float(
                            revenu.quantite
                        ),
                        "Prix unitaire": float(
                            revenu.prix_unitaire
                        ),
                        "Montant": float(
                            revenu.montant
                        ),
                        "Date": revenu.date_revenu,
                        "Parcelle": (
                            parcelle_names.get(
                                revenu.parcelle_id,
                                f"ID {revenu.parcelle_id}",
                            )
                            if revenu.parcelle_id
                            is not None
                            else "—"
                        ),
                        "Culture": (
                            culture_names.get(
                                revenu.culture_id,
                                f"ID {revenu.culture_id}",
                            )
                            if revenu.culture_id
                            is not None
                            else "—"
                        ),
                    }
                )

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "Aucun revenu."
            )


    # --------------------------------------------------------
    # RÉCOLTES
    # --------------------------------------------------------

    elif detail_type == "Récoltes":

        if filtered_recoltes:

            rows = []

            for recolte in filtered_recoltes:

                rows.append(
                    {
                        "ID": recolte.id,
                        "Culture": culture_names.get(
                            recolte.culture_id,
                            f"ID {recolte.culture_id}",
                        ),
                        "Date": recolte.date_recolte,
                        "Quantité": float(
                            recolte.quantite
                        ),
                        "Unité": recolte.unite,
                        "Qualité": (
                            recolte.qualite
                            or ""
                        ),
                    }
                )

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "Aucune récolte."
            )


    # --------------------------------------------------------
    # TRAVAUX
    # --------------------------------------------------------

    else:

        if filtered_travaux:

            rows = []

            for travail in filtered_travaux:

                rows.append(
                    {
                        "ID": travail.id,
                        "Type": travail.type_travail,
                        "Date": travail.date_travail,
                        "Coût": float(
                            travail.cout
                        ),
                        "Parcelle": parcelle_names.get(
                            travail.parcelle_id,
                            f"ID {travail.parcelle_id}",
                        ),
                        "Culture": (
                            culture_names.get(
                                travail.culture_id,
                                f"ID {travail.culture_id}",
                            )
                            if travail.culture_id
                            is not None
                            else "—"
                        ),
                    }
                )

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "Aucun travail."
            )


# ============================================================
# EXPLICATION
# ============================================================

st.divider()

with st.expander(
    "📚 Comprendre les indicateurs"
):

    st.markdown(
        """
        ### 💰 Chiffre d'affaires

        Le chiffre d'affaires correspond à la somme des revenus :

        $$
        CA =
        \\sum_{i=1}^{n} Revenus_i
        $$

        ---

        ### 💸 Dépenses

        Les dépenses correspondent aux sorties d'argent
        enregistrées dans VolyTrack :

        $$
        Dépenses =
        \\sum_{i=1}^{n} Dépense_i
        $$

        ---

        ### 📈 Marge

        La marge simplifiée est calculée par :

        $$
        Marge =
        Revenus - Dépenses
        $$

        ---

        ### 📊 Rentabilité

        La rentabilité est calculée ici par :

        $$
        Rentabilité =
        \\frac{Marge}{Dépenses}
        \\times 100
        $$

        ---

        ### 🌾 Rendement

        Lorsque les unités de production et de superficie
        sont compatibles :

        $$
        Rendement =
        \\frac{Production}{Superficie}
        $$

        Le rendement devra être interprété avec attention
        lorsque plusieurs unités de mesure sont utilisées.

        ---

        ### ⚠️ Attention aux unités

        Les récoltes peuvent être exprimées en :

        - kg ;
        - tonnes ;
        - sacs ;
        - litres ;
        - autres unités.

        Il n'est donc pas correct d'additionner directement
        des quantités exprimées dans des unités différentes.

        Analytics évite donc de présenter une production globale
        lorsque les unités ne sont pas homogènes.
        """
    )

