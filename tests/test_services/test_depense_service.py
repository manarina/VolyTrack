"""
Tests du service Depense
========================

Couverture :

- initialisation
- CREATE
- validation métier
- existence parcelle
- existence culture
- cohérence culture / parcelle
- GET BY ID
- GET ALL
- GET BY PARCELLE
- GET BY CULTURE
- UPDATE
- DELETE
- existence
- recherche
- validations des types
- validations des identifiants
"""

import pytest

from core.database.schema import create_tables

from core.models.depense import Depense
from core.models.parcelle import Parcelle
from core.models.culture import Culture

from core.repositories.depense_repository import DepenseRepository
from core.repositories.parcelle_repository import ParcelleRepository
from core.repositories.culture_repository import CultureRepository

from core.services.depense_service import DepenseService


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def depense_repository():
    create_tables()
    return DepenseRepository()


@pytest.fixture
def parcelle_repository():
    create_tables()
    return ParcelleRepository()


@pytest.fixture
def culture_repository():
    create_tables()
    return CultureRepository()


@pytest.fixture
def service(
    depense_repository,
    parcelle_repository,
    culture_repository,
):
    return DepenseService(
        repository=depense_repository,
        parcelle_repository=parcelle_repository,
        culture_repository=culture_repository,
    )


@pytest.fixture
def parcelle(
    parcelle_repository,
):
    return parcelle_repository.create(
        Parcelle(
            nom="Parcelle Depense Test",
            superficie=3.0,
            unite_superficie="ha",
            localisation="Zone Test",
        )
    )


@pytest.fixture
def culture(
    culture_repository,
    parcelle,
):
    return culture_repository.create(
        Culture(
            parcelle_id=parcelle.id,
            nom="Riz",
            variete="Makalioka",
            date_semis="2026-06-01",
            statut="En cours",
        )
    )


@pytest.fixture
def depense(
    service,
    parcelle,
    culture,
):
    return service.create_depense(
        Depense(
            categorie="Semences",
            montant=25000.0,
            date_depense="2026-06-01",
            parcelle_id=parcelle.id,
            culture_id=culture.id,
            description="Achat de semences",
        )
    )


# ============================================================
# INITIALISATION
# ============================================================


def test_service_initialization():

    service = DepenseService()

    assert isinstance(
        service.repository,
        DepenseRepository,
    )

    assert isinstance(
        service.parcelle_repository,
        ParcelleRepository,
    )

    assert isinstance(
        service.culture_repository,
        CultureRepository,
    )


def test_service_invalid_depense_repository(
    parcelle_repository,
    culture_repository,
):

    with pytest.raises(TypeError):

        DepenseService(
            repository="repository invalide",
            parcelle_repository=parcelle_repository,
            culture_repository=culture_repository,
        )


def test_service_invalid_parcelle_repository(
    depense_repository,
    culture_repository,
):

    with pytest.raises(TypeError):

        DepenseService(
            repository=depense_repository,
            parcelle_repository="repository invalide",
            culture_repository=culture_repository,
        )


def test_service_invalid_culture_repository(
    depense_repository,
    parcelle_repository,
):

    with pytest.raises(TypeError):

        DepenseService(
            repository=depense_repository,
            parcelle_repository=parcelle_repository,
            culture_repository="repository invalide",
        )


# ============================================================
# CREATE
# ============================================================


def test_create_depense(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=50000.0,
        date_depense="2026-05-10",
        description="Achat d'engrais",
    )

    result = service.create_depense(
        depense
    )

    assert result is depense
    assert result.id is not None
    assert result.id > 0
    assert result.categorie == "Engrais"
    assert result.montant == 50000.0


def test_create_depense_with_parcelle(
    service,
    parcelle,
):

    depense = Depense(
        categorie="Labour",
        montant=30000.0,
        date_depense="2026-05-15",
        parcelle_id=parcelle.id,
    )

    result = service.create_depense(
        depense
    )

    assert result.id is not None
    assert result.parcelle_id == parcelle.id


