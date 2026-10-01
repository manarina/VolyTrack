
"""
Repository Travail
==================

Gère l'accès aux données des travaux agricoles dans
la base SQLite de VolyTrack.

Relations :

    Parcelle
       │
       └── Travail
              │
              └── Culture (optionnelle)
"""

from typing import Optional

from core.database.connection import get_connection
from core.models.travail import Travail


class TravailRepository:
    """
    Repository permettant de gérer les travaux agricoles.
    """

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, travail: Travail) -> Travail:
        """
        Enregistre un nouveau travail.

        Parameters
        ----------
        travail : Travail
            Travail à enregistrer.

        Returns
        -------
        Travail
            Travail enregistré avec son identifiant.
        """

        if not isinstance(travail, Travail):
            raise TypeError(
                "travail doit être une instance de Travail."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

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
                    travail.parcelle_id,
                    travail.culture_id,
                    travail.type_travail,
                    travail.date_travail,
                    travail.cout,
                    travail.description,
                ),
            )

            travail.id = cursor.lastrowid

            connection.commit()

            return travail

        finally:
            connection.close()

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_by_id(
        self,
        travail_id: int,
    ) -> Optional[Travail]:
        """
        Récupère un travail par son identifiant.

        Parameters
        ----------
        travail_id : int
            Identifiant du travail.

        Returns
        -------
        Optional[Travail]
            Travail trouvé ou None.
        """

        if not isinstance(travail_id, int):
            raise TypeError(
                "L'identifiant du travail doit être un entier."
            )

        if travail_id <= 0:
            raise ValueError(
                "L'identifiant du travail doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    parcelle_id,
                    culture_id,
                    type_travail,
                    date_travail,
                    cout,
                    description
                FROM travaux
                WHERE id = ?
                """,
                (travail_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Travail(
                id=row["id"],
                parcelle_id=row["parcelle_id"],
                culture_id=row["culture_id"],
                type_travail=row["type_travail"],
                date_travail=row["date_travail"],
                cout=row["cout"],
                description=row["description"],
            )

        finally:
            connection.close()

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all(self) -> list[Travail]:
        """
        Récupère tous les travaux.

        Returns
        -------
        list[Travail]
            Liste des travaux.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    parcelle_id,
                    culture_id,
                    type_travail,
                    date_travail,
                    cout,
                    description
                FROM travaux
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                Travail(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
                    type_travail=row["type_travail"],
                    date_travail=row["date_travail"],
                    cout=row["cout"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # GET BY PARCELLE
    # ========================================================

    def get_by_parcelle_id(
        self,
        parcelle_id: int,
    ) -> list[Travail]:
        """
        Récupère tous les travaux d'une parcelle.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.

        Returns
        -------
        list[Travail]
            Travaux associés à la parcelle.
        """

        if not isinstance(parcelle_id, int):
            raise TypeError(
                "L'identifiant de la parcelle doit être un entier."
            )

        if parcelle_id <= 0:
            raise ValueError(
                "L'identifiant de la parcelle doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    parcelle_id,
                    culture_id,
                    type_travail,
                    date_travail,
                    cout,
                    description
                FROM travaux
                WHERE parcelle_id = ?
                ORDER BY id
                """,
                (parcelle_id,),
            )

            rows = cursor.fetchall()

            return [
                Travail(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
                    type_travail=row["type_travail"],
                    date_travail=row["date_travail"],
                    cout=row["cout"],
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
    ) -> list[Travail]:
        """
        Récupère tous les travaux associés à une culture.

        Parameters
        ----------
        culture_id : int
            Identifiant de la culture.

        Returns
        -------
        list[Travail]
            Travaux associés à la culture.
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
                    parcelle_id,
                    culture_id,
                    type_travail,
                    date_travail,
                    cout,
                    description
                FROM travaux
                WHERE culture_id = ?
                ORDER BY id
                """,
                (culture_id,),
            )

            rows = cursor.fetchall()

            return [
                Travail(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
                    type_travail=row["type_travail"],
                    date_travail=row["date_travail"],
                    cout=row["cout"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, travail: Travail) -> Travail:
        """
        Modifie un travail existant.

        Parameters
        ----------
        travail : Travail
            Travail contenant les nouvelles données.

        Returns
        -------
        Travail
            Travail modifié.
        """

        if not isinstance(travail, Travail):
            raise TypeError(
                "travail doit être une instance de Travail."
            )

        if travail.id is None:
            raise ValueError(
                "Le travail doit posséder un identifiant "
                "pour être modifié."
            )

        if not isinstance(travail.id, int):
            raise TypeError(
                "L'identifiant du travail doit être un entier."
            )

        if travail.id <= 0:
            raise ValueError(
                "L'identifiant du travail doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE travaux
                SET
                    parcelle_id = ?,
                    culture_id = ?,
                    type_travail = ?,
                    date_travail = ?,
                    cout = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    travail.parcelle_id,
                    travail.culture_id,
                    travail.type_travail,
                    travail.date_travail,
                    travail.cout,
                    travail.description,
                    travail.id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucun travail trouvé avec l'identifiant "
                    f"{travail.id}."
                )

            connection.commit()

            return travail

        finally:
            connection.close()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, travail_id: int) -> bool:
        """
        Supprime un travail.

        Parameters
        ----------
        travail_id : int
            Identifiant du travail.

        Returns
        -------
        bool
            True si la suppression a été effectuée.
        """

        if not isinstance(travail_id, int):
            raise TypeError(
                "L'identifiant du travail doit être un entier."
            )

        if travail_id <= 0:
            raise ValueError(
                "L'identifiant du travail doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM travaux
                WHERE id = ?
                """,
                (travail_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucun travail trouvé avec l'identifiant "
                    f"{travail_id}."
                )

            connection.commit()

            return True

        finally:
            connection.close()

