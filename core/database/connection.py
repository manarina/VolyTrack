from pathlib import Path
import sqlite3


# ============================================================
# CONFIGURATION DE LA BASE DE DONNÉES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "volytrack.db"


# ============================================================
# PRÉPARATION DU DOSSIER DATA
# ============================================================

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONNEXION SQLITE
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Crée et retourne une connexion à la base SQLite VolyTrack.

    Returns:
        sqlite3.Connection: connexion active à SQLite.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
    )

    connection.row_factory = sqlite3.Row

    return connection