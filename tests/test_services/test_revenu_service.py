
import pytest

from core.models.culture import Culture
from core.models.parcelle import Parcelle
from core.models.revenu import Revenu

from core.repositories.culture_repository import (
    CultureRepository,
)

from core.repositories.parcelle_repository import (
    ParcelleRepository,
)

from core.repositories.revenu_repository import (
    RevenuRepository,
)

from core.services.revenu_service import (
    RevenuService,
)

from core.database.connection import (
    get_connection,
)


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture(autouse=True)
def clean_revenus_table():
    """
    Nettoie la table revenus avant chaque test.

    Les repositories utilisent la base SQLite réelle du projet.
    Sans nettoyage, les données créées par un test restent
    disponibles pour les tests suivants.
    """

    connection = get_connection()

    try:
        connection.execute(
            "DELETE FROM revenus"
        )

        connection.commit()

    finally:
        connection.close()


@pytest.fixture
def repository():
    return RevenuRepository()


@pytest.fixture
def parcelle_repository():
    return ParcelleRepository()


@pytest.fixture
def culture_repository():
    return CultureRepository()


@pytest.fixture
def service(
    repository,
    parcelle_repository,
    culture_repository,
):
    return RevenuService(
        repository=repository,
        parcelle_repository=parcelle_repository,
        culture_repository=culture_repository,
    )


@pytest.fixture
def parcelle(parcelle_repository):
    return parcelle_repository.create(
        Parcelle(
            nom="Parcelle Test",
            superficie=2.0,
            unite_superficie="ha",
        )
    )


@pytest.fixture
def autre_parcelle(parcelle_repository):
    return parcelle_repository.create(
        Parcelle(
            nom="Autre Parcelle",
            superficie=3.0,
            unite_superficie="ha",
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
            nom="Tomate",
            variete="Roma",
            date_semis="2026-01-10",
        )
    )


@pytest.fixture
def autre_culture(
    culture_repository,
    autre_parcelle,
):
    return culture_repository.create(
        Culture(
            parcelle_id=autre_parcelle.id,
            nom="Maïs",
            variete="Hybride",
            date_semis="2026-01-15",
        )
    )


@pytest.fixture
def revenu():
    return Revenu(
        produit="Tomates",
        quantite=100.0,
        prix_unitaire=500.0,
        montant=50000.0,
        date_revenu="2026-05-01",
    )


# ============================================================
# INITIALISATION
# ============================================================


def test_service_initialization(
    service,
    repository,
    parcelle_repository,
    culture_repository,
):

    assert isinstance(
        service,
        RevenuService,
    )

    assert service.repository is repository

    assert (
        service.parcelle_repository
        is parcelle_repository
    )

    assert (
        service.culture_repository
        is culture_repository
    )


def test_service_invalid_revenu_repository(
    parcelle_repository,
    culture_repository,
):

    with pytest.raises(
        TypeError,
        match="repository doit être une instance",
    ):
        RevenuService(
            repository="invalid",
            parcelle_repository=parcelle_repository,
            culture_repository=culture_repository,
        )


def test_service_invalid_parcelle_repository(
    repository,
    culture_repository,
):

    with pytest.raises(
        TypeError,
        match="parcelle_repository doit être une instance",
    ):
        RevenuService(
            repository=repository,
            parcelle_repository="invalid",
            culture_repository=culture_repository,
        )


def test_service_invalid_culture_repository(
    repository,
    parcelle_repository,
):

    with pytest.raises(
        TypeError,
        match="culture_repository doit être une instance",
    ):
        RevenuService(
            repository=repository,
            parcelle_repository=parcelle_repository,
            culture_repository="invalid",
        )


# ============================================================
# CREATE
# ============================================================


def test_create_revenu(
    service,
    revenu,
):

    result = service.create_revenu(
        revenu
    )

    assert result.id is not None
    assert result.produit == "Tomates"
    assert result.quantite == 100.0
    assert result.prix_unitaire == 500.0
    assert result.montant == 50000.0


def test_create_revenu_with_parcelle(
    service,
    revenu,
    parcelle,
):

    revenu.parcelle_id = parcelle.id

    result = service.create_revenu(
        revenu
    )

    assert result.id is not None
    assert result.parcelle_id == parcelle.id


def test_create_revenu_with_culture(
    service,
    revenu,
    culture,
):

    revenu.culture_id = culture.id

    result = service.create_revenu(
        revenu
    )

    assert result.id is not None
    assert result.culture_id == culture.id


def test_create_revenu_with_parcelle_and_culture(
    service,
    revenu,
    parcelle,
    culture,
):

    revenu.parcelle_id = parcelle.id
    revenu.culture_id = culture.id

    result = service.create_revenu(
        revenu
    )

    assert result.id is not None
    assert result.parcelle_id == parcelle.id
    assert result.culture_id == culture.id


