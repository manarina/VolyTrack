"""
Modèle Revenu
=============

Représente un revenu issu de la vente d'une production agricole
dans VolyTrack.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Revenu:
    """
    Représente un revenu agricole.

    Attributes
    ----------
    produit : str
        Nom du produit vendu.
    quantite : float
        Quantité vendue.
    prix_unitaire : float
        Prix de vente par unité.
    montant : float
        Montant total du revenu.
    date_revenu : str
        Date du revenu au format YYYY-MM-DD.
    parcelle_id : Optional[int]
        Identifiant de la parcelle concernée.
    culture_id : Optional[int]
        Identifiant de la culture concernée.
    description : Optional[str]
        Description complémentaire.
    id : Optional[int]
        Identifiant du revenu en base de données.
    """

    produit: str
    quantite: float
    prix_unitaire: float
    montant: float
    date_revenu: str
    parcelle_id: Optional[int] = None
    culture_id: Optional[int] = None
    description: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """Valide les données du revenu."""

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
        # VALIDATION PRODUIT
        # ====================================================

        if not isinstance(
            self.produit,
            str,
        ):
            raise TypeError(
                "Le produit doit être une chaîne de caractères."
            )

        if not self.produit.strip():
            raise ValueError(
                "Le produit ne peut pas être vide."
            )

        # ====================================================
        # VALIDATION QUANTITÉ
        # ====================================================

        if not isinstance(
            self.quantite,
            (int, float),
        ):
            raise TypeError(
                "La quantité doit être un nombre."
            )

        if self.quantite <= 0:
            raise ValueError(
                "La quantité doit être strictement positive."
            )

        # ====================================================
        # VALIDATION PRIX UNITAIRE
        # ====================================================

        if not isinstance(
            self.prix_unitaire,
            (int, float),
        ):
            raise TypeError(
                "Le prix unitaire doit être un nombre."
            )

        if self.prix_unitaire < 0:
            raise ValueError(
                "Le prix unitaire ne peut pas être négatif."
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
            self.date_revenu,
            str,
        ):
            raise TypeError(
                "La date du revenu doit être une chaîne "
                "de caractères."
            )

        if not self.date_revenu.strip():
            raise ValueError(
                "La date du revenu ne peut pas être vide."
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