from core.database.connection import get_connection


# ============================================================
# CRÉATION DU SCHÉMA
# ============================================================

def create_tables() -> None:
    """
    Crée toutes les tables nécessaires à VolyTrack.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # ========================================================
    # PARCELLES
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS parcelles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            superficie REAL NOT NULL,
            unite_superficie TEXT NOT NULL DEFAULT 'ha',
            localisation TEXT,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # ========================================================
    # CULTURES
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cultures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parcelle_id INTEGER NOT NULL,
            nom TEXT NOT NULL,
            variete TEXT,
            date_semis TEXT,
            date_prevue_recolte TEXT,
            statut TEXT NOT NULL DEFAULT 'Planifiée',
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (parcelle_id)
                REFERENCES parcelles(id)
                ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # TRAVAUX
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS travaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parcelle_id INTEGER NOT NULL,
            culture_id INTEGER,
            type_travail TEXT NOT NULL,
            date_travail TEXT NOT NULL,
            cout REAL NOT NULL DEFAULT 0,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (parcelle_id)
                REFERENCES parcelles(id)
                ON DELETE CASCADE,

            FOREIGN KEY (culture_id)
                REFERENCES cultures(id)
                ON DELETE SET NULL
        )
        """
    )

    # ========================================================
    # DÉPENSES
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS depenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parcelle_id INTEGER,
            culture_id INTEGER,
            categorie TEXT NOT NULL,
            montant REAL NOT NULL,
            date_depense TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (parcelle_id)
                REFERENCES parcelles(id)
                ON DELETE SET NULL,

            FOREIGN KEY (culture_id)
                REFERENCES cultures(id)
                ON DELETE SET NULL
        )
        """
    )

    # ========================================================
    # REVENUS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS revenus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parcelle_id INTEGER,
            culture_id INTEGER,
            produit TEXT NOT NULL,
            quantite REAL NOT NULL,
            prix_unitaire REAL NOT NULL,
            montant REAL NOT NULL,
            date_revenu TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (parcelle_id)
                REFERENCES parcelles(id)
                ON DELETE SET NULL,

            FOREIGN KEY (culture_id)
                REFERENCES cultures(id)
                ON DELETE SET NULL
        )
        """
    )

    # ========================================================
    # RÉCOLTES
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recoltes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            culture_id INTEGER NOT NULL,
            date_recolte TEXT NOT NULL,
            quantite REAL NOT NULL,
            unite TEXT NOT NULL,
            qualite TEXT,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (culture_id)
                REFERENCES cultures(id)
                ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    connection.commit()

    connection.close()
    
   
# ============================================================
# INITIALISATION COMPLÈTE
# ============================================================

def initialize_database() -> None:
    """
    Initialise la base de données VolyTrack.
    """

    create_tables() 