"""
Repository Parcelle
===================

Gère l'accès aux données des parcelles dans la base SQLite
de VolyTrack.

Responsabilités :
    - créer une parcelle ;
    - récupérer une parcelle ;
    - récupérer toutes les parcelles ;
    - modifier une parcelle ;
    - supprimer une parcelle.
"""

from typing import Optional

from core.database.connection import get_connection
from core.models.parcelle import Parcelle


class ParcelleRepository:
    """
    Repository permettant de gérer les parcelles.

    Le repository fait le lien entre :

        Modèle Parcelle
              ↓
        SQLite
    """

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, parcelle: Parcelle) -> Parcelle:
        """
        Enregistre une nouvelle parcelle en base de données.

        Parameters
        ----------
        parcelle : Parcelle
            Parcelle à enregistrer.

        Returns
        -------
        Parcelle
            Parcelle enregistrée avec son identifiant.
        """

        if not isinstance(parcelle, Parcelle):
            raise TypeError(
                "parcelle doit être une instance de Parcelle."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

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
                    parcelle.nom,
                    parcelle.superficie,
                    parcelle.unite_superficie,
                    parcelle.localisation,
                    parcelle.description,
                ),
            )

            parcelle.id = cursor.lastrowid

            connection.commit()

            return parcelle

        finally:
            connection.close()

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_by_id(
        self,
        parcelle_id: int,
    ) -> Optional[Parcelle]:
        """
        Récupère une parcelle à partir de son identifiant.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.

        Returns
        -------
        Optional[Parcelle]
            La parcelle trouvée ou None.
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
                    nom,
                    superficie,
                    unite_superficie,
                    localisation,
                    description
                FROM parcelles
                WHERE id = ?
                """,
                (parcelle_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Parcelle(
                id=row["id"],
                nom=row["nom"],
                superficie=row["superficie"],
                unite_superficie=row["unite_superficie"],
                localisation=row["localisation"],
                description=row["description"],
            )

        finally:
            connection.close()

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all(self) -> list[Parcelle]:
        """
        Récupère toutes les parcelles.

        Returns
        -------
        list[Parcelle]
            Liste des parcelles.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    nom,
                    superficie,
                    unite_superficie,
                    localisation,
                    description
                FROM parcelles
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                Parcelle(
                    id=row["id"],
                    nom=row["nom"],
                    superficie=row["superficie"],
                    unite_superficie=row["unite_superficie"],
                    localisation=row["localisation"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, parcelle: Parcelle) -> Parcelle:
        """
        Modifie une parcelle existante.

        Parameters
        ----------
        parcelle : Parcelle
            Parcelle contenant les nouvelles données.

        Returns
        -------
        Parcelle
            Parcelle modifiée.

        Raises
        ------
        ValueError
            Si la parcelle ne possède pas d'identifiant ou
            si elle n'existe pas.
        """

        if not isinstance(parcelle, Parcelle):
            raise TypeError(
                "parcelle doit être une instance de Parcelle."
            )

        if parcelle.id is None:
            raise ValueError(
                "La parcelle doit posséder un identifiant "
                "pour être modifiée."
            )

        if not isinstance(parcelle.id, int):
            raise TypeError(
                "L'identifiant de la parcelle doit être un entier."
            )

        if parcelle.id <= 0:
            raise ValueError(
                "L'identifiant de la parcelle doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE parcelles
                SET
                    nom = ?,
                    superficie = ?,
                    unite_superficie = ?,
                    localisation = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    parcelle.nom,
                    parcelle.superficie,
                    parcelle.unite_superficie,
                    parcelle.localisation,
                    parcelle.description,
                    parcelle.id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune parcelle trouvée avec l'identifiant "
                    f"{parcelle.id}."
                )

            connection.commit()

            return parcelle

        finally:
            connection.close()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, parcelle_id: int) -> bool:
        """
        Supprime une parcelle.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.

        Returns
        -------
        bool
            True si la suppression a été effectuée.

        Raises
        ------
        ValueError
            Si aucune parcelle ne correspond à l'identifiant.
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
                DELETE FROM parcelles
                WHERE id = ?
                """,
                (parcelle_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune parcelle trouvée avec l'identifiant "
                    f"{parcelle_id}."
                )

            connection.commit()

            return True

        finally:
            connection.close()