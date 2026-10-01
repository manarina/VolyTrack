
"""
VolyTrack — Gestion des Dépenses
================================

Interface Streamlit pour gérer les dépenses agricoles.

Fonctionnalités :
    - affichage des dépenses ;
    - recherche ;
    - filtrage par parcelle ;
    - filtrage par culture ;
    - création ;
    - modification ;
    - suppression ;
    - calcul du total des dépenses.
"""

import streamlit as st
import pandas as pd

from core.services.depense_service import DepenseService
from core.services.parcelle_service import ParcelleService
from core.services.culture_service import CultureService


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VolyTrack — Dépenses",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# SERVICES
# ============================================================

depense_service = DepenseService()
parcelle_service = ParcelleService()
culture_service = CultureService()


# ============================================================
# HEADER
# ============================================================

st.title("💰 VolyTrack — Dépenses")

st.markdown(
    """
    Gérez les **dépenses agricoles** de votre exploitation.

    Vous pouvez enregistrer :
    - la catégorie de dépense ;
    - le montant ;
    - la date ;
    - la parcelle concernée ;
    - éventuellement la culture concernée ;
    - une description.
    """
)

st.divider()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

try:

    depenses = depense_service.get_all_depenses()
    parcelles = parcelle_service.get_all_parcelles()
    cultures = culture_service.get_all_cultures()

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


# ============================================================
# MÉTRIQUES
# ============================================================

total_depenses = len(depenses)

montant_total = sum(
    float(depense.montant)
    for depense in depenses
)

montant_moyen = (
    montant_total / total_depenses
    if total_depenses > 0
    else 0.0
)

depenses_avec_parcelle = sum(
    1
    for depense in depenses
    if depense.parcelle_id is not None
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Nombre de dépenses",
        total_depenses,
    )

with col2:

    st.metric(
        "💵 Montant total",
        f"{montant_total:,.0f} Ar",
    )

with col3:

    st.metric(
        "📊 Dépense moyenne",
        f"{montant_moyen:,.0f} Ar",
    )

with col4:

    st.metric(
        "🌾 Avec parcelle",
        depenses_avec_parcelle,
    )


st.divider()


# ============================================================
# RECHERCHE ET FILTRES
# ============================================================

st.subheader("🔎 Rechercher et filtrer")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:

    search_query = st.text_input(
        "Recherche",
        placeholder=(
            "Ex. semences, engrais, carburant..."
        ),
        key="depenses_search",
    )

with filter_col2:

    parcelle_filter_options = {
        "Toutes les parcelles": None
    }

    for parcelle in parcelles:

        parcelle_filter_options[
            f"{parcelle.nom} (ID {parcelle.id})"
        ] = parcelle.id

    selected_parcelle_filter = st.selectbox(
        "Parcelle",
        options=list(
            parcelle_filter_options.keys()
        ),
        key="depenses_parcelle_filter",
    )

with filter_col3:

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
        key="depenses_culture_filter",
    )


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

filtered_depenses = depenses

if search_query.strip():

    try:

        filtered_depenses = (
            depense_service.search_depenses(
                search_query.strip()
            )
        )

    except Exception as exc:

        st.error(
            f"❌ Erreur pendant la recherche : {exc}"
        )

        filtered_depenses = []


selected_parcelle_id = (
    parcelle_filter_options[
        selected_parcelle_filter
    ]
)

selected_culture_id = (
    culture_filter_options[
        selected_culture_filter
    ]
)

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


st.divider()


# ============================================================
# AJOUT D'UNE DÉPENSE
# ============================================================

st.subheader("➕ Ajouter une dépense")

