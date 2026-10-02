
"""
VolyTrack — Gestion des Récoltes
================================

Interface Streamlit pour gérer les récoltes agricoles.

Fonctionnalités :
    - affichage des récoltes ;
    - recherche ;
    - filtrage par culture ;
    - création ;
    - modification ;
    - suppression ;
    - calcul des quantités récoltées ;
    - association avec une culture ;
    - association indirecte avec une parcelle.
"""

import streamlit as st
import pandas as pd

from core.models.recolte import Recolte

from core.services.recolte_service import RecolteService
from core.services.culture_service import CultureService
from core.services.parcelle_service import ParcelleService


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VolyTrack — Récoltes",
    page_icon="🌾",
    layout="wide",
)


# ============================================================
# SERVICES
# ============================================================

recolte_service = RecolteService()
culture_service = CultureService()
parcelle_service = ParcelleService()


# ============================================================
# HEADER
# ============================================================

st.title("🌾 VolyTrack — Récoltes")

st.markdown(
    """
    Gérez les **récoltes agricoles** de votre exploitation.

    Vous pouvez enregistrer :

    - la culture récoltée ;
    - la date de récolte ;
    - la quantité produite ;
    - l'unité de mesure ;
    - la qualité ;
    - une description.
    """
)

st.divider()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

try:

    recoltes = recolte_service.get_all_recoltes()
    cultures = culture_service.get_all_cultures()
    parcelles = parcelle_service.get_all_parcelles()

except Exception as exc:

    st.error(
        f"❌ Impossible de charger les données : {exc}"
    )

    st.stop()


# ============================================================
# DICTIONNAIRES DE CORRESPONDANCE
# ============================================================

culture_names = {
    culture.id: culture.nom
    for culture in cultures
}

culture_parcelle_ids = {
    culture.id: culture.parcelle_id
    for culture in cultures
}

parcelle_names = {
    parcelle.id: parcelle.nom
    for parcelle in parcelles
}


# ============================================================
# MÉTRIQUES
# ============================================================

total_recoltes = len(recoltes)

quantite_totale = sum(
    float(recolte.quantite)
    for recolte in recoltes
)

recoltes_avec_qualite = sum(
    1
    for recolte in recoltes
    if recolte.qualite
)

cultures_recoltees = len(
    set(
        recolte.culture_id
        for recolte in recoltes
    )
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌾 Nombre de récoltes",
        total_recoltes,
    )


with col2:

    st.metric(
        "📦 Quantité totale",
        f"{quantite_totale:,.2f}",
    )


with col3:

    st.metric(
        "🌱 Cultures récoltées",
        cultures_recoltees,
    )


with col4:

    st.metric(
        "⭐ Avec qualité",
        recoltes_avec_qualite,
    )


st.divider()


# ============================================================
# RECHERCHE ET FILTRAGE
# ============================================================

st.subheader("🔎 Rechercher et filtrer")


filter_col1, filter_col2 = st.columns(2)


with filter_col1:

    search_query = st.text_input(
        "Recherche",
        placeholder="Ex. riz, maïs, bonne qualité...",
        key="recoltes_search",
    )


with filter_col2:

    culture_filter_options = {
        "Toutes les cultures": None
    }

    for culture in cultures:

        culture_filter_options[
            f"{culture.nom} (ID {culture.id})"
        ] = culture.id

    selected_culture_filter = st.selectbox(
        "Culture",
        options=list(
            culture_filter_options.keys()
        ),
        key="recoltes_culture_filter",
    )


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

filtered_recoltes = recoltes


if search_query.strip():

    try:

        filtered_recoltes = (
            recolte_service.search_recoltes(
                search_query.strip()
            )
        )

    except Exception as exc:

        st.error(
            f"❌ Erreur pendant la recherche : {exc}"
        )

        filtered_recoltes = []


selected_culture_id = (
    culture_filter_options[
        selected_culture_filter
    ]
)


if selected_culture_id is not None:

    filtered_recoltes = [
        recolte
        for recolte in filtered_recoltes
        if recolte.culture_id == selected_culture_id
    ]


