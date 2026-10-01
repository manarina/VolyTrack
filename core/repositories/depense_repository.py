"""
Repository Depense
==================

Gère l'accès aux données des dépenses dans la base SQLite
de VolyTrack.

Relations :

    Parcelle
       │
       └── Depense
              │
              └── Culture (optionnelle)
"""

from typing import Optional

from core.database.connection import get_connection
from core.models.depense import Depense


class DepenseRepository:
    """
    Repository permettant de gérer les dépenses agricoles.
    """

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, depense: Depense) -> Depense:
        """
        Enregistre une nouvelle dépense.
        """

        if not isinstance(depense, Depense):
            raise TypeError(
                "depense doit être une instance de Depense."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

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
                    depense.parcelle_id,
                    depense.culture_id,
                    depense.categorie,
                    depense.montant,
                    depense.date_depense,
                    depense.description,
                ),
            )

            depense.id = cursor.lastrowid

            connection.commit()

            return depense

        finally:
            connection.close()

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_by_id(
        self,
        depense_id: int,
    ) -> Optional[Depense]:
        """
        Récupère une dépense par son identifiant.
        """

        if not isinstance(depense_id, int):
            raise TypeError(
                "L'identifiant de la dépense doit être un entier."
            )

        if depense_id <= 0:
            raise ValueError(
                "L'identifiant de la dépense doit être "
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
                    categorie,
                    montant,
                    date_depense,
                    description
                FROM depenses
                WHERE id = ?
                """,
                (depense_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Depense(
                id=row["id"],
                parcelle_id=row["parcelle_id"],
                culture_id=row["culture_id"],
                categorie=row["categorie"],
                montant=row["montant"],
                date_depense=row["date_depense"],
                description=row["description"],
            )

        finally:
            connection.close()

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all(self) -> list[Depense]:
        """
        Récupère toutes les dépenses.
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
                    categorie,
                    montant,
                    date_depense,
                    description
                FROM depenses
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                Depense(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
                    categorie=row["categorie"],
                    montant=row["montant"],
                    date_depense=row["date_depense"],
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
    ) -> list[Depense]:
        """
        Récupère toutes les dépenses d'une parcelle.
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
                    categorie,
                    montant,
                    date_depense,
                    description
                FROM depenses
                WHERE parcelle_id = ?
                ORDER BY id
                """,
                (parcelle_id,),
            )

            rows = cursor.fetchall()

            return [
                Depense(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
                    categorie=row["categorie"],
                    montant=row["montant"],
                    date_depense=row["date_depense"],
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
    ) -> list[Depense]:
        """
        Récupère toutes les dépenses associées à une culture.
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
                    categorie,
                    montant,
                    date_depense,
                    description
                FROM depenses
                WHERE culture_id = ?
                ORDER BY id
                """,
                (culture_id,),
            )

            rows = cursor.fetchall()

            return [
                Depense(
                    id=row["id"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
                    categorie=row["categorie"],
                    montant=row["montant"],
                    date_depense=row["date_depense"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, depense: Depense) -> Depense:
        """
        Modifie une dépense existante.
        """

        if not isinstance(depense, Depense):
            raise TypeError(
                "depense doit être une instance de Depense."
            )

        if depense.id is None:
            raise ValueError(
                "La dépense doit posséder un identifiant "
                "pour être modifiée."
            )

        if not isinstance(depense.id, int):
            raise TypeError(
                "L'identifiant de la dépense doit être un entier."
            )

        if depense.id <= 0:
            raise ValueError(
                "L'identifiant de la dépense doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE depenses
                SET
                    parcelle_id = ?,
                    culture_id = ?,
                    categorie = ?,
                    montant = ?,
                    date_depense = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    depense.parcelle_id,
                    depense.culture_id,
                    depense.categorie,
                    depense.montant,
                    depense.date_depense,
                    depense.description,
                    depense.id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune dépense trouvée avec l'identifiant "
                    f"{depense.id}."
                )

            connection.commit()

            return depense

        finally:
            connection.close()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, depense_id: int) -> bool:
        """
        Supprime une dépense.
        """

        if not isinstance(depense_id, int):
            raise TypeError(
                "L'identifiant de la dépense doit être un entier."
            )

        if depense_id <= 0:
            raise ValueError(
                "L'identifiant de la dépense doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM depenses
                WHERE id = ?
                """,
                (depense_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucune dépense trouvée avec l'identifiant "
                    f"{depense_id}."
                )

            connection.commit()

            return True

        finally:
            connection.close()

