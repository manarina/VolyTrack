
"""
VolyTrack — Gestion des Cultures
================================

Interface Streamlit permettant de :

- consulter les cultures ;
- rechercher une culture ;
- créer une culture ;
- modifier une culture ;
- supprimer une culture ;
- associer une culture à une parcelle ;
- gérer le statut et les dates de culture.

La logique métier est déléguée à CultureService.
"""

import streamlit as st
import pandas as pd

from core.services.culture_service import CultureService
from core.services.parcelle_service import ParcelleService


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cultures — VolyTrack",
    page_icon="🌱",
    layout="wide",
)


# ============================================================
# SERVICES
# ============================================================

culture_service = CultureService()
parcelle_service = ParcelleService()


# ============================================================
# TITRE
# ============================================================

st.title("🌱 Gestion des Cultures")

st.markdown(
    """
    Gérez les cultures de votre exploitation agricole.

    Vous pouvez créer, consulter, rechercher, modifier
    et supprimer les cultures enregistrées dans VolyTrack.
    """
)

st.divider()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

try:

    cultures = (
        culture_service.get_all_cultures()
    )

except Exception as exc:

    st.error(
        f"❌ Impossible de charger les cultures : {exc}"
    )

    cultures = []


try:

    parcelles = (
        parcelle_service.get_all_parcelles()
    )

except Exception as exc:

    st.error(
        f"❌ Impossible de charger les parcelles : {exc}"
    )

    parcelles = []


# ============================================================
# INDICATEURS
# ============================================================

total_cultures = len(cultures)

total_parcelles = len(parcelles)

statuts = [
    culture.statut
    for culture in cultures
    if culture.statut
]

cultures_planifiees = sum(
    1
    for culture in cultures
    if culture.statut == "Planifiée"
)

cultures_en_cours = sum(
    1
    for culture in cultures
    if culture.statut == "En cours"
)

cultures_terminees = sum(
    1
    for culture in cultures
    if culture.statut == "Terminée"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌱 Cultures",
        total_cultures,
    )


with col2:

    st.metric(
        "🌾 Parcelles",
        total_parcelles,
    )


with col3:

    st.metric(
        "🚜 En cours",
        cultures_en_cours,
    )


