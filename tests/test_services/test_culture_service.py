
"""
Tests du service Culture
========================

Couverture :

- initialisation
- CREATE
- GET BY ID
- GET ALL
- GET BY PARCELLE
- UPDATE
- DELETE
- existence
- existence de la parcelle
- validation métier
- recherche
- validations des types
- validations des identifiants
"""

import pytest

from core.database.schema import create_tables
from core.models.culture import Culture
from core.models.parcelle import Parcelle
from core.repositories.culture_repository import CultureRepository
from core.repositories.parcelle_repository import ParcelleRepository
from core.services.culture_service import CultureService


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def culture_repository():
    """
    Initialise les tables et retourne le repository Culture.
    """

    create_tables()

    return CultureRepository()


@pytest.fixture
def parcelle_repository():
    """
    Initialise les tables et retourne le repository Parcelle.
    """

    create_tables()

    return ParcelleRepository()


@pytest.fixture
def service(
    culture_repository,
    parcelle_repository,
):
    """
    Retourne un CultureService configuré
    avec ses deux repositories.
    """

    return CultureService(
        repository=culture_repository,
        parcelle_repository=parcelle_repository,
    )


@pytest.fixture
def parcelle(
    parcelle_repository,
):
    """
    Crée une parcelle de test.
    """

    return parcelle_repository.create(
        Parcelle(
            nom="Parcelle Culture Test",
            superficie=2.0,
            unite_superficie="ha",
            localisation="Zone Test",
            description="Parcelle utilisée pour les tests",
        )
    )


@pytest.fixture
def culture(
    service,
    parcelle,
):
    """
    Crée une culture de test.
    """

    return service.create_culture(
        Culture(
            parcelle_id=parcelle.id,
            nom="Riz",
            variete="Makalioka",
            date_semis="2026-06-01",
            date_prevue_recolte="2026-10-01",
            statut="En cours",
            description="Culture de test",
        )
    )


# ============================================================
# INITIALISATION
# ============================================================


def test_service_initialization():
    """
    Vérifie l'initialisation automatique des repositories.
    """

    service = CultureService()

    assert isinstance(
        service.repository,
        CultureRepository,
    )

    assert isinstance(
        service.parcelle_repository,
        ParcelleRepository,
    )


def test_service_invalid_culture_repository(
    parcelle_repository,
):
    """
    Vérifie qu'un mauvais repository Culture est refusé.
    """

    with pytest.raises(TypeError):
        CultureService(
            repository="repository invalide",
            parcelle_repository=parcelle_repository,
        )


def test_service_invalid_parcelle_repository(
    culture_repository,
):
    """
    Vérifie qu'un mauvais repository Parcelle est refusé.
    """

    with pytest.raises(TypeError):
        CultureService(
            repository=culture_repository,
            parcelle_repository="repository invalide",
        )


# ============================================================
# CREATE
# ============================================================


