"""
Modèle Recolte
==============

Représente une récolte agricole issue d'une culture
dans VolyTrack.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Recolte:
    """
    Représente une récolte agricole.

    Attributes
    ----------
    culture_id : int
        Identifiant de la culture récoltée.
    date_recolte : str
        Date de la récolte.
    quantite : float
        Quantité récoltée.
    unite : str
        Unité de mesure de la quantité.
    qualite : Optional[str]
        Qualité de la récolte.
    description : Optional[str]
        Description complémentaire.
    id : Optional[int]
        Identifiant de la récolte en base de données.
    """

    culture_id: int
    date_recolte: str
    quantite: float
    unite: str
    qualite: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """Valide les données de la récolte."""

        # ====================================================
        # VALIDATION CULTURE
        # ====================================================

        if not isinstance(
            self.culture_id,
            int,
        ):
            raise TypeError(
                "L'identifiant de la culture doit être un entier."
            )

        if self.culture_id <= 0:
            raise ValueError(
                "L'identifiant de la culture doit être "
                "strictement positif."
            )

        # ====================================================
        # VALIDATION DATE
        # ====================================================

        if not isinstance(
            self.date_recolte,
            str,
        ):
            raise TypeError(
                "La date de récolte doit être une chaîne "
                "de caractères."
            )

        if not self.date_recolte.strip():
            raise ValueError(
                "La date de récolte ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION QUANTITÉ
        # ====================================================

        if not isinstance(
            self.quantite,
            (int, float),
        ):
            raise TypeError(
                "La quantité récoltée doit être un nombre."
            )

        if self.quantite <= 0:
            raise ValueError(
                "La quantité récoltée doit être "
                "strictement positive."
            )

        # ====================================================
        # VALIDATION UNITÉ
        # ====================================================

        if not isinstance(
            self.unite,
            str,
        ):
            raise TypeError(
                "L'unité doit être une chaîne de caractères."
            )

        if not self.unite.strip():
            raise ValueError(
                "L'unité ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION QUALITÉ
        # ====================================================

        if (
            self.qualite is not None
            and not isinstance(
                self.qualite,
                str,
            )
        ):
            raise TypeError(
                "La qualité doit être une chaîne ou None."
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