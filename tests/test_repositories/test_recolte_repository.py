
"""
Tests du repository Recolte
===========================

Couverture :

- CREATE
- GET BY ID
- GET ALL
- GET BY CULTURE
- UPDATE
- DELETE
- validations des types
- validations des identifiants
- gestion des récoltes inexistantes
"""

import pytest

from core.database.schema import create_tables
from core.models.culture import Culture
from core.models.parcelle import Parcelle
from core.models.recolte import Recolte
from core.repositories.culture_repository import CultureRepository
from core.repositories.parcelle_repository import ParcelleRepository
from core.repositories.recolte_repository import RecolteRepository


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def repository():
    """
    Initialise les tables et retourne le repository.
    """

    create_tables()

    return RecolteRepository()


@pytest.fixture
def culture():
    """
    Crée une parcelle puis une culture de test.

    Une récolte doit obligatoirement être associée
    à une culture existante.
    """

    create_tables()

    parcelle_repository = ParcelleRepository()
    culture_repository = CultureRepository()

    parcelle = parcelle_repository.create(
        Parcelle(
            nom="Parcelle Test Recolte",
            superficie=2.0,
            unite_superficie="ha",
            localisation="Zone Test",
            description="Parcelle utilisée pour les tests de récolte",
        )
    )

    return culture_repository.create(
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


@pytest.fixture
def recolte(repository, culture):
    """
    Crée une récolte de test.
    """

    return repository.create(
        Recolte(
            culture_id=culture.id,
            date_recolte="2026-10-01",
            quantite=500.0,
            unite="kg",
            qualite="Bonne",
            description="Récolte principale",
        )
    )


# ============================================================
# CREATE
# ============================================================


def test_create_recolte(repository, culture):
    """
    Vérifie qu'une récolte peut être créée.
    """

    recolte = Recolte(
        culture_id=culture.id,
        date_recolte="2026-10-01",
        quantite=500.0,
        unite="kg",
        qualite="Bonne",
        description="Première récolte",
    )

    result = repository.create(recolte)

    assert result is recolte
    assert result.id is not None
    assert result.id > 0
    assert result.culture_id == culture.id
    assert result.date_recolte == "2026-10-01"
    assert result.quantite == 500.0
    assert result.unite == "kg"
    assert result.qualite == "Bonne"
    assert result.description == "Première récolte"


def test_create_recolte_without_optional_fields(
    repository,
    culture,
):
    """
    Vérifie que les champs optionnels peuvent être absents.
    """

    recolte = Recolte(
        culture_id=culture.id,
        date_recolte="2026-10-02",
        quantite=250.0,
        unite="kg",
    )

    result = repository.create(recolte)

    assert result.id is not None
    assert result.qualite is None
    assert result.description is None


def test_create_recolte_persists_data(
    repository,
    culture,
):
    """
    Vérifie que la récolte créée est réellement persistée.
    """

    recolte = Recolte(
        culture_id=culture.id,
        date_recolte="2026-10-03",
        quantite=750.0,
        unite="kg",
        qualite="Excellente",
        description="Grande récolte",
    )

    created = repository.create(recolte)

    result = repository.get_by_id(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.culture_id == culture.id
    assert result.date_recolte == "2026-10-03"
    assert result.quantite == 750.0
    assert result.unite == "kg"
    assert result.qualite == "Excellente"
    assert result.description == "Grande récolte"


def test_create_recolte_invalid_type(repository):
    """
    Vérifie que create() refuse un objet qui n'est pas
    une instance de Recolte.
    """

    with pytest.raises(TypeError):
        repository.create(
            "recolte invalide"
        )


# ============================================================
# GET BY ID
# ============================================================


def test_get_recolte_by_id(repository, recolte):
    """
    Vérifie la récupération d'une récolte par son ID.
    """

    result = repository.get_by_id(
        recolte.id
    )

    assert result is not None
    assert result.id == recolte.id
    assert result.culture_id == recolte.culture_id
    assert result.date_recolte == recolte.date_recolte
    assert result.quantite == recolte.quantite
    assert result.unite == recolte.unite
    assert result.qualite == recolte.qualite
    assert result.description == recolte.description


def test_get_recolte_by_id_not_found(repository):
    """
    Vérifie qu'une récolte inexistante retourne None.
    """

    result = repository.get_by_id(999999)

    assert result is None


def test_get_recolte_by_id_invalid_type(repository):
    """
    Vérifie que get_by_id() refuse un ID non entier.
    """

    with pytest.raises(TypeError):
        repository.get_by_id("1")


def test_get_recolte_by_id_invalid_zero(repository):
    """
    Vérifie qu'un ID égal à zéro est refusé.
    """

    with pytest.raises(ValueError):
        repository.get_by_id(0)


def test_get_recolte_by_id_invalid_negative(repository):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(ValueError):
        repository.get_by_id(-1)


# ============================================================
# GET ALL
# ============================================================


def test_get_all_recoltes(repository, recolte):
    """
    Vérifie que get_all() retourne les récoltes existantes.
    """

    result = repository.get_all()

    assert isinstance(result, list)
    assert len(result) >= 1

    ids = [
        item.id
        for item in result
    ]

    assert recolte.id in ids


def test_get_all_recoltes_returns_recolte_instances(
    repository,
    recolte,
):
    """
    Vérifie que get_all() retourne uniquement des objets
    Recolte.
    """

    result = repository.get_all()

    assert all(
        isinstance(item, Recolte)
        for item in result
    )


def test_get_all_recoltes_ordered_by_id(
    repository,
    culture,
):
    """
    Vérifie que les résultats sont ordonnés par ID.
    """

    first = repository.create(
        Recolte(
            culture_id=culture.id,
            date_recolte="2026-10-04",
            quantite=100.0,
            unite="kg",
        )
    )

    second = repository.create(
        Recolte(
            culture_id=culture.id,
            date_recolte="2026-10-05",
            quantite=200.0,
            unite="kg",
        )
    )

    result = repository.get_all()

    ids = [
        item.id
        for item in result
        if item.id in {
            first.id,
            second.id,
        }
    ]

    assert ids == sorted(ids)


# ============================================================
# GET BY CULTURE
# ============================================================


def test_get_recoltes_by_culture(
    repository,
    culture,
):
    """
    Vérifie la récupération des récoltes d'une culture.
    """

    first = repository.create(
        Recolte(
            culture_id=culture.id,
            date_recolte="2026-10-10",
            quantite=100.0,
            unite="kg",
        )
    )

    second = repository.create(
        Recolte(
            culture_id=culture.id,
            date_recolte="2026-10-11",
            quantite=200.0,
            unite="kg",
        )
    )

    result = repository.get_by_culture_id(
        culture.id
    )

    ids = [
        item.id
        for item in result
    ]

    assert first.id in ids
    assert second.id in ids


def test_get_recoltes_by_culture_returns_correct_culture(
    repository,
    culture,
):
    """
    Vérifie que les résultats appartiennent bien
    à la culture demandée.
    """

    repository.create(
        Recolte(
            culture_id=culture.id,
            date_recolte="2026-10-12",
            quantite=300.0,
            unite="kg",
        )
    )

    result = repository.get_by_culture_id(
        culture.id
    )

    assert all(
        item.culture_id == culture.id
        for item in result
    )


def test_get_recoltes_by_culture_empty(repository):
    """
    Vérifie qu'une culture sans récolte retourne
    une liste vide.
    """

    result = repository.get_by_culture_id(
        999999
    )

    assert result == []


def test_get_recoltes_by_culture_invalid_type(
    repository,
):
    """
    Vérifie que culture_id doit être un entier.
    """

    with pytest.raises(TypeError):
        repository.get_by_culture_id("1")


def test_get_recoltes_by_culture_invalid_zero(
    repository,
):
    """
    Vérifie qu'un culture_id égal à zéro est refusé.
    """

    with pytest.raises(ValueError):
        repository.get_by_culture_id(0)


def test_get_recoltes_by_culture_invalid_negative(
    repository,
):
    """
    Vérifie qu'un culture_id négatif est refusé.
    """

    with pytest.raises(ValueError):
        repository.get_by_culture_id(-1)


# ============================================================
# UPDATE
# ============================================================


def test_update_recolte(
    repository,
    recolte,
):
    """
    Vérifie la modification d'une récolte.
    """

    recolte.culture_id = recolte.culture_id
    recolte.date_recolte = "2026-11-01"
    recolte.quantite = 800.0
    recolte.unite = "kg"
    recolte.qualite = "Excellente"
    recolte.description = "Récolte modifiée"

    result = repository.update(
        recolte
    )

    assert result is recolte

    updated = repository.get_by_id(
        recolte.id
    )

    assert updated is not None
    assert updated.date_recolte == "2026-11-01"
    assert updated.quantite == 800.0
    assert updated.unite == "kg"
    assert updated.qualite == "Excellente"
    assert updated.description == "Récolte modifiée"


def test_update_recolte_without_id(
    repository,
    culture,
):
    """
    Vérifie qu'une récolte sans ID ne peut pas être modifiée.
    """

    recolte = Recolte(
        culture_id=culture.id,
        date_recolte="2026-11-02",
        quantite=400.0,
        unite="kg",
    )

    with pytest.raises(ValueError):
        repository.update(recolte)


def test_update_recolte_invalid_type(
    repository,
):
    """
    Vérifie que update() refuse un mauvais type.
    """

    with pytest.raises(TypeError):
        repository.update(
            "recolte invalide"
        )


def test_update_recolte_invalid_id_type(
    repository,
    culture,
):
    """
    Vérifie que le repository détecte un ID
    qui n'est pas un entier.
    """

    # Création avec un ID valide afin de passer
    # la validation du modèle Recolte.
    recolte = Recolte(
        id=1,
        culture_id=culture.id,
        date_recolte="2026-11-03",
        quantite=400.0,
        unite="kg",
    )

    # Modification volontaire après construction
    # pour tester spécifiquement la validation
    # effectuée par le repository.
    recolte.id = "1"

    with pytest.raises(TypeError):
        repository.update(recolte)



def test_update_recolte_invalid_id(
    repository,
    culture,
):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    recolte = Recolte(
        id=-1,
        culture_id=culture.id,
        date_recolte="2026-11-04",
        quantite=400.0,
        unite="kg",
    )

    with pytest.raises(ValueError):
        repository.update(recolte)


def test_update_recolte_not_found(
    repository,
    culture,
):
    """
    Vérifie qu'une récolte inexistante ne peut pas être modifiée.
    """

    recolte = Recolte(
        id=999999,
        culture_id=culture.id,
        date_recolte="2026-11-05",
        quantite=400.0,
        unite="kg",
    )

    with pytest.raises(ValueError):
        repository.update(recolte)


# ============================================================
# DELETE
# ============================================================


def test_delete_recolte(
    repository,
    recolte,
):
    """
    Vérifie la suppression d'une récolte.
    """

    result = repository.delete(
        recolte.id
    )

    assert result is True

    deleted = repository.get_by_id(
        recolte.id
    )

    assert deleted is None


def test_delete_recolte_not_found(
    repository,
):
    """
    Vérifie qu'une récolte inexistante provoque
    une erreur lors de la suppression.
    """

    with pytest.raises(ValueError):
        repository.delete(999999)


def test_delete_recolte_invalid_type(
    repository,
):
    """
    Vérifie que delete() refuse un ID non entier.
    """

    with pytest.raises(TypeError):
        repository.delete("1")


def test_delete_recolte_invalid_zero(
    repository,
):
    """
    Vérifie qu'un ID égal à zéro est refusé.
    """

    with pytest.raises(ValueError):
        repository.delete(0)


def test_delete_recolte_invalid_negative(
    repository,
):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(ValueError):
        repository.delete(-1)


# ============================================================
# INTÉGRITÉ DES DONNÉES
# ============================================================


def test_update_preserves_recolte_id(
    repository,
    recolte,
):
    """
    Vérifie que l'ID reste inchangé après modification.
    """

    original_id = recolte.id

    recolte.quantite = 1200.0

    repository.update(recolte)

    assert recolte.id == original_id

    result = repository.get_by_id(
        original_id
    )

    assert result is not None
    assert result.id == original_id
    assert result.quantite == 1200.0


def test_create_multiple_recoltes(
    repository,
    culture,
):
    """
    Vérifie la création de plusieurs récoltes.
    """

    recoltes = []

    for index in range(3):

        recolte = repository.create(
            Recolte(
                culture_id=culture.id,
                date_recolte=f"2026-10-{15 + index}",
                quantite=100.0 * (index + 1),
                unite="kg",
            )
        )

        recoltes.append(recolte)

    assert len(recoltes) == 3

    ids = [
        item.id
        for item in recoltes
    ]

    assert len(set(ids)) == 3

