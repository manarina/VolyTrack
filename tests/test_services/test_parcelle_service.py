"""
Tests du service Parcelle
=========================

Couverture :

- initialisation du service
- CREATE
- GET BY ID
- GET ALL
- UPDATE
- DELETE
- existence
- validation métier
- recherche
- validations des identifiants
- validation des types
"""

import pytest

from core.database.schema import create_tables
from core.models.parcelle import Parcelle
from core.repositories.parcelle_repository import ParcelleRepository
from core.services.parcelle_service import ParcelleService


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def repository():
    """
    Initialise les tables et retourne un repository.
    """

    create_tables()

    return ParcelleRepository()


@pytest.fixture
def service(repository):
    """
    Retourne un service utilisant le repository de test.
    """

    return ParcelleService(
        repository=repository
    )


@pytest.fixture
def parcelle(service):
    """
    Crée une parcelle de test.
    """

    return service.create_parcelle(
        Parcelle(
            nom="Parcelle Service Test",
            superficie=2.5,
            unite_superficie="ha",
            localisation="Zone Test",
            description="Parcelle utilisée pour les tests du service",
        )
    )


# ============================================================
# INITIALISATION
# ============================================================


def test_service_initialization():
    """
    Vérifie que le service peut être initialisé
    sans repository explicite.
    """

    service = ParcelleService()

    assert isinstance(
        service.repository,
        ParcelleRepository,
    )


def test_service_invalid_repository():
    """
    Vérifie que le service refuse un mauvais repository.
    """

    with pytest.raises(TypeError):
        ParcelleService(
            repository="repository invalide"
        )


# ============================================================
# CREATE
# ============================================================


def test_create_parcelle(
    service,
):
    """
    Vérifie la création d'une parcelle.
    """

    parcelle = Parcelle(
        nom="Parcelle A",
        superficie=3.0,
        unite_superficie="ha",
        localisation="Nord",
    )

    result = service.create_parcelle(
        parcelle
    )

    assert result is parcelle
    assert result.id is not None
    assert result.id > 0


def test_create_parcelle_invalid_type(
    service,
):
    """
    Vérifie que create_parcelle() refuse un mauvais type.
    """

    with pytest.raises(TypeError):
        service.create_parcelle(
            "parcelle invalide"
        )


# ============================================================
# GET BY ID
# ============================================================


def test_get_parcelle(
    service,
    parcelle,
):
    """
    Vérifie la récupération d'une parcelle.
    """

    result = service.get_parcelle(
        parcelle.id
    )

    assert result is not None
    assert result.id == parcelle.id
    assert result.nom == parcelle.nom
    assert result.superficie == parcelle.superficie


def test_get_parcelle_not_found(
    service,
):
    """
    Vérifie qu'une parcelle inexistante retourne None.
    """

    result = service.get_parcelle(
        999999
    )

    assert result is None


def test_get_parcelle_invalid_type(
    service,
):
    """
    Vérifie qu'un ID non entier est refusé.
    """

    with pytest.raises(TypeError):
        service.get_parcelle(
            "1"
        )


def test_get_parcelle_invalid_zero(
    service,
):
    """
    Vérifie qu'un ID égal à zéro est refusé.
    """

    with pytest.raises(ValueError):
        service.get_parcelle(
            0
        )


def test_get_parcelle_invalid_negative(
    service,
):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(ValueError):
        service.get_parcelle(
            -1
        )


# ============================================================
# GET ALL
# ============================================================


def test_get_all_parcelles(
    service,
    parcelle,
):
    """
    Vérifie que toutes les parcelles sont retournées.
    """

    result = service.get_all_parcelles()

    assert isinstance(
        result,
        list,
    )

    assert any(
        item.id == parcelle.id
        for item in result
    )


def test_get_all_parcelles_returns_parcelle_instances(
    service,
    parcelle,
):
    """
    Vérifie que les résultats sont des objets Parcelle.
    """

    result = service.get_all_parcelles()

    assert all(
        isinstance(item, Parcelle)
        for item in result
    )


# ============================================================
# UPDATE
# ============================================================


def test_update_parcelle(
    service,
    parcelle,
):
    """
    Vérifie la modification d'une parcelle.
    """

    parcelle.nom = "Parcelle Modifiée"
    parcelle.superficie = 4.0
    parcelle.localisation = "Nouvelle Zone"

    result = service.update_parcelle(
        parcelle
    )

    assert result is parcelle

    updated = service.get_parcelle(
        parcelle.id
    )

    assert updated is not None
    assert updated.nom == "Parcelle Modifiée"
    assert updated.superficie == 4.0
    assert updated.localisation == "Nouvelle Zone"


def test_update_parcelle_without_id(
    service,
):
    """
    Vérifie qu'une parcelle sans ID ne peut pas
    être modifiée.
    """

    parcelle = Parcelle(
        nom="Sans ID",
        superficie=2.0,
        unite_superficie="ha",
    )

    with pytest.raises(ValueError):
        service.update_parcelle(
            parcelle
        )


