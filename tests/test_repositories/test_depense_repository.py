import pytest

from core.database.schema import create_tables
from core.models.culture import Culture
from core.models.depense import Depense
from core.models.parcelle import Parcelle
from core.repositories.culture_repository import CultureRepository
from core.repositories.depense_repository import DepenseRepository
from core.repositories.parcelle_repository import ParcelleRepository


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture
def repository():
    create_tables()

    return DepenseRepository()


@pytest.fixture
def parcelle():
    create_tables()

    repository = ParcelleRepository()

    return repository.create(
        Parcelle(
            nom="Parcelle Depense Test",
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

def test_create_depense(
    repository,
    parcelle,
    culture,
):
    depense = Depense(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        categorie="Semences",
        montant=50000,
        date_depense="2026-10-01",
        description="Achat de semences",
    )

    result = repository.create(depense)

    assert result.id is not None
    assert result.id > 0
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id
    assert result.categorie == "Semences"
    assert result.montant == 50000


# ============================================================
# CREATE SANS PARCELLE NI CULTURE
# ============================================================

def test_create_depense_without_relations(repository):
    depense = Depense(
        categorie="Divers",
        montant=10000,
        date_depense="2026-10-02",
        description="Dépense générale",
    )

    result = repository.create(depense)

    assert result.id is not None
    assert result.parcelle_id is None
    assert result.culture_id is None


# ============================================================
# GET BY ID
# ============================================================

def test_get_depense_by_id(
    repository,
    parcelle,
    culture,
):
    depense = Depense(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        categorie="Engrais",
        montant=75000,
        date_depense="2026-10-03",
    )

    created = repository.create(depense)

    result = repository.get_by_id(
        created.id
    )

    assert result is not None
    assert result.id == created.id
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id
    assert result.categorie == "Engrais"
    assert result.montant == 75000
    assert result.date_depense == "2026-10-03"


# ============================================================
# GET BY ID — NOT FOUND
# ============================================================

def test_get_depense_by_id_not_found(repository):
    result = repository.get_by_id(999999)

    assert result is None


# ============================================================
# GET ALL
# ============================================================

def test_get_all_depenses(
    repository,
    parcelle,
):
    first = Depense(
        parcelle_id=parcelle.id,
        categorie="Semences",
        montant=30000,
        date_depense="2026-10-01",
    )

    second = Depense(
        parcelle_id=parcelle.id,
        categorie="Engrais",
        montant=50000,
        date_depense="2026-10-02",
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_all()

    categories = [
        depense.categorie
        for depense in result
    ]

    assert "Semences" in categories
    assert "Engrais" in categories


# ============================================================
# GET BY PARCELLE
# ============================================================

def test_get_depenses_by_parcelle(
    repository,
    parcelle,
):
    first = Depense(
        parcelle_id=parcelle.id,
        categorie="Semences",
        montant=30000,
        date_depense="2026-10-01",
    )

    second = Depense(
        parcelle_id=parcelle.id,
        categorie="Engrais",
        montant=50000,
        date_depense="2026-10-02",
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_by_parcelle_id(
        parcelle.id
    )

    categories = [
        depense.categorie
        for depense in result
    ]

    assert len(result) >= 2
    assert "Semences" in categories
    assert "Engrais" in categories


# ============================================================
# GET BY PARCELLE — EMPTY
# ============================================================

def test_get_depenses_by_parcelle_empty(repository):
    parcelle_repository = ParcelleRepository()

    parcelle = parcelle_repository.create(
        Parcelle(
            nom="Parcelle Sans Depense",
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

def test_get_depenses_by_culture(
    repository,
    parcelle,
    culture,
):
    first = Depense(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        categorie="Semences",
        montant=20000,
        date_depense="2026-10-01",
    )

    second = Depense(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        categorie="Engrais",
        montant=40000,
        date_depense="2026-10-15",
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_by_culture_id(
        culture.id
    )

    categories = [
        depense.categorie
        for depense in result
    ]

    assert len(result) >= 2
    assert "Semences" in categories
    assert "Engrais" in categories


# ============================================================
# GET BY CULTURE — EMPTY
# ============================================================

def test_get_depenses_by_culture_empty(
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

def test_update_depense(
    repository,
    parcelle,
    culture,
):
    depense = Depense(
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        categorie="Semences",
        montant=30000,
        date_depense="2026-10-01",
        description="Ancienne description",
    )

    created = repository.create(depense)

    created.categorie = "Semences améliorées"
    created.montant = 45000
    created.description = "Nouvelle description"

    result = repository.update(created)

    assert result.id == created.id
    assert result.categorie == "Semences améliorées"
    assert result.montant == 45000
    assert result.description == "Nouvelle description"

    saved = repository.get_by_id(
        created.id
    )

    assert saved is not None
    assert saved.categorie == "Semences améliorées"
    assert saved.montant == 45000
    assert saved.description == "Nouvelle description"


# ============================================================
# UPDATE — WITHOUT ID
# ============================================================

def test_update_depense_without_id(
    repository,
):
    depense = Depense(
        categorie="Semences",
        montant=30000,
        date_depense="2026-10-01",
    )

    with pytest.raises(
        ValueError,
        match="doit posséder un identifiant",
    ):
        repository.update(depense)


# ============================================================
# UPDATE — NOT FOUND
# ============================================================

def test_update_depense_not_found(
    repository,
):
    depense = Depense(
        id=999999,
        categorie="Dépense inexistante",
        montant=10000,
        date_depense="2026-10-01",
    )

    with pytest.raises(
        ValueError,
        match="Aucune dépense trouvée",
    ):
        repository.update(depense)


# ============================================================
# DELETE
# ============================================================

def test_delete_depense(
    repository,
):
    depense = Depense(
        categorie="Dépense à supprimer",
        montant=10000,
        date_depense="2026-10-01",
    )

    created = repository.create(depense)

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

def test_delete_depense_not_found(repository):
    with pytest.raises(
        ValueError,
        match="Aucune dépense trouvée",
    ):
        repository.delete(999999)


# ============================================================
# GET BY ID — INVALID TYPE
# ============================================================

def test_get_depense_invalid_id_type(repository):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.get_by_id("1")


# ============================================================
# GET BY ID — INVALID VALUE
# ============================================================

def test_get_depense_invalid_id(repository):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_id(0)


# ============================================================
# GET BY PARCELLE — INVALID TYPE
# ============================================================

def test_get_depenses_by_parcelle_invalid_id(
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

def test_get_depenses_by_parcelle_invalid_id_value(
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

def test_get_depenses_by_culture_invalid_id(
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

def test_get_depenses_by_culture_invalid_id_value(
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

def test_delete_depense_invalid_id_type(repository):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.delete("1")


# ============================================================
# DELETE — INVALID VALUE
# ============================================================

def test_delete_depense_invalid_id(repository):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.delete(-1)


# ============================================================
# CREATE — INVALID TYPE
# ============================================================

def test_create_invalid_depense_type(repository):
    with pytest.raises(
        TypeError,
        match="instance de Depense",
    ):
        repository.create("Depense")


# ============================================================
# UPDATE — INVALID TYPE
# ============================================================

def test_update_invalid_depense_type(repository):
    with pytest.raises(
        TypeError,
        match="instance de Depense",
    ):
        repository.update("Depense")