def test_create_culture(
    service,
    parcelle,
):
    """
    Vérifie la création d'une culture.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Maïs",
        variete="Local",
        date_semis="2026-05-01",
        date_prevue_recolte="2026-09-01",
        statut="Planifiée",
    )

    result = service.create_culture(
        culture
    )

    assert result is culture
    assert result.id is not None
    assert result.id > 0
    assert result.parcelle_id == parcelle.id
    assert result.nom == "Maïs"


def test_create_culture_invalid_type(
    service,
):
    """
    Vérifie qu'un mauvais type est refusé.
    """

    with pytest.raises(TypeError):
        service.create_culture(
            "culture invalide"
        )


def test_create_culture_invalid_parcelle(
    service,
):
    """
    Vérifie qu'une culture ne peut pas être créée
    avec une parcelle inexistante.
    """

    culture = Culture(
        parcelle_id=999999,
        nom="Riz",
        variete="Makalioka",
        date_semis="2026-06-01",
        date_prevue_recolte="2026-10-01",
    )

    with pytest.raises(ValueError):
        service.create_culture(
            culture
        )


# ============================================================
# GET BY ID
# ============================================================


def test_get_culture(
    service,
    culture,
):
    """
    Vérifie la récupération d'une culture.
    """

    result = service.get_culture(
        culture.id
    )

    assert result is not None
    assert result.id == culture.id
    assert result.parcelle_id == culture.parcelle_id
    assert result.nom == culture.nom


def test_get_culture_not_found(
    service,
):
    """
    Vérifie qu'une culture inexistante retourne None.
    """

    result = service.get_culture(
        999999
    )

    assert result is None


def test_get_culture_invalid_type(
    service,
):
    """
    Vérifie qu'un ID non entier est refusé.
    """

    with pytest.raises(TypeError):
        service.get_culture(
            "1"
        )


def test_get_culture_invalid_zero(
    service,
):
    """
    Vérifie qu'un ID égal à zéro est refusé.
    """

    with pytest.raises(ValueError):
        service.get_culture(
            0
        )


def test_get_culture_invalid_negative(
    service,
):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(ValueError):
        service.get_culture(
            -1
        )


# ============================================================
# GET ALL
# ============================================================


def test_get_all_cultures(
    service,
    culture,
):
    """
    Vérifie que toutes les cultures sont retournées.
    """

    result = service.get_all_cultures()

    assert isinstance(
        result,
        list,
    )

    assert any(
        item.id == culture.id
        for item in result
    )


def test_get_all_cultures_returns_culture_instances(
    service,
    culture,
):
    """
    Vérifie que get_all retourne uniquement
    des objets Culture.
    """

    result = service.get_all_cultures()

    assert all(
        isinstance(item, Culture)
        for item in result
    )


# ============================================================
# GET BY PARCELLE
# ============================================================


def test_get_cultures_by_parcelle(
    service,
    parcelle,
):
    """
    Vérifie la récupération des cultures
    d'une parcelle.
    """

    first = service.create_culture(
        Culture(
            parcelle_id=parcelle.id,
            nom="Riz",
            variete="Makalioka",
            date_semis="2026-06-01",
        )
    )

    second = service.create_culture(
        Culture(
            parcelle_id=parcelle.id,
            nom="Maïs",
            variete="Local",
            date_semis="2026-06-05",
        )
    )

    result = service.get_cultures_by_parcelle(
        parcelle.id
    )

    ids = [
        item.id
        for item in result
    ]

    assert first.id in ids
    assert second.id in ids


def test_get_cultures_by_parcelle_returns_correct_parcelle(
    service,
    parcelle,
):
    """
    Vérifie que toutes les cultures retournées
    appartiennent à la parcelle demandée.
    """

    service.create_culture(
        Culture(
            parcelle_id=parcelle.id,
            nom="Riz",
            variete="Makalioka",
        )
    )

    result = service.get_cultures_by_parcelle(
        parcelle.id
    )

    assert all(
        item.parcelle_id == parcelle.id
        for item in result
    )


def test_get_cultures_by_parcelle_empty(
    service,
):
    """
    Vérifie qu'une parcelle sans culture retourne
    une liste vide.
    """

    result = service.get_cultures_by_parcelle(
        999999
    )

    assert result == []


def test_get_cultures_by_parcelle_invalid_type(
    service,
):
    """
    Vérifie le type de parcelle_id.
    """

    with pytest.raises(TypeError):
        service.get_cultures_by_parcelle(
            "1"
        )


def test_get_cultures_by_parcelle_invalid_zero(
    service,
):
    """
    Vérifie qu'un ID zéro est refusé.
    """

    with pytest.raises(ValueError):
        service.get_cultures_by_parcelle(
            0
        )


def test_get_cultures_by_parcelle_invalid_negative(
    service,
):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(ValueError):
        service.get_cultures_by_parcelle(
            -1
        )


# ============================================================
# UPDATE
# ============================================================


def test_update_culture(
    service,
    culture,
):
    """
    Vérifie la modification d'une culture.
    """

    culture.nom = "Riz Modifié"
    culture.variete = "Nouvelle Variété"
    culture.statut = "Récoltée"
    culture.description = "Culture modifiée"

    result = service.update_culture(
        culture
    )

    assert result is culture

    updated = service.get_culture(
        culture.id
    )

    assert updated is not None
    assert updated.nom == "Riz Modifié"
    assert updated.variete == "Nouvelle Variété"
    assert updated.statut == "Récoltée"
    assert updated.description == "Culture modifiée"


def test_update_culture_without_id(
    service,
    parcelle,
):
    """
    Vérifie qu'une culture sans ID ne peut pas
    être modifiée.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Culture Sans ID",
    )

    with pytest.raises(ValueError):
        service.update_culture(
            culture
        )


def test_update_culture_invalid_type(
    service,
):
    """
    Vérifie qu'un mauvais type est refusé.
    """

    with pytest.raises(TypeError):
        service.update_culture(
            "culture invalide"
        )


def test_update_culture_invalid_id(
    service,
    parcelle,
):
    """
    Vérifie qu'un ID invalide est refusé.
    """

    culture = Culture(
        id=-1,
        parcelle_id=parcelle.id,
        nom="Culture Invalide",
    )

    with pytest.raises(ValueError):
        service.update_culture(
            culture
        )


