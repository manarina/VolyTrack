
"""
VolyTrack — Gestion des Revenus
================================

Interface Streamlit pour gérer les revenus agricoles.

Fonctionnalités :
    - affichage des revenus ;
    - recherche ;
    - filtrage par parcelle ;
    - filtrage par culture ;
    - création ;
    - modification ;
    - suppression ;
    - calcul du chiffre d'affaires ;
    - calcul des quantités ;
    - calcul du prix unitaire moyen.
"""

import streamlit as st
import pandas as pd

from core.models.revenu import Revenu

from core.services.revenu_service import RevenuService
from core.services.parcelle_service import ParcelleService
from core.services.culture_service import CultureService


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VolyTrack — Revenus",
    page_icon="💵",
    layout="wide",
)


# ============================================================
# SERVICES
# ============================================================

revenu_service = RevenuService()
parcelle_service = ParcelleService()
culture_service = CultureService()


# ============================================================
# HEADER
# ============================================================

st.title("💵 VolyTrack — Revenus")

st.markdown(
    """
    Gérez les **revenus agricoles** générés par votre exploitation.

    Vous pouvez enregistrer :

    - le produit vendu ;
    - la quantité ;
    - le prix unitaire ;
    - le montant ;
    - la date ;
    - la parcelle concernée ;
    - la culture concernée ;
    - une description.
    """
)

st.divider()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

try:

    revenus = revenu_service.get_all_revenus()
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

total_revenus = len(revenus)

chiffre_affaires = sum(
    float(revenu.montant)
    for revenu in revenus
)

quantite_totale = sum(
    float(revenu.quantite)
    for revenu in revenus
)

prix_moyen = (
    chiffre_affaires / quantite_totale
    if quantite_totale > 0
    else 0.0
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💵 Nombre de revenus",
        total_revenus,
    )

with col2:

    st.metric(
        "💰 Chiffre d'affaires",
        f"{chiffre_affaires:,.0f} Ar",
    )

with col3:

    st.metric(
        "📦 Quantité totale",
        f"{quantite_totale:,.2f}",
    )

with col4:

    st.metric(
        "🏷️ Prix moyen",
        f"{prix_moyen:,.0f} Ar",
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
            "Ex. riz, maïs, légumes..."
        ),
        key="revenus_search",
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
        key="revenus_parcelle_filter",
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
        key="revenus_culture_filter",
    )


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

filtered_revenus = revenus

if search_query.strip():

    try:

        filtered_revenus = (
            revenu_service.search_revenus(
                search_query.strip()
            )
        )

    except Exception as exc:

        st.error(
            f"❌ Erreur pendant la recherche : {exc}"
        )

        filtered_revenus = []


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


st.divider()


# ============================================================
# AJOUT D'UN REVENU
# ============================================================

st.subheader("➕ Ajouter un revenu")

