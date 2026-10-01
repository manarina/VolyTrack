import pytest

from core.database.schema import create_tables
from core.models.parcelle import Parcelle
from core.repositories.parcelle_repository import ParcelleRepository


# ============================================================
# INITIALISATION
# ============================================================

@pytest.fixture
def repository():
    """
    Initialise les tables et retourne le repository.
    """

    create_tables()

    return ParcelleRepository()


# ============================================================
# CREATE
# ============================================================

def test_create_parcelle(repository):
    """
    Vérifie qu'une parcelle peut être enregistrée.
    """

    parcelle = Parcelle(
        nom="Parcelle Test",
        superficie=2.5,
        unite_superficie="ha",
        localisation="Nord",
        description="Parcelle de test",
    )

    result = repository.create(parcelle)

    assert result.id is not None
    assert result.id > 0
    assert result.nom == "Parcelle Test"
    assert result.superficie == 2.5


# ============================================================
# GET BY ID
# ============================================================

def test_get_parcelle_by_id(repository):
    """
    Vérifie la récupération d'une parcelle par son ID.
    """

    parcelle = Parcelle(
        nom="Parcelle Nord",
        superficie=1.5,
    )

    created = repository.create(parcelle)

    result = repository.get_by_id(
        created.id
    )

    assert result is not None
    assert result.id == created.id
    assert result.nom == "Parcelle Nord"
    assert result.superficie == 1.5


# ============================================================
# GET BY ID — INEXISTANT
# ============================================================

def test_get_parcelle_by_id_not_found(repository):
    """
    Vérifie qu'une parcelle inexistante retourne None.
    """

    result = repository.get_by_id(999999)

    assert result is None


# ============================================================
# GET ALL
# ============================================================

def test_get_all_parcelles(repository):
    """
    Vérifie la récupération de toutes les parcelles.
    """

    first = Parcelle(
        nom="Parcelle A",
        superficie=1.0,
    )

    second = Parcelle(
        nom="Parcelle B",
        superficie=2.0,
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_all()

    names = [
        parcelle.nom
        for parcelle in result
    ]

    assert "Parcelle A" in names
    assert "Parcelle B" in names


# ============================================================
# UPDATE
# ============================================================

def test_update_parcelle(repository):
    """
    Vérifie qu'une parcelle peut être modifiée.
    """

    parcelle = Parcelle(
        nom="Ancien nom",
        superficie=1.0,
        localisation="Nord",
    )

    created = repository.create(parcelle)

    created.nom = "Nouveau nom"
    created.superficie = 2.0
    created.localisation = "Sud"

    result = repository.update(created)

    assert result.id == created.id
    assert result.nom == "Nouveau nom"
    assert result.superficie == 2.0
    assert result.localisation == "Sud"

    saved = repository.get_by_id(
        created.id
    )

    assert saved is not None
    assert saved.nom == "Nouveau nom"
    assert saved.superficie == 2.0
    assert saved.localisation == "Sud"


# ============================================================
# UPDATE — SANS ID
# ============================================================

def test_update_parcelle_without_id(repository):
    """
    Vérifie qu'une parcelle sans ID ne peut pas être modifiée.
    """

    parcelle = Parcelle(
        nom="Parcelle Test",
        superficie=1.0,
    )

    with pytest.raises(
        ValueError,
        match="doit posséder un identifiant",
    ):
        repository.update(parcelle)


# ============================================================
# UPDATE — INEXISTANTE
# ============================================================

def test_update_parcelle_not_found(repository):
    """
    Vérifie qu'une parcelle inexistante ne peut pas être modifiée.
    """

    parcelle = Parcelle(
        id=999999,
        nom="Parcelle Inexistante",
        superficie=1.0,
    )

    with pytest.raises(
        ValueError,
        match="Aucune parcelle trouvée",
    ):
        repository.update(parcelle)


# ============================================================
# DELETE
# ============================================================

def test_delete_parcelle(repository):
    """
    Vérifie qu'une parcelle peut être supprimée.
    """

    parcelle = Parcelle(
        nom="Parcelle à supprimer",
        superficie=1.0,
    )

    created = repository.create(parcelle)

    result = repository.delete(
        created.id
    )

    assert result is True

    deleted = repository.get_by_id(
        created.id
    )

    assert deleted is None


# ============================================================
# DELETE — INEXISTANTE
# ============================================================

def test_delete_parcelle_not_found(repository):
    """
    Vérifie la suppression d'une parcelle inexistante.
    """

    with pytest.raises(
        ValueError,
        match="Aucune parcelle trouvée",
    ):
        repository.delete(999999)


# ============================================================
# GET BY ID — TYPE INVALIDE
# ============================================================

def test_get_parcelle_invalid_id_type(repository):
    """
    Vérifie la validation du type de l'ID.
    """

    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.get_by_id("1")


# ============================================================
# GET BY ID — ID INVALIDE
# ============================================================

def test_get_parcelle_invalid_id(repository):
    """
    Vérifie qu'un ID nul ou négatif est refusé.
    """

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_id(0)


# ============================================================
# DELETE — TYPE INVALIDE
# ============================================================

def test_delete_parcelle_invalid_id_type(repository):
    """
    Vérifie la validation du type lors de la suppression.
    """

    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.delete("1")


# ============================================================
# DELETE — ID INVALIDE
# ============================================================

def test_delete_parcelle_invalid_id(repository):
    """
    Vérifie qu'un ID négatif est refusé lors de la suppression.
    """

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.delete(-1)


# ============================================================
# CREATE — TYPE INVALIDE
# ============================================================

def test_create_invalid_parcelle_type(repository):
    """
    Vérifie que create() exige une instance de Parcelle.
    """

    with pytest.raises(
        TypeError,
        match="instance de Parcelle",
    ):
        repository.create("Parcelle")


# ============================================================
# UPDATE — TYPE INVALIDE
# ============================================================

def test_update_invalid_parcelle_type(repository):
    """
    Vérifie que update() exige une instance de Parcelle.
    """

    with pytest.raises(
        TypeError,
        match="instance de Parcelle",
    ):
        repository.update("Parcelle")