"""
Repository Recolte
==================

Gère l'accès aux données des récoltes dans la base SQLite
de VolyTrack.

Relation :

    Parcelle
       │
       └── Culture
              │
              └── Recolte
                     │
                     └── culture_id
"""

from typing import Optional

from core.database.connection import get_connection
from core.models.recolte import Recolte


class RecolteRepository:
    """
    Repository permettant de gérer les récoltes agricoles.
    """

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, recolte: Recolte) -> Recolte:
        """
        Enregistre une nouvelle récolte.
        """

        if not isinstance(recolte, Recolte):
            raise TypeError(
                "recolte doit être une instance de Recolte."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

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
                    recolte.culture_id,
                    recolte.date_recolte,
                    recolte.quantite,
                    recolte.unite,
                    recolte.qualite,
                    recolte.description,
                ),
            )

            recolte.id = cursor.lastrowid

            connection.commit()

            return recolte

        finally:
            connection.close()

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_by_id(
        self,
        recolte_id: int,
    ) -> Optional[Recolte]:
        """
        Récupère une récolte par son identifiant.
        """

        if not isinstance(recolte_id, int):
            raise TypeError(
                "L'identifiant de la récolte doit être un entier."
            )

        if recolte_id <= 0:
            raise ValueError(
                "L'identifiant de la récolte doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    culture_id,
                    date_recolte,
                    quantite,
                    unite,
                    qualite,
                    description
                FROM recoltes
                WHERE id = ?
                """,
                (recolte_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Recolte(
                id=row["id"],
                culture_id=row["culture_id"],
                date_recolte=row["date_recolte"],
                quantite=row["quantite"],
                unite=row["unite"],
                qualite=row["qualite"],
                description=row["description"],
            )

        finally:
            connection.close()

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all(self) -> list[Recolte]:
        """
        Récupère toutes les récoltes.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    culture_id,
                    date_recolte,
                    quantite,
                    unite,
                    qualite,
                    description
                FROM recoltes
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                Recolte(
                    id=row["id"],
                    culture_id=row["culture_id"],
                    date_recolte=row["date_recolte"],
                    quantite=row["quantite"],
                    unite=row["unite"],
                    qualite=row["qualite"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # GET BY CULTURE
    # ========================================================

    def get_by_culture_id(
        self,
        culture_id: int,
    ) -> list[Recolte]:
        """
        Récupère toutes les récoltes associées à une culture.
        """

        if not isinstance(culture_id, int):
            raise TypeError(
                "L'identifiant de la culture doit être un entier."
            )

        if culture_id <= 0:
            raise ValueError(
                "L'identifiant de la culture doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    culture_id,
                    date_recolte,
                    quantite,
                    unite,
                    qualite,
                    description
                FROM recoltes
                WHERE culture_id = ?
                ORDER BY id
                """,
                (culture_id,),
            )

            rows = cursor.fetchall()

            return [
                Recolte(
                    id=row["id"],
                    culture_id=row["culture_id"],
                    date_recolte=row["date_recolte"],
                    quantite=row["quantite"],
                    unite=row["unite"],
                    qualite=row["qualite"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, recolte: Recolte) -> Recolte:
        """
        Modifie une récolte existante.
        """

        if not isinstance(recolte, Recolte):
            raise TypeError(
                "recolte doit être une instance de Recolte."
            )

        if recolte.id is None:
            raise ValueError(
                "La récolte doit posséder un identifiant "
                "pour être modifiée."
            )

        if not isinstance(recolte.id, int):
            raise TypeError(
                "L'identifiant de la récolte doit être un entier."
            )

        if recolte.id <= 0:
            raise ValueError(
                "L'identifiant de la récolte doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE recoltes
                SET
                    culture_id = ?,
                    date_recolte = ?,
                    quantite = ?,
                    unite = ?,
                    qualite = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    recolte.culture_id,
                    recolte.date_recolte,
                    recolte.quantite,
                    recolte.unite,
                    recolte.qualite,
                    recolte.description,
                    recolte.id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune récolte trouvée avec l'identifiant "
                    f"{recolte.id}."
                )

            connection.commit()

            return recolte

        finally:
            connection.close()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, recolte_id: int) -> bool:
        """
        Supprime une récolte.
        """

        if not isinstance(recolte_id, int):
            raise TypeError(
                "L'identifiant de la récolte doit être un entier."
            )

        if recolte_id <= 0:
            raise ValueError(
                "L'identifiant de la récolte doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM recoltes
                WHERE id = ?
                """,
                (recolte_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune récolte trouvée avec l'identifiant "
                    f"{recolte_id}."
                )

            connection.commit()

            return True

        finally:
            connection.close()

