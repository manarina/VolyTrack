
"""
Service Culture
===============

Contient la logique métier liée aux cultures agricoles.

Architecture :

    Interface Streamlit
            ↓
      CultureService
            ↓
     CultureRepository
            ↓
          SQLite
"""

from __future__ import annotations

from typing import Optional

from core.models.culture import Culture
from core.repositories.culture_repository import CultureRepository
from core.repositories.parcelle_repository import ParcelleRepository


class CultureService:
    """
    Service métier pour la gestion des cultures.

    Le service centralise les validations métier et délègue
    l'accès aux données aux repositories.
    """

    def __init__(
        self,
        repository: Optional[CultureRepository] = None,
        parcelle_repository: Optional[ParcelleRepository] = None,
    ) -> None:
        """
        Initialise le service.

        Parameters
        ----------
        repository : CultureRepository, optional
            Repository des cultures.

        parcelle_repository : ParcelleRepository, optional
            Repository permettant de vérifier l'existence
            des parcelles associées.
        """

        if repository is None:
            repository = CultureRepository()

        if parcelle_repository is None:
            parcelle_repository = ParcelleRepository()

        if not isinstance(
            repository,
            CultureRepository,
        ):
            raise TypeError(
                "repository doit être une instance "
                "de CultureRepository."
            )

        if not isinstance(
            parcelle_repository,
            ParcelleRepository,
        ):
            raise TypeError(
                "parcelle_repository doit être une instance "
                "de ParcelleRepository."
            )

        self.repository = repository
        self.parcelle_repository = parcelle_repository

    # ========================================================
    # CREATE
    # ========================================================

    def create_culture(
        self,
        culture: Culture,
    ) -> Culture:
        """
        Crée une nouvelle culture.

        Vérifie au préalable que la parcelle associée
        existe réellement.

        Parameters
        ----------
        culture : Culture
            Culture à créer.

        Returns
        -------
        Culture
            Culture créée avec son identifiant.
        """

        if not isinstance(
            culture,
            Culture,
        ):
            raise TypeError(
                "culture doit être une instance de Culture."
            )

        self.validate_culture(
            culture
        )

        if not self.parcelle_exists(
            culture.parcelle_id
        ):
            raise ValueError(
                f"Aucune parcelle trouvée avec l'identifiant "
                f"{culture.parcelle_id}."
            )

        return self.repository.create(
            culture
        )

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_culture(
        self,
        culture_id: int,
    ) -> Optional[Culture]:
        """
        Récupère une culture par son identifiant.
        """

        self._validate_id(
            culture_id
        )

        return self.repository.get_by_id(
            culture_id
        )

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all_cultures(self) -> list[Culture]:
        """
        Retourne toutes les cultures.
        """

        return self.repository.get_all()

    # ========================================================
    # GET BY PARCELLE
    # ========================================================

    def get_cultures_by_parcelle(
        self,
        parcelle_id: int,
    ) -> list[Culture]:
        """
        Retourne toutes les cultures associées à une parcelle.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.
        """

        self._validate_parcelle_id(
            parcelle_id
        )

        return self.repository.get_by_parcelle_id(
            parcelle_id
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update_culture(
        self,
        culture: Culture,
    ) -> Culture:
        """
        Modifie une culture existante.

        Vérifie également que la parcelle associée existe.
        """

        if not isinstance(
            culture,
            Culture,
        ):
            raise TypeError(
                "culture doit être une instance de Culture."
            )

        if culture.id is None:
            raise ValueError(
                "La culture doit posséder un identifiant "
                "pour être modifiée."
            )

        self._validate_id(
            culture.id
        )

        self.validate_culture(
            culture
        )

        if not self.parcelle_exists(
            culture.parcelle_id
        ):
            raise ValueError(
                f"Aucune parcelle trouvée avec l'identifiant "
                f"{culture.parcelle_id}."
            )

        return self.repository.update(
            culture
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_culture(
        self,
        culture_id: int,
    ) -> bool:
        """
        Supprime une culture.
        """

        self._validate_id(
            culture_id
        )

        return self.repository.delete(
            culture_id
        )

    # ========================================================
    # EXISTENCE
    # ========================================================

    def culture_exists(
        self,
        culture_id: int,
    ) -> bool:
        """
        Vérifie si une culture existe.
        """

        self._validate_id(
            culture_id
        )

        return (
            self.repository.get_by_id(
                culture_id
            )
            is not None
        )

    # ========================================================
    # PARCELLE EXISTE
    # ========================================================

    def parcelle_exists(
        self,
        parcelle_id: int,
    ) -> bool:
        """
        Vérifie si la parcelle associée existe.
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
    # VALIDATION CULTURE
    # ========================================================

    def validate_culture(
        self,
        culture: Culture,
    ) -> bool:
        """
        Effectue les validations métier d'une culture.
        """

        if not isinstance(
            culture,
            Culture,
        ):
            raise TypeError(
                "culture doit être une instance de Culture."
            )

        self._validate_parcelle_id(
            culture.parcelle_id
        )

        if not culture.nom.strip():
            raise ValueError(
                "Le nom de la culture ne doit pas être vide."
            )

        if culture.statut is not None:
            if not isinstance(
                culture.statut,
                str,
            ):
                raise TypeError(
                    "Le statut de la culture doit être une chaîne."
                )

            if not culture.statut.strip():
                raise ValueError(
                    "Le statut de la culture ne doit pas être vide."
                )

        return True

    # ========================================================
    # RECHERCHE PAR NOM
    # ========================================================

    def search_cultures(
        self,
        search_term: str,
    ) -> list[Culture]:
        """
        Recherche les cultures par nom.

        La recherche n'est pas sensible à la casse.
        """

        if not isinstance(
            search_term,
            str,
        ):
            raise TypeError(
                "search_term doit être une chaîne de caractères."
            )

        search_term = search_term.strip().lower()

        if not search_term:
            return self.get_all_cultures()

        cultures = self.get_all_cultures()

        return [
            culture
            for culture in cultures
            if search_term
            in culture.nom.lower()
        ]

    # ========================================================
    # VALIDATION ID CULTURE
    # ========================================================

    @staticmethod
    def _validate_id(
        culture_id: int,
    ) -> None:
        """
        Valide un identifiant de culture.
        """

        if not isinstance(
            culture_id,
            int,
        ):
            raise TypeError(
                "L'identifiant de la culture doit être un entier."
            )

        if culture_id <= 0:
            raise ValueError(
                "L'identifiant de la culture doit être "
                "strictement positif."
            )

    # ========================================================
    # VALIDATION ID PARCELLE
    # ========================================================

    @staticmethod
    def _validate_parcelle_id(
        parcelle_id: int,
    ) -> None:
        """
        Valide un identifiant de parcelle.
        """

        if not isinstance(
            parcelle_id,
            int,
        ):
            raise TypeError(
                "L'identifiant de la parcelle doit être un entier."
            )

        if parcelle_id <= 0:
            raise ValueError(
                "L'identifiant de la parcelle doit être "
                "strictement positif."
            )

