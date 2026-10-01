
"""
VolyTrack — Gestion des Travaux
================================

Interface Streamlit pour gérer les travaux agricoles.

Fonctionnalités :
    - affichage des travaux ;
    - recherche ;
    - création ;
    - modification ;
    - suppression ;
    - association avec une parcelle ;
    - association optionnelle avec une culture ;
    - suivi du coût des travaux.
"""

import streamlit as st
import pandas as pd

from core.services.travail_service import TravailService
from core.services.parcelle_service import ParcelleService
from core.services.culture_service import CultureService


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VolyTrack — Travaux",
    page_icon="🔨",
    layout="wide",
)


# ============================================================
# SERVICES
# ============================================================

travail_service = TravailService()
parcelle_service = ParcelleService()
culture_service = CultureService()


# ============================================================
# HEADER
# ============================================================

st.title("🔨 VolyTrack — Travaux")

st.markdown(
    """
    Gérez les **travaux agricoles** réalisés sur vos parcelles.

    Vous pouvez enregistrer :
    - le type de travail ;
    - la date ;
    - la parcelle concernée ;
    - éventuellement la culture concernée ;
    - le coût ;
    - une description.
    """
)

st.divider()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

try:

    travaux = travail_service.get_all_travaux()
    parcelles = parcelle_service.get_all_parcelles()
    cultures = culture_service.get_all_cultures()

except Exception as exc:

    st.error(
        f"❌ Impossible de charger les données : {exc}"
    )

    st.stop()


# ============================================================
# DICTIONNAIRES DE CORRESPONDANCE
# ============================================================

parcelle_names = {
    parcelle.id: parcelle.nom
    for parcelle in parcelles
}

culture_names = {
    culture.id: culture.nom
    for culture in cultures
}


# ============================================================
# MÉTRIQUES
# ============================================================

total_travaux = len(travaux)

total_cout = sum(
    float(travail.cout)
    for travail in travaux
)

travaux_avec_culture = sum(
    1
    for travail in travaux
    if travail.culture_id is not None
)

travaux_sans_culture = (
    total_travaux
    - travaux_avec_culture
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🔨 Total travaux",
        total_travaux,
    )

with col2:

    st.metric(
        "💰 Coût total",
        f"{total_cout:,.0f} Ar",
    )

with col3:

    st.metric(
        "🌱 Avec culture",
        travaux_avec_culture,
    )

