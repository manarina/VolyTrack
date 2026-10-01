"""
Repository Revenu
=================

Gère l'accès aux données des revenus dans la base SQLite
de VolyTrack.

Relations :

    Parcelle
       │
       └── Revenu
              │
              └── Culture (optionnelle)
"""

from typing import Optional

from core.database.connection import get_connection
from core.models.revenu import Revenu


class RevenuRepository:
    """
    Repository permettant de gérer les revenus agricoles.
    """

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, revenu: Revenu) -> Revenu:
        """
        Enregistre un nouveau revenu.
        """

        if not isinstance(revenu, Revenu):
            raise TypeError(
                "revenu doit être une instance de Revenu."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO revenus (
                    produit,
                    quantite,
                    prix_unitaire,
                    montant,
                    date_revenu,
                    parcelle_id,
                    culture_id,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    revenu.produit,
                    revenu.quantite,
                    revenu.prix_unitaire,
                    revenu.montant,
                    revenu.date_revenu,
                    revenu.parcelle_id,
                    revenu.culture_id,
                    revenu.description,
                ),
            )

            revenu.id = cursor.lastrowid

            connection.commit()

            return revenu

        finally:
            connection.close()

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_by_id(
        self,
        revenu_id: int,
    ) -> Optional[Revenu]:
        """
        Récupère un revenu par son identifiant.
        """

        if not isinstance(revenu_id, int):
            raise TypeError(
                "L'identifiant du revenu doit être un entier."
            )

        if revenu_id <= 0:
            raise ValueError(
                "L'identifiant du revenu doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    produit,
                    quantite,
                    prix_unitaire,
                    montant,
                    date_revenu,
                    parcelle_id,
                    culture_id,
                    description
                FROM revenus
                WHERE id = ?
                """,
                (revenu_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Revenu(
                id=row["id"],
                produit=row["produit"],
                quantite=row["quantite"],
                prix_unitaire=row["prix_unitaire"],
                montant=row["montant"],
                date_revenu=row["date_revenu"],
                parcelle_id=row["parcelle_id"],
                culture_id=row["culture_id"],
                description=row["description"],
            )

        finally:
            connection.close()

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all(self) -> list[Revenu]:
        """
        Récupère tous les revenus.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    produit,
                    quantite,
                    prix_unitaire,
                    montant,
                    date_revenu,
                    parcelle_id,
                    culture_id,
                    description
                FROM revenus
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                Revenu(
                    id=row["id"],
                    produit=row["produit"],
                    quantite=row["quantite"],
                    prix_unitaire=row["prix_unitaire"],
                    montant=row["montant"],
                    date_revenu=row["date_revenu"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
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
    ) -> list[Revenu]:
        """
        Récupère tous les revenus associés à une parcelle.
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
                    produit,
                    quantite,
                    prix_unitaire,
                    montant,
                    date_revenu,
                    parcelle_id,
                    culture_id,
                    description
                FROM revenus
                WHERE parcelle_id = ?
                ORDER BY id
                """,
                (parcelle_id,),
            )

            rows = cursor.fetchall()

            return [
                Revenu(
                    id=row["id"],
                    produit=row["produit"],
                    quantite=row["quantite"],
                    prix_unitaire=row["prix_unitaire"],
                    montant=row["montant"],
                    date_revenu=row["date_revenu"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
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
    ) -> list[Revenu]:
        """
        Récupère tous les revenus associés à une culture.
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
                    produit,
                    quantite,
                    prix_unitaire,
                    montant,
                    date_revenu,
                    parcelle_id,
                    culture_id,
                    description
                FROM revenus
                WHERE culture_id = ?
                ORDER BY id
                """,
                (culture_id,),
            )

            rows = cursor.fetchall()

            return [
                Revenu(
                    id=row["id"],
                    produit=row["produit"],
                    quantite=row["quantite"],
                    prix_unitaire=row["prix_unitaire"],
                    montant=row["montant"],
                    date_revenu=row["date_revenu"],
                    parcelle_id=row["parcelle_id"],
                    culture_id=row["culture_id"],
                    description=row["description"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, revenu: Revenu) -> Revenu:
        """
        Modifie un revenu existant.
        """

        if not isinstance(revenu, Revenu):
            raise TypeError(
                "revenu doit être une instance de Revenu."
            )

        if revenu.id is None:
            raise ValueError(
                "Le revenu doit posséder un identifiant "
                "pour être modifié."
            )

        if not isinstance(revenu.id, int):
            raise TypeError(
                "L'identifiant du revenu doit être un entier."
            )

        if revenu.id <= 0:
            raise ValueError(
                "L'identifiant du revenu doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE revenus
                SET
                    produit = ?,
                    quantite = ?,
                    prix_unitaire = ?,
                    montant = ?,
                    date_revenu = ?,
                    parcelle_id = ?,
                    culture_id = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    revenu.produit,
                    revenu.quantite,
                    revenu.prix_unitaire,
                    revenu.montant,
                    revenu.date_revenu,
                    revenu.parcelle_id,
                    revenu.culture_id,
                    revenu.description,
                    revenu.id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucun revenu trouvé avec l'identifiant "
                    f"{revenu.id}."
                )

            connection.commit()

            return revenu

        finally:
            connection.close()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, revenu_id: int) -> bool:
        """
        Supprime un revenu.
        """

        if not isinstance(revenu_id, int):
            raise TypeError(
                "L'identifiant du revenu doit être un entier."
            )

        if revenu_id <= 0:
            raise ValueError(
                "L'identifiant du revenu doit être "
                "strictement positif."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM revenus
                WHERE id = ?
                """,
                (revenu_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Aucun revenu trouvé avec l'identifiant "
                    f"{revenu_id}."
                )

            connection.commit()

            return True

        finally:
            connection.close()

