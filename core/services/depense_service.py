"""
Service métier pour la gestion des dépenses.

Responsabilités :
- validation des dépenses ;
- création ;
- consultation ;
- modification ;
- suppression ;
- recherche ;
- vérification des parcelles ;
- vérification des cultures ;
- vérification de la cohérence culture / parcelle.
"""

from __future__ import annotations

from typing import Optional

from core.models.depense import Depense

from core.repositories.depense_repository import (
    DepenseRepository,
)

from core.repositories.parcelle_repository import (
    ParcelleRepository,
)

from core.repositories.culture_repository import (
    CultureRepository,
)


class DepenseService:
    """
    Service métier de gestion des dépenses.
    """

    # ========================================================
    # INITIALISATION
    # ========================================================

    def __init__(
        self,
        repository: Optional[DepenseRepository] = None,
        parcelle_repository: Optional[ParcelleRepository] = None,
        culture_repository: Optional[CultureRepository] = None,
    ) -> None:

        if repository is None:
            repository = DepenseRepository()

        if parcelle_repository is None:
            parcelle_repository = ParcelleRepository()

        if culture_repository is None:
            culture_repository = CultureRepository()

        if not isinstance(
            repository,
            DepenseRepository,
        ):
            raise TypeError(
                "repository doit être une instance "
                "de DepenseRepository."
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

    def create_depense(
        self,
        depense: Depense,
    ) -> Depense:
        """
        Crée une nouvelle dépense après validation métier.
        """

        if not isinstance(
            depense,
            Depense,
        ):
            raise TypeError(
                "depense doit être une instance de Depense."
            )

        self.validate_depense(depense)

        # ----------------------------------------------------
        # PARCELLE
        # ----------------------------------------------------

        if depense.parcelle_id is not None:

            if not self.parcelle_exists(
                depense.parcelle_id
            ):
                raise ValueError(
                    "Aucune parcelle trouvée avec "
                    f"l'identifiant {depense.parcelle_id}."
                )

        # ----------------------------------------------------
        # CULTURE
        # ----------------------------------------------------

        self._validate_culture_relationship(
            depense
        )

        return self.repository.create(
            depense
        )

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_depense(
        self,
        depense_id: int,
    ) -> Optional[Depense]:
        """
        Retourne une dépense par son identifiant.
        """

        self._validate_id(
            depense_id
        )

        return self.repository.get_by_id(
            depense_id
        )

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all_depenses(
        self,
    ) -> list[Depense]:
        """
        Retourne toutes les dépenses.
        """

        return self.repository.get_all()

    # ========================================================
    # GET BY PARCELLE
    # ========================================================

    def get_depenses_by_parcelle(
        self,
        parcelle_id: int,
    ) -> list[Depense]:
        """
        Retourne les dépenses associées à une parcelle.
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

    def get_depenses_by_culture(
        self,
        culture_id: int,
    ) -> list[Depense]:
        """
        Retourne les dépenses associées à une culture.
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

    def update_depense(
        self,
        depense: Depense,
    ) -> Depense:
        """
        Modifie une dépense existante.
        """

        if not isinstance(
            depense,
            Depense,
        ):
            raise TypeError(
                "depense doit être une instance de Depense."
            )

        if depense.id is None:
            raise ValueError(
                "La dépense doit posséder un identifiant "
                "pour être modifiée."
            )

        self._validate_id(
            depense.id
        )

        self.validate_depense(
            depense
        )

        # ----------------------------------------------------
        # PARCELLE
        # ----------------------------------------------------

        if depense.parcelle_id is not None:

            if not self.parcelle_exists(
                depense.parcelle_id
            ):
                raise ValueError(
                    "Aucune parcelle trouvée avec "
                    f"l'identifiant {depense.parcelle_id}."
                )

        # ----------------------------------------------------
        # CULTURE
        # ----------------------------------------------------

        self._validate_culture_relationship(
            depense
        )

        return self.repository.update(
            depense
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_depense(
        self,
        depense_id: int,
    ) -> bool:
        """
        Supprime une dépense.
        """

        self._validate_id(
            depense_id
        )

        return self.repository.delete(
            depense_id
        )

    # ========================================================
    # EXISTS
    # ========================================================

    def depense_exists(
        self,
        depense_id: int,
    ) -> bool:
        """
        Vérifie si une dépense existe.
        """

        self._validate_id(
            depense_id
        )

        return (
            self.repository.get_by_id(
                depense_id
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

    def validate_depense(
        self,
        depense: Depense,
    ) -> bool:
        """
        Effectue les validations métier d'une dépense.
        """

        if not isinstance(
            depense,
            Depense,
        ):
            raise TypeError(
                "depense doit être une instance de Depense."
            )

        # ----------------------------------------------------
        # CATÉGORIE
        # ----------------------------------------------------

        if not isinstance(
            depense.categorie,
            str,
        ):
            raise TypeError(
                "La catégorie de la dépense doit être "
                "une chaîne."
            )

        if not depense.categorie.strip():
            raise ValueError(
                "La catégorie de la dépense "
                "ne doit pas être vide."
            )

        # ----------------------------------------------------
        # MONTANT
        # ----------------------------------------------------

        if not isinstance(
            depense.montant,
            (int, float),
        ):
            raise TypeError(
                "Le montant de la dépense doit être numérique."
            )

        if depense.montant < 0:
            raise ValueError(
                "Le montant de la dépense "
                "ne peut pas être négatif."
            )

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if not isinstance(
            depense.date_depense,
            str,
        ):
            raise TypeError(
                "La date de la dépense doit être une chaîne."
            )

        if not depense.date_depense.strip():
            raise ValueError(
                "La date de la dépense ne doit pas être vide."
            )

        # ----------------------------------------------------
        # PARCELLE
        # ----------------------------------------------------

        if depense.parcelle_id is not None:

            self._validate_parcelle_id(
                depense.parcelle_id
            )

        # ----------------------------------------------------
        # CULTURE
        # ----------------------------------------------------

        if depense.culture_id is not None:

            self._validate_culture_id(
                depense.culture_id
            )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        if depense.description is not None:

            if not isinstance(
                depense.description,
                str,
            ):
                raise TypeError(
                    "La description de la dépense "
                    "doit être une chaîne."
                )

        return True

    # ========================================================
    # RELATION CULTURE / PARCELLE
    # ========================================================

    def _validate_culture_relationship(
        self,
        depense: Depense,
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

        if depense.culture_id is None:
            return

        culture = self.culture_repository.get_by_id(
            depense.culture_id
        )

        if culture is None:
            raise ValueError(
                "Aucune culture trouvée avec "
                f"l'identifiant {depense.culture_id}."
            )

        if depense.parcelle_id is None:
            return

        if culture.parcelle_id != depense.parcelle_id:
            raise ValueError(
                "La culture sélectionnée n'appartient "
                "pas à la parcelle de la dépense."
            )

    # ========================================================
    # SEARCH
    # ========================================================

    def search_depenses(
        self,
        search_term: str,
    ) -> list[Depense]:
        """
        Recherche les dépenses par catégorie.
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
            return self.get_all_depenses()

        depenses = self.get_all_depenses()

        return [
            depense
            for depense in depenses
            if search_term in depense.categorie.lower()
        ]

    # ========================================================
    # VALIDATION ID DÉPENSE
    # ========================================================

    @staticmethod
    def _validate_id(
        depense_id: int,
    ) -> None:

        if not isinstance(
            depense_id,
            int,
        ):
            raise TypeError(
                "L'identifiant de la dépense "
                "doit être un entier."
            )

        if depense_id <= 0:
            raise ValueError(
                "L'identifiant de la dépense "
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

