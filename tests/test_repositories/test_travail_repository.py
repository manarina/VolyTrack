import pytest

from core.database.schema import create_tables
from core.models.culture import Culture
from core.models.parcelle import Parcelle
from core.models.travail import Travail
from core.repositories.culture_repository import CultureRepository
from core.repositories.parcelle_repository import ParcelleRepository
from core.repositories.travail_repository import TravailRepository


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture
def repository():
    create_tables()

    return TravailRepository()


@pytest.fixture
def parcelle():
    create_tables()

    repository = ParcelleRepository()

    return repository.create(
        Parcelle(
            nom="Parcelle Travail Test",
            superficie=1.5,
        )
    )


@pytest.fixture
def culture(parcelle):
    repository = CultureRepository()

    return repository.create(
        Culture(
            parcelle_id=parcelle.id,
            nom="Riz",
            variete="Makalioka",
            statut="En cours",
        )
    )


# ============================================================
# CREATE
# ============================================================

def test_create_travail(
    repository,
    parcelle,
    culture,
):
    travail = Travail(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        type_travail="Labour",
        date_travail="2026-10-01",
        cout=50000,
        description="Labour de la parcelle",
    )

    result = repository.create(travail)

    assert result.id is not None
    assert result.id > 0
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id
    assert result.type_travail == "Labour"
    assert result.cout == 50000


# ============================================================
# CREATE SANS CULTURE
# ============================================================

def test_create_travail_without_culture(
    repository,
    parcelle,
):
    travail = Travail(
        parcelle_id=parcelle.id,
        type_travail="Préparation du sol",
        date_travail="2026-10-02",
        cout=30000,
    )

    result = repository.create(travail)

    assert result.id is not None
    assert result.culture_id is None


# ============================================================
# GET BY ID
# ============================================================

def test_get_travail_by_id(
    repository,
    parcelle,
    culture,
):
    travail = Travail(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        type_travail="Semis",
        date_travail="2026-10-03",
        cout=25000,
    )

    created = repository.create(travail)

    result = repository.get_by_id(
        created.id
    )

    assert result is not None
    assert result.id == created.id
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id
    assert result.type_travail == "Semis"
    assert result.date_travail == "2026-10-03"
    assert result.cout == 25000


# ============================================================
# GET BY ID — NOT FOUND
# ============================================================

def test_get_travail_by_id_not_found(repository):
    result = repository.get_by_id(999999)

    assert result is None


# ============================================================
# GET ALL
# ============================================================

