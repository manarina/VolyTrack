
"""
VolyTrack — Gestion des Parcelles
=================================

Interface Streamlit permettant de :

- consulter les parcelles ;
- rechercher une parcelle ;
- créer une parcelle ;
- modifier une parcelle ;
- supprimer une parcelle ;
- afficher quelques statistiques.

La logique métier est déléguée à ParcelleService.
"""

import streamlit as st
import pandas as pd

from core.services.parcelle_service import ParcelleService
from core.models.parcelle import Parcelle

from core.repositories.parcelle_repository import ParcelleRepository

repository = ParcelleRepository()

print(repository.count())


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Parcelles — VolyTrack",
    page_icon="🌾",
    layout="wide",
)


# ============================================================
# SERVICE
# ============================================================

service = ParcelleService()


# ============================================================
# TITRE
# ============================================================

st.title("🌾 Gestion des Parcelles")

st.markdown(
    """
    Gérez les parcelles de votre exploitation agricole.

    Vous pouvez créer, consulter, rechercher, modifier
    et supprimer les parcelles enregistrées dans VolyTrack.
    """
)

st.divider()


# ============================================================
# RÉCUPÉRATION DES PARCELLES
# ============================================================

try:

    parcelles = service.get_all_parcelles()

except Exception as exc:

    st.error(
        f"❌ Impossible de charger les parcelles : {exc}"
    )

    parcelles = []


# ============================================================
# INDICATEURS
# ============================================================

total_parcelles = service.count_parcelles()

total_superficie = sum(
    parcelle.superficie
    for parcelle in parcelles
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🌾 Nombre de parcelles",
        total_parcelles,
    )

with col2:

    st.metric(
        "📐 Superficie totale",
        f"{total_superficie:.2f} ha",
    )

