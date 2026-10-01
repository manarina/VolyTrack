"""
Service métier pour la gestion des récoltes.

Le RecolteService centralise :
    - la création des récoltes ;
    - la consultation ;
    - la modification ;
    - la suppression ;
    - la recherche ;
    - la validation métier ;
    - la vérification de la relation avec une culture.
"""

from __future__ import annotations

from typing import Any

from core.models.recolte import Recolte
from core.repositories.recolte_repository import RecolteRepository
from core.repositories.culture_repository import CultureRepository


class RecolteService:
    """
    Service métier pour les récoltes.

    Parameters
    ----------
    repository : RecolteRepository, optional
        Repository utilisé pour accéder aux récoltes.

    culture_repository : CultureRepository, optional
        Repository utilisé pour vérifier l'existence des cultures.
    """

    def __init__(
        self,
        repository: RecolteRepository | None = None,
        culture_repository: CultureRepository | None = None,
    ) -> None:

        self.repository = (
            repository
            if repository is not None
            else RecolteRepository()
        )

        self.culture_repository = (
            culture_repository
            if culture_repository is not None
            else CultureRepository()
        )

    # ========================================================
    # VALIDATION DES IDENTIFIANTS
    # ========================================================

    @staticmethod
    def _validate_id(
        value: Any,
        field_name: str = "id",
    ) -> int:
        """
        Valide un identifiant.

        Returns
        -------
        int
            Identifiant validé.
        """

        if isinstance(value, bool):
            raise ValueError(
                f"{field_name} doit être un entier positif."
            )

        if not isinstance(value, int):
            raise ValueError(
                f"{field_name} doit être un entier positif."
            )

        if value <= 0:
            raise ValueError(
                f"{field_name} doit être supérieur à zéro."
            )

        return value

    # ========================================================
    # VALIDATION D'UNE RÉCOLTE
    # ========================================================

    def validate_recolte(
        self,
        recolte: Recolte,
    ) -> bool:
        """
        Valide une récolte avant son enregistrement.

        Vérifications :
            - type Recolte ;
            - culture_id ;
            - date_recolte ;
            - quantité ;
            - unité ;
            - qualité ;
            - description ;
            - relation avec la culture.

        Returns
        -------
        bool
            True si la récolte est valide.

        Raises
        ------
        ValueError
            Si les données sont invalides.
        """

        if not isinstance(recolte, Recolte):
            raise ValueError(
                "La récolte doit être une instance de Recolte."
            )

        # ----------------------------------------------------
        # CULTURE ID
        # ----------------------------------------------------

        self._validate_id(
            recolte.culture_id,
            "culture_id",
        )

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if not isinstance(
            recolte.date_recolte,
            str,
        ):
            raise ValueError(
                "La date de récolte doit être une chaîne de caractères."
            )

        if not recolte.date_recolte.strip():
            raise ValueError(
                "La date de récolte ne peut pas être vide."
            )

        # ----------------------------------------------------
        # QUANTITÉ
        # ----------------------------------------------------

        if isinstance(
            recolte.quantite,
            bool,
        ):
            raise ValueError(
                "La quantité doit être un nombre positif."
            )

        if not isinstance(
            recolte.quantite,
            (int, float),
        ):
            raise ValueError(
                "La quantité doit être un nombre."
            )

        if recolte.quantite <= 0:
            raise ValueError(
                "La quantité doit être strictement positive."
            )

        # ----------------------------------------------------
        # UNITÉ
        # ----------------------------------------------------

        if not isinstance(
            recolte.unite,
            str,
        ):
            raise ValueError(
                "L'unité doit être une chaîne de caractères."
            )

        if not recolte.unite.strip():
            raise ValueError(
                "L'unité ne peut pas être vide."
            )

        # ----------------------------------------------------
        # QUALITÉ
        # ----------------------------------------------------

        if recolte.qualite is not None:

            if not isinstance(
                recolte.qualite,
                str,
            ):
                raise ValueError(
                    "La qualité doit être une chaîne "
                    "de caractères ou None."
                )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        if recolte.description is not None:

            if not isinstance(
                recolte.description,
                str,
            ):
                raise ValueError(
                    "La description doit être une chaîne "
                    "de caractères ou None."
                )

        # ----------------------------------------------------
        # ID OPTIONNEL
        # ----------------------------------------------------

        if recolte.id is not None:

            self._validate_id(
                recolte.id,
                "id",
            )

        # ----------------------------------------------------
        # RELATION CULTURE
        # ----------------------------------------------------

        if not self.culture_exists(
            recolte.culture_id
        ):
            raise ValueError(
                f"La culture {recolte.culture_id} "
                "n'existe pas."
            )

        return True

    # ========================================================
    # EXISTENCE CULTURE
    # ========================================================

    def culture_exists(
        self,
        culture_id: int,
    ) -> bool:
        """
        Vérifie si une culture existe.
        """

        self._validate_id(
            culture_id,
            "culture_id",
        )

        culture = self.culture_repository.get_by_id(
            culture_id
        )

        return culture is not None

    # ========================================================
    # CRÉATION
    # ========================================================

    def create_recolte(
        self,
        recolte: Recolte,
    ) -> Recolte:
        """
        Crée une nouvelle récolte.

        Returns
        -------
        Recolte
            Récolte créée.
        """

        self.validate_recolte(
            recolte
        )

        return self.repository.create(
            recolte
        )

    # ========================================================
    # CONSULTATION PAR ID
    # ========================================================

    def get_recolte(
        self,
        recolte_id: int,
    ) -> Recolte | None:
        """
        Retourne une récolte par son identifiant.
        """

        self._validate_id(
            recolte_id,
            "recolte_id",
        )

        return self.repository.get_by_id(
            recolte_id
        )

    # ========================================================
    # CONSULTATION DE TOUTES LES RÉCOLTES
    # ========================================================

    def get_all_recoltes(self) -> list[Recolte]:
        """
        Retourne toutes les récoltes.
        """

        return self.repository.get_all()

    # ========================================================
    # CONSULTATION PAR CULTURE
    # ========================================================

    def get_recoltes_by_culture(
        self,
        culture_id: int,
    ) -> list[Recolte]:
        """
        Retourne les récoltes associées à une culture.
        """

        self._validate_id(
            culture_id,
            "culture_id",
        )

        return self.repository.get_by_culture_id(
            culture_id
        )

    # ========================================================
    # EXISTENCE D'UNE RÉCOLTE
    # ========================================================

    def recolte_exists(
        self,
        recolte_id: int,
    ) -> bool:
        """
        Vérifie si une récolte existe.
        """

        self._validate_id(
            recolte_id,
            "recolte_id",
        )

        return (
            self.repository.get_by_id(
                recolte_id
            )
            is not None
        )

    # ========================================================
    # MODIFICATION
    # ========================================================

    def update_recolte(
        self,
        recolte: Recolte,
    ) -> Recolte:
        """
        Modifie une récolte existante.

        Raises
        ------
        ValueError
            Si la récolte n'existe pas ou si les données
            sont invalides.
        """

        if recolte.id is None:
            raise ValueError(
                "L'identifiant de la récolte est obligatoire "
                "pour une modification."
            )

        self._validate_id(
            recolte.id,
            "id",
        )

        self.validate_recolte(
            recolte
        )

        existing = self.repository.get_by_id(
            recolte.id
        )

        if existing is None:
            raise ValueError(
                f"Aucune récolte trouvée avec "
                f"l'identifiant {recolte.id}."
            )

        return self.repository.update(
            recolte
        )

    # ========================================================
    # SUPPRESSION
    # ========================================================

    def delete_recolte(
        self,
        recolte_id: int,
    ) -> bool:
        """
        Supprime une récolte.

        Returns
        -------
        bool
            True si la suppression a réussi.
        """

        self._validate_id(
            recolte_id,
            "recolte_id",
        )

        existing = self.repository.get_by_id(
            recolte_id
        )

        if existing is None:
            raise ValueError(
                f"Aucune récolte trouvée avec "
                f"l'identifiant {recolte_id}."
            )

        result = self.repository.delete(
            recolte_id
        )

        return bool(result)

    # ========================================================
    # RECHERCHE
    # ========================================================

    def search_recoltes(
        self,
        search: str,
    ) -> list[Recolte]:
        """
        Recherche des récoltes.

        La recherche porte sur :
            - la date ;
            - l'unité ;
            - la qualité ;
            - la description.

        Une recherche vide ou composée uniquement
        d'espaces retourne toutes les récoltes.

        Parameters
        ----------
        search : str
            Texte recherché.

        Returns
        -------
        list[Recolte]
            Récoltes correspondantes.
        """

        if not isinstance(
            search,
            str,
        ):
            raise ValueError(
                "Le terme de recherche doit être une chaîne."
            )

        search = search.strip()

        if not search:
            return self.get_all_recoltes()

        search_lower = search.lower()

        recoltes = self.get_all_recoltes()

        results = []

        for recolte in recoltes:

            searchable_values = [
                recolte.date_recolte,
                recolte.unite,
                recolte.qualite or "",
                recolte.description or "",
            ]

            if any(
                search_lower in str(value).lower()
                for value in searchable_values
            ):
                results.append(
                    recolte
                )

        return results

