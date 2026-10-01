"""
Repository Culture
==================

Gère l'accès aux données des cultures dans la base SQLite
de VolyTrack.
"""

from typing import Optional

from core.database.connection import get_connection
from core.models.culture import Culture


class CultureRepository:
    """
    Repository permettant de gérer les cultures.

    Relation :

        Parcelle
            ↓
        Culture
            ↓
        parcelle_id
    """

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, culture: Culture) -> Culture:
        """
        Enregistre une nouvelle culture.

        Parameters
        ----------
        culture : Culture
            Culture à enregistrer.

        Returns
        -------
        Culture
            Culture enregistrée avec son identifiant.
        """

        if not isinstance(culture, Culture):
            raise TypeError(
                "culture doit être une instance de Culture."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

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
                    culture.parcelle_id,
                    culture.nom,
                    culture.variete,
                    culture.date_semis,
                    culture.date_prevue_recolte,
                    culture.statut,
                    culture.description,
                ),
            )

            culture.id = cursor.lastrowid

            connection.commit()

            return culture

        finally:
            connection.close()

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_by_id(
        self,
        culture_id: int,
    ) -> Optional[Culture]:
        """
        Récupère une culture par son identifiant.

        Parameters
        ----------
        culture_id : int
            Identifiant de la culture.

        Returns
        -------
        Optional[Culture]
            Culture trouvée ou None.
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
                    nom,
                    variete,
                    date_semis,
                    date_prevue_recolte,
                    statut,
                    description
                FROM cultures
                WHERE id = ?
                """,
                (culture_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Culture(
                id=row["id"],
                parcelle_id=row["parcelle_id"],
                nom=row["nom"],
                variete=row["variete"],
                date_semis=row["date_semis"],
                date_prevue_recolte=row["date_prevue_recolte"],
                statut=row["statut"],
                description=row["description"],
            )

        finally:
            connection.close()

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all(self) -> list[Culture]:
        """
        Récupère toutes les cultures.

        Returns
        -------
        list[Culture]
            Liste des cultures.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    parcelle_id,
                    nom,
                    variete,
                    date_semis,
                    date_prevue_recolte,
                    statut,
                    description
                FROM cultures
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                Culture(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    nom=row["nom"],
                    variete=row["variete"],
                    date_semis=row["date_semis"],
                    date_prevue_recolte=row[
                        "date_prevue_recolte"
                    ],
                    statut=row["statut"],
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
    ) -> list[Culture]:
        """
        Récupère toutes les cultures d'une parcelle.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.

        Returns
        -------
        list[Culture]
            Cultures associées à la parcelle.
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
                    nom,
                    variete,
                    date_semis,
                    date_prevue_recolte,
                    statut,
                    description
                FROM cultures
                WHERE parcelle_id = ?
                ORDER BY id
                """,
                (parcelle_id,),
            )

            rows = cursor.fetchall()

            return [
                Culture(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    nom=row["nom"],
                    variete=row["variete"],
                    date_semis=row["date_semis"],
                    date_prevue_recolte=row[
                        "date_prevue_recolte"
                    ],
                    statut=row["statut"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, culture: Culture) -> Culture:
        """
        Modifie une culture existante.

        Parameters
        ----------
        culture : Culture
            Culture contenant les nouvelles données.

        Returns
        -------
        Culture
            Culture modifiée.
        """

        if not isinstance(culture, Culture):
            raise TypeError(
                "culture doit être une instance de Culture."
            )

        if culture.id is None:
            raise ValueError(
                "La culture doit posséder un identifiant "
                "pour être modifiée."
            )

        if not isinstance(culture.id, int):
            raise TypeError(
                "L'identifiant de la culture doit être un entier."
            )

        if culture.id <= 0:
            raise ValueError(
                "L'identifiant de la culture doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE cultures
                SET
                    parcelle_id = ?,
                    nom = ?,
                    variete = ?,
                    date_semis = ?,
                    date_prevue_recolte = ?,
                    statut = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    culture.parcelle_id,
                    culture.nom,
                    culture.variete,
                    culture.date_semis,
                    culture.date_prevue_recolte,
                    culture.statut,
                    culture.description,
                    culture.id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune culture trouvée avec l'identifiant "
                    f"{culture.id}."
                )

            connection.commit()

            return culture

        finally:
            connection.close()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, culture_id: int) -> bool:
        """
        Supprime une culture.

        Parameters
        ----------
        culture_id : int
            Identifiant de la culture.

        Returns
        -------
        bool
            True si la suppression a été effectuée.
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
                DELETE FROM cultures
                WHERE id = ?
                """,
                (culture_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune culture trouvée avec l'identifiant "
                    f"{culture_id}."
                )

            connection.commit()

            return True

        finally:
            connection.close()