# ============================================================
# AJOUT D'UNE RÉCOLTE
# ============================================================

st.divider()

st.subheader("➕ Ajouter une récolte")


if not cultures:

    st.warning(
        """
        ⚠️ Aucune culture n'est actuellement disponible.

        Créez d'abord une culture dans
        **03_Cultures.py** avant d'enregistrer une récolte.
        """
    )

else:

    with st.form(
        "create_recolte_form",
        clear_on_submit=True,
    ):

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # CULTURE + INFORMATIONS PRINCIPALES
        # ----------------------------------------------------

        with col1:

            create_culture_options = {}

            for culture in cultures:

                parcelle_name = parcelle_names.get(
                    culture.parcelle_id,
                    f"ID {culture.parcelle_id}",
                )

                create_culture_options[
                    (
                        f"{culture.nom} — "
                        f"{parcelle_name} "
                        f"(ID {culture.id})"
                    )
                ] = culture.id

            selected_create_culture = st.selectbox(
                "Culture *",
                options=list(
                    create_culture_options.keys()
                ),
                key="recolte_create_culture",
            )

            date_recolte = st.date_input(
                "Date de récolte *",
                key="recolte_create_date",
            )

            quantite = st.number_input(
                "Quantité *",
                min_value=0.01,
                value=1.0,
                step=0.1,
                key="recolte_create_quantite",
            )

        # ----------------------------------------------------
        # UNITÉ + QUALITÉ + DESCRIPTION
        # ----------------------------------------------------

        with col2:

            unite = st.text_input(
                "Unité *",
                value="kg",
                placeholder="kg, tonne, sac, litre...",
                key="recolte_create_unite",
            )

            qualite = st.text_input(
                "Qualité",
                placeholder=(
                    "Ex. Excellente, bonne, moyenne..."
                ),
                key="recolte_create_qualite",
            )

            description = st.text_area(
                "Description",
                placeholder=(
                    "Informations complémentaires..."
                ),
                key="recolte_create_description",
            )

        # ----------------------------------------------------
        # BOUTON D'ENREGISTREMENT
        # ----------------------------------------------------

        submitted = st.form_submit_button(
            "💾 Enregistrer la récolte",
            type="primary",
            use_container_width=True,
        )

        # ----------------------------------------------------
        # CRÉATION
        # ----------------------------------------------------

        if submitted:

            try:

                # --------------------------------------------
                # RÉCUPÉRATION DE LA CULTURE
                # --------------------------------------------

                culture_id = (
                    create_culture_options[
                        selected_create_culture
                    ]
                )

                # --------------------------------------------
                # VALIDATIONS
                # --------------------------------------------

                if quantite <= 0:

                    raise ValueError(
                        "La quantité doit être supérieure à zéro."
                    )

                if not unite.strip():

                    raise ValueError(
                        "L'unité ne doit pas être vide."
                    )

                # --------------------------------------------
                # CRÉATION DU MODÈLE RECOLTE
                # --------------------------------------------

                recolte = Recolte(
                    culture_id=culture_id,
                    date_recolte=date_recolte.isoformat(),
                    quantite=float(quantite),
                    unite=unite.strip(),
                    qualite=(
                        qualite.strip()
                        if qualite
                        else None
                    ),
                    description=(
                        description.strip()
                        if description
                        else None
                    ),
                )

                # --------------------------------------------
                # APPEL DU SERVICE
                # --------------------------------------------

                recolte = (
                    recolte_service.create_recolte(
                        recolte
                    )
                )

                st.success(
                    "✅ Récolte enregistrée avec succès."
                )

                st.rerun()

            except (ValueError, TypeError) as exc:

                st.error(
                    f"❌ {exc}"
                )

            except Exception as exc:

                st.error(
                    f"❌ Une erreur est survenue : {exc}"
                )



# ============================================================
# LISTE DES RÉCOLTES
# ============================================================

st.divider()

st.subheader("📋 Liste des récoltes")


if not filtered_recoltes:

    st.info(
        "Aucune récolte ne correspond aux critères."
    )