def test_create_revenu_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="revenu doit être une instance",
    ):
        service.create_revenu(
            "invalid"
        )


def test_create_revenu_invalid_parcelle(
    service,
    revenu,
):

    revenu.parcelle_id = 999999

    with pytest.raises(
        ValueError,
        match="Aucune parcelle trouvée",
    ):
        service.create_revenu(
            revenu
        )


def test_create_revenu_invalid_culture(
    service,
    revenu,
):

    revenu.culture_id = 999999

    with pytest.raises(
        ValueError,
        match="Aucune culture trouvée",
    ):
        service.create_revenu(
            revenu
        )


def test_create_revenu_culture_wrong_parcelle(
    service,
    revenu,
    parcelle,
    autre_culture,
):

    revenu.parcelle_id = parcelle.id
    revenu.culture_id = autre_culture.id

    with pytest.raises(
        ValueError,
        match="n'appartient pas à la parcelle",
    ):
        service.create_revenu(
            revenu
        )


# ============================================================
# GET
# ============================================================


def test_get_revenu(
    service,
    revenu,
):

    created = service.create_revenu(
        revenu
    )

    result = service.get_revenu(
        created.id
    )

    assert result is not None
    assert result.id == created.id
    assert result.produit == "Tomates"


def test_get_revenu_not_found(
    service,
):

    result = service.get_revenu(
        999999
    )

    assert result is None


def test_get_revenu_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="identifiant du revenu",
    ):
        service.get_revenu(
            "1"
        )


