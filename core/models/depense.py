"""
Modèle Depense
==============

Représente une dépense agricole dans VolyTrack.
"""


from dataclasses import dataclass
from typing import Optional


@dataclass
class Depense:
    """
    Représente une dépense liée à une exploitation agricole.

    Attributes
    ----------
    categorie : str
        Catégorie de la dépense.
    montant : float
        Montant de la dépense.
    date_depense : str
        Date de la dépense au format YYYY-MM-DD.
    parcelle_id : Optional[int]
        Identifiant de la parcelle concernée.
    culture_id : Optional[int]
        Identifiant de la culture concernée.
    description : Optional[str]
        Description complémentaire.
    id : Optional[int]
        Identifiant de la dépense en base de données.
    """

    categorie: str
    montant: float
    date_depense: str
    parcelle_id: Optional[int] = None
    culture_id: Optional[int] = None
    description: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """Valide les données de la dépense."""

        # ====================================================
        # VALIDATION PARCELLE
        # ====================================================

        if self.parcelle_id is not None:

            if not isinstance(
                self.parcelle_id,
                int,
            ):
                raise TypeError(
                    "L'identifiant de la parcelle doit être "
                    "un entier ou None."
                )

            if self.parcelle_id <= 0:
                raise ValueError(
                    "L'identifiant de la parcelle doit être "
                    "strictement positif."
                )

        # ====================================================
        # VALIDATION CULTURE
        # ====================================================

        if self.culture_id is not None:

            if not isinstance(
                self.culture_id,
                int,
            ):
                raise TypeError(
                    "L'identifiant de la culture doit être "
                    "un entier ou None."
                )

            if self.culture_id <= 0:
                raise ValueError(
                    "L'identifiant de la culture doit être "
                    "strictement positif."
                )

        # ====================================================
        # VALIDATION CATÉGORIE
        # ====================================================

        if not isinstance(
            self.categorie,
            str,
        ):
            raise TypeError(
                "La catégorie doit être une chaîne "
                "de caractères."
            )

        if not self.categorie.strip():
            raise ValueError(
                "La catégorie ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION MONTANT
        # ====================================================

        if not isinstance(
            self.montant,
            (int, float),
        ):
            raise TypeError(
                "Le montant doit être un nombre."
            )

        if self.montant < 0:
            raise ValueError(
                "Le montant ne peut pas être négatif."
            )

        # ====================================================
        # VALIDATION DATE
        # ====================================================

        if not isinstance(
            self.date_depense,
            str,
        ):
            raise TypeError(
                "La date de dépense doit être une chaîne "
                "de caractères."
            )

        if not self.date_depense.strip():
            raise ValueError(
                "La date de dépense ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION DESCRIPTION
        # ====================================================

        if (
            self.description is not None
            and not isinstance(
                self.description,
                str,
            )
        ):
            raise TypeError(
                "La description doit être une chaîne ou None."
            )

        # ====================================================
        # VALIDATION ID
        # ====================================================

        if (
            self.id is not None
            and not isinstance(
                self.id,
                int,
            )
        ):
            raise TypeError(
                "L'identifiant doit être un entier ou None."
            )