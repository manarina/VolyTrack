
"""
Service Travail
===============

Contient la logique métier liée aux travaux agricoles.

Architecture :

    Interface Streamlit
            ↓
       TravailService
            ↓
      TravailRepository
            ↓
          SQLite

Le service vérifie notamment :

- l'existence de la parcelle ;
- l'existence de la culture lorsqu'elle est renseignée ;
- la cohérence entre la parcelle et la culture ;
- la validité des coûts ;
- la validité des identifiants ;
- les règles métier avant création ou modification.
"""

from __future__ import annotations

from typing import Optional

from core.models.travail import Travail
from core.repositories.travail_repository import TravailRepository
from core.repositories.parcelle_repository import ParcelleRepository
from core.repositories.culture_repository import CultureRepository


class TravailService:
    """
    Service métier pour la gestion des travaux agricoles.
    """

    def __init__(
        self,
        repository: Optional[TravailRepository] = None,
        parcelle_repository: Optional[ParcelleRepository] = None,
        culture_repository: Optional[CultureRepository] = None,
    ) -> None:
        """
        Initialise le service.

        Parameters
        ----------
        repository : TravailRepository, optional
            Repository principal des travaux.

        parcelle_repository : ParcelleRepository, optional
            Repository permettant de vérifier les parcelles.

        culture_repository : CultureRepository, optional
            Repository permettant de vérifier les cultures.
        """

        if repository is None:
            repository = TravailRepository()

        if parcelle_repository is None:
            parcelle_repository = ParcelleRepository()

        if culture_repository is None:
            culture_repository = CultureRepository()

        if not isinstance(
            repository,
            TravailRepository,
        ):
            raise TypeError(
                "repository doit être une instance "
                "de TravailRepository."
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

    def create_travail(
        self,
        travail: Travail,
    ) -> Travail:
        """
        Crée un nouveau travail agricole.

        Vérifie :

        - le type de l'objet ;
        - la validité métier ;
        - l'existence de la parcelle ;
        - l'existence de la culture si renseignée ;
        - la cohérence culture/parcelle.
        """

        if not isinstance(
            travail,
            Travail,
        ):
            raise TypeError(
                "travail doit être une instance de Travail."
            )

        self.validate_travail(
            travail
        )

        if not self.parcelle_exists(
            travail.parcelle_id
        ):
            raise ValueError(
                f"Aucune parcelle trouvée avec "
                f"l'identifiant {travail.parcelle_id}."
            )

        self._validate_culture_relationship(
            travail
        )

        return self.repository.create(
            travail
        )

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_travail(
        self,
        travail_id: int,
    ) -> Optional[Travail]:
        """
        Récupère un travail par son identifiant.
        """

        self._validate_id(
            travail_id
        )

        return self.repository.get_by_id(
            travail_id
        )

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all_travaux(
        self,
    ) -> list[Travail]:
        """
        Retourne tous les travaux.
        """

        return self.repository.get_all()

    # ========================================================
    # GET BY PARCELLE
    # ========================================================

    def get_travaux_by_parcelle(
        self,
        parcelle_id: int,
    ) -> list[Travail]:
        """
        Retourne les travaux associés à une parcelle.
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

    def get_travaux_by_culture(
        self,
        culture_id: int,
    ) -> list[Travail]:
        """
        Retourne les travaux associés à une culture.
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

    def update_travail(
        self,
        travail: Travail,
    ) -> Travail:
        """
        Modifie un travail existant.

        Vérifie également que la nouvelle association
        parcelle/culture reste cohérente.
        """

        if not isinstance(
            travail,
            Travail,
        ):
            raise TypeError(
                "travail doit être une instance de Travail."
            )

        if travail.id is None:
            raise ValueError(
                "Le travail doit posséder un identifiant "
                "pour être modifié."
            )

        self._validate_id(
            travail.id
        )

        self.validate_travail(
            travail
        )

        if not self.parcelle_exists(
            travail.parcelle_id
        ):
            raise ValueError(
                f"Aucune parcelle trouvée avec "
                f"l'identifiant {travail.parcelle_id}."
            )

        self._validate_culture_relationship(
            travail
        )

        return self.repository.update(
            travail
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_travail(
        self,
        travail_id: int,
    ) -> bool:
        """
        Supprime un travail.
        """

        self._validate_id(
            travail_id
        )

        return self.repository.delete(
            travail_id
        )

    # ========================================================
    # EXISTS
    # ========================================================

    def travail_exists(
        self,
        travail_id: int,
    ) -> bool:
        """
        Vérifie si un travail existe.
        """

        self._validate_id(
            travail_id
        )

        return (
            self.repository.get_by_id(
                travail_id
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
    # VALIDATION MÉTIER
    # ========================================================

    def validate_travail(
        self,
        travail: Travail,
    ) -> bool:
        """
        Effectue les validations métier d'un travail.

        Les validations structurelles sont déjà réalisées
        par le modèle Travail.

        Cette méthode vérifie les règles propres au service.
        """

        if not isinstance(
            travail,
            Travail,
        ):
            raise TypeError(
                "travail doit être une instance de Travail."
            )

        self._validate_parcelle_id(
            travail.parcelle_id
        )

        if not isinstance(
            travail.type_travail,
            str,
        ):
            raise TypeError(
                "Le type de travail doit être une chaîne."
            )

        if not travail.type_travail.strip():
            raise ValueError(
                "Le type de travail ne doit pas être vide."
            )

        if not isinstance(
            travail.date_travail,
            str,
        ):
            raise TypeError(
                "La date du travail doit être une chaîne."
            )

        if not travail.date_travail.strip():
            raise ValueError(
                "La date du travail ne doit pas être vide."
            )

        if not isinstance(
            travail.cout,
            (int, float),
        ):
            raise TypeError(
                "Le coût du travail doit être numérique."
            )

        if travail.cout < 0:
            raise ValueError(
                "Le coût du travail ne peut pas être négatif."
            )

        if travail.culture_id is not None:
            self._validate_culture_id(
                travail.culture_id
            )

        if travail.description is not None:

            if not isinstance(
                travail.description,
                str,
            ):
                raise TypeError(
                    "La description du travail doit être "
                    "une chaîne."
                )

        return True

    # ========================================================
    # COHÉRENCE CULTURE / PARCELLE
    # ========================================================

    def _validate_culture_relationship(
        self,
        travail: Travail,
    ) -> None:
        """
        Vérifie l'association entre culture et parcelle.

        Si aucune culture n'est renseignée, aucune vérification
        supplémentaire n'est nécessaire.

        Si une culture est renseignée :

        1. elle doit exister ;
        2. elle doit appartenir à la même parcelle.
        """

        if travail.culture_id is None:
            return

        culture = self.culture_repository.get_by_id(
            travail.culture_id
        )

        if culture is None:
            raise ValueError(
                f"Aucune culture trouvée avec "
                f"l'identifiant {travail.culture_id}."
            )

        if culture.parcelle_id != travail.parcelle_id:
            raise ValueError(
                "La culture sélectionnée n'appartient pas "
                "à la parcelle du travail."
            )

    # ========================================================
    # RECHERCHE
    # ========================================================

    def search_travaux(
        self,
        search_term: str,
    ) -> list[Travail]:
        """
        Recherche des travaux par type de travail.

        La recherche est insensible à la casse.

        Une recherche vide retourne tous les travaux.
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
            return self.get_all_travaux()

        travaux = self.get_all_travaux()

        return [
            travail
            for travail in travaux
            if search_term
            in travail.type_travail.lower()
        ]

    # ========================================================
    # VALIDATION ID TRAVAIL
    # ========================================================

    @staticmethod
    def _validate_id(
        travail_id: int,
    ) -> None:
        """
        Valide l'identifiant d'un travail.
        """

        if not isinstance(
            travail_id,
            int,
        ):
            raise TypeError(
                "L'identifiant du travail doit être un entier."
            )

        if travail_id <= 0:
            raise ValueError(
                "L'identifiant du travail doit être "
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
        Valide l'identifiant d'une parcelle.
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

    # ========================================================
    # VALIDATION ID CULTURE
    # ========================================================

    @staticmethod
    def _validate_culture_id(
        culture_id: int,
    ) -> None:
        """
        Valide l'identifiant d'une culture.
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

