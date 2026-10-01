"""
Modèle Parcelle
===============

Représente une parcelle agricole dans VolyTrack.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Parcelle:
    """
    Représente une parcelle agricole.

    Attributes
    ----------
    nom : str
        Nom de la parcelle.
    superficie : float
        Superficie de la parcelle.
    unite_superficie : str
        Unité utilisée pour la superficie.
    localisation : Optional[str]
        Localisation de la parcelle.
    description : Optional[str]
        Description complémentaire.
    id : Optional[int]
        Identifiant de la parcelle en base de données.
    """

    nom: str
    superficie: float
    unite_superficie: str = "ha"
    localisation: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """
        Valide les données de la parcelle après sa création.
        """

        # ====================================================
        # VALIDATION DU NOM
        # ====================================================

        if not isinstance(self.nom, str):
            raise TypeError(
                "Le nom de la parcelle doit être une chaîne de caractères."
            )

        if not self.nom.strip():
            raise ValueError(
                "Le nom de la parcelle ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION DE LA SUPERFICIE
        # ====================================================

        if not isinstance(
            self.superficie,
            (int, float),
        ):
            raise TypeError(
                "La superficie doit être un nombre."
            )

        if self.superficie <= 0:
            raise ValueError(
                "La superficie doit être strictement positive."
            )

        # ====================================================
        # VALIDATION DE L'UNITÉ
        # ====================================================

        if not isinstance(
            self.unite_superficie,
            str,
        ):
            raise TypeError(
                "L'unité de superficie doit être une chaîne de caractères."
            )

        if not self.unite_superficie.strip():
            raise ValueError(
                "L'unité de superficie ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION DE LA LOCALISATION
        # ====================================================

        if (
            self.localisation is not None
            and not isinstance(
                self.localisation,
                str,
            )
        ):
            raise TypeError(
                "La localisation doit être une chaîne ou None."
            )

        # ====================================================
        # VALIDATION DE LA DESCRIPTION
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
        # VALIDATION DE L'ID
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