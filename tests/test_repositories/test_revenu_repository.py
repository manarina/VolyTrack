import pytest

from core.database.schema import create_tables
from core.models.culture import Culture
from core.models.parcelle import Parcelle
from core.models.revenu import Revenu
from core.repositories.culture_repository import CultureRepository
from core.repositories.parcelle_repository import ParcelleRepository
from core.repositories.revenu_repository import RevenuRepository


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture
def repository():
    create_tables()

    return RevenuRepository()


@pytest.fixture
def parcelle():
    create_tables()

    repository = ParcelleRepository()

    return repository.create(
        Parcelle(
            nom="Parcelle Revenu Test",
            superficie=2.0,
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

def test_create_revenu(
    repository,
    parcelle,
    culture,
):
    revenu = Revenu(
        produit="Riz",
        quantite=100,
        prix_unitaire=2500,
        montant=250000,
        date_revenu="2026-10-01",
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        description="Vente de riz",
    )

    result = repository.create(revenu)

    assert result.id is not None
    assert result.id > 0
    assert result.produit == "Riz"
    assert result.quantite == 100
    assert result.prix_unitaire == 2500
    assert result.montant == 250000
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id


# ============================================================
# CREATE SANS RELATIONS
# ============================================================

def test_create_revenu_without_relations(repository):
    revenu = Revenu(
        produit="Tomates",
        quantite=50,
        prix_unitaire=1500,
        montant=75000,
        date_revenu="2026-10-02",
        description="Vente générale",
    )

    result = repository.create(revenu)

    assert result.id is not None
    assert result.parcelle_id is None
    assert result.culture_id is None


# ============================================================
# GET BY ID
# ============================================================

def test_get_revenu_by_id(
    repository,
    parcelle,
    culture,
):
    revenu = Revenu(
        produit="Maïs",
        quantite=80,
        prix_unitaire=2000,
        montant=160000,
        date_revenu="2026-10-03",
        parcelle_id=parcelle.id,
        culture_id=culture.id,
    )

    created = repository.create(revenu)

    result = repository.get_by_id(
        created.id
    )

    assert result is not None
    assert result.id == created.id
    assert result.produit == "Maïs"
    assert result.quantite == 80
    assert result.prix_unitaire == 2000
    assert result.montant == 160000
    assert result.date_revenu == "2026-10-03"
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id


# ============================================================
# GET BY ID — NOT FOUND
# ============================================================

def test_get_revenu_by_id_not_found(repository):
    result = repository.get_by_id(999999)

    assert result is None


# ============================================================
# GET ALL
# ============================================================

def test_get_all_revenus(
    repository,
    parcelle,
):
    first = Revenu(
        produit="Riz",
        quantite=100,
        prix_unitaire=2500,
        montant=250000,
        date_revenu="2026-10-01",
        parcelle_id=parcelle.id,
    )

    second = Revenu(
        produit="Maïs",
        quantite=80,
        prix_unitaire=2000,
        montant=160000,
        date_revenu="2026-10-02",
        parcelle_id=parcelle.id,
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_all()

    produits = [
        revenu.produit
        for revenu in result
    ]

    assert "Riz" in produits
    assert "Maïs" in produits


# ============================================================
# GET BY PARCELLE
# ============================================================

def test_get_revenus_by_parcelle(
    repository,
    parcelle,
):
    first = Revenu(
        produit="Riz",
        quantite=100,
        prix_unitaire=2500,
        montant=250000,
        date_revenu="2026-10-01",
        parcelle_id=parcelle.id,
    )

    second = Revenu(
        produit="Maïs",
        quantite=80,
        prix_unitaire=2000,
        montant=160000,
        date_revenu="2026-10-02",
        parcelle_id=parcelle.id,
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_by_parcelle_id(
        parcelle.id
    )

    produits = [
        revenu.produit
        for revenu in result
    ]

    assert len(result) >= 2
    assert "Riz" in produits
    assert "Maïs" in produits


# ============================================================
# GET BY PARCELLE — EMPTY
# ============================================================

def test_get_revenus_by_parcelle_empty(
    repository,
):
    parcelle_repository = ParcelleRepository()

    parcelle = parcelle_repository.create(
        Parcelle(
            nom="Parcelle Sans Revenu",
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

def test_get_revenus_by_culture(
    repository,
    parcelle,
    culture,
):
    first = Revenu(
        produit="Riz",
        quantite=100,
        prix_unitaire=2500,
        montant=250000,
        date_revenu="2026-10-01",
        parcelle_id=parcelle.id,
        culture_id=culture.id,
    )

    second = Revenu(
        produit="Riz",
        quantite=50,
        prix_unitaire=2700,
        montant=135000,
        date_revenu="2026-10-15",
        parcelle_id=parcelle.id,
        culture_id=culture.id,
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_by_culture_id(
        culture.id
    )

    assert len(result) >= 2

    produits = [
        revenu.produit
        for revenu in result
    ]

    assert "Riz" in produits


# ============================================================
# GET BY CULTURE — EMPTY
# ============================================================

def test_get_revenus_by_culture_empty(
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

def test_update_revenu(
    repository,
    parcelle,
    culture,
):
    revenu = Revenu(
        produit="Riz",
        quantite=100,
        prix_unitaire=2500,
        montant=250000,
        date_revenu="2026-10-01",
        parcelle_id=parcelle.id,
        culture_id=culture.id,
        description="Ancienne description",
    )

    created = repository.create(revenu)

    created.produit = "Riz premium"
    created.quantite = 120
    created.prix_unitaire = 3000
    created.montant = 360000
    created.description = "Nouvelle description"

    result = repository.update(created)

    assert result.id == created.id
    assert result.produit == "Riz premium"
    assert result.quantite == 120
    assert result.prix_unitaire == 3000
    assert result.montant == 360000
    assert result.description == "Nouvelle description"

    saved = repository.get_by_id(
        created.id
    )

    assert saved is not None
    assert saved.produit == "Riz premium"
    assert saved.quantite == 120
    assert saved.prix_unitaire == 3000
    assert saved.montant == 360000
    assert saved.description == "Nouvelle description"


# ============================================================
# UPDATE — WITHOUT ID
# ============================================================

def test_update_revenu_without_id(
    repository,
):
    revenu = Revenu(
        produit="Riz",
        quantite=100,
        prix_unitaire=2500,
        montant=250000,
        date_revenu="2026-10-01",
    )

    with pytest.raises(
        ValueError,
        match="doit posséder un identifiant",
    ):
        repository.update(revenu)


# ============================================================
# UPDATE — NOT FOUND
# ============================================================

def test_update_revenu_not_found(
    repository,
):
    revenu = Revenu(
        id=999999,
        produit="Revenu inexistant",
        quantite=10,
        prix_unitaire=1000,
        montant=10000,
        date_revenu="2026-10-01",
    )

    with pytest.raises(
        ValueError,
        match="Aucun revenu trouvé",
    ):
        repository.update(revenu)


# ============================================================
# DELETE
# ============================================================

def test_delete_revenu(
    repository,
):
    revenu = Revenu(
        produit="Revenu à supprimer",
        quantite=10,
        prix_unitaire=1000,
        montant=10000,
        date_revenu="2026-10-01",
    )

    created = repository.create(revenu)

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

def test_delete_revenu_not_found(repository):
    with pytest.raises(
        ValueError,
        match="Aucun revenu trouvé",
    ):
        repository.delete(999999)


# ============================================================
# GET BY ID — INVALID TYPE
# ============================================================

def test_get_revenu_invalid_id_type(repository):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.get_by_id("1")


# ============================================================
# GET BY ID — INVALID VALUE
# ============================================================

def test_get_revenu_invalid_id(repository):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_id(0)


# ============================================================
# GET BY PARCELLE — INVALID TYPE
# ============================================================

def test_get_revenus_by_parcelle_invalid_id(
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

def test_get_revenus_by_parcelle_invalid_id_value(
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

def test_get_revenus_by_culture_invalid_id(
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

def test_get_revenus_by_culture_invalid_id_value(
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

def test_delete_revenu_invalid_id_type(repository):
    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.delete("1")


# ============================================================
# DELETE — INVALID VALUE
# ============================================================

def test_delete_revenu_invalid_id(repository):
    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.delete(-1)


# ============================================================
# CREATE — INVALID TYPE
# ============================================================

def test_create_invalid_revenu_type(repository):
    with pytest.raises(
        TypeError,
        match="instance de Revenu",
    ):
        repository.create("Revenu")


# ============================================================
# UPDATE — INVALID TYPE
# ============================================================

def test_update_invalid_revenu_type(repository):
    with pytest.raises(
        TypeError,
        match="instance de Revenu",
    ):
        repository.update("Revenu")

