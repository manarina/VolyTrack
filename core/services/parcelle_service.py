"""
Service Parcelle
================

Contient la logique métier liée aux parcelles agricoles.

Architecture :

    Interface Streamlit
            ↓
    ParcelleService
            ↓
    ParcelleRepository
            ↓
          SQLite
"""

from __future__ import annotations

from typing import Optional

from core.models.parcelle import Parcelle
from core.repositories.parcelle_repository import ParcelleRepository


class ParcelleService:
    """
    Service métier pour la gestion des parcelles.

    Le service centralise les validations et les opérations
    métier avant de déléguer l'accès aux données au repository.
    """

    def __init__(
        self,
        repository: Optional[ParcelleRepository] = None,
    ) -> None:
        """
        Initialise le service.

        Parameters
        ----------
        repository : ParcelleRepository, optional
            Repository utilisé pour accéder aux données.
            Si aucun repository n'est fourni, une nouvelle
            instance est créée.
        """

        if repository is None:
            repository = ParcelleRepository()

        if not isinstance(
            repository,
            ParcelleRepository,
        ):
            raise TypeError(
                "repository doit être une instance "
                "de ParcelleRepository."
            )

        self.repository = repository

    # ========================================================
    # CREATE
    # ========================================================

    def create_parcelle(
        self,
        parcelle: Parcelle,
    ) -> Parcelle:
        """
        Crée une nouvelle parcelle.

        Parameters
        ----------
        parcelle : Parcelle
            Parcelle à créer.

        Returns
        -------
        Parcelle
            Parcelle créée avec son identifiant.

        Raises
        ------
        TypeError
            Si parcelle n'est pas une instance de Parcelle.
        """

        if not isinstance(
            parcelle,
            Parcelle,
        ):
            raise TypeError(
                "parcelle doit être une instance de Parcelle."
            )

        return self.repository.create(
            parcelle
        )

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_parcelle(
        self,
        parcelle_id: int,
    ) -> Optional[Parcelle]:
        """
        Récupère une parcelle par son identifiant.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.

        Returns
        -------
        Parcelle | None
            Parcelle trouvée ou None si elle n'existe pas.
        """

        self._validate_id(
            parcelle_id
        )

        return self.repository.get_by_id(
            parcelle_id
        )

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all_parcelles(self) -> list[Parcelle]:
        """
        Retourne toutes les parcelles.

        Returns
        -------
        list[Parcelle]
            Liste des parcelles.
        """

        return self.repository.get_all()
    
    def count_parcelles(self) -> int:
       """
       Retourne le nombre réel de parcelles en base SQLite.
       """
       return self.repository.count()

    # ========================================================
    # UPDATE
    # ========================================================

    def update_parcelle(
        self,
        parcelle: Parcelle,
    ) -> Parcelle:
        """
        Modifie une parcelle existante.

        Parameters
        ----------
        parcelle : Parcelle
            Parcelle contenant un identifiant valide.

        Returns
        -------
        Parcelle
            Parcelle modifiée.

        Raises
        ------
        TypeError
            Si parcelle n'est pas une instance de Parcelle.

        ValueError
            Si la parcelle ne possède pas d'identifiant.
        """

        if not isinstance(
            parcelle,
            Parcelle,
        ):
            raise TypeError(
                "parcelle doit être une instance de Parcelle."
            )

        if parcelle.id is None:
            raise ValueError(
                "La parcelle doit posséder un identifiant "
                "pour être modifiée."
            )

        self._validate_id(
            parcelle.id
        )

        return self.repository.update(
            parcelle
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_parcelle(
        self,
        parcelle_id: int,
    ) -> bool:
        """
        Supprime une parcelle.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.

        Returns
        -------
        bool
            True si la suppression a réussi.
        """

        self._validate_id(
            parcelle_id
        )

        return self.repository.delete(
            parcelle_id
        )

    # ========================================================
    # EXISTENCE
    # ========================================================

    def parcelle_exists(
        self,
        parcelle_id: int,
    ) -> bool:
        """
        Vérifie si une parcelle existe.

        Parameters
        ----------
        parcelle_id : int
            Identifiant de la parcelle.

        Returns
        -------
        bool
            True si la parcelle existe, sinon False.
        """

        self._validate_id(
            parcelle_id
        )

        return (
            self.repository.get_by_id(
                parcelle_id
            )
            is not None
        )

    # ========================================================
    # VALIDATION MÉTIER
    # ========================================================

    def validate_parcelle(
        self,
        parcelle: Parcelle,
    ) -> bool:
        """
        Vérifie qu'une parcelle est valide.

        Le modèle Parcelle effectue déjà les validations
        structurelles. Cette méthode fournit une porte d'entrée
        claire pour la validation métier depuis l'interface.

        Parameters
        ----------
        parcelle : Parcelle
            Parcelle à vérifier.

        Returns
        -------
        bool
            True si la parcelle est valide.

        Raises
        ------
        TypeError
            Si parcelle n'est pas une instance de Parcelle.
        """

        if not isinstance(
            parcelle,
            Parcelle,
        ):
            raise TypeError(
                "parcelle doit être une instance de Parcelle."
            )

        if parcelle.superficie <= 0:
            raise ValueError(
                "La superficie doit être strictement positive."
            )

        if not parcelle.nom.strip():
            raise ValueError(
                "Le nom de la parcelle ne doit pas être vide."
            )

        if not parcelle.unite_superficie.strip():
            raise ValueError(
                "L'unité de superficie ne doit pas être vide."
            )

        return True

    # ========================================================
    # RECHERCHE PAR NOM
    # ========================================================

    def search_parcelles(
        self,
        search_term: str,
    ) -> list[Parcelle]:
        """
        Recherche des parcelles à partir de leur nom.

        La recherche est effectuée en mémoire à partir
        des parcelles retournées par le repository.

        Parameters
        ----------
        search_term : str
            Texte recherché dans le nom.

        Returns
        -------
        list[Parcelle]
            Parcelles correspondant à la recherche.

        Raises
        ------
        TypeError
            Si search_term n'est pas une chaîne.
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
            return self.get_all_parcelles()

        parcelles = self.get_all_parcelles()

        return [
            parcelle
            for parcelle in parcelles
            if search_term
            in parcelle.nom.lower()
        ]

    # ========================================================
    # VALIDATION ID
    # ========================================================

    @staticmethod
    def _validate_id(
        parcelle_id: int,
    ) -> None:
        """
        Valide un identifiant de parcelle.

        Parameters
        ----------
        parcelle_id : int
            Identifiant à vérifier.
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