def test_get_revenu_invalid_zero(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.get_revenu(
            0
        )


def test_get_revenu_invalid_negative(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.get_revenu(
            -1
        )


# ============================================================
# GET ALL
# ============================================================


def test_get_all_revenus(
    service,
):

    revenu_1 = Revenu(
        produit="Tomates",
        quantite=10,
        prix_unitaire=500,
        montant=5000,
        date_revenu="2026-05-01",
    )

    revenu_2 = Revenu(
        produit="Maïs",
        quantite=20,
        prix_unitaire=1000,
        montant=20000,
        date_revenu="2026-05-02",
    )

    service.create_revenu(
        revenu_1
    )

    service.create_revenu(
        revenu_2
    )

    result = service.get_all_revenus()

    assert len(result) == 2


def test_get_all_revenus_returns_instances(
    service,
    revenu,
):

    service.create_revenu(
        revenu
    )

    result = service.get_all_revenus()

    assert all(
        isinstance(item, Revenu)
        for item in result
    )


# ============================================================
# GET BY PARCELLE
# ============================================================


def test_get_revenus_by_parcelle(
    service,
    revenu,
    parcelle,
):

    revenu.parcelle_id = parcelle.id

    service.create_revenu(
        revenu
    )

    result = service.get_revenus_by_parcelle(
        parcelle.id
    )

    assert len(result) == 1
    assert result[0].parcelle_id == parcelle.id


def test_get_revenus_by_parcelle_empty(
    service,
    parcelle,
):

    result = service.get_revenus_by_parcelle(
        parcelle.id
    )

    assert result == []


def test_get_revenus_by_parcelle_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="identifiant de la parcelle",
    ):
        service.get_revenus_by_parcelle(
            "1"
        )


def test_get_revenus_by_parcelle_invalid_zero(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.get_revenus_by_parcelle(
            0
        )


def test_get_revenus_by_parcelle_invalid_negative(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.get_revenus_by_parcelle(
            -1
        )


# ============================================================
# GET BY CULTURE
# ============================================================


def test_get_revenus_by_culture(
    service,
    revenu,
    culture,
):

    revenu.culture_id = culture.id

    service.create_revenu(
        revenu
    )

    result = service.get_revenus_by_culture(
        culture.id
    )

    assert len(result) == 1
    assert result[0].culture_id == culture.id


def test_get_revenus_by_culture_empty(
    service,
    culture,
):

    result = service.get_revenus_by_culture(
        culture.id
    )

    assert result == []


def test_get_revenus_by_culture_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="identifiant de la culture",
    ):
        service.get_revenus_by_culture(
            "1"
        )


def test_get_revenus_by_culture_invalid_zero(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.get_revenus_by_culture(
            0
        )


def test_get_revenus_by_culture_invalid_negative(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.get_revenus_by_culture(
            -1
        )


# ============================================================
# UPDATE
# ============================================================


def test_update_revenu(
    service,
    revenu,
):

    created = service.create_revenu(
        revenu
    )

    created.produit = "Tomates premium"
    created.quantite = 120.0
    created.montant = 60000.0

    result = service.update_revenu(
        created
    )

    assert result.id == created.id
    assert result.produit == "Tomates premium"
    assert result.quantite == 120.0
    assert result.montant == 60000.0


def test_update_revenu_without_id(
    service,
    revenu,
):

    with pytest.raises(
        ValueError,
        match="doit posséder un identifiant",
    ):
        service.update_revenu(
            revenu
        )


def test_update_revenu_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="revenu doit être une instance",
    ):
        service.update_revenu(
            "invalid"
        )


def test_update_revenu_invalid_id(
    service,
    revenu,
):

    created = service.create_revenu(
        revenu
    )

    created.id = -1

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.update_revenu(
            created
        )


def test_update_revenu_not_found(
    service,
    revenu,
):

    revenu.id = 999999

    with pytest.raises(
        ValueError,
        match="Aucun revenu trouvé",
    ):
        service.update_revenu(
            revenu
        )


def test_update_revenu_invalid_parcelle(
    service,
    revenu,
):

    created = service.create_revenu(
        revenu
    )

    created.parcelle_id = 999999

    with pytest.raises(
        ValueError,
        match="Aucune parcelle trouvée",
    ):
        service.update_revenu(
            created
        )


def test_update_revenu_invalid_culture(
    service,
    revenu,
):

    created = service.create_revenu(
        revenu
    )

    created.culture_id = 999999

    with pytest.raises(
        ValueError,
        match="Aucune culture trouvée",
    ):
        service.update_revenu(
            created
        )


def test_update_revenu_culture_wrong_parcelle(
    service,
    revenu,
    parcelle,
    autre_culture,
):

    created = service.create_revenu(
        revenu
    )

    created.parcelle_id = parcelle.id
    created.culture_id = autre_culture.id

    with pytest.raises(
        ValueError,
        match="n'appartient pas à la parcelle",
    ):
        service.update_revenu(
            created
        )


# ============================================================
# DELETE
# ============================================================


def test_delete_revenu(
    service,
    revenu,
):

    created = service.create_revenu(
        revenu
    )

    result = service.delete_revenu(
        created.id
    )

    assert result is True

    assert (
        service.get_revenu(
            created.id
        )
        is None
    )


def test_delete_revenu_not_found(
    service,
):

    with pytest.raises(
        ValueError,
        match="Aucun revenu trouvé",
    ):
        service.delete_revenu(
            999999
        )


def test_delete_revenu_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="identifiant du revenu",
    ):
        service.delete_revenu(
            "1"
        )


def test_delete_revenu_invalid_zero(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.delete_revenu(
            0
        )


def test_delete_revenu_invalid_negative(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.delete_revenu(
            -1
        )


# ============================================================
# EXISTS
# ============================================================


def test_revenu_exists(
    service,
    revenu,
):

    created = service.create_revenu(
        revenu
    )

    assert (
        service.revenu_exists(
            created.id
        )
        is True
    )


def test_revenu_does_not_exist(
    service,
):

    assert (
        service.revenu_exists(
            999999
        )
        is False
    )


def test_revenu_exists_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="identifiant du revenu",
    ):
        service.revenu_exists(
            "1"
        )


# ============================================================
# PARCELLE EXISTS
# ============================================================


def test_parcelle_exists(
    service,
    parcelle,
):

    assert (
        service.parcelle_exists(
            parcelle.id
        )
        is True
    )


def test_parcelle_does_not_exist(
    service,
):

    assert (
        service.parcelle_exists(
            999999
        )
        is False
    )


def test_parcelle_exists_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="identifiant de la parcelle",
    ):
        service.parcelle_exists(
            "1"
        )


def test_parcelle_exists_invalid_zero(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.parcelle_exists(
            0
        )


def test_parcelle_exists_invalid_negative(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
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

    assert (
        service.culture_exists(
            culture.id
        )
        is True
    )


def test_culture_does_not_exist(
    service,
):

    assert (
        service.culture_exists(
            999999
        )
        is False
    )


def test_culture_exists_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="identifiant de la culture",
    ):
        service.culture_exists(
            "1"
        )


def test_culture_exists_invalid_zero(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.culture_exists(
            0
        )


def test_culture_exists_invalid_negative(
    service,
):

    with pytest.raises(
        ValueError,
        match="strictement positif",
    ):
        service.culture_exists(
            -1
        )


# ============================================================
# VALIDATE
# ============================================================


def test_validate_revenu(
    service,
    revenu,
):

    assert (
        service.validate_revenu(
            revenu
        )
        is True
    )


def test_validate_revenu_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="revenu doit être une instance",
    ):
        service.validate_revenu(
            "invalid"
        )


def test_validate_revenu_invalid_product_type(
    service,
    revenu,
):

    revenu.produit = 123

    with pytest.raises(
        TypeError,
        match="produit du revenu",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_empty_product(
    service,
    revenu,
):

    revenu.produit = "   "

    with pytest.raises(
        ValueError,
        match="produit du revenu ne doit pas être vide",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_invalid_quantity_type(
    service,
    revenu,
):

    revenu.quantite = "100"

    with pytest.raises(
        TypeError,
        match="quantité du revenu",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_zero_quantity(
    service,
    revenu,
):

    revenu.quantite = 0

    with pytest.raises(
        ValueError,
        match="quantité du revenu doit être",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_negative_quantity(
    service,
    revenu,
):

    revenu.quantite = -10

    with pytest.raises(
        ValueError,
        match="quantité du revenu doit être",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_invalid_unit_price_type(
    service,
    revenu,
):

    revenu.prix_unitaire = "500"

    with pytest.raises(
        TypeError,
        match="prix unitaire du revenu",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_negative_unit_price(
    service,
    revenu,
):

    revenu.prix_unitaire = -500

    with pytest.raises(
        ValueError,
        match="prix unitaire",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_invalid_amount_type(
    service,
    revenu,
):

    revenu.montant = "50000"

    with pytest.raises(
        TypeError,
        match="montant du revenu",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_negative_amount(
    service,
    revenu,
):

    revenu.montant = -50000

    with pytest.raises(
        ValueError,
        match="montant du revenu ne peut pas être négatif",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_inconsistent_amount(
    service,
    revenu,
):

    revenu.montant = 40000.0

    with pytest.raises(
        ValueError,
        match="montant du revenu doit être égal",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_float_tolerance(
    service,
    revenu,
):

    revenu.quantite = 0.1
    revenu.prix_unitaire = 0.2
    revenu.montant = 0.02

    assert (
        service.validate_revenu(
            revenu
        )
        is True
    )


def test_validate_revenu_invalid_date_type(
    service,
    revenu,
):

    revenu.date_revenu = 20260501

    with pytest.raises(
        TypeError,
        match="date du revenu",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_empty_date(
    service,
    revenu,
):

    revenu.date_revenu = "   "

    with pytest.raises(
        ValueError,
        match="date du revenu ne doit pas être vide",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_invalid_parcelle_type(
    service,
    revenu,
):

    revenu.parcelle_id = "1"

    with pytest.raises(
        TypeError,
        match="identifiant de la parcelle",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_invalid_culture_type(
    service,
    revenu,
):

    revenu.culture_id = "1"

    with pytest.raises(
        TypeError,
        match="identifiant de la culture",
    ):
        service.validate_revenu(
            revenu
        )


def test_validate_revenu_invalid_description_type(
    service,
    revenu,
):

    revenu.description = 123

    with pytest.raises(
        TypeError,
        match="description du revenu",
    ):
        service.validate_revenu(
            revenu
        )


# ============================================================
# SEARCH
# ============================================================


def test_search_revenus(
    service,
):

    service.create_revenu(
        Revenu(
            produit="Tomates",
            quantite=10,
            prix_unitaire=500,
            montant=5000,
            date_revenu="2026-05-01",
        )
    )

    service.create_revenu(
        Revenu(
            produit="Maïs",
            quantite=20,
            prix_unitaire=1000,
            montant=20000,
            date_revenu="2026-05-02",
        )
    )

    result = service.search_revenus(
        "Tom"
    )

    assert len(result) == 1
    assert result[0].produit == "Tomates"


def test_search_revenus_case_insensitive(
    service,
):

    service.create_revenu(
        Revenu(
            produit="Tomates",
            quantite=10,
            prix_unitaire=500,
            montant=5000,
            date_revenu="2026-05-01",
        )
    )

    result = service.search_revenus(
        "tomates"
    )

    assert len(result) == 1
    assert result[0].produit == "Tomates"


def test_search_revenus_empty_search(
    service,
):

    service.create_revenu(
        Revenu(
            produit="Tomates",
            quantite=10,
            prix_unitaire=500,
            montant=5000,
            date_revenu="2026-05-01",
        )
    )

    service.create_revenu(
        Revenu(
            produit="Maïs",
            quantite=20,
            prix_unitaire=1000,
            montant=20000,
            date_revenu="2026-05-02",
        )
    )

    result = service.search_revenus(
        ""
    )

    assert len(result) == 2


def test_search_revenus_whitespace_search(
    service,
):

    service.create_revenu(
        Revenu(
            produit="Tomates",
            quantite=10,
            prix_unitaire=500,
            montant=5000,
            date_revenu="2026-05-01",
        )
    )

    result = service.search_revenus(
        "   "
    )

    assert len(result) == 1
    assert result[0].produit == "Tomates"


def test_search_revenus_invalid_type(
    service,
):

    with pytest.raises(
        TypeError,
        match="search_term doit être une chaîne",
    ):
        service.search_revenus(
            123
        )