def test_create_depense_with_culture(
    service,
    culture,
):

    depense = Depense(
        categorie="Semences",
        montant=20000.0,
        date_depense="2026-06-01",
        culture_id=culture.id,
    )

    result = service.create_depense(
        depense
    )

    assert result.id is not None
    assert result.culture_id == culture.id


def test_create_depense_with_parcelle_and_culture(
    service,
    parcelle,
    culture,
):

    depense = Depense(
        categorie="Traitement",
        montant=35000.0,
        date_depense="2026-06-05",
        parcelle_id=parcelle.id,
        culture_id=culture.id,
    )

    result = service.create_depense(
        depense
    )

    assert result.id is not None
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id


def test_create_depense_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.create_depense(
            "depense invalide"
        )


def test_create_depense_invalid_parcelle(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
        parcelle_id=999999,
    )

    with pytest.raises(
        ValueError,
        match="Aucune parcelle trouvée",
    ):

        service.create_depense(
            depense
        )


def test_create_depense_invalid_culture(
    service,
):

    depense = Depense(
        categorie="Semences",
        montant=20000.0,
        date_depense="2026-06-01",
        culture_id=999999,
    )

    with pytest.raises(
        ValueError,
        match="Aucune culture trouvée",
    ):

        service.create_depense(
            depense
        )


def test_create_depense_culture_wrong_parcelle(
    service,
    parcelle,
    parcelle_repository,
    culture_repository,
):

    other_parcelle = parcelle_repository.create(
        Parcelle(
            nom="Autre Parcelle Depense",
            superficie=4.0,
            unite_superficie="ha",
            localisation="Autre Zone",
        )
    )

    other_culture = culture_repository.create(
        Culture(
            parcelle_id=other_parcelle.id,
            nom="Maïs",
            variete="Local",
        )
    )

    depense = Depense(
        categorie="Semences",
        montant=20000.0,
        date_depense="2026-06-01",
        parcelle_id=parcelle.id,
        culture_id=other_culture.id,
    )

    with pytest.raises(
        ValueError,
        match="n'appartient pas",
    ):

        service.create_depense(
            depense
        )


# ============================================================
# GET BY ID
# ============================================================


def test_get_depense(
    service,
    depense,
):

    result = service.get_depense(
        depense.id
    )

    assert result is not None
    assert result.id == depense.id
    assert result.categorie == depense.categorie
    assert result.montant == depense.montant


def test_get_depense_not_found(
    service,
):

    result = service.get_depense(
        999999
    )

    assert result is None


def test_get_depense_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.get_depense(
            "1"
        )


def test_get_depense_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.get_depense(
            0
        )


def test_get_depense_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.get_depense(
            -1
        )


# ============================================================
# GET ALL
# ============================================================


def test_get_all_depenses(
    service,
    depense,
):

    result = service.get_all_depenses()

    assert isinstance(
        result,
        list,
    )

    assert any(
        item.id == depense.id
        for item in result
    )


def test_get_all_depenses_returns_instances(
    service,
    depense,
):

    result = service.get_all_depenses()

    assert all(
        isinstance(
            item,
            Depense,
        )
        for item in result
    )


# ============================================================
# GET BY PARCELLE
# ============================================================


def test_get_depenses_by_parcelle(
    service,
    depense,
    parcelle,
):

    result = service.get_depenses_by_parcelle(
        parcelle.id
    )

    assert any(
        item.id == depense.id
        for item in result
    )


def test_get_depenses_by_parcelle_empty(
    service,
):

    result = service.get_depenses_by_parcelle(
        999999
    )

    assert result == []


def test_get_depenses_by_parcelle_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.get_depenses_by_parcelle(
            "1"
        )


def test_get_depenses_by_parcelle_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.get_depenses_by_parcelle(
            0
        )


def test_get_depenses_by_parcelle_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.get_depenses_by_parcelle(
            -1
        )


# ============================================================
# GET BY CULTURE
# ============================================================


