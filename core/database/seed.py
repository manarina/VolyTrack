from core.database.connection import get_connection


# ============================================================
# DONNÉES DE DÉMONSTRATION
# ============================================================

def seed_database() -> None:
    """
    Insère des données de démonstration dans VolyTrack.

    Les données ne sont ajoutées que si la base est vide.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # ========================================================
    # VÉRIFICATION
    # ========================================================

    cursor.execute(
        "SELECT COUNT(*) FROM parcelles"
    )

    parcelle_count = cursor.fetchone()[0]

    if parcelle_count > 0:
        connection.close()
        return

    # ========================================================
    # PARCELLES
    # ========================================================

    cursor.execute(
        """
        INSERT INTO parcelles (
            nom,
            superficie,
            unite_superficie,
            localisation,
            description
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            "Parcelle Nord",
            1.5,
            "ha",
            "Zone Nord",
            "Parcelle principale de démonstration",
        ),
    )

    parcelle_1 = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO parcelles (
            nom,
            superficie,
            unite_superficie,
            localisation,
            description
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            "Parcelle Sud",
            0.8,
            "ha",
            "Zone Sud",
            "Deuxième parcelle de démonstration",
        ),
    )

    parcelle_2 = cursor.lastrowid

    # ========================================================
    # CULTURES
    # ========================================================

    cursor.execute(
        """
        INSERT INTO cultures (
            parcelle_id,
            nom,
            variete,
            date_semis,
            date_prevue_recolte,
            statut,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_1,
            "Riz",
            "Variété locale",
            "2026-09-01",
            "2027-01-15",
            "En croissance",
            "Culture de démonstration",
        ),
    )

    culture_1 = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO cultures (
            parcelle_id,
            nom,
            variete,
            date_semis,
            date_prevue_recolte,
            statut,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_2,
            "Tomate",
            "Roma",
            "2026-09-10",
            "2026-12-10",
            "En croissance",
            "Culture maraîchère de démonstration",
        ),
    )

    culture_2 = cursor.lastrowid

    # ========================================================
    # TRAVAUX
    # ========================================================

    cursor.execute(
        """
        INSERT INTO travaux (
            parcelle_id,
            culture_id,
            type_travail,
            date_travail,
            cout,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_1,
            culture_1,
            "Préparation du sol",
            "2026-08-25",
            150000,
            "Préparation avant semis",
        ),
    )

    cursor.execute(
        """
        INSERT INTO travaux (
            parcelle_id,
            culture_id,
            type_travail,
            date_travail,
            cout,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_2,
            culture_2,
            "Désherbage",
            "2026-09-20",
            50000,
            "Entretien de la culture",
        ),
    )

    # ========================================================
    # DÉPENSES
    # ========================================================

    cursor.execute(
        """
        INSERT INTO depenses (
            parcelle_id,
            culture_id,
            categorie,
            montant,
            date_depense,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_1,
            culture_1,
            "Semences",
            120000,
            "2026-09-01",
            "Achat de semences",
        ),
    )

    cursor.execute(
        """
        INSERT INTO depenses (
            parcelle_id,
            culture_id,
            categorie,
            montant,
            date_depense,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_2,
            culture_2,
            "Engrais",
            80000,
            "2026-09-15",
            "Achat d'engrais",
        ),
    )

    # ========================================================
    # RÉCOLTES
    # ========================================================

    cursor.execute(
        """
        INSERT INTO recoltes (
            culture_id,
            date_recolte,
            quantite,
            unite,
            qualite,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            culture_1,
            "2027-01-15",
            2500,
            "kg",
            "Bonne",
            "Récolte prévisionnelle de démonstration",
        ),
    )

    # ========================================================
    # REVENUS
    # ========================================================

    cursor.execute(
        """
        INSERT INTO revenus (
            parcelle_id,
            culture_id,
            produit,
            quantite,
            prix_unitaire,
            montant,
            date_revenu,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_1,
            culture_1,
            "Riz",
            2500,
            1500,
            3750000,
            "2027-01-20",
            "Vente prévisionnelle",
        ),
    )

    cursor.execute(
        """
        INSERT INTO revenus (
            parcelle_id,
            culture_id,
            produit,
            quantite,
            prix_unitaire,
            montant,
            date_revenu,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            parcelle_2,
            culture_2,
            "Tomate",
            800,
            2000,
            1600000,
            "2026-12-15",
            "Vente prévisionnelle",
        ),
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    connection.commit()

    connection.close()