else:

    table_rows = []


    for recolte in filtered_recoltes:

        culture_name = culture_names.get(
            recolte.culture_id,
            f"ID {recolte.culture_id}",
        )

        parcelle_id = culture_parcelle_ids.get(
            recolte.culture_id
        )

        parcelle_name = (
            parcelle_names.get(
                parcelle_id,
                f"ID {parcelle_id}",
            )
            if parcelle_id is not None
            else "—"
        )


        table_rows.append(
            {
                "ID": recolte.id,
                "Culture": culture_name,
                "Parcelle": parcelle_name,
                "Date": recolte.date_recolte,
                "Quantité": float(recolte.quantite),
                "Unité": recolte.unite,
                "Qualité": recolte.qualite or "",
                "Description": recolte.description or "",
            }
        )


    recoltes_df = pd.DataFrame(
        table_rows
    )


    st.dataframe(
        recoltes_df,
        use_container_width=True,
        hide_index=True,
    )


    filtered_quantity = sum(
        float(recolte.quantite)
        for recolte in filtered_recoltes
    )


    st.info(
        f"📦 Quantité correspondant aux filtres : "
        f"**{filtered_quantity:,.2f}**"
    )


# ============================================================
# MODIFICATION
# ============================================================

st.divider()

st.subheader("✏️ Modifier une récolte")


if not recoltes:

    st.info(
        "Aucune récolte disponible pour la modification."
    )

else:

    update_options = {

        (
            f"#{recolte.id} — "
            f"{culture_names.get(recolte.culture_id, 'ID ' + str(recolte.culture_id))} — "
            f"{recolte.quantite:,.2f} "
            f"{recolte.unite} — "
            f"{recolte.date_recolte}"
        ):
        recolte.id

        for recolte in recoltes
    }


    selected_update_label = st.selectbox(
        "Sélectionner une récolte",
        options=list(
            update_options.keys()
        ),
        key="recolte_update_selection",
    )


    selected_update_id = update_options[
        selected_update_label
    ]


    selected_recolte = next(
        (
            recolte
            for recolte in recoltes
            if recolte.id == selected_update_id
        ),
        None,
    )


    if selected_recolte is not None:

        with st.form(
            "update_recolte_form"
        ):

            col1, col2 = st.columns(2)


            with col1:

                update_culture_options = {}

                for culture in cultures:

                    parcelle_name = parcelle_names.get(
                        culture.parcelle_id,
                        f"ID {culture.parcelle_id}",
                    )

                    update_culture_options[
                        (
                            f"{culture.nom} — "
                            f"{parcelle_name} "
                            f"(ID {culture.id})"
                        )
                    ] = culture.id


                current_culture_label = next(
                    (
                        label
                        for label, value
                        in update_culture_options.items()
                        if value
                        == selected_recolte.culture_id
                    ),
                    None,
                )


                if current_culture_label is None:

                    current_culture_label = (
                        list(
                            update_culture_options.keys()
                        )[0]
                    )


                update_culture_label = st.selectbox(
                    "Culture *",
                    options=list(
                        update_culture_options.keys()
                    ),
                    index=list(
                        update_culture_options.keys()
                    ).index(
                        current_culture_label
                    ),
                    key="recolte_update_culture",
                )


                try:

                    current_date = pd.to_datetime(
                        selected_recolte.date_recolte
                    ).date()

                except Exception:

                    current_date = (
                        pd.Timestamp.today().date()
                    )


                update_date = st.date_input(
                    "Date de récolte *",
                    value=current_date,
                    key="recolte_update_date",
                )


                update_quantite = st.number_input(
                    "Quantité *",
                    min_value=0.01,
                    value=float(
                        selected_recolte.quantite
                    ),
                    step=0.1,
                    key="recolte_update_quantite",
                )


            with col2:

                update_unite = st.text_input(
                    "Unité *",
                    value=selected_recolte.unite,
                    key="recolte_update_unite",
                )


                update_qualite = st.text_input(
                    "Qualité",
                    value=selected_recolte.qualite or "",
                    key="recolte_update_qualite",
                )


                update_description = st.text_area(
                    "Description",
                    value=(
                        selected_recolte.description
                        or ""
                    ),
                    key="recolte_update_description",
                )


            update_submitted = st.form_submit_button(
                "💾 Enregistrer les modifications",
                type="primary",
                use_container_width=True,
            )


            if update_submitted:

                try:

                    if update_quantite <= 0:

                        raise ValueError(
                            "La quantité doit être supérieure à zéro."
                        )


                    if not update_unite.strip():

                        raise ValueError(
                            "L'unité ne doit pas être vide."
                        )


                    selected_recolte.culture_id = (
                        update_culture_options[
                            update_culture_label
                        ]
                    )


                    selected_recolte.date_recolte = (
                        update_date.isoformat()
                    )


                    selected_recolte.quantite = float(
                        update_quantite
                    )


                    selected_recolte.unite = (
                        update_unite.strip()
                    )


                    selected_recolte.qualite = (
                        update_qualite.strip()
                        or None
                    )


                    selected_recolte.description = (
                        update_description.strip()
                        or None
                    )


                    recolte_service.update_recolte(
                        selected_recolte
                    )


                    st.success(
                        "✅ Récolte modifiée avec succès."
                    )

                    st.rerun()


                except (ValueError, TypeError) as exc:

                    st.error(
                        f"❌ {exc}"
                    )


                except Exception as exc:

                    st.error(
                        f"❌ Une erreur est survenue : {exc}"
                    )


