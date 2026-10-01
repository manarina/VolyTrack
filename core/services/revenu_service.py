"""
Service métier pour la gestion des revenus.

Responsabilités :
- validation des revenus ;
- création ;
- consultation ;
- modification ;
- suppression ;
- recherche ;
- vérification des parcelles ;
- vérification des cultures ;
- vérification de la cohérence culture / parcelle ;
- vérification de la cohérence :
      montant = quantite × prix_unitaire.
"""

from __future__ import annotations

from math import isclose
from typing import Optional

from core.models.revenu import Revenu

from core.repositories.revenu_repository import (
    RevenuRepository,
)

from core.repositories.parcelle_repository import (
    ParcelleRepository,
)

from core.repositories.culture_repository import (
    CultureRepository,
)


class RevenuService:
    """
    Service métier de gestion des revenus.
    """

    # ========================================================
    # INITIALISATION
    # ========================================================

    def __init__(
        self,
        repository: Optional[RevenuRepository] = None,
        parcelle_repository: Optional[ParcelleRepository] = None,
        culture_repository: Optional[CultureRepository] = None,
    ) -> None:

        if repository is None:
            repository = RevenuRepository()

        if parcelle_repository is None:
            parcelle_repository = ParcelleRepository()

        if culture_repository is None:
            culture_repository = CultureRepository()

        if not isinstance(
            repository,
            RevenuRepository,
        ):
            raise TypeError(
                "repository doit être une instance "
                "de RevenuRepository."
            )

        if not isinstance(
            parcelle_repository,
            ParcelleRepository,
        ):
            raise TypeError(
                "parcelle_repository doit être une instance "
                "de ParcelleRepository."
            )

        if not isinstance(
            culture_repository,
            CultureRepository,
        ):
            raise TypeError(
                "culture_repository doit être une instance "
                "de CultureRepository."
            )

        self.repository = repository
        self.parcelle_repository = parcelle_repository
        self.culture_repository = culture_repository

    # ========================================================
    # CREATE
    # ========================================================

    def create_revenu(
        self,
        revenu: Revenu,
    ) -> Revenu:
        """
        Crée un nouveau revenu après validation métier.
        """

        if not isinstance(
            revenu,
            Revenu,
        ):
            raise TypeError(
                "revenu doit être une instance de Revenu."
            )

        self.validate_revenu(revenu)

        # ----------------------------------------------------
        # PARCELLE
        # ----------------------------------------------------

        if revenu.parcelle_id is not None:

            if not self.parcelle_exists(
                revenu.parcelle_id
            ):
                raise ValueError(
                    "Aucune parcelle trouvée avec "
                    f"l'identifiant {revenu.parcelle_id}."
                )

        # ----------------------------------------------------
        # CULTURE
        # ----------------------------------------------------

        self._validate_culture_relationship(
            revenu
        )

        return self.repository.create(
            revenu
        )

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_revenu(
        self,
        revenu_id: int,
    ) -> Optional[Revenu]:
        """
        Retourne un revenu par son identifiant.
        """

        self._validate_id(
            revenu_id
        )

        return self.repository.get_by_id(
            revenu_id
        )

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all_revenus(
        self,
    ) -> list[Revenu]:
        """
        Retourne tous les revenus.
        """

        return self.repository.get_all()

    # ========================================================
    # GET BY PARCELLE
    # ========================================================

    def get_revenus_by_parcelle(
        self,
        parcelle_id: int,
    ) -> list[Revenu]:
        """
        Retourne les revenus associés à une parcelle.
        """

        self._validate_parcelle_id(
            parcelle_id
        )

        return self.repository.get_by_parcelle_id(
            parcelle_id
        )

    # ========================================================
    # GET BY CULTURE
    # ========================================================

    def get_revenus_by_culture(
        self,
        culture_id: int,
    ) -> list[Revenu]:
        """
        Retourne les revenus associés à une culture.
        """

        self._validate_culture_id(
            culture_id
        )

        return self.repository.get_by_culture_id(
            culture_id
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update_revenu(
        self,
        revenu: Revenu,
    ) -> Revenu:
        """
        Modifie un revenu existant.
        """

        if not isinstance(
            revenu,
            Revenu,
        ):
            raise TypeError(
                "revenu doit être une instance de Revenu."
            )

        if revenu.id is None:
            raise ValueError(
                "Le revenu doit posséder un identifiant "
                "pour être modifié."
            )

        self._validate_id(
            revenu.id
        )

        self.validate_revenu(
            revenu
        )

        # ----------------------------------------------------
        # PARCELLE
        # ----------------------------------------------------

        if revenu.parcelle_id is not None:

            if not self.parcelle_exists(
                revenu.parcelle_id
            ):
                raise ValueError(
                    "Aucune parcelle trouvée avec "
                    f"l'identifiant {revenu.parcelle_id}."
                )

        # ----------------------------------------------------
        # CULTURE
        # ----------------------------------------------------

        self._validate_culture_relationship(
            revenu
        )

        return self.repository.update(
            revenu
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_revenu(
        self,
        revenu_id: int,
    ) -> bool:
        """
        Supprime un revenu.
        """

        self._validate_id(
            revenu_id
        )

        return self.repository.delete(
            revenu_id
        )

    # ========================================================
    # EXISTS
    # ========================================================

    def revenu_exists(
        self,
        revenu_id: int,
    ) -> bool:
        """
        Vérifie si un revenu existe.
        """

        self._validate_id(
            revenu_id
        )

        return (
            self.repository.get_by_id(
                revenu_id
            )
            is not None
        )

    # ========================================================
    # PARCELLE EXISTS
    # ========================================================

    def parcelle_exists(
        self,
        parcelle_id: int,
    ) -> bool:
        """
        Vérifie si une parcelle existe.
        """

        self._validate_parcelle_id(
            parcelle_id
        )

        return (
            self.parcelle_repository.get_by_id(
                parcelle_id
            )
            is not None
        )

    # ========================================================
    # CULTURE EXISTS
    # ========================================================

    def culture_exists(
        self,
        culture_id: int,
    ) -> bool:
        """
        Vérifie si une culture existe.
        """

        self._validate_culture_id(
            culture_id
        )

        return (
            self.culture_repository.get_by_id(
                culture_id
            )
            is not None
        )

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_revenu(
        self,
        revenu: Revenu,
    ) -> bool:
        """
        Effectue les validations métier d'un revenu.
        """

        if not isinstance(
            revenu,
            Revenu,
        ):
            raise TypeError(
                "revenu doit être une instance de Revenu."
            )

        # ----------------------------------------------------
        # PRODUIT
        # ----------------------------------------------------

        if not isinstance(
            revenu.produit,
            str,
        ):
            raise TypeError(
                "Le produit du revenu doit être une chaîne."
            )

        if not revenu.produit.strip():
            raise ValueError(
                "Le produit du revenu ne doit pas être vide."
            )

        # ----------------------------------------------------
        # QUANTITÉ
        # ----------------------------------------------------

        if not isinstance(
            revenu.quantite,
            (int, float),
        ):
            raise TypeError(
                "La quantité du revenu doit être numérique."
            )

        if revenu.quantite <= 0:
            raise ValueError(
                "La quantité du revenu doit être "
                "strictement positive."
            )

        # ----------------------------------------------------
        # PRIX UNITAIRE
        # ----------------------------------------------------

        if not isinstance(
            revenu.prix_unitaire,
            (int, float),
        ):
            raise TypeError(
                "Le prix unitaire du revenu doit être numérique."
            )

        if revenu.prix_unitaire < 0:
            raise ValueError(
                "Le prix unitaire du revenu "
                "ne peut pas être négatif."
            )

        # ----------------------------------------------------
        # MONTANT
        # ----------------------------------------------------

        if not isinstance(
            revenu.montant,
            (int, float),
        ):
            raise TypeError(
                "Le montant du revenu doit être numérique."
            )

        if revenu.montant < 0:
            raise ValueError(
                "Le montant du revenu ne peut pas être négatif."
            )

        # ----------------------------------------------------
        # COHÉRENCE MONTANT
        # ----------------------------------------------------

        expected_amount = (
            revenu.quantite
            * revenu.prix_unitaire
        )

        if not isclose(
            float(revenu.montant),
            float(expected_amount),
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):
            raise ValueError(
                "Le montant du revenu doit être égal à "
                "la quantité multipliée par le prix unitaire."
            )

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if not isinstance(
            revenu.date_revenu,
            str,
        ):
            raise TypeError(
                "La date du revenu doit être une chaîne."
            )

        if not revenu.date_revenu.strip():
            raise ValueError(
                "La date du revenu ne doit pas être vide."
            )

        # ----------------------------------------------------
        # PARCELLE
        # ----------------------------------------------------

        if revenu.parcelle_id is not None:

            self._validate_parcelle_id(
                revenu.parcelle_id
            )

        # ----------------------------------------------------
        # CULTURE
        # ----------------------------------------------------

        if revenu.culture_id is not None:

            self._validate_culture_id(
                revenu.culture_id
            )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        if revenu.description is not None:

            if not isinstance(
                revenu.description,
                str,
            ):
                raise TypeError(
                    "La description du revenu "
                    "doit être une chaîne."
                )

        return True

    # ========================================================
    # RELATION CULTURE / PARCELLE
    # ========================================================

    def _validate_culture_relationship(
        self,
        revenu: Revenu,
    ) -> None:
        """
        Vérifie la relation entre culture et parcelle.

        Cas possibles :

        1. aucune culture :
           aucune vérification supplémentaire ;

        2. culture renseignée sans parcelle :
           la culture doit simplement exister ;

        3. culture + parcelle :
           la culture doit appartenir à la parcelle.
        """

        if revenu.culture_id is None:
            return

        culture = self.culture_repository.get_by_id(
            revenu.culture_id
        )

        if culture is None:
            raise ValueError(
                "Aucune culture trouvée avec "
                f"l'identifiant {revenu.culture_id}."
            )

        if revenu.parcelle_id is None:
            return

        if culture.parcelle_id != revenu.parcelle_id:
            raise ValueError(
                "La culture sélectionnée n'appartient "
                "pas à la parcelle du revenu."
            )

    # ========================================================
    # SEARCH
    # ========================================================

    def search_revenus(
        self,
        search_term: str,
    ) -> list[Revenu]:
        """
        Recherche les revenus par produit.
        """

        if not isinstance(
            search_term,
            str,
        ):
            raise TypeError(
                "search_term doit être une chaîne "
                "de caractères."
            )

        search_term = search_term.strip().lower()

        if not search_term:
            return self.get_all_revenus()

        revenus = self.get_all_revenus()

        return [
            revenu
            for revenu in revenus
            if search_term in revenu.produit.lower()
        ]

    # ========================================================
    # VALIDATION ID REVENU
    # ========================================================

    @staticmethod
    def _validate_id(
        revenu_id: int,
    ) -> None:

        if not isinstance(
            revenu_id,
            int,
        ):
            raise TypeError(
                "L'identifiant du revenu "
                "doit être un entier."
            )

        if revenu_id <= 0:
            raise ValueError(
                "L'identifiant du revenu "
                "doit être strictement positif."
            )

    # ========================================================
    # VALIDATION ID PARCELLE
    # ========================================================

    @staticmethod
    def _validate_parcelle_id(
        parcelle_id: int,
    ) -> None:

        if not isinstance(
            parcelle_id,
            int,
        ):
            raise TypeError(
                "L'identifiant de la parcelle "
                "doit être un entier."
            )

        if parcelle_id <= 0:
            raise ValueError(
                "L'identifiant de la parcelle "
                "doit être strictement positif."
            )

    # ========================================================
    # VALIDATION ID CULTURE
    # ========================================================

    @staticmethod
    def _validate_culture_id(
        culture_id: int,
    ) -> None:

        if not isinstance(
            culture_id,
            int,
        ):
            raise TypeError(
                "L'identifiant de la culture "
                "doit être un entier."
            )

        if culture_id <= 0:
            raise ValueError(
                "L'identifiant de la culture "
                "doit être strictement positif."
            )

