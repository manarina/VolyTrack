"""
Tests du service Travail
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

from core.models.travail import Travail
from core.models.parcelle import Parcelle
from core.models.culture import Culture

from core.repositories.travail_repository import TravailRepository
from core.repositories.parcelle_repository import ParcelleRepository
from core.repositories.culture_repository import CultureRepository

from core.services.travail_service import TravailService


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def travail_repository():
    create_tables()
    return TravailRepository()


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
    travail_repository,
    parcelle_repository,
    culture_repository,
):
    return TravailService(
        repository=travail_repository,
        parcelle_repository=parcelle_repository,
        culture_repository=culture_repository,
    )


@pytest.fixture
def parcelle(
    parcelle_repository,
):
    return parcelle_repository.create(
        Parcelle(
            nom="Parcelle Travail Test",
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
def travail(
    service,
    parcelle,
    culture,
):
    return service.create_travail(
        Travail(
            parcelle_id=parcelle.id,
            culture_id=culture.id,
            type_travail="Semis",
            date_travail="2026-06-01",
            cout=15000.0,
            description="Semis du riz",
        )
    )


# ============================================================
# INITIALISATION
# ============================================================


def test_service_initialization():

    service = TravailService()

    assert isinstance(
        service.repository,
        TravailRepository,
    )

    assert isinstance(
        service.parcelle_repository,
        ParcelleRepository,
    )

    assert isinstance(
        service.culture_repository,
        CultureRepository,
    )


def test_service_invalid_travail_repository(
    parcelle_repository,
    culture_repository,
):

    with pytest.raises(TypeError):

        TravailService(
            repository="repository invalide",
            parcelle_repository=parcelle_repository,
            culture_repository=culture_repository,
        )


def test_service_invalid_parcelle_repository(
    travail_repository,
    culture_repository,
):

    with pytest.raises(TypeError):

        TravailService(
            repository=travail_repository,
            parcelle_repository="repository invalide",
            culture_repository=culture_repository,
        )


def test_service_invalid_culture_repository(
    travail_repository,
    parcelle_repository,
):

    with pytest.raises(TypeError):

        TravailService(
            repository=travail_repository,
            parcelle_repository=parcelle_repository,
            culture_repository="repository invalide",
        )


# ============================================================
# CREATE
# ============================================================


def test_create_travail(
    service,
    parcelle,
):

    travail = Travail(
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-05-10",
        cout=25000.0,
        description="Labour de la parcelle",
    )

    result = service.create_travail(
        travail
    )

    assert result is travail
    assert result.id is not None
    assert result.id > 0
    assert result.parcelle_id == parcelle.id
    assert result.type_travail == "Labour"


def test_create_travail_with_culture(
    service,
    parcelle,
    culture,
):

    travail = Travail(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        type_travail="Semis",
        date_travail="2026-06-01",
        cout=10000.0,
    )

    result = service.create_travail(
        travail
    )

    assert result.id is not None
    assert result.culture_id == culture.id


def test_create_travail_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.create_travail(
            "travail invalide"
        )


def test_create_travail_invalid_parcelle(
    service,
):

    travail = Travail(
        parcelle_id=999999,
        type_travail="Labour",
        date_travail="2026-05-01",
        cout=10000.0,
    )

    with pytest.raises(ValueError):

        service.create_travail(
            travail
        )


def test_create_travail_invalid_culture(
    service,
    parcelle,
):

    travail = Travail(
        parcelle_id=parcelle.id,
        culture_id=999999,
        type_travail="Semis",
        date_travail="2026-06-01",
        cout=10000.0,
    )

    with pytest.raises(ValueError):

        service.create_travail(
            travail
        )


def test_create_travail_culture_wrong_parcelle(
    service,
    parcelle,
    culture_repository,
):

    other_parcelle = parcelle_repository_create(
        culture_repository
    )

    other_culture = culture_repository.create(
        Culture(
            parcelle_id=other_parcelle.id,
            nom="Maïs",
            variete="Local",
        )
    )

    travail = Travail(
        parcelle_id=parcelle.id,
        culture_id=other_culture.id,
        type_travail="Semis",
        date_travail="2026-06-01",
        cout=10000.0,
    )

    with pytest.raises(ValueError):

        service.create_travail(
            travail
        )


# ============================================================
# GET BY ID
# ============================================================


def test_get_travail(
    service,
    travail,
):

    result = service.get_travail(
        travail.id
    )

    assert result is not None
    assert result.id == travail.id
    assert result.type_travail == travail.type_travail


def test_get_travail_not_found(
    service,
):

    result = service.get_travail(
        999999
    )

    assert result is None


def test_get_travail_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.get_travail(
            "1"
        )


def test_get_travail_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.get_travail(
            0
        )


def test_get_travail_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.get_travail(
            -1
        )


# ============================================================
# GET ALL
# ============================================================


def test_get_all_travaux(
    service,
    travail,
):

    result = service.get_all_travaux()

    assert isinstance(
        result,
        list,
    )

    assert any(
        item.id == travail.id
        for item in result
    )


def test_get_all_travaux_returns_instances(
    service,
    travail,
):

    result = service.get_all_travaux()

    assert all(
        isinstance(
            item,
            Travail,
        )
        for item in result
    )


# ============================================================
# GET BY PARCELLE
# ============================================================


def test_get_travaux_by_parcelle(
    service,
    travail,
    parcelle,
):

    result = service.get_travaux_by_parcelle(
        parcelle.id
    )

    assert any(
        item.id == travail.id
        for item in result
    )


def test_get_travaux_by_parcelle_empty(
    service,
):

    result = service.get_travaux_by_parcelle(
        999999
    )

    assert result == []


def test_get_travaux_by_parcelle_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.get_travaux_by_parcelle(
            "1"
        )


def test_get_travaux_by_parcelle_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.get_travaux_by_parcelle(
            0
        )


def test_get_travaux_by_parcelle_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.get_travaux_by_parcelle(
            -1
        )


# ============================================================
# GET BY CULTURE
# ============================================================


def test_get_travaux_by_culture(
    service,
    travail,
    culture,
):

    result = service.get_travaux_by_culture(
        culture.id
    )

    assert any(
        item.id == travail.id
        for item in result
    )


def test_get_travaux_by_culture_empty(
    service,
):

    result = service.get_travaux_by_culture(
        999999
    )

    assert result == []


def test_get_travaux_by_culture_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.get_travaux_by_culture(
            "1"
        )


def test_get_travaux_by_culture_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.get_travaux_by_culture(
            0
        )


def test_get_travaux_by_culture_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.get_travaux_by_culture(
            -1
        )


# ============================================================
# UPDATE
# ============================================================


def test_update_travail(
    service,
    travail,
):

    travail.type_travail = "Désherbage"
    travail.cout = 20000.0
    travail.description = "Désherbage manuel"

    result = service.update_travail(
        travail
    )

    assert result is travail

    updated = service.get_travail(
        travail.id
    )

    assert updated is not None
    assert updated.type_travail == "Désherbage"
    assert updated.cout == 20000.0
    assert updated.description == "Désherbage manuel"


def test_update_travail_without_id(
    service,
    parcelle,
):

    travail = Travail(
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-05-01",
        cout=10000.0,
    )

    with pytest.raises(ValueError):

        service.update_travail(
            travail
        )


def test_update_travail_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.update_travail(
            "travail invalide"
        )


def test_update_travail_invalid_id(
    service,
    parcelle,
):

    travail = Travail(
        id=-1,
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-05-01",
        cout=10000.0,
    )

    with pytest.raises(ValueError):

        service.update_travail(
            travail
        )


def test_update_travail_not_found(
    service,
    parcelle,
):

    travail = Travail(
        id=999999,
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-05-01",
        cout=10000.0,
    )

    with pytest.raises(ValueError):

        service.update_travail(
            travail
        )


def test_update_travail_invalid_parcelle(
    service,
    travail,
):

    travail.parcelle_id = 999999

    with pytest.raises(ValueError):

        service.update_travail(
            travail
        )


def test_update_travail_invalid_culture(
    service,
    travail,
):

    travail.culture_id = 999999

    with pytest.raises(ValueError):

        service.update_travail(
            travail
        )


# ============================================================
# DELETE
# ============================================================


def test_delete_travail(
    service,
    travail,
):

    result = service.delete_travail(
        travail.id
    )

    assert result is True

    assert (
        service.get_travail(
            travail.id
        )
        is None
    )


def test_delete_travail_not_found(
    service,
):

    with pytest.raises(ValueError):

        service.delete_travail(
            999999
        )


def test_delete_travail_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.delete_travail(
            "1"
        )


def test_delete_travail_invalid_zero(
    service,
):

    with pytest.raises(ValueError):

        service.delete_travail(
            0
        )


def test_delete_travail_invalid_negative(
    service,
):

    with pytest.raises(ValueError):

        service.delete_travail(
            -1
        )


# ============================================================
# EXISTS
# ============================================================


def test_travail_exists(
    service,
    travail,
):

    assert service.travail_exists(
        travail.id
    ) is True


def test_travail_does_not_exist(
    service,
):

    assert service.travail_exists(
        999999
    ) is False


def test_travail_exists_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.travail_exists(
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


# ============================================================
# VALIDATION
# ============================================================


def test_validate_travail(
    service,
    parcelle,
):

    travail = Travail(
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-05-01",
        cout=10000.0,
    )

    assert service.validate_travail(
        travail
    ) is True


def test_validate_travail_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.validate_travail(
            "travail invalide"
        )


def test_validate_travail_negative_cost(
    service,
    parcelle,
):

    # Le modèle Travail interdit déjà un coût négatif
    # lors de sa construction.
    # On crée donc d'abord un objet valide, puis on
    # modifie sa valeur afin de tester la validation
    # spécifique du service.

    travail = Travail(
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-05-01",
        cout=10000.0,
    )

    travail.cout = -100.0

    with pytest.raises(
        ValueError,
        match="Le coût du travail ne peut pas être négatif.",
    ):
        service.validate_travail(
            travail
        )



# ============================================================
# SEARCH
# ============================================================


def test_search_travaux(
    service,
    parcelle,
):

    service.create_travail(
        Travail(
            parcelle_id=parcelle.id,
            type_travail="Labour",
            date_travail="2026-05-01",
            cout=10000.0,
        )
    )

    service.create_travail(
        Travail(
            parcelle_id=parcelle.id,
            type_travail="Semis",
            date_travail="2026-06-01",
            cout=15000.0,
        )
    )

    result = service.search_travaux(
        "labour"
    )

    assert len(result) >= 1

    assert any(
        item.type_travail == "Labour"
        for item in result
    )


def test_search_travaux_case_insensitive(
    service,
    parcelle,
):

    service.create_travail(
        Travail(
            parcelle_id=parcelle.id,
            type_travail="Désherbage",
            date_travail="2026-06-10",
            cout=12000.0,
        )
    )

    result = service.search_travaux(
        "DÉSHERBAGE"
    )

    assert any(
        item.type_travail == "Désherbage"
        for item in result
    )


def test_search_travaux_empty_search(
    service,
    travail,
):

    result = service.search_travaux(
        ""
    )

    assert any(
        item.id == travail.id
        for item in result
    )


def test_search_travaux_invalid_type(
    service,
):

    with pytest.raises(TypeError):

        service.search_travaux(
            123
        )


# ============================================================
# HELPER POUR CRÉER UNE AUTRE PARCELLE
# ============================================================


def parcelle_repository_create(
    culture_repository,
):
    """
    Crée une autre parcelle directement via SQLite.

    Le repository Culture n'expose pas le repository Parcelle,
    on utilise donc ici une connexion indépendante.
    """

    from core.repositories.parcelle_repository import (
        ParcelleRepository,
    )

    repository = ParcelleRepository()

    return repository.create(
        Parcelle(
            nom="Autre Parcelle",
            superficie=4.0,
            unite_superficie="ha",
            localisation="Autre Zone",
        )
    )