with st.form(
    "create_revenu_form",
    clear_on_submit=True,
):

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # INFORMATIONS DU REVENU
    # --------------------------------------------------------

    with col1:

        produit = st.text_input(
            "Produit vendu *",
            placeholder=(
                "Ex. Riz, maïs, tomate..."
            ),
            key="revenu_create_produit",
        )

        quantite = st.number_input(
            "Quantité *",
            min_value=0.01,
            value=1.0,
            step=0.1,
            key="revenu_create_quantite",
        )

        prix_unitaire = st.number_input(
            "Prix unitaire (Ar) *",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key="revenu_create_prix_unitaire",
        )

        date_revenu = st.date_input(
            "Date du revenu *",
            key="revenu_create_date",
        )

    # --------------------------------------------------------
    # PARCELLE + CULTURE
    # --------------------------------------------------------

    with col2:

        montant_calcule = (
            float(quantite)
            * float(prix_unitaire)
        )

        st.metric(
            "💰 Montant calculé",
            f"{montant_calcule:,.0f} Ar",
        )

        # ----------------------------------------------------
        # PARCELLES
        # ----------------------------------------------------

        create_parcelle_options = {
            "Aucune parcelle": None
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
            key="revenu_create_parcelle",
        )

        selected_create_parcelle_id = (
            create_parcelle_options[
                selected_create_parcelle
            ]
        )

        # ----------------------------------------------------
        # CULTURES DE LA PARCELLE
        # ----------------------------------------------------

        cultures_de_la_parcelle = [
            culture
            for culture in cultures
            if (
                selected_create_parcelle_id is not None
                and culture.parcelle_id
                == selected_create_parcelle_id
            )
        ]

        create_culture_options = {
            "Aucune culture": None
        }

        for culture in cultures_de_la_parcelle:

            create_culture_options[
                f"{culture.nom} (ID {culture.id})"
            ] = culture.id

        selected_create_culture = st.selectbox(
            "Culture",
            options=list(
                create_culture_options.keys()
            ),
            key="revenu_create_culture",
        )

        description = st.text_area(
            "Description",
            placeholder=(
                "Informations complémentaires..."
            ),
            key="revenu_create_description",
        )

    # --------------------------------------------------------
    # BOUTON D'ENREGISTREMENT
    # --------------------------------------------------------

    submitted = st.form_submit_button(
        "💾 Enregistrer le revenu",
        type="primary",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # CRÉATION DU REVENU
    # --------------------------------------------------------

    if submitted:

        try:

            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if not produit.strip():

                raise ValueError(
                    "Le produit ne doit pas être vide."
                )

            if quantite <= 0:

                raise ValueError(
                    "La quantité doit être supérieure à zéro."
                )

            if prix_unitaire < 0:

                raise ValueError(
                    "Le prix unitaire ne peut pas être négatif."
                )

            # ------------------------------------------------
            # RÉCUPÉRATION DES IDENTIFIANTS
            # ------------------------------------------------

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

            # ------------------------------------------------
            # CALCUL DU MONTANT
            # ------------------------------------------------

            montant = (
                float(quantite)
                * float(prix_unitaire)
            )

            # ------------------------------------------------
            # CRÉATION DU MODÈLE REVENU
            # ------------------------------------------------

            revenu = Revenu(
                produit=produit.strip(),
                quantite=float(quantite),
                prix_unitaire=float(prix_unitaire),
                montant=montant,
                date_revenu=date_revenu.isoformat(),
                parcelle_id=parcelle_id,
                culture_id=culture_id,
                description=(
                    description.strip()
                    if description
                    else None
                ),
            )

            # ------------------------------------------------
            # APPEL DU SERVICE
            # ------------------------------------------------

            revenu = (
                revenu_service.create_revenu(
                    revenu
                )
            )

            st.success(
                "✅ Revenu enregistré avec succès."
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
# LISTE DES REVENUS
# ============================================================

st.subheader("📋 Liste des revenus")

if not filtered_revenus:

    st.info(
        "Aucun revenu ne correspond aux critères."
    )

else:

    table_rows = []

    for revenu in filtered_revenus:

        table_rows.append(
            {
                "ID": revenu.id,
                "Produit": revenu.produit,
                "Quantité": float(
                    revenu.quantite
                ),
                "Prix unitaire (Ar)": float(
                    revenu.prix_unitaire
                ),
                "Montant (Ar)": float(
                    revenu.montant
                ),
                "Date": revenu.date_revenu,
                "Parcelle": (
                    parcelle_names.get(
                        revenu.parcelle_id,
                        f"ID {revenu.parcelle_id}",
                    )
                    if revenu.parcelle_id is not None
                    else "—"
                ),
                "Culture": (
                    culture_names.get(
                        revenu.culture_id,
                        f"ID {revenu.culture_id}",
                    )
                    if revenu.culture_id is not None
                    else "—"
                ),
                "Description": (
                    revenu.description
                    or ""
                ),
            }
        )

    revenus_df = pd.DataFrame(
        table_rows
    )

    st.dataframe(
        revenus_df,
        use_container_width=True,
        hide_index=True,
    )

    filtered_chiffre_affaires = sum(
        float(revenu.montant)
        for revenu in filtered_revenus
    )

    filtered_quantite = sum(
        float(revenu.quantite)
        for revenu in filtered_revenus
    )

    st.info(
        f"💰 Chiffre d'affaires correspondant aux filtres : "
        f"**{filtered_chiffre_affaires:,.0f} Ar**  \n"
        f"📦 Quantité correspondante : "
        f"**{filtered_quantite:,.2f}**"
    )


st.divider()


# ============================================================
# MODIFICATION
# ============================================================

st.subheader("✏️ Modifier un revenu")

if not revenus:

    st.info(
        "Aucun revenu disponible pour la modification."
    )

else:

    update_options = {
        (
            f"#{revenu.id} — "
            f"{revenu.produit} — "
            f"{revenu.montant:,.0f} Ar — "
            f"{revenu.date_revenu}"
        ):
        revenu.id
        for revenu in revenus
    }

    selected_update_label = st.selectbox(
        "Sélectionner un revenu",
        options=list(
            update_options.keys()
        ),
        key="revenu_update_selection",
    )

    selected_update_id = update_options[
        selected_update_label
    ]

    selected_revenu = next(
        (
            revenu
            for revenu in revenus
            if revenu.id == selected_update_id
        ),
        None,
    )

    if selected_revenu is not None:

        with st.form(
            "update_revenu_form"
        ):

            col1, col2 = st.columns(2)

            with col1:

                update_produit = st.text_input(
                    "Produit vendu *",
                    value=(
                        selected_revenu.produit
                    ),
                    key="revenu_update_produit",
                )

                update_quantite = st.number_input(
                    "Quantité *",
                    min_value=0.01,
                    value=float(
                        selected_revenu.quantite
                    ),
                    step=0.1,
                    key="revenu_update_quantite",
                )

                update_prix_unitaire = st.number_input(
                    "Prix unitaire (Ar) *",
                    min_value=0.0,
                    value=float(
                        selected_revenu.prix_unitaire
                    ),
                    step=100.0,
                    key="revenu_update_prix_unitaire",
                )

                update_montant = (
                    float(update_quantite)
                    * float(update_prix_unitaire)
                )

                st.metric(
                    "💰 Nouveau montant",
                    f"{update_montant:,.0f} Ar",
                )

                try:

                    current_date = pd.to_datetime(
                        selected_revenu.date_revenu
                    ).date()

                except Exception:

                    current_date = (
                        pd.Timestamp.today().date()
                    )

                update_date = st.date_input(
                    "Date du revenu *",
                    value=current_date,
                    key="revenu_update_date",
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
                        == selected_revenu.parcelle_id
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
                    key="revenu_update_parcelle",
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
                        == selected_revenu.culture_id
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
                    key="revenu_update_culture",
                )

                update_description = st.text_area(
                    "Description",
                    value=(
                        selected_revenu.description
                        or ""
                    ),
                    key="revenu_update_description",
                )

            update_submitted = st.form_submit_button(
                "💾 Enregistrer les modifications",
                type="primary",
                use_container_width=True,
            )

            if update_submitted:

                try:

                    if not update_produit.strip():

                        raise ValueError(
                            "Le produit ne doit pas être vide."
                        )

                    if update_quantite <= 0:

                        raise ValueError(
                            "La quantité doit être supérieure à zéro."
                        )

                    if update_prix_unitaire < 0:

                        raise ValueError(
                            "Le prix unitaire ne peut pas être négatif."
                        )

                    selected_revenu.produit = (
                        update_produit.strip()
                    )

                    selected_revenu.quantite = float(
                        update_quantite
                    )

                    selected_revenu.prix_unitaire = float(
                        update_prix_unitaire
                    )

                    selected_revenu.montant = (
                        float(update_quantite)
                        * float(update_prix_unitaire)
                    )

                    selected_revenu.date_revenu = (
                        update_date.isoformat()
                    )

                    selected_revenu.parcelle_id = (
                        update_parcelle_options[
                            update_parcelle_label
                        ]
                    )

                    selected_revenu.culture_id = (
                        update_culture_options[
                            update_culture_label
                        ]
                    )

                    selected_revenu.description = (
                        update_description.strip()
                        or None
                    )

                    revenu_service.update_revenu(
                        selected_revenu
                    )

                    st.success(
                        "✅ Revenu modifié avec succès."
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

st.subheader("🗑️ Supprimer un revenu")

if not revenus:

    st.info(
        "Aucun revenu disponible pour la suppression."
    )

else:

    delete_options = {
        (
            f"#{revenu.id} — "
            f"{revenu.produit} — "
            f"{revenu.montant:,.0f} Ar"
        ):
        revenu.id
        for revenu in revenus
    }

    delete_label = st.selectbox(
        "Sélectionner le revenu à supprimer",
        options=list(
            delete_options.keys()
        ),
        key="revenu_delete_selection",
    )

    delete_id = delete_options[
        delete_label
    ]

    confirm_delete = st.checkbox(
        "Je confirme vouloir supprimer ce revenu.",
        key="revenu_delete_confirmation",
    )

    if st.button(
        "🗑️ Supprimer",
        type="secondary",
        disabled=not confirm_delete,
        key="revenu_delete_button",
    ):

        try:

            revenu_service.delete_revenu(
                delete_id
            )

            st.success(
                "✅ Revenu supprimé avec succès."
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
    "📚 Comprendre la gestion des revenus"
):

    st.markdown(
        """
        ### Revenu agricole

        Un revenu représente une entrée d'argent générée
        par la vente d'une production agricole.

        Exemples :

        - vente de riz ;
        - vente de maïs ;
        - vente de légumes ;
        - vente de fruits ;
        - vente de miel ;
        - vente d'animaux ou de produits d'élevage.

        ### Calcul du montant

        Le montant d'une vente est calculé par :

        $$
        Montant =
        Quantité \\times Prix\\ unitaire
        $$

        Par exemple, si :

        - quantité = 100 kg ;
        - prix unitaire = 2 000 Ar ;

        alors :

        $$
        Montant =
        100 \\times 2\\,000
        =
        200\\,000\\ Ar
        $$

        ### Chiffre d'affaires

        Le chiffre d'affaires total correspond à :

        $$
        CA =
        \\sum_{i=1}^{n} Montant_i
        $$

        ### Marge

        Les revenus seront ensuite utilisés avec les dépenses
        pour calculer la marge de l'exploitation :

        $$
        Marge =
        Revenus - Dépenses
        $$

        Cette information sera exploitée dans le
        **Dashboard** et dans le module **Analytics**.
        """
    )