with col3:

    if total_parcelles > 0:

        moyenne_superficie = (
            total_superficie
            / total_parcelles
        )

    else:

        moyenne_superficie = 0.0

    st.metric(
        "📊 Superficie moyenne",
        f"{moyenne_superficie:.2f} ha",
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Rechercher une parcelle")

search_query = st.text_input(
    "Nom, localisation ou description",
    placeholder="Ex. Parcelle Nord",
    key="parcelles_search",
)


# ============================================================
# FORMULAIRE DE CRÉATION
# ============================================================

with st.expander(
    "➕ Ajouter une nouvelle parcelle",
    expanded=False,
):

    with st.form(
        "create_parcelle_form",
        clear_on_submit=True,
    ):

        st.markdown(
            "### 🌱 Nouvelle parcelle"
        )

        col1, col2 = st.columns(2)

        with col1:

            nom = st.text_input(
                "Nom de la parcelle *",
                placeholder="Ex. Parcelle Nord",
            )

        with col2:

            superficie = st.number_input(
                "Superficie *",
                min_value=0.01,
                value=1.0,
                step=0.1,
                format="%.2f",
            )

        col3, col4 = st.columns(2)

        with col3:

            unite_superficie = st.selectbox(
                "Unité de superficie",
                [
                    "ha",
                    "m²",
                ],
            )

        with col4:

            localisation = st.text_input(
                "Localisation",
                placeholder="Ex. Anosivelo",
            )

        description = st.text_area(
            "Description",
            placeholder=(
                "Informations complémentaires "
                "sur la parcelle..."
            ),
        )

        submitted = st.form_submit_button(
            "💾 Enregistrer la parcelle",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        try:

            if not nom.strip():
                raise ValueError(
                    "Le nom de la parcelle est obligatoire."
                )

            parcelle = Parcelle(
                nom=nom.strip(),
                superficie=float(superficie),
                unite_superficie=unite_superficie,
                localisation=localisation.strip() or None,
                description=description.strip() or None,
            )

            parcelle = service.create_parcelle(parcelle)

            st.success(
                f"✅ Parcelle « {parcelle.nom} » "
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
# LISTE DES PARCELLES
# ============================================================

st.subheader("📋 Liste des parcelles")


# ------------------------------------------------------------
# FILTRAGE
# ------------------------------------------------------------

if search_query.strip():

    try:

        filtered_parcelles = service.search_parcelles(
            search_query
        )

    except (ValueError, TypeError) as exc:

        st.error(
            f"❌ Erreur de recherche : {exc}"
        )

        filtered_parcelles = []

else:

    filtered_parcelles = parcelles


# ------------------------------------------------------------
# AFFICHAGE VIDE
# ------------------------------------------------------------

if not filtered_parcelles:

    if search_query.strip():

        st.info(
            "🔎 Aucune parcelle ne correspond "
            "à votre recherche."
        )

    else:

        st.info(
            "🌱 Aucune parcelle enregistrée pour le moment."
        )


# ------------------------------------------------------------
# TABLEAU
# ------------------------------------------------------------

else:

    table_rows = []

    for parcelle in filtered_parcelles:

        table_rows.append(
            {
                "ID": parcelle.id,
                "Nom": parcelle.nom,
                "Superficie": parcelle.superficie,
                "Unité": parcelle.unite_superficie,
                "Localisation": (
                    parcelle.localisation
                    or ""
                ),
                "Description": (
                    parcelle.description
                    or ""
                ),
            }
        )

    parcelles_df = pd.DataFrame(
        table_rows
    )

    st.dataframe(
        parcelles_df,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# ============================================================
# MODIFICATION
# ============================================================

st.subheader("✏️ Modifier une parcelle")


if not parcelles:

    st.info(
        "Aucune parcelle disponible à modifier."
    )

else:

    parcelle_options = {
        f"{parcelle.id} — {parcelle.nom}": parcelle.id
        for parcelle in parcelles
    }

    selected_parcelle_label = st.selectbox(
        "Sélectionner une parcelle",
        options=list(
            parcelle_options.keys()
        ),
        key="parcelle_edit_selection",
    )

    selected_parcelle_id = parcelle_options[
        selected_parcelle_label
    ]

    try:

        selected_parcelle = service.get_parcelle(
            selected_parcelle_id
        )

    except Exception as exc:

        st.error(
            f"❌ Impossible de charger la parcelle : {exc}"
        )

        selected_parcelle = None

    if selected_parcelle is not None:

        with st.form(
            "update_parcelle_form"
        ):

            col1, col2 = st.columns(2)

            with col1:

                edit_nom = st.text_input(
                    "Nom",
                    value=selected_parcelle.nom,
                )

            with col2:

                edit_superficie = st.number_input(
                    "Superficie",
                    min_value=0.01,
                    value=float(
                        selected_parcelle.superficie
                    ),
                    step=0.1,
                    format="%.2f",
                )

            col3, col4 = st.columns(2)

            with col3:

                edit_unite = st.selectbox(
                    "Unité",
                    [
                        "ha",
                        "m²",
                    ],
                    index=(
                        0
                        if selected_parcelle.unite_superficie
                        == "ha"
                        else 1
                    ),
                )

            with col4:

                edit_localisation = st.text_input(
                    "Localisation",
                    value=(
                        selected_parcelle.localisation
                        or ""
                    ),
                )

            edit_description = st.text_area(
                "Description",
                value=(
                    selected_parcelle.description
                    or ""
                ),
            )

            update_submitted = st.form_submit_button(
                "💾 Enregistrer les modifications",
                type="primary",
                use_container_width=True,
            )

            if update_submitted:

                try:

                    selected_parcelle.nom = edit_nom
                    selected_parcelle.superficie = (
                        edit_superficie
                    )
                    selected_parcelle.unite_superficie = (
                        edit_unite
                    )
                    selected_parcelle.localisation = (
                        edit_localisation
                        or None
                    )
                    selected_parcelle.description = (
                        edit_description
                        or None
                    )

                    updated_parcelle = (
                        service.update_parcelle(
                            selected_parcelle
                        )
                    )

                    st.success(
                        f"✅ Parcelle « "
                        f"{updated_parcelle.nom} "
                        f"» mise à jour."
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

st.subheader("🗑️ Supprimer une parcelle")


if not parcelles:

    st.info(
        "Aucune parcelle disponible à supprimer."
    )

else:

    delete_options = {
        f"{parcelle.id} — {parcelle.nom}": parcelle.id
        for parcelle in parcelles
    }

    selected_delete_label = st.selectbox(
        "Parcelle à supprimer",
        options=list(
            delete_options.keys()
        ),
        key="parcelle_delete_selection",
    )

    selected_delete_id = delete_options[
        selected_delete_label
    ]

    st.warning(
        """
        ⚠️ La suppression d'une parcelle peut avoir
        des conséquences sur les données associées
        selon les règles définies dans la base de données.
        """
    )

    confirm_delete = st.checkbox(
        "Je confirme vouloir supprimer cette parcelle.",
        key="confirm_delete_parcelle",
    )

    if st.button(
        "🗑️ Supprimer la parcelle",
        type="secondary",
        use_container_width=True,
        disabled=not confirm_delete,
    ):

        try:

            service.delete_parcelle(
                selected_delete_id
            )

            st.success(
                "✅ Parcelle supprimée avec succès."
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