with st.form(
    "create_depense_form",
    clear_on_submit=True,
):

    col1, col2 = st.columns(2)

    with col1:

        categorie = st.text_input(
            "Catégorie *",
            placeholder=(
                "Ex. Semences, engrais, carburant..."
            ),
            key="depense_create_categorie",
        )

        montant = st.number_input(
            "Montant (Ar) *",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key="depense_create_montant",
        )

        date_depense = st.date_input(
            "Date de la dépense *",
            key="depense_create_date",
        )

    with col2:

        create_parcelle_options = {
            "Aucune parcelle":
            None
        }

        for parcelle in parcelles:

            create_parcelle_options[
                f"{parcelle.nom} (ID {parcelle.id})"
            ] = parcelle.id

        selected_create_parcelle = st.selectbox(
            "Parcelle",
            options=list(
                create_parcelle_options.keys()
            ),
            key="depense_create_parcelle",
        )

        create_culture_options = {
            "Aucune culture":
            None
        }

        for culture in cultures:

            create_culture_options[
                f"{culture.nom} (ID {culture.id})"
            ] = culture.id

        selected_create_culture = st.selectbox(
            "Culture",
            options=list(
                create_culture_options.keys()
            ),
            key="depense_create_culture",
        )

        description = st.text_area(
            "Description",
            placeholder=(
                "Informations complémentaires..."
            ),
            key="depense_create_description",
        )

    submitted = st.form_submit_button(
        "💾 Enregistrer la dépense",
        type="primary",
        use_container_width=True,
    )

    if submitted:

        try:

            parcelle_id = (
                create_parcelle_options[
                    selected_create_parcelle
                ]
            )

            culture_id = (
                create_culture_options[
                    selected_create_culture
                ]
            )

            depense_service.create_depense(
                categorie=categorie.strip(),
                montant=float(montant),
                date_depense=date_depense.isoformat(),
                parcelle_id=parcelle_id,
                culture_id=culture_id,
                description=description.strip() or None,
            )

            st.success(
                "✅ Dépense enregistrée avec succès."
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
# LISTE DES DÉPENSES
# ============================================================

st.subheader("📋 Liste des dépenses")

if not filtered_depenses:

    st.info(
        "Aucune dépense ne correspond aux critères."
    )

else:

    table_rows = []

    for depense in filtered_depenses:

        table_rows.append(
            {
                "ID": depense.id,
                "Catégorie": depense.categorie,
                "Montant (Ar)": float(
                    depense.montant
                ),
                "Date": depense.date_depense,
                "Parcelle": (
                    parcelle_names.get(
                        depense.parcelle_id,
                        f"ID {depense.parcelle_id}",
                    )
                    if depense.parcelle_id is not None
                    else "—"
                ),
                "Culture": (
                    culture_names.get(
                        depense.culture_id,
                        f"ID {depense.culture_id}",
                    )
                    if depense.culture_id is not None
                    else "—"
                ),
                "Description": (
                    depense.description
                    or ""
                ),
            }
        )

    depenses_df = pd.DataFrame(
        table_rows
    )

    st.dataframe(
        depenses_df,
        use_container_width=True,
        hide_index=True,
    )

    filtered_total = sum(
        float(depense.montant)
        for depense in filtered_depenses
    )

    st.info(
        f"💰 Total correspondant aux filtres : "
        f"**{filtered_total:,.0f} Ar**"
    )


st.divider()


# ============================================================
# MODIFICATION
# ============================================================

st.subheader("✏️ Modifier une dépense")

if not depenses:

    st.info(
        "Aucune dépense disponible pour la modification."
    )

else:

    update_options = {
        (
            f"#{depense.id} — "
            f"{depense.categorie} — "
            f"{depense.montant:,.0f} Ar — "
            f"{depense.date_depense}"
        ):
        depense.id
        for depense in depenses
    }

    selected_update_label = st.selectbox(
        "Sélectionner une dépense",
        options=list(
            update_options.keys()
        ),
        key="depense_update_selection",
    )

    selected_update_id = update_options[
        selected_update_label
    ]

    selected_depense = next(
        (
            depense
            for depense in depenses
            if depense.id == selected_update_id
        ),
        None,
    )

    if selected_depense is not None:

        with st.form(
            "update_depense_form"
        ):

            col1, col2 = st.columns(2)

            with col1:

                update_categorie = st.text_input(
                    "Catégorie *",
                    value=(
                        selected_depense.categorie
                    ),
                    key="depense_update_categorie",
                )

                update_montant = st.number_input(
                    "Montant (Ar) *",
                    min_value=0.0,
                    value=float(
                        selected_depense.montant
                    ),
                    step=100.0,
                    key="depense_update_montant",
                )

                try:

                    current_date = pd.to_datetime(
                        selected_depense.date_depense
                    ).date()

                except Exception:

                    current_date = (
                        pd.Timestamp.today().date()
                    )

                update_date = st.date_input(
                    "Date de la dépense *",
                    value=current_date,
                    key="depense_update_date",
                )

            with col2:

                update_parcelle_options = {
                    "Aucune parcelle":
                    None
                }

                for parcelle in parcelles:

                    update_parcelle_options[
                        f"{parcelle.nom} "
                        f"(ID {parcelle.id})"
                    ] = parcelle.id

                current_parcelle_label = next(
                    (
                        label
                        for label, value
                        in update_parcelle_options.items()
                        if value
                        == selected_depense.parcelle_id
                    ),
                    "Aucune parcelle",
                )

                update_parcelle_label = st.selectbox(
                    "Parcelle",
                    options=list(
                        update_parcelle_options.keys()
                    ),
                    index=list(
                        update_parcelle_options.keys()
                    ).index(
                        current_parcelle_label
                    ),
                    key="depense_update_parcelle",
                )

                update_culture_options = {
                    "Aucune culture":
                    None
                }

                for culture in cultures:

                    update_culture_options[
                        f"{culture.nom} "
                        f"(ID {culture.id})"
                    ] = culture.id

                current_culture_label = next(
                    (
                        label
                        for label, value
                        in update_culture_options.items()
                        if value
                        == selected_depense.culture_id
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
                    key="depense_update_culture",
                )

                update_description = st.text_area(
                    "Description",
                    value=(
                        selected_depense.description
                        or ""
                    ),
                    key="depense_update_description",
                )

            update_submitted = st.form_submit_button(
                "💾 Enregistrer les modifications",
                type="primary",
                use_container_width=True,
            )

            if update_submitted:

                try:

                    selected_depense.categorie = (
                        update_categorie.strip()
                    )

                    selected_depense.montant = float(
                        update_montant
                    )

                    selected_depense.date_depense = (
                        update_date.isoformat()
                    )

                    selected_depense.parcelle_id = (
                        update_parcelle_options[
                            update_parcelle_label
                        ]
                    )

                    selected_depense.culture_id = (
                        update_culture_options[
                            update_culture_label
                        ]
                    )

                    selected_depense.description = (
                        update_description.strip()
                        or None
                    )

                    depense_service.update_depense(
                        selected_depense
                    )

                    st.success(
                        "✅ Dépense modifiée avec succès."
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

st.subheader("🗑️ Supprimer une dépense")

if not depenses:

    st.info(
        "Aucune dépense disponible pour la suppression."
    )

else:

    delete_options = {
        (
            f"#{depense.id} — "
            f"{depense.categorie} — "
            f"{depense.montant:,.0f} Ar"
        ):
        depense.id
        for depense in depenses
    }

    delete_label = st.selectbox(
        "Sélectionner la dépense à supprimer",
        options=list(
            delete_options.keys()
        ),
        key="depense_delete_selection",
    )

    delete_id = delete_options[
        delete_label
    ]

    confirm_delete = st.checkbox(
        "Je confirme vouloir supprimer cette dépense.",
        key="depense_delete_confirmation",
    )

    if st.button(
        "🗑️ Supprimer",
        type="secondary",
        disabled=not confirm_delete,
        key="depense_delete_button",
    ):

        try:

            depense_service.delete_depense(
                delete_id
            )

            st.success(
                "✅ Dépense supprimée avec succès."
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
# EXPLICATION
# ============================================================

with st.expander(
    "📚 Comprendre la gestion des dépenses"
):

    st.markdown(
        """
        ### Dépense agricole

        Une dépense représente une sortie d'argent liée
        à l'exploitation agricole.

        Exemples :

        - achat de semences ;
        - engrais ;
        - produits phytosanitaires ;
        - carburant ;
        - main-d'œuvre ;
        - matériel ;
        - transport ;
        - irrigation.

        ### Association avec une parcelle

        Une dépense peut être associée à une parcelle
        lorsqu'elle concerne directement celle-ci.

        ### Association avec une culture

        Une dépense peut également être associée
        à une culture particulière.

        ### Calcul financier

        Le montant total des dépenses correspond à :

        $$
        Total\\ des\\ dépenses
        =
        \\sum_{i=1}^{n} montant_i
        $$

        Cette donnée sera ensuite utilisée dans le
        **Dashboard** et dans les **Analytics** pour
        calculer notamment la marge :

        $$
        Marge = Revenus - Dépenses
        $$
        """
    )

