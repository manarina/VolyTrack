import pytest

from core.database.connection import get_connection
from core.database.schema import create_tables
from core.models.culture import Culture
from core.models.parcelle import Parcelle
from core.repositories.culture_repository import CultureRepository
from core.repositories.parcelle_repository import ParcelleRepository


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture
def repository():
    """
    Initialise les tables et retourne le repository Culture.
    """

    create_tables()

    return CultureRepository()


@pytest.fixture
def parcelle():
    """
    Crée une parcelle de test et retourne son ID.
    """

    create_tables()

    repository = ParcelleRepository()

    result = repository.create(
        Parcelle(
            nom="Parcelle Culture Test",
            superficie=1.5,
        )
    )

    return result


# ============================================================
# CREATE
# ============================================================

def test_create_culture(repository, parcelle):
    """
    Vérifie qu'une culture peut être créée.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Riz",
        variete="Makalioka",
        date_semis="2026-10-01",
        date_prevue_recolte="2027-01-15",
        statut="Planifiée",
        description="Culture de riz",
    )

    result = repository.create(culture)

    assert result.id is not None
    assert result.id > 0
    assert result.parcelle_id == parcelle.id
    assert result.nom == "Riz"
    assert result.variete == "Makalioka"


# ============================================================
# GET BY ID
# ============================================================

def test_get_culture_by_id(repository, parcelle):
    """
    Vérifie la récupération d'une culture par son ID.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Tomate",
        variete="Roma",
        statut="En cours",
    )

    created = repository.create(culture)

    result = repository.get_by_id(
        created.id
    )

    assert result is not None
    assert result.id == created.id
    assert result.parcelle_id == parcelle.id
    assert result.nom == "Tomate"
    assert result.variete == "Roma"
    assert result.statut == "En cours"


# ============================================================
# GET BY ID — INEXISTANT
# ============================================================

def test_get_culture_by_id_not_found(repository):
    """
    Vérifie qu'une culture inexistante retourne None.
    """

    result = repository.get_by_id(999999)

    assert result is None


# ============================================================
# GET ALL
# ============================================================

def test_get_all_cultures(repository, parcelle):
    """
    Vérifie la récupération de toutes les cultures.
    """

    first = Culture(
        parcelle_id=parcelle.id,
        nom="Riz",
    )

    second = Culture(
        parcelle_id=parcelle.id,
        nom="Tomate",
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_all()

    names = [
        culture.nom
        for culture in result
    ]

    assert "Riz" in names
    assert "Tomate" in names


# ============================================================
# GET BY PARCELLE
# ============================================================

def test_get_cultures_by_parcelle(repository, parcelle):
    """
    Vérifie la récupération des cultures d'une parcelle.
    """

    first = Culture(
        parcelle_id=parcelle.id,
        nom="Riz",
    )

    second = Culture(
        parcelle_id=parcelle.id,
        nom="Maïs",
    )

    repository.create(first)
    repository.create(second)

    result = repository.get_by_parcelle_id(
        parcelle.id
    )

    names = [
        culture.nom
        for culture in result
    ]

    assert len(result) >= 2
    assert "Riz" in names
    assert "Maïs" in names


# ============================================================
# GET BY PARCELLE — AUCUNE CULTURE
# ============================================================

def test_get_cultures_by_parcelle_empty(repository):
    """
    Vérifie qu'une parcelle sans culture retourne une liste vide.
    """

    parcelle_repository = ParcelleRepository()

    parcelle = parcelle_repository.create(
        Parcelle(
            nom="Parcelle Sans Culture",
            superficie=1.0,
        )
    )

    result = repository.get_by_parcelle_id(
        parcelle.id
    )

    assert result == []


# ============================================================
# UPDATE
# ============================================================

def test_update_culture(repository, parcelle):
    """
    Vérifie qu'une culture peut être modifiée.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Riz",
        variete="Ancienne variété",
        statut="Planifiée",
    )

    created = repository.create(culture)

    created.nom = "Riz amélioré"
    created.variete = "Nouvelle variété"
    created.statut = "En cours"

    result = repository.update(created)

    assert result.id == created.id
    assert result.nom == "Riz amélioré"
    assert result.variete == "Nouvelle variété"
    assert result.statut == "En cours"

    saved = repository.get_by_id(
        created.id
    )

    assert saved is not None
    assert saved.nom == "Riz amélioré"
    assert saved.variete == "Nouvelle variété"
    assert saved.statut == "En cours"


# ============================================================
# UPDATE — SANS ID
# ============================================================

def test_update_culture_without_id(repository, parcelle):
    """
    Vérifie qu'une culture sans ID ne peut pas être modifiée.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Riz",
    )

    with pytest.raises(
        ValueError,
        match="doit posséder un identifiant",
    ):
        repository.update(culture)


# ============================================================
# UPDATE — INEXISTANTE
# ============================================================

def test_update_culture_not_found(repository, parcelle):
    """
    Vérifie qu'une culture inexistante ne peut pas être modifiée.
    """

    culture = Culture(
        id=999999,
        parcelle_id=parcelle.id,
        nom="Culture inexistante",
    )

    with pytest.raises(
        ValueError,
        match="Aucune culture trouvée",
    ):
        repository.update(culture)


# ============================================================
# DELETE
# ============================================================

def test_delete_culture(repository, parcelle):
    """
    Vérifie qu'une culture peut être supprimée.
    """

    culture = Culture(
        parcelle_id=parcelle.id,
        nom="Culture à supprimer",
    )

    created = repository.create(culture)

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

def test_delete_culture_not_found(repository):
    """
    Vérifie la suppression d'une culture inexistante.
    """

    with pytest.raises(
        ValueError,
        match="Aucune culture trouvée",
    ):
        repository.delete(999999)


# ============================================================
# GET BY ID — TYPE INVALIDE
# ============================================================

def test_get_culture_invalid_id_type(repository):
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

def test_get_culture_invalid_id(repository):
    """
    Vérifie qu'un ID nul ou négatif est refusé.
    """

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_id(0)


# ============================================================
# GET BY PARCELLE — TYPE INVALIDE
# ============================================================

def test_get_cultures_by_parcelle_invalid_id(repository):
    """
    Vérifie la validation de l'ID de parcelle.
    """

    with pytest.raises(
        TypeError,
        match="doit être un entier",
    ):
        repository.get_by_parcelle_id("1")


# ============================================================
# GET BY PARCELLE — ID INVALIDE
# ============================================================

def test_get_cultures_by_parcelle_invalid_id_value(repository):
    """
    Vérifie qu'un ID de parcelle invalide est refusé.
    """

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.get_by_parcelle_id(0)


# ============================================================
# DELETE — TYPE INVALIDE
# ============================================================

def test_delete_culture_invalid_id_type(repository):
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

def test_delete_culture_invalid_id(repository):
    """
    Vérifie qu'un ID négatif est refusé.
    """

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        repository.delete(-1)


# ============================================================
# CREATE — TYPE INVALIDE
# ============================================================

def test_create_invalid_culture_type(repository):
    """
    Vérifie que create() exige une instance de Culture.
    """

    with pytest.raises(
        TypeError,
        match="instance de Culture",
    ):
        repository.create("Culture")


# ============================================================
# UPDATE — TYPE INVALIDE
# ============================================================

def test_update_invalid_culture_type(repository):
    """
    Vérifie que update() exige une instance de Culture.
    """

    with pytest.raises(
        TypeError,
        match="instance de Culture",
    ):
        repository.update("Culture")