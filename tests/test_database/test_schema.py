from core.database.connection import get_connection
from core.database.schema import initialize_database


# ============================================================
# CONFIGURATION
# ============================================================

EXPECTED_TABLES = {
    "parcelles",
    "cultures",
    "travaux",
    "depenses",
    "revenus",
    "recoltes",
}


# ============================================================
# FIXTURE SIMPLE
# ============================================================

def setup_database():
    """
    Initialise la base avant chaque test.
    """

    initialize_database()


# ============================================================
# TEST CRÉATION DES TABLES
# ============================================================

def test_all_expected_tables_exist():
    """
    Vérifie que toutes les tables principales
    de VolyTrack existent.
    """

    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

        existing_tables = {
            row[0]
            for row in rows
        }

        assert EXPECTED_TABLES.issubset(
            existing_tables
        )

    finally:
        connection.close()


# ============================================================
# TEST TABLE PARCELLES
# ============================================================

def test_parcelles_table_structure():
    """
    Vérifie les colonnes principales de la table parcelles.
    """

    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            "PRAGMA table_info(parcelles)"
        ).fetchall()

        columns = {
            row[1]
            for row in rows
        }

        expected_columns = {
            "id",
            "nom",
            "superficie",
            "unite_superficie",
            "localisation",
            "description",
            "created_at",
        }

        assert expected_columns.issubset(
            columns
        )

    finally:
        connection.close()


# ============================================================
# TEST TABLE CULTURES
# ============================================================

def test_cultures_table_structure():
    """
    Vérifie les colonnes principales de la table cultures.
    """

    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            "PRAGMA table_info(cultures)"
        ).fetchall()

        columns = {
            row[1]
            for row in rows
        }

        expected_columns = {
            "id",
            "parcelle_id",
            "nom",
            "variete",
            "date_semis",
            "date_prevue_recolte",
            "statut",
            "description",
            "created_at",
        }

        assert expected_columns.issubset(
            columns
        )

    finally:
        connection.close()


# ============================================================
# TEST TABLE TRAVAUX
# ============================================================

def test_travaux_table_structure():
    """
    Vérifie les colonnes principales de la table travaux.
    """

    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            "PRAGMA table_info(travaux)"
        ).fetchall()

        columns = {
            row[1]
            for row in rows
        }

        expected_columns = {
            "id",
            "parcelle_id",
            "culture_id",
            "type_travail",
            "date_travail",
            "cout",
            "description",
            "created_at",
        }

        assert expected_columns.issubset(
            columns
        )

    finally:
        connection.close()


# ============================================================
# TEST TABLE DEPENSES
# ============================================================

def test_depenses_table_structure():
    """
    Vérifie les colonnes principales de la table depenses.
    """

    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            "PRAGMA table_info(depenses)"
        ).fetchall()

        columns = {
            row[1]
            for row in rows
        }

        expected_columns = {
            "id",
            "parcelle_id",
            "culture_id",
            "categorie",
            "montant",
            "date_depense",
            "description",
            "created_at",
        }

        assert expected_columns.issubset(
            columns
        )

    finally:
        connection.close()


# ============================================================
# TEST TABLE REVENUS
# ============================================================

def test_revenus_table_structure():
    """
    Vérifie les colonnes principales de la table revenus.
    """

    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            "PRAGMA table_info(revenus)"
        ).fetchall()

        columns = {
            row[1]
            for row in rows
        }

        expected_columns = {
            "id",
            "parcelle_id",
            "culture_id",
            "produit",
            "quantite",
            "prix_unitaire",
            "montant",
            "date_revenu",
            "description",
            "created_at",
        }

        assert expected_columns.issubset(
            columns
        )

    finally:
        connection.close()


# ============================================================
# TEST TABLE RECOLTES
# ============================================================

def test_recoltes_table_structure():
    """
    Vérifie les colonnes principales de la table recoltes.
    """

    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            "PRAGMA table_info(recoltes)"
        ).fetchall()

        columns = {
            row[1]
            for row in rows
        }

        expected_columns = {
            "id",
            "culture_id",
            "date_recolte",
            "quantite",
            "unite",
            "qualite",
            "description",
            "created_at",
        }

        assert expected_columns.issubset(
            columns
        )

    finally:
        connection.close()


# ============================================================
# TEST INSERTION PARCELLE
# ============================================================

def test_insert_parcelle():
    """
    Vérifie qu'une parcelle peut être insérée
    et récupérée depuis SQLite.
    """

    setup_database()

    connection = get_connection()

    try:
        cursor = connection.execute(
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
                "Parcelle Test",
                1.5,
                "ha",
                "Zone Test",
                "Test automatique",
            ),
        )

        connection.commit()

        parcelle_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT *
            FROM parcelles
            WHERE id = ?
            """,
            (parcelle_id,),
        ).fetchone()

        assert row is not None
        assert row["nom"] == "Parcelle Test"
        assert row["superficie"] == 1.5

    finally:
        connection.close()


# ============================================================
# TEST INITIALISATION RÉPÉTÉE
# ============================================================

def test_initialize_database_is_idempotent():
    """
    Vérifie que l'initialisation peut être exécutée
    plusieurs fois sans erreur.
    """

    initialize_database()
    initialize_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

        existing_tables = {
            row[0]
            for row in rows
        }

        assert EXPECTED_TABLES.issubset(
            existing_tables
        )

    finally:
        connection.close()