def test_get_depenses_by_culture(
    service,
    depense,
    culture,
):

    result = service.get_depenses_by_culture(
        culture.id
    )

    assert any(
        item.id == depense.id
        for item in result
    )


def test_get_depenses_by_culture_empty(
    service,
):

    result = service.get_depenses_by_culture(
        999999
    )

    assert result == []


def test_get_depenses_by_culture_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.get_depenses_by_culture(
            "1"
        )


def test_get_depenses_by_culture_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.get_depenses_by_culture(
            0
        )


def test_get_depenses_by_culture_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.get_depenses_by_culture(
            -1
        )


# ============================================================
# UPDATE
# ============================================================


def test_update_depense(
    service,
    depense,
):

    depense.categorie = "Engrais"
    depense.montant = 45000.0
    depense.description = "Nouvel achat d'engrais"

    result = service.update_depense(
        depense
    )

    assert result is depense

    updated = service.get_depense(
        depense.id
    )

    assert updated is not None
    assert updated.categorie == "Engrais"
    assert updated.montant == 45000.0
    assert updated.description == "Nouvel achat d'engrais"


def test_update_depense_without_id(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    with pytest.raises(ValueError):

        service.update_depense(
            depense
        )


def test_update_depense_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.update_depense(
            "depense invalide"
        )


def test_update_depense_invalid_id(
    service,
    depense,
):

    # Le modèle peut valider l'ID lors de sa construction.
    # On modifie donc l'objet après sa création afin de
    # tester la validation propre au service.

    depense.id = -1

    with pytest.raises(ValueError):

        service.update_depense(
            depense
        )


def test_update_depense_not_found(
    service,
    parcelle,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
        parcelle_id=parcelle.id,
    )

    depense.id = 999999

    with pytest.raises(ValueError):

        service.update_depense(
            depense
        )


def test_update_depense_invalid_parcelle(
    service,
    depense,
):

    depense.parcelle_id = 999999

    with pytest.raises(ValueError):

        service.update_depense(
            depense
        )


def test_update_depense_invalid_culture(
    service,
    depense,
):

    depense.culture_id = 999999

    with pytest.raises(ValueError):

        service.update_depense(
            depense
        )


def test_update_depense_culture_wrong_parcelle(
    service,
    depense,
    parcelle_repository,
    culture_repository,
):

    other_parcelle = parcelle_repository.create(
        Parcelle(
            nom="Parcelle Update Depense",
            superficie=5.0,
            unite_superficie="ha",
            localisation="Zone Update",
        )
    )

    other_culture = culture_repository.create(
        Culture(
            parcelle_id=other_parcelle.id,
            nom="Maïs",
            variete="Local",
        )
    )

    depense.parcelle_id = (
        depense.parcelle_id
    )

    depense.culture_id = (
        other_culture.id
    )

    with pytest.raises(ValueError):

        service.update_depense(
            depense
        )


# ============================================================
# DELETE
# ============================================================


def test_delete_depense(
    service,
    depense,
):

    result = service.delete_depense(
        depense.id
    )

    assert result is True

    assert (
        service.get_depense(
            depense.id
        )
        is None
    )


def test_delete_depense_not_found(
    service,
):

    with pytest.raises(ValueError):

        service.delete_depense(
            999999
        )


def test_delete_depense_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.delete_depense(
            "1"
        )


def test_delete_depense_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.delete_depense(
            0
        )


def test_delete_depense_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.delete_depense(
            -1
        )


# ============================================================
# EXISTS
# ============================================================


def test_depense_exists(
    service,
    depense,
):

    assert service.depense_exists(
        depense.id
    ) is True


def test_depense_does_not_exist(
    service,
):

    assert service.depense_exists(
        999999
    ) is False


def test_depense_exists_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.depense_exists(
            "1"
        )


# ============================================================
# PARCELLE EXISTS
# ============================================================


def test_parcelle_exists(
    service,
    parcelle,
):

    assert service.parcelle_exists(
        parcelle.id
    ) is True


def test_parcelle_does_not_exist(
    service,
):

    assert service.parcelle_exists(
        999999
    ) is False


def test_parcelle_exists_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.parcelle_exists(
            "1"
        )


def test_parcelle_exists_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.parcelle_exists(
            0
        )


def test_parcelle_exists_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.parcelle_exists(
            -1
        )


# ============================================================
# CULTURE EXISTS
# ============================================================


def test_culture_exists(
    service,
    culture,
):

    assert service.culture_exists(
        culture.id
    ) is True


def test_culture_does_not_exist(
    service,
):

    assert service.culture_exists(
        999999
    ) is False


def test_culture_exists_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.culture_exists(
            "1"
        )


def test_culture_exists_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.culture_exists(
            0
        )


def test_culture_exists_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.culture_exists(
            -1
        )


# ============================================================
# VALIDATION
# ============================================================


def test_validate_depense(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    assert service.validate_depense(
        depense
    ) is True


def test_validate_depense_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.validate_depense(
            "depense invalide"
        )


def test_validate_depense_negative_amount(
    service,
):

    # Le modèle Depense peut déjà refuser un montant
    # négatif lors de sa construction.
    # On crée donc un objet valide puis on modifie
    # le montant pour tester le service.

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.montant = -100.0

    with pytest.raises(
        ValueError,
        match="ne peut pas être négatif",
    ):

        service.validate_depense(
            depense
        )


def test_validate_depense_invalid_category_type(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.categorie = 123

    with pytest.raises(TypeError):

        service.validate_depense(
            depense
        )


def test_validate_depense_empty_category(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.categorie = "   "

    with pytest.raises(ValueError):

        service.validate_depense(
            depense
        )


def test_validate_depense_invalid_amount_type(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.montant = "25000"

    with pytest.raises(TypeError):

        service.validate_depense(
            depense
        )


def test_validate_depense_invalid_date_type(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.date_depense = 20260501

    with pytest.raises(TypeError):

        service.validate_depense(
            depense
        )


def test_validate_depense_empty_date(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.date_depense = "   "

    with pytest.raises(ValueError):

        service.validate_depense(
            depense
        )


def test_validate_depense_invalid_parcelle_type(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.parcelle_id = "1"

    with pytest.raises(TypeError):

        service.validate_depense(
            depense
        )


def test_validate_depense_invalid_culture_type(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.culture_id = "1"

    with pytest.raises(TypeError):

        service.validate_depense(
            depense
        )


def test_validate_depense_invalid_description_type(
    service,
):

    depense = Depense(
        categorie="Engrais",
        montant=25000.0,
        date_depense="2026-05-01",
    )

    depense.description = 123

    with pytest.raises(TypeError):

        service.validate_depense(
            depense
        )


# ============================================================
# SEARCH
# ============================================================


def test_search_depenses(
    service,
):

    service.create_depense(
        Depense(
            categorie="Engrais",
            montant=50000.0,
            date_depense="2026-05-01",
        )
    )

    service.create_depense(
        Depense(
            categorie="Semences",
            montant=25000.0,
            date_depense="2026-06-01",
        )
    )

    result = service.search_depenses(
        "engrais"
    )

    assert len(result) >= 1

    assert any(
        item.categorie == "Engrais"
        for item in result
    )


def test_search_depenses_case_insensitive(
    service,
):

    service.create_depense(
        Depense(
            categorie="Pesticide",
            montant=35000.0,
            date_depense="2026-06-10",
        )
    )

    result = service.search_depenses(
        "PESTICIDE"
    )

    assert any(
        item.categorie == "Pesticide"
        for item in result
    )


def test_search_depenses_empty_search(
    service,
    depense,
):

    result = service.search_depenses(
        ""
    )

    assert any(
        item.id == depense.id
        for item in result
    )


def test_search_depenses_whitespace_search(
    service,
    depense,
):

    result = service.search_depenses(
        "   "
    )

    assert any(
        item.id == depense.id
        for item in result
    )


def test_search_depenses_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.search_depenses(
            123
        )