with col4:

    st.metric(
        "✅ Terminées",
        cultures_terminees,
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Rechercher une culture")

search_query = st.text_input(
    "Nom, variété, statut ou description",
    placeholder="Ex. Riz, Makalioka, En cours...",
    key="cultures_search",
)


# ============================================================
# AJOUT D'UNE CULTURE
# ============================================================

with st.expander(
    "➕ Ajouter une nouvelle culture",
    expanded=False,
):

    if not parcelles:

        st.warning(
            """
            ⚠️ Aucune parcelle n'est disponible.

            Créez d'abord une parcelle dans
            **🌾 Parcelles** avant d'ajouter une culture.
            """
        )

    else:

        with st.form(
            "create_culture_form",
            clear_on_submit=True,
        ):

            st.markdown(
                "### 🌱 Nouvelle culture"
            )

            # ------------------------------------------------
            # PARCELLE
            # ------------------------------------------------

            parcelle_options = {
                f"{parcelle.id} — {parcelle.nom}": parcelle.id
                for parcelle in parcelles
            }

            selected_parcelle_label = st.selectbox(
                "Parcelle *",
                options=list(
                    parcelle_options.keys()
                ),
            )

            selected_parcelle_id = (
                parcelle_options[
                    selected_parcelle_label
                ]
            )

            # ------------------------------------------------
            # INFORMATIONS
            # ------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                nom = st.text_input(
                    "Nom de la culture *",
                    placeholder="Ex. Riz",
                )

            with col2:

                variete = st.text_input(
                    "Variété",
                    placeholder="Ex. Makalioka",
                )

            # ------------------------------------------------
            # DATES
            # ------------------------------------------------

            col3, col4 = st.columns(2)

            with col3:

                date_semis = st.date_input(
                    "Date de semis",
                    value=None,
                )

            with col4:

                date_prevue_recolte = st.date_input(
                    "Date prévue de récolte",
                    value=None,
                )

            # ------------------------------------------------
            # STATUT
            # ------------------------------------------------

            statut = st.selectbox(
                "Statut",
                [
                    "Planifiée",
                    "En cours",
                    "Terminée",
                ],
            )

            # ------------------------------------------------
            # DESCRIPTION
            # ------------------------------------------------

            description = st.text_area(
                "Description",
                placeholder=(
                    "Informations complémentaires "
                    "sur la culture..."
                ),
            )

            submitted = st.form_submit_button(
                "💾 Enregistrer la culture",
                type="primary",
                use_container_width=True,
            )

            if submitted:

                try:

                    culture = (
                        culture_service.create_culture(
                            parcelle_id=selected_parcelle_id,
                            nom=nom,
                            variete=variete or None,
                            date_semis=(
                                date_semis.isoformat()
                                if date_semis
                                else None
                            ),
                            date_prevue_recolte=(
                                date_prevue_recolte.isoformat()
                                if date_prevue_recolte
                                else None
                            ),
                            statut=statut,
                            description=(
                                description
                                or None
                            ),
                        )
                    )

                    st.success(
                        f"✅ Culture « {culture.nom} » "
                        "créée avec succès."
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


st.divider()


# ============================================================
# LISTE DES CULTURES
# ============================================================

st.subheader("📋 Liste des cultures")


# ------------------------------------------------------------
# FILTRAGE
# ------------------------------------------------------------

if search_query.strip():

    try:

        filtered_cultures = (
            culture_service.search_cultures(
                search_query
            )
        )

    except (ValueError, TypeError) as exc:

        st.error(
            f"❌ Erreur de recherche : {exc}"
        )

        filtered_cultures = []

else:

    filtered_cultures = cultures


# ------------------------------------------------------------
# AFFICHAGE
# ------------------------------------------------------------

if not filtered_cultures:

    if search_query.strip():

        st.info(
            "🔎 Aucune culture ne correspond "
            "à votre recherche."
        )

    else:

        st.info(
            "🌱 Aucune culture enregistrée pour le moment."
        )

else:

    table_rows = []

    # Dictionnaire permettant de retrouver le nom
    # d'une parcelle à partir de son identifiant.

    parcelle_names = {
        parcelle.id: parcelle.nom
        for parcelle in parcelles
    }

    for culture in filtered_cultures:

        table_rows.append(
            {
                "ID": culture.id,
                "Nom": culture.nom,
                "Variété": (
                    culture.variete
                    or ""
                ),
                "Parcelle": (
                    parcelle_names.get(
                        culture.parcelle_id,
                        f"ID {culture.parcelle_id}",
                    )
                ),
                "Date semis": (
                    culture.date_semis
                    or ""
                ),
                "Récolte prévue": (
                    culture.date_prevue_recolte
                    or ""
                ),
                "Statut": (
                    culture.statut
                ),
                "Description": (
                    culture.description
                    or ""
                ),
            }
        )

    cultures_df = pd.DataFrame(
        table_rows
    )

    st.dataframe(
        cultures_df,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# ============================================================
# MODIFICATION
# ============================================================

st.subheader("✏️ Modifier une culture")


if not cultures:

    st.info(
        "Aucune culture disponible à modifier."
    )

else:

    culture_options = {
        f"{culture.id} — {culture.nom}": culture.id
        for culture in cultures
    }

    selected_culture_label = st.selectbox(
        "Sélectionner une culture",
        options=list(
            culture_options.keys()
        ),
        key="culture_edit_selection",
    )

    selected_culture_id = (
        culture_options[
            selected_culture_label
        ]
    )

    try:

        selected_culture = (
            culture_service.get_culture(
                selected_culture_id
            )
        )

    except Exception as exc:

        st.error(
            f"❌ Impossible de charger la culture : {exc}"
        )

        selected_culture = None


    if selected_culture is not None:

        with st.form(
            "update_culture_form"
        ):

            # ------------------------------------------------
            # PARCELLE
            # ------------------------------------------------

            if not parcelles:

                st.error(
                    "Aucune parcelle disponible."
                )

            else:

                edit_parcelle_options = {
                    f"{parcelle.id} — {parcelle.nom}":
                    parcelle.id
                    for parcelle in parcelles
                }

                current_parcelle_label = next(
                    (
                        label
                        for label, parcelle_id
                        in edit_parcelle_options.items()
                        if parcelle_id
                        == selected_culture.parcelle_id
                    ),
                    list(
                        edit_parcelle_options.keys()
                    )[0],
                )

                edit_parcelle_label = st.selectbox(
                    "Parcelle",
                    options=list(
                        edit_parcelle_options.keys()
                    ),
                    index=list(
                        edit_parcelle_options.keys()
                    ).index(
                        current_parcelle_label
                    ),
                )

                edit_parcelle_id = (
                    edit_parcelle_options[
                        edit_parcelle_label
                    ]
                )

            # ------------------------------------------------
            # INFORMATIONS
            # ------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                edit_nom = st.text_input(
                    "Nom",
                    value=selected_culture.nom,
                )

            with col2:

                edit_variete = st.text_input(
                    "Variété",
                    value=(
                        selected_culture.variete
                        or ""
                    ),
                )

            # ------------------------------------------------
            # DATES
            # ------------------------------------------------

            def parse_culture_date(
                value
            ):
                """
                Convertit une date ISO stockée en base
                vers un objet compatible avec st.date_input.
                """

                if not value:

                    return None

                try:

                    return pd.to_datetime(
                        value
                    ).date()

                except (
                    ValueError,
                    TypeError,
                ):

                    return None

            edit_date_semis = st.date_input(
                "Date de semis",
                value=parse_culture_date(
                    selected_culture.date_semis
                ),
            )

            edit_date_prevue_recolte = st.date_input(
                "Date prévue de récolte",
                value=parse_culture_date(
                    selected_culture.date_prevue_recolte
                ),
            )

            # ------------------------------------------------
            # STATUT
            # ------------------------------------------------

            status_options = [
                "Planifiée",
                "En cours",
                "Terminée",
            ]

            current_status = (
                selected_culture.statut
                if selected_culture.statut
                in status_options
                else status_options[0]
            )

            edit_statut = st.selectbox(
                "Statut",
                status_options,
                index=status_options.index(
                    current_status
                ),
            )

            # ------------------------------------------------
            # DESCRIPTION
            # ------------------------------------------------

            edit_description = st.text_area(
                "Description",
                value=(
                    selected_culture.description
                    or ""
                ),
            )

            update_submitted = (
                st.form_submit_button(
                    "💾 Enregistrer les modifications",
                    type="primary",
                    use_container_width=True,
                )
            )

            if update_submitted:

                try:

                    selected_culture.parcelle_id = (
                        edit_parcelle_id
                    )

                    selected_culture.nom = (
                        edit_nom
                    )

                    selected_culture.variete = (
                        edit_variete
                        or None
                    )

                    selected_culture.date_semis = (
                        edit_date_semis.isoformat()
                        if edit_date_semis
                        else None
                    )

                    selected_culture.date_prevue_recolte = (
                        edit_date_prevue_recolte.isoformat()
                        if edit_date_prevue_recolte
                        else None
                    )

                    selected_culture.statut = (
                        edit_statut
                    )

                    selected_culture.description = (
                        edit_description
                        or None
                    )

                    updated_culture = (
                        culture_service.update_culture(
                            selected_culture
                        )
                    )

                    st.success(
                        f"✅ Culture « "
                        f"{updated_culture.nom} "
                        "» mise à jour."
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


st.divider()


# ============================================================
# SUPPRESSION
# ============================================================

st.subheader("🗑️ Supprimer une culture")


if not cultures:

    st.info(
        "Aucune culture disponible à supprimer."
    )

else:

    delete_options = {
        f"{culture.id} — {culture.nom}": culture.id
        for culture in cultures
    }

    selected_delete_label = st.selectbox(
        "Culture à supprimer",
        options=list(
            delete_options.keys()
        ),
        key="culture_delete_selection",
    )

    selected_delete_id = (
        delete_options[
            selected_delete_label
        ]
    )

    st.warning(
        """
        ⚠️ La suppression d'une culture peut avoir
        des conséquences sur les travaux, dépenses,
        revenus ou récoltes associés selon les règles
        définies dans la base de données.
        """
    )

    confirm_delete = st.checkbox(
        "Je confirme vouloir supprimer cette culture.",
        key="confirm_delete_culture",
    )

    if st.button(
        "🗑️ Supprimer la culture",
        type="secondary",
        use_container_width=True,
        disabled=not confirm_delete,
    ):

        try:

            culture_service.delete_culture(
                selected_delete_id
            )

            st.success(
                "✅ Culture supprimée avec succès."
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