with col4:

    st.metric(
        "📋 Sans culture",
        travaux_sans_culture,
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Rechercher un travail")

search_query = st.text_input(
    "Recherche",
    placeholder=(
        "Ex. labour, semis, désherbage..."
    ),
    key="travaux_search",
)

if search_query.strip():

    try:

        travaux = travail_service.search_travaux(
            search_query.strip()
        )

    except Exception as exc:

        st.error(
            f"❌ Erreur pendant la recherche : {exc}"
        )

        travaux = []

st.divider()


# ============================================================
# CRÉATION
# ============================================================

st.subheader("➕ Ajouter un travail")

if not parcelles:

    st.warning(
        """
        ⚠️ Aucune parcelle n'est disponible.

        Créez d'abord une parcelle avant d'ajouter
        un travail.
        """
    )

else:

    with st.form(
        "create_travail_form",
        clear_on_submit=True,
    ):

        col1, col2 = st.columns(2)

        with col1:

            parcelle_options = {
                f"{parcelle.nom} (ID {parcelle.id})":
                parcelle.id
                for parcelle in parcelles
            }

            selected_parcelle_label = st.selectbox(
                "Parcelle *",
                options=list(
                    parcelle_options.keys()
                ),
                key="travail_create_parcelle",
            )

            type_travail = st.text_input(
                "Type de travail *",
                placeholder=(
                    "Ex. Labour, semis, désherbage..."
                ),
                key="travail_create_type",
            )

            date_travail = st.date_input(
                "Date du travail *",
                key="travail_create_date",
            )

        with col2:

            culture_options = {
                "Aucune culture":
                None
            }

            for culture in cultures:

                culture_options[
                    f"{culture.nom} "
                    f"(ID {culture.id})"
                ] = culture.id

            selected_culture_label = st.selectbox(
                "Culture",
                options=list(
                    culture_options.keys()
                ),
                key="travail_create_culture",
            )

            cout = st.number_input(
                "Coût (Ar)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                key="travail_create_cout",
            )

            description = st.text_area(
                "Description",
                placeholder=(
                    "Informations complémentaires..."
                ),
                key="travail_create_description",
            )

        submitted = st.form_submit_button(
            "💾 Enregistrer le travail",
            type="primary",
            use_container_width=True,
        )

        if submitted:

            try:

                parcelle_id = parcelle_options[
                    selected_parcelle_label
                ]

                culture_id = culture_options[
                    selected_culture_label
                ]

                travail_service.create_travail(
                    parcelle_id=parcelle_id,
                    type_travail=type_travail.strip(),
                    date_travail=date_travail.isoformat(),
                    culture_id=culture_id,
                    cout=float(cout),
                    description=description.strip() or None,
                )

                st.success(
                    "✅ Travail enregistré avec succès."
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
# LISTE DES TRAVAUX
# ============================================================

st.subheader("📋 Liste des travaux")

if not travaux:

    st.info(
        "Aucun travail ne correspond aux critères."
    )

else:

    table_rows = []

    for travail in travaux:

        table_rows.append(
            {
                "ID": travail.id,
                "Type de travail": travail.type_travail,
                "Date": travail.date_travail,
                "Parcelle": parcelle_names.get(
                    travail.parcelle_id,
                    f"ID {travail.parcelle_id}",
                ),
                "Culture": (
                    culture_names.get(
                        travail.culture_id,
                        f"ID {travail.culture_id}",
                    )
                    if travail.culture_id is not None
                    else "—"
                ),
                "Coût (Ar)": float(
                    travail.cout
                ),
                "Description": (
                    travail.description
                    or ""
                ),
            }
        )

    travaux_df = pd.DataFrame(
        table_rows
    )

    st.dataframe(
        travaux_df,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# ============================================================
# MODIFICATION
# ============================================================

st.subheader("✏️ Modifier un travail")

if not travaux:

    st.info(
        "Aucun travail disponible pour la modification."
    )

else:

    travail_options = {
        (
            f"#{travail.id} — "
            f"{travail.type_travail} — "
            f"{travail.date_travail}"
        ):
        travail.id
        for travail in travaux
    }

    selected_travail_label = st.selectbox(
        "Sélectionner un travail",
        options=list(
            travail_options.keys()
        ),
        key="travail_update_selection",
    )

    selected_travail_id = travail_options[
        selected_travail_label
    ]

    selected_travail = next(
        (
            travail
            for travail in travaux
            if travail.id == selected_travail_id
        ),
        None,
    )

    if selected_travail is not None:

        with st.form(
            "update_travail_form"
        ):

            col1, col2 = st.columns(2)

            with col1:

                update_parcelle_options = {
                    (
                        f"{parcelle.nom} "
                        f"(ID {parcelle.id})"
                    ):
                    parcelle.id
                    for parcelle in parcelles
                }

                current_parcelle_label = next(
                    (
                        label
                        for label, value
                        in update_parcelle_options.items()
                        if value
                        == selected_travail.parcelle_id
                    ),
                    list(
                        update_parcelle_options.keys()
                    )[0]
                    if update_parcelle_options
                    else None,
                )

                update_parcelle_label = st.selectbox(
                    "Parcelle *",
                    options=list(
                        update_parcelle_options.keys()
                    ),
                    index=(
                        list(
                            update_parcelle_options.keys()
                        ).index(
                            current_parcelle_label
                        )
                        if current_parcelle_label
                        in update_parcelle_options
                        else 0
                    ),
                    key="travail_update_parcelle",
                )

                update_type = st.text_input(
                    "Type de travail *",
                    value=(
                        selected_travail.type_travail
                    ),
                    key="travail_update_type",
                )

                try:

                    current_date = pd.to_datetime(
                        selected_travail.date_travail
                    ).date()

                except Exception:

                    current_date = (
                        pd.Timestamp.today().date()
                    )

                update_date = st.date_input(
                    "Date du travail *",
                    value=current_date,
                    key="travail_update_date",
                )

            with col2:

                update_culture_options = {
                    "Aucune culture":
                    None
                }

                for culture in cultures:

                    update_culture_options[
                        (
                            f"{culture.nom} "
                            f"(ID {culture.id})"
                        )
                    ] = culture.id

                current_culture_label = next(
                    (
                        label
                        for label, value
                        in update_culture_options.items()
                        if value
                        == selected_travail.culture_id
                    ),
                    "Aucune culture",
                )

                update_culture_label = st.selectbox(
                    "Culture",
                    options=list(
                        update_culture_options.keys()
                    ),
                    index=list(
                        update_culture_options.keys()
                    ).index(
                        current_culture_label
                    ),
                    key="travail_update_culture",
                )

                update_cout = st.number_input(
                    "Coût (Ar)",
                    min_value=0.0,
                    value=float(
                        selected_travail.cout
                    ),
                    step=100.0,
                    key="travail_update_cout",
                )

                update_description = st.text_area(
                    "Description",
                    value=(
                        selected_travail.description
                        or ""
                    ),
                    key="travail_update_description",
                )

            update_submitted = st.form_submit_button(
                "💾 Enregistrer les modifications",
                type="primary",
                use_container_width=True,
            )

            if update_submitted:

                try:

                    selected_travail.parcelle_id = (
                        update_parcelle_options[
                            update_parcelle_label
                        ]
                    )

                    selected_travail.type_travail = (
                        update_type.strip()
                    )

                    selected_travail.date_travail = (
                        update_date.isoformat()
                    )

                    selected_travail.culture_id = (
                        update_culture_options[
                            update_culture_label
                        ]
                    )

                    selected_travail.cout = float(
                        update_cout
                    )

                    selected_travail.description = (
                        update_description.strip()
                        or None
                    )

                    travail_service.update_travail(
                        selected_travail
                    )

                    st.success(
                        "✅ Travail modifié avec succès."
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

st.subheader("🗑️ Supprimer un travail")

if not travaux:

    st.info(
        "Aucun travail disponible pour la suppression."
    )

else:

    delete_options = {
        (
            f"#{travail.id} — "
            f"{travail.type_travail} — "
            f"{travail.date_travail}"
        ):
        travail.id
        for travail in travaux
    }

    delete_label = st.selectbox(
        "Sélectionner le travail à supprimer",
        options=list(
            delete_options.keys()
        ),
        key="travail_delete_selection",
    )

    delete_id = delete_options[
        delete_label
    ]

    confirm_delete = st.checkbox(
        "Je confirme vouloir supprimer ce travail.",
        key="travail_delete_confirmation",
    )

    if st.button(
        "🗑️ Supprimer",
        type="secondary",
        disabled=not confirm_delete,
        key="travail_delete_button",
    ):

        try:

            travail_service.delete_travail(
                delete_id
            )

            st.success(
                "✅ Travail supprimé avec succès."
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
# INFORMATIONS
# ============================================================

with st.expander(
    "📚 Comprendre la gestion des travaux"
):

    st.markdown(
        """
        ### Travail agricole

        Un travail représente une opération effectuée
        dans le cadre de l'exploitation agricole.

        Exemples :

        - préparation du sol ;
        - labour ;
        - semis ;
        - fertilisation ;
        - désherbage ;
        - traitement ;
        - irrigation ;
        - entretien.

        ### Association avec une parcelle

        Chaque travail doit être associé à une parcelle.

        ### Association avec une culture

        Une culture peut être associée au travail lorsqu'elle
        est connue.

        L'association avec une culture reste optionnelle.

        ### Coût

        Le coût représente la dépense directement associée
        au travail enregistré.

        Le service garantit que le coût ne peut pas être négatif.
        """
    )