# ============================================================
# SUPPRESSION
# ============================================================

st.divider()

st.subheader("🗑️ Supprimer une récolte")


if not recoltes:

    st.info(
        "Aucune récolte disponible pour la suppression."
    )

else:

    delete_options = {

        (
            f"#{recolte.id} — "
            f"{culture_names.get(recolte.culture_id, 'ID ' + str(recolte.culture_id))} — "
            f"{recolte.quantite:,.2f} "
            f"{recolte.unite}"
        ):
        recolte.id

        for recolte in recoltes
    }


    delete_label = st.selectbox(
        "Sélectionner la récolte à supprimer",
        options=list(
            delete_options.keys()
        ),
        key="recolte_delete_selection",
    )


    delete_id = delete_options[
        delete_label
    ]


    confirm_delete = st.checkbox(
        "Je confirme vouloir supprimer cette récolte.",
        key="recolte_delete_confirmation",
    )


    if st.button(
        "🗑️ Supprimer",
        type="secondary",
        disabled=not confirm_delete,
        key="recolte_delete_button",
    ):

        try:

            recolte_service.delete_recolte(
                delete_id
            )


            st.success(
                "✅ Récolte supprimée avec succès."
            )

            st.rerun()


        except (ValueError, TypeError) as exc:

            st.error(
                f"❌ {exc}"
            )


        except Exception as exc:

            st.error(
                f"❌ Une erreur est survenue : {exc}"
            )


# ============================================================
# EXPLICATION
# ============================================================

st.divider()

with st.expander(
    "📚 Comprendre la gestion des récoltes"
):

    st.markdown(
        """
        ### 🌾 Récolte agricole

        Une récolte représente la production obtenue
        après la culture d'une parcelle.

        Une récolte est associée à une **culture**.

        La culture permet ensuite de retrouver
        la **parcelle** concernée.

        ### 📦 Quantité récoltée

        La quantité permet de mesurer la production.

        Exemples :

        - 500 kg de riz ;
        - 20 sacs de maïs ;
        - 100 kg de tomates ;
        - 50 litres de miel.

        ### 📊 Rendement

        Le rendement pourra ensuite être calculé
        dans le module **Dashboard / Analytics**.

        La formule générale est :

        $$
        Rendement =
        \\frac{Production}{Superficie}
        $$

        Par exemple, si une parcelle de 2 hectares
        produit 4 000 kg :

        $$
        Rendement =
        \\frac{4000}{2}
        =
        2000\\ kg/ha
        $$

        Les données des récoltes seront utilisées
        ultérieurement pour analyser :

        - la production ;
        - le rendement ;
        - les performances des cultures ;
        - les revenus par culture ;
        - la rentabilité de l'exploitation.
        """
    )