def test_get_all_travaux(
    repository,
    parcelle,
):
    first = Travail(
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-10-01",
        cout=30000,
    )

    second = Travail(
        parcelle_id=parcelle.id,
        type_travail="Semis",
        date_travail="2026-10-02",
        cout=20000,
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_all()

    names = [
        travail.type_travail
        for travail in result
    ]

    assert "Labour" in names
    assert "Semis" in names


# ============================================================
# GET BY PARCELLE
# ============================================================

def test_get_travaux_by_parcelle(
    repository,
    parcelle,
):
    first = Travail(
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-10-01",
        cout=30000,
    )

    second = Travail(
        parcelle_id=parcelle.id,
        type_travail="Semis",
        date_travail="2026-10-02",
        cout=20000,
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_by_parcelle_id(
        parcelle.id
    )

    names = [
        travail.type_travail
        for travail in result
    ]

    assert len(result) >= 2
    assert "Labour" in names
    assert "Semis" in names


# ============================================================
# GET BY PARCELLE — EMPTY
# ============================================================

def test_get_travaux_by_parcelle_empty(
    repository,
):
    parcelle_repository = ParcelleRepository()

    parcelle = parcelle_repository.create(
        Parcelle(
            nom="Parcelle Sans Travail",
            superficie=1.0,
        )
    )

    result = repository.get_by_parcelle_id(
        parcelle.id
    )

    assert result == []


# ============================================================
# GET BY CULTURE
# ============================================================

def test_get_travaux_by_culture(
    repository,
    parcelle,
    culture,
):
    first = Travail(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        type_travail="Semis",
        date_travail="2026-10-01",
        cout=20000,
    )

    second = Travail(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        type_travail="Fertilisation",
        date_travail="2026-10-15",
        cout=15000,
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_by_culture_id(
        culture.id
    )

    names = [
        travail.type_travail
        for travail in result
    ]

    assert len(result) >= 2
    assert "Semis" in names
    assert "Fertilisation" in names


# ============================================================
# GET BY CULTURE — EMPTY
# ============================================================

def test_get_travaux_by_culture_empty(
    repository,
    parcelle,
    culture,
):
    result = repository.get_by_culture_id(
        culture.id
    )

    assert result == []


# ============================================================
# UPDATE
# ============================================================

def test_update_travail(
    repository,
    parcelle,
    culture,
):
    travail = Travail(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        type_travail="Labour",
        date_travail="2026-10-01",
        cout=30000,
        description="Ancienne description",
    )

    created = repository.create(travail)

    created.type_travail = "Labour profond"
    created.cout = 45000
    created.description = "Nouvelle description"

    result = repository.update(created)

    assert result.id == created.id
    assert result.type_travail == "Labour profond"
    assert result.cout == 45000
    assert result.description == "Nouvelle description"

    saved = repository.get_by_id(
        created.id
    )

    assert saved is not None
    assert saved.type_travail == "Labour profond"
    assert saved.cout == 45000
    assert saved.description == "Nouvelle description"


# ============================================================
# UPDATE — WITHOUT ID
# ============================================================

def test_update_travail_without_id(
    repository,
    parcelle,
):
    travail = Travail(
        parcelle_id=parcelle.id,
        type_travail="Labour",
        date_travail="2026-10-01",
        cout=30000,
    )

    with pytest.raises(
        ValueError,
        match="doit posséder un identifiant",
    ):
        repository.update(travail)


# ============================================================
# UPDATE — NOT FOUND
# ============================================================

def test_update_travail_not_found(
    repository,
    parcelle,
):
    travail = Travail(
        id=999999,
        parcelle_id=parcelle.id,
        type_travail="Travail inexistant",
        date_travail="2026-10-01",
        cout=10000,
    )

    with pytest.raises(
        ValueError,
        match="Aucun travail trouvé",
    ):
        repository.update(travail)


# ============================================================
# DELETE
# ============================================================

def test_delete_travail(
    repository,
    parcelle,
):
    travail = Travail(
        parcelle_id=parcelle.id,
        type_travail="Travail à supprimer",
        date_travail="2026-10-01",
        cout=10000,
    )

    created = repository.create(travail)

    result = repository.delete(
        created.id
    )

    assert result is True

    deleted = repository.get_by_id(
        created.id
    )

    assert deleted is None


# ============================================================
# DELETE — NOT FOUND
# ============================================================

def test_delete_travail_not_found(repository):
    with pytest.raises(
        ValueError,
        match="Aucun travail trouvé",
    ):
        repository.delete(999999)


# ============================================================
# GET BY ID — INVALID TYPE
# ============================================================

def test_get_travail_invalid_id_type(repository):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.get_by_id("1")


# ============================================================
# GET BY ID — INVALID VALUE
# ============================================================

def test_get_travail_invalid_id(repository):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_id(0)


# ============================================================
# GET BY PARCELLE — INVALID TYPE
# ============================================================

def test_get_travaux_by_parcelle_invalid_id(
    repository,
):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.get_by_parcelle_id("1")


# ============================================================
# GET BY PARCELLE — INVALID VALUE
# ============================================================

def test_get_travaux_by_parcelle_invalid_id_value(
    repository,
):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_parcelle_id(0)


# ============================================================
# GET BY CULTURE — INVALID TYPE
# ============================================================

def test_get_travaux_by_culture_invalid_id(
    repository,
):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.get_by_culture_id("1")


# ============================================================
# GET BY CULTURE — INVALID VALUE
# ============================================================

def test_get_travaux_by_culture_invalid_id_value(
    repository,
):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_culture_id(0)


# ============================================================
# DELETE — INVALID TYPE
# ============================================================

def test_delete_travail_invalid_id_type(repository):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.delete("1")


# ============================================================
# DELETE — INVALID VALUE
# ============================================================

def test_delete_travail_invalid_id(repository):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.delete(-1)


# ============================================================
# CREATE — INVALID TYPE
# ============================================================

def test_create_invalid_travail_type(repository):
    with pytest.raises(
        TypeError,
        match="instance de Travail",
    ):
        repository.create("Travail")


# ============================================================
# UPDATE — INVALID TYPE
# ============================================================

def test_update_invalid_travail_type(repository):
    with pytest.raises(
        TypeError,
        match="instance de Travail",
    ):
        repository.update("Travail")

