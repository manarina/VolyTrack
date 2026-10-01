import sqlite3

from core.database.connection import (
    DATABASE_PATH,
    get_connection,
)


# ============================================================
# TEST CONNEXION
# ============================================================

def test_database_path_exists():
    """
    Vérifie que le chemin de la base SQLite est correctement défini.
    """

    assert DATABASE_PATH.name == "volytrack.db"


def test_get_connection_returns_sqlite_connection():
    """
    Vérifie que get_connection() retourne bien
    une connexion SQLite.
    """

    connection = get_connection()

    try:
        assert isinstance(
            connection,
            sqlite3.Connection,
        )

    finally:
        connection.close()


def test_connection_can_execute_query():
    """
    Vérifie que la connexion peut exécuter
    une requête SQLite simple.
    """

    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT 1"
        )

        result = cursor.fetchone()[0]

        assert result == 1

    finally:
        connection.close()