def test_update_culture_not_found(
    service,
    parcelle,
):
    """
    Vérifie qu'une culture inexistante ne peut pas
    être modifiée.
    """

    culture = Culture(
        id=999999,
        parcelle_id=parcelle.id,
        nom="Culture Inexistante",
    )

    with pytest.raises(ValueError):
        service.update_culture(
            culture
        )


def test_update_culture_invalid_parcelle(
    service,
    culture,
):
    """
    Vérifie qu'une culture ne peut pas être modifiée
    vers une parcelle inexistante.
    """

    culture.parcelle_id = 999999

    with pytest.raises(ValueError):
        service.update_culture(
            culture
        )


# ============================================================
# DELETE
# ============================================================


def test_delete_culture(
    service,
    culture,
):
    """
    Vérifie la suppression d'une culture.
    """

    result = service.delete_culture(
        culture.id
    )

    assert result is True

    assert (
        service.get_culture(
            culture.id
        )
        is None
    )


def test_delete_culture_not_found(
    service,
):
    """
    Vérifie la suppression d'une culture inexistante.
    """

    with pytest.raises(ValueError):
        service.delete_culture(
            999999
        )


def test_delete_culture_invalid_type(
    service,
):
    """
    Vérifie qu'un ID non entier est refusé.
    """

    with pytest.raises(TypeError):
        service.delete_culture(
            "1"
        )


def test_delete_culture_invalid_zero(
    service,
):
    """
    Vérifie qu'un ID égal à zéro est refusé.
    """

    with pytest.raises(ValueError):
        service.delete_culture(
            0
        )


def test_delete_culture_invalid_negative(
    service,
):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(ValueError):
        service.delete_culture(
            -1
        )


# ============================================================
# EXISTENCE
# ============================================================


def test_culture_exists(
    service,
    culture,
):
    """
    Vérifie qu'une culture existante est détectée.
    """

    assert service.culture_exists(
        culture.id
    ) is True


def test_culture_does_not_exist(
    service,
):
    """
    Vérifie qu'une culture inexistante
    est correctement détectée.
    """

    assert service.culture_exists(
        999999
    ) is False


def test_culture_exists_invalid_type(
    service,
):
    """
    Vérifie le type de l'ID.
    """

    with pytest.raises(TypeError):
        service.culture_exists(
            "1"
        )


# ============================================================
# PARCELLE EXISTENCE
# ============================================================


def test_parcelle_exists(
    service,
    parcelle,
):
    """
    Vérifie l'existence d'une parcelle.
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
    Vérifie le type de l'identifiant.
    """

    with pytest.raises(TypeError):
        service.parcelle_exists(
            "1"
        )


def test_parcelle_exists_invalid_zero(
    service,
):
    """
    Vérifie qu'un ID zéro est refusé.
    """

    with pytest.raises(ValueError):
        service.parcelle_exists(
            0
        )


# ============================================================
# VALIDATION
# ============================================================


def test_validate_culture(
    service,
    parcelle,
):
    """
    Vérifie qu'une culture valide est acceptée.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Riz",
        variete="Makalioka",
    )

    assert service.validate_culture(
        culture
    ) is True


def test_validate_culture_invalid_type(
    service,
):
    """
    Vérifie qu'un mauvais type est refusé.
    """

    with pytest.raises(TypeError):
        service.validate_culture(
            "culture invalide"
        )


# ============================================================
# RECHERCHE
# ============================================================


def test_search_cultures(
    service,
    parcelle,
):
    """
    Vérifie la recherche par nom.
    """

    service.create_culture(
        Culture(
            parcelle_id=parcelle.id,
            nom="Riz",
            variete="Makalioka",
        )
    )

    service.create_culture(
        Culture(
            parcelle_id=parcelle.id,
            nom="Maïs",
            variete="Local",
        )
    )

    result = service.search_cultures(
        "riz"
    )

    assert len(result) >= 1

    assert any(
        "riz" in item.nom.lower()
        for item in result
    )


def test_search_cultures_case_insensitive(
    service,
    parcelle,
):
    """
    Vérifie que la recherche ignore la casse.
    """

    service.create_culture(
        Culture(
            parcelle_id=parcelle.id,
            nom="Grande Culture",
        )
    )

    result = service.search_cultures(
        "GRANDE"
    )

    assert any(
        item.nom == "Grande Culture"
        for item in result
    )


def test_search_cultures_empty_search(
    service,
    culture,
):
    """
    Une recherche vide retourne toutes les cultures.
    """

    result = service.search_cultures(
        ""
    )

    assert any(
        item.id == culture.id
        for item in result
    )


def test_search_cultures_invalid_type(
    service,
):
    """
    Vérifie que search_term doit être une chaîne.
    """

    with pytest.raises(TypeError):
        service.search_cultures(
            123
        )