def test_update_parcelle_invalid_type(
    service,
):
    """
    Vérifie qu'un mauvais type est refusé.
    """

    with pytest.raises(TypeError):
        service.update_parcelle(
            "parcelle invalide"
        )


def test_update_parcelle_invalid_id(
    service,
):
    """
    Vérifie qu'un ID invalide est refusé.
    """

    parcelle = Parcelle(
        id=-1,
        nom="Parcelle Invalide",
        superficie=2.0,
        unite_superficie="ha",
    )

    with pytest.raises(ValueError):
        service.update_parcelle(
            parcelle
        )


def test_update_parcelle_not_found(
    service,
):
    """
    Vérifie qu'une parcelle inexistante
    ne peut pas être modifiée.
    """

    parcelle = Parcelle(
        id=999999,
        nom="Parcelle Inexistante",
        superficie=2.0,
        unite_superficie="ha",
    )

    with pytest.raises(ValueError):
        service.update_parcelle(
            parcelle
        )


# ============================================================
# DELETE
# ============================================================


def test_delete_parcelle(
    service,
    parcelle,
):
    """
    Vérifie la suppression d'une parcelle.
    """

    result = service.delete_parcelle(
        parcelle.id
    )

    assert result is True

    assert (
        service.get_parcelle(
            parcelle.id
        )
        is None
    )


def test_delete_parcelle_not_found(
    service,
):
    """
    Vérifie qu'une parcelle inexistante
    ne peut pas être supprimée.
    """

    with pytest.raises(ValueError):
        service.delete_parcelle(
            999999
        )


def test_delete_parcelle_invalid_type(
    service,
):
    """
    Vérifie qu'un ID non entier est refusé.
    """

    with pytest.raises(TypeError):
        service.delete_parcelle(
            "1"
        )


def test_delete_parcelle_invalid_zero(
    service,
):
    """
    Vérifie qu'un ID égal à zéro est refusé.
    """

    with pytest.raises(ValueError):
        service.delete_parcelle(
            0
        )


def test_delete_parcelle_invalid_negative(
    service,
):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(ValueError):
        service.delete_parcelle(
            -1
        )


# ============================================================
# EXISTENCE
# ============================================================


def test_parcelle_exists(
    service,
    parcelle,
):
    """
    Vérifie qu'une parcelle existante est détectée.
    """

    assert service.parcelle_exists(
        parcelle.id
    ) is True


def test_parcelle_does_not_exist(
    service,
):
    """
    Vérifie qu'une parcelle inexistante
    est correctement détectée.
    """

    assert service.parcelle_exists(
        999999
    ) is False


def test_parcelle_exists_invalid_type(
    service,
):
    """
    Vérifie la validation du type de l'ID.
    """

    with pytest.raises(TypeError):
        service.parcelle_exists(
            "1"
        )


# ============================================================
# VALIDATION MÉTIER
# ============================================================


def test_validate_parcelle(
    service,
):
    """
    Vérifie qu'une parcelle valide est acceptée.
    """

    parcelle = Parcelle(
        nom="Parcelle Valide",
        superficie=2.0,
        unite_superficie="ha",
    )

    assert service.validate_parcelle(
        parcelle
    ) is True


def test_validate_parcelle_invalid_type(
    service,
):
    """
    Vérifie qu'un mauvais type est refusé.
    """

    with pytest.raises(TypeError):
        service.validate_parcelle(
            "parcelle invalide"
        )


# ============================================================
# SEARCH
# ============================================================


def test_search_parcelles(
    service,
):
    """
    Vérifie la recherche par nom.
    """

    service.create_parcelle(
        Parcelle(
            nom="Parcelle Riz",
            superficie=2.0,
            unite_superficie="ha",
        )
    )

    service.create_parcelle(
        Parcelle(
            nom="Parcelle Maïs",
            superficie=3.0,
            unite_superficie="ha",
        )
    )

    result = service.search_parcelles(
        "riz"
    )

    assert len(result) >= 1

    assert any(
        "riz" in item.nom.lower()
        for item in result
    )


def test_search_parcelles_case_insensitive(
    service,
):
    """
    Vérifie que la recherche n'est pas sensible
    aux majuscules/minuscules.
    """

    service.create_parcelle(
        Parcelle(
            nom="Grande Parcelle",
            superficie=2.0,
            unite_superficie="ha",
        )
    )

    result = service.search_parcelles(
        "GRANDE"
    )

    assert any(
        item.nom == "Grande Parcelle"
        for item in result
    )


def test_search_parcelles_empty_search(
    service,
    parcelle,
):
    """
    Une recherche vide retourne toutes les parcelles.
    """

    result = service.search_parcelles(
        ""
    )

    assert any(
        item.id == parcelle.id
        for item in result
    )


def test_search_parcelles_invalid_type(
    service,
):
    """
    Vérifie que search_term doit être une chaîne.
    """

    with pytest.raises(TypeError):
        service.search_parcelles(
            123
        )

