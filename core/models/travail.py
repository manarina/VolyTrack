"""
Modèle Travail
==============

Représente un travail agricole effectué sur une parcelle
et éventuellement associé à une culture dans VolyTrack.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Travail:
    """
    Représente un travail agricole.

    Attributes
    ----------
    parcelle_id : int
        Identifiant de la parcelle concernée.
    type_travail : str
        Type de travail effectué.
    date_travail : str
        Date du travail au format YYYY-MM-DD.
    culture_id : Optional[int]
        Identifiant de la culture associée.
    cout : float
        Coût du travail.
    description : Optional[str]
        Description complémentaire.
    id : Optional[int]
        Identifiant du travail en base de données.
    """

    parcelle_id: int
    type_travail: str
    date_travail: str
    culture_id: Optional[int] = None
    cout: float = 0.0
    description: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """Valide les données du travail agricole."""

        # ====================================================
        # VALIDATION PARCELLE
        # ====================================================

        if not isinstance(self.parcelle_id, int):
            raise TypeError(
                "L'identifiant de la parcelle doit être un entier."
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

            if not isinstance(self.culture_id, int):
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
        # VALIDATION TYPE DE TRAVAIL
        # ====================================================

        if not isinstance(self.type_travail, str):
            raise TypeError(
                "Le type de travail doit être une chaîne "
                "de caractères."
            )

        if not self.type_travail.strip():
            raise ValueError(
                "Le type de travail ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION DATE
        # ====================================================

        if not isinstance(self.date_travail, str):
            raise TypeError(
                "La date du travail doit être une chaîne "
                "de caractères."
            )

        if not self.date_travail.strip():
            raise ValueError(
                "La date du travail ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION COÛT
        # ====================================================

        if not isinstance(
            self.cout,
            (int, float),
        ):
            raise TypeError(
                "Le coût du travail doit être un nombre."
            )

        if self.cout < 0:
            raise ValueError(
                "Le coût du travail ne peut pas être négatif."
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