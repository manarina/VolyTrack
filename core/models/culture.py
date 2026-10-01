"""
Modèle Culture
==============

Représente une culture agricole associée à une parcelle
dans VolyTrack.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Culture:
    """
    Représente une culture agricole.

    Attributes
    ----------
    parcelle_id : int
        Identifiant de la parcelle associée.
    nom : str
        Nom de la culture.
    variete : Optional[str]
        Variété de la culture.
    date_semis : Optional[str]
        Date de semis au format YYYY-MM-DD.
    date_prevue_recolte : Optional[str]
        Date prévue de récolte au format YYYY-MM-DD.
    statut : str
        État actuel de la culture.
    description : Optional[str]
        Description complémentaire.
    id : Optional[int]
        Identifiant de la culture en base de données.
    """

    parcelle_id: int
    nom: str
    variete: Optional[str] = None
    date_semis: Optional[str] = None
    date_prevue_recolte: Optional[str] = None
    statut: str = "Planifiée"
    description: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """Valide les données de la culture."""

        # ====================================================
        # VALIDATION PARCELLE
        # ====================================================

        if not isinstance(self.parcelle_id, int):
            raise TypeError(
                "L'identifiant de la parcelle doit être un entier."
            )

        if self.parcelle_id <= 0:
            raise ValueError(
                "L'identifiant de la parcelle doit être strictement positif."
            )

        # ====================================================
        # VALIDATION NOM
        # ====================================================

        if not isinstance(self.nom, str):
            raise TypeError(
                "Le nom de la culture doit être une chaîne de caractères."
            )

        if not self.nom.strip():
            raise ValueError(
                "Le nom de la culture ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION VARIÉTÉ
        # ====================================================

        if (
            self.variete is not None
            and not isinstance(self.variete, str)
        ):
            raise TypeError(
                "La variété doit être une chaîne ou None."
            )

        # ====================================================
        # VALIDATION DATES
        # ====================================================

        if (
            self.date_semis is not None
            and not isinstance(self.date_semis, str)
        ):
            raise TypeError(
                "La date de semis doit être une chaîne ou None."
            )

        if (
            self.date_prevue_recolte is not None
            and not isinstance(
                self.date_prevue_recolte,
                str,
            )
        ):
            raise TypeError(
                "La date prévue de récolte doit être une chaîne ou None."
            )

        # ====================================================
        # VALIDATION STATUT
        # ====================================================

        if not isinstance(self.statut, str):
            raise TypeError(
                "Le statut doit être une chaîne de caractères."
            )

        if not self.statut.strip():
            raise ValueError(
                "Le statut ne peut pas être vide."
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
            and not isinstance(self.id, int)
        ):
            raise TypeError(
                "L'identifiant doit être un entier ou None."
            )