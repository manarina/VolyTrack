
"""
Tests du RecolteService.

Couverture :
    - création ;
    - consultation ;
    - modification ;
    - suppression ;
    - recherche ;
    - validation ;
    - relation avec Culture ;
    - gestion des erreurs.
"""

import pytest

from core.database.connection import get_connection
from core.models.culture import Culture
from core.models.recolte import Recolte
from core.repositories.culture_repository import CultureRepository
from core.repositories.recolte_repository import RecolteRepository
from core.services.recolte_service import RecolteService


# ============================================================
# NETTOYAGE DE LA TABLE
# ============================================================


@pytest.fixture(autouse=True)
def clean_recoltes_table():
    """
    Nettoie la table recoltes avant et après chaque test.

    Cela évite que les données persistantes de SQLite
    influencent les résultats des tests.
    """

    def clear_table():
        connection = get_connection()

        try:
            connection.execute(
                "DELETE FROM recoltes"
            )

            connection.commit()

        finally:
            connection.close()

    clear_table()

    yield

    clear_table()


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def repository():
    """Repository des récoltes."""
    return RecolteRepository()


@pytest.fixture
def culture_repository():
    """Repository des cultures."""
    return CultureRepository()


@pytest.fixture
def service(
    repository,
    culture_repository,
):
    """Service de gestion des récoltes."""
    return RecolteService(
        repository=repository,
        culture_repository=culture_repository,
    )


@pytest.fixture
def culture(
    culture_repository,
):
    """Culture utilisée par les tests."""

    culture = Culture(
        parcelle_id=1,
        nom="Riz",
        variete="Makalioka",
        date_semis="2026-01-10",
        date_prevue_recolte="2026-05-10",
        statut="En cours",
        description="Culture de riz",
    )

    return culture_repository.create(
        culture
    )


@pytest.fixture
def autre_culture(
    culture_repository,
):
    """Deuxième culture utilisée par les tests."""

    culture = Culture(
        parcelle_id=1,
        nom="Maïs",
        variete="Maïs local",
        date_semis="2026-02-01",
        date_prevue_recolte="2026-06-01",
        statut="En cours",
        description="Culture de maïs",
    )

    return culture_repository.create(
        culture
    )


@pytest.fixture
def recolte(culture):
    """Récolte valide."""

    return Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
        qualite="Bonne",
        description="Première récolte",
    )


# ============================================================
# CRÉATION
# ============================================================


def test_create_recolte(
    service,
    recolte,
):
    """Une récolte valide doit être créée."""

    result = service.create_recolte(
        recolte
    )

    assert result is not None
    assert result.id is not None
    assert result.culture_id == recolte.culture_id
    assert result.quantite == 500.0
    assert result.unite == "kg"


def test_create_recolte_culture_inexistante(
    service,
):
    """La création doit échouer si la culture n'existe pas."""

    recolte = Recolte(
        culture_id=999999,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
    )

    with pytest.raises(
        ValueError,
        match="n'existe pas",
    ):
        service.create_recolte(
            recolte
        )


def test_create_recolte_invalid_type(
    service,
):
    """Le service doit refuser un objet qui n'est pas une Recolte."""

    with pytest.raises(
        ValueError,
        match="instance de Recolte",
    ):
        service.create_recolte(
            "invalid"
        )


# ============================================================
# CONSULTATION PAR ID
# ============================================================


def test_get_recolte(
    service,
    recolte,
):
    """Une récolte doit pouvoir être récupérée par son ID."""

    created = service.create_recolte(
        recolte
    )

    result = service.get_recolte(
        created.id
    )

    assert result is not None
    assert result.id == created.id
    assert result.culture_id == created.culture_id


def test_get_recolte_not_found(
    service,
):
    """Un ID inexistant doit retourner None."""

    result = service.get_recolte(
        999999
    )

    assert result is None


def test_get_recolte_invalid_id(
    service,
):
    """Un ID invalide doit être rejeté."""

    with pytest.raises(
        ValueError,
        match="recolte_id doit être supérieur à zéro",
    ):
        service.get_recolte(
            0
        )


def test_get_recolte_invalid_id_type(
    service,
):
    """Un ID non entier doit être rejeté."""

    with pytest.raises(
        ValueError,
        match="recolte_id doit être un entier positif",
    ):
        service.get_recolte(
            "1"
        )


# ============================================================
# CONSULTATION DE TOUTES LES RÉCOLTES
# ============================================================


def test_get_all_recoltes(
    service,
    culture,
):
    """Le service doit retourner toutes les récoltes."""

    recolte_1 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
    )

    recolte_2 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-06-10",
        quantite=300.0,
        unite="kg",
    )

    service.create_recolte(
        recolte_1
    )

    service.create_recolte(
        recolte_2
    )

    result = service.get_all_recoltes()

    assert len(result) == 2


# ============================================================
# CONSULTATION PAR CULTURE
# ============================================================


def test_get_recoltes_by_culture(
    service,
    culture,
    autre_culture,
):
    """Le service doit filtrer les récoltes par culture."""

    recolte_1 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
    )

    recolte_2 = Recolte(
        culture_id=autre_culture.id,
        date_recolte="2026-06-10",
        quantite=300.0,
        unite="kg",
    )

    service.create_recolte(
        recolte_1
    )

    service.create_recolte(
        recolte_2
    )

    result = service.get_recoltes_by_culture(
        culture.id
    )

    assert len(result) == 1
    assert result[0].culture_id == culture.id


def test_get_recoltes_by_culture_invalid_id(
    service,
):
    """Un ID de culture invalide doit être rejeté."""

    with pytest.raises(
        ValueError,
        match="culture_id doit être supérieur à zéro",
    ):
        service.get_recoltes_by_culture(
            0
        )


# ============================================================
# EXISTENCE
# ============================================================


def test_recolte_exists(
    service,
    recolte,
):
    """recolte_exists doit retourner True pour une récolte existante."""

    created = service.create_recolte(
        recolte
    )

    assert service.recolte_exists(
        created.id
    ) is True


def test_recolte_not_exists(
    service,
):
    """recolte_exists doit retourner False pour un ID inexistant."""

    assert service.recolte_exists(
        999999
    ) is False


def test_recolte_exists_invalid_id(
    service,
):
    """recolte_exists doit refuser un ID invalide."""

    with pytest.raises(
        ValueError,
        match="recolte_id doit être supérieur à zéro",
    ):
        service.recolte_exists(
            0
        )


# ============================================================
# CULTURE EXISTS
# ============================================================


def test_culture_exists(
    service,
    culture,
):
    """culture_exists doit détecter une culture existante."""

    assert service.culture_exists(
        culture.id
    ) is True


def test_culture_not_exists(
    service,
):
    """culture_exists doit retourner False si la culture n'existe pas."""

    assert service.culture_exists(
        999999
    ) is False


def test_culture_exists_invalid_id(
    service,
):
    """culture_exists doit refuser un ID invalide."""

    with pytest.raises(
        ValueError,
        match="culture_id doit être supérieur à zéro",
    ):
        service.culture_exists(
            0
        )


# ============================================================
# MODIFICATION
# ============================================================


def test_update_recolte(
    service,
    recolte,
):
    """Une récolte existante doit pouvoir être modifiée."""

    created = service.create_recolte(
        recolte
    )

    created.quantite = 750.0
    created.unite = "kg"
    created.qualite = "Très bonne"

    result = service.update_recolte(
        created
    )

    assert result is not None
    assert result.id == created.id
    assert result.quantite == 750.0
    assert result.qualite == "Très bonne"


def test_update_recolte_not_found(
    service,
    culture,
):
    """La modification d'une récolte inexistante doit échouer."""

    recolte = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
        id=999999,
    )

    with pytest.raises(
        ValueError,
        match="Aucune récolte trouvée",
    ):
        service.update_recolte(
            recolte
        )


def test_update_recolte_without_id(
    service,
    recolte,
):
    """Une modification sans ID doit être refusée."""

    with pytest.raises(
        ValueError,
        match="identifiant de la récolte est obligatoire",
    ):
        service.update_recolte(
            recolte
        )


# ============================================================
# SUPPRESSION
# ============================================================


def test_delete_recolte(
    service,
    recolte,
):
    """Une récolte existante doit pouvoir être supprimée."""

    created = service.create_recolte(
        recolte
    )

    result = service.delete_recolte(
        created.id
    )

    assert result is True

    assert service.get_recolte(
        created.id
    ) is None


def test_delete_recolte_not_found(
    service,
):
    """La suppression d'une récolte inexistante doit échouer."""

    with pytest.raises(
        ValueError,
        match="Aucune récolte trouvée",
    ):
        service.delete_recolte(
            999999
        )


def test_delete_recolte_invalid_id(
    service,
):
    """La suppression doit refuser un ID invalide."""

    with pytest.raises(
        ValueError,
        match="recolte_id doit être supérieur à zéro",
    ):
        service.delete_recolte(
            0
        )


# ============================================================
# VALIDATION — TYPE
# ============================================================


def test_validate_recolte_invalid_type(
    service,
):
    """validate_recolte doit refuser un mauvais type."""

    with pytest.raises(
        ValueError,
        match="instance de Recolte",
    ):
        service.validate_recolte(
            "invalid"
        )


# ============================================================
# VALIDATION — CULTURE
# ============================================================


def test_validate_recolte_invalid_culture_id(
    service,
    recolte,
):
    """culture_id doit être un entier positif."""

    recolte.culture_id = 0

    with pytest.raises(
        ValueError,
        match="culture_id doit être supérieur à zéro",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_invalid_culture_type(
    service,
    recolte,
):
    """culture_id doit être un entier."""

    recolte.culture_id = "1"

    with pytest.raises(
        ValueError,
        match="culture_id doit être un entier positif",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_culture_not_found(
    service,
    recolte,
):
    """Une culture inexistante doit être refusée."""

    recolte.culture_id = 999999

    with pytest.raises(
        ValueError,
        match="n'existe pas",
    ):
        service.validate_recolte(
            recolte
        )


# ============================================================
# VALIDATION — DATE
# ============================================================


def test_validate_recolte_invalid_date_type(
    service,
    recolte,
):
    """La date doit être une chaîne."""

    recolte.date_recolte = 20260510

    with pytest.raises(
        ValueError,
        match="date de récolte doit être une chaîne",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_empty_date(
    service,
    recolte,
):
    """La date ne doit pas être vide."""

    recolte.date_recolte = "   "

    with pytest.raises(
        ValueError,
        match="date de récolte ne peut pas être vide",
    ):
        service.validate_recolte(
            recolte
        )


# ============================================================
# VALIDATION — QUANTITÉ
# ============================================================


def test_validate_recolte_invalid_quantity_type(
    service,
    recolte,
):
    """La quantité doit être numérique."""

    recolte.quantite = "500"

    with pytest.raises(
        ValueError,
        match="quantité doit être un nombre",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_boolean_quantity(
    service,
    recolte,
):
    """Une valeur booléenne ne doit pas être acceptée comme quantité."""

    recolte.quantite = True

    with pytest.raises(
        ValueError,
        match="quantité doit être un nombre positif",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_zero_quantity(
    service,
    recolte,
):
    """La quantité doit être strictement positive."""

    recolte.quantite = 0

    with pytest.raises(
        ValueError,
        match="quantité doit être strictement positive",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_negative_quantity(
    service,
    recolte,
):
    """Une quantité négative doit être refusée."""

    recolte.quantite = -10

    with pytest.raises(
        ValueError,
        match="quantité doit être strictement positive",
    ):
        service.validate_recolte(
            recolte
        )


# ============================================================
# VALIDATION — UNITÉ
# ============================================================


def test_validate_recolte_invalid_unit_type(
    service,
    recolte,
):
    """L'unité doit être une chaîne."""

    recolte.unite = 100

    with pytest.raises(
        ValueError,
        match="unité doit être une chaîne",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_empty_unit(
    service,
    recolte,
):
    """L'unité ne doit pas être vide."""

    recolte.unite = "   "

    with pytest.raises(
        ValueError,
        match="unité ne peut pas être vide",
    ):
        service.validate_recolte(
            recolte
        )


# ============================================================
# VALIDATION — QUALITÉ
# ============================================================


def test_validate_recolte_invalid_quality_type(
    service,
    recolte,
):
    """La qualité doit être une chaîne ou None."""

    recolte.qualite = 100

    with pytest.raises(
        ValueError,
        match="qualité doit être une chaîne",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_quality_none(
    service,
    recolte,
):
    """La qualité peut être None."""

    recolte.qualite = None

    assert service.validate_recolte(
        recolte
    ) is True


# ============================================================
# VALIDATION — DESCRIPTION
# ============================================================


def test_validate_recolte_invalid_description_type(
    service,
    recolte,
):
    """La description doit être une chaîne ou None."""

    recolte.description = 123

    with pytest.raises(
        ValueError,
        match="description doit être une chaîne",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_description_none(
    service,
    recolte,
):
    """La description peut être None."""

    recolte.description = None

    assert service.validate_recolte(
        recolte
    ) is True


# ============================================================
# VALIDATION — ID
# ============================================================


def test_validate_recolte_invalid_id(
    service,
    recolte,
):
    """Un ID négatif doit être refusé."""

    recolte.id = -1

    with pytest.raises(
        ValueError,
        match="id doit être supérieur à zéro",
    ):
        service.validate_recolte(
            recolte
        )


def test_validate_recolte_invalid_id_type(
    service,
    recolte,
):
    """Un ID non entier doit être refusé."""

    # Le modèle Recolte valide normalement l'ID lors de
    # sa construction. On modifie ensuite l'attribut pour
    # tester explicitement la validation du service.
    recolte.id = "1"

    with pytest.raises(
        ValueError,
        match="id doit être un entier positif",
    ):
        service.validate_recolte(
            recolte
        )


# ============================================================
# VALIDATION COMPLÈTE
# ============================================================


def test_validate_recolte_valid(
    service,
    recolte,
):
    """Une récolte valide doit passer toutes les validations."""

    assert service.validate_recolte(
        recolte
    ) is True


# ============================================================
# RECHERCHE
# ============================================================


def test_search_recoltes_by_date(
    service,
    culture,
):
    """La recherche doit fonctionner sur la date."""

    recolte_1 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
    )

    recolte_2 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-06-20",
        quantite=300.0,
        unite="kg",
    )

    service.create_recolte(
        recolte_1
    )

    service.create_recolte(
        recolte_2
    )

    result = service.search_recoltes(
        "05-10"
    )

    assert len(result) == 1
    assert result[0].date_recolte == "2026-05-10"


def test_search_recoltes_by_unit(
    service,
    culture,
):
    """La recherche doit fonctionner sur l'unité."""

    recolte_1 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
    )

    recolte_2 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-06-20",
        quantite=2.0,
        unite="tonnes",
    )

    service.create_recolte(
        recolte_1
    )

    service.create_recolte(
        recolte_2
    )

    result = service.search_recoltes(
        "tonnes"
    )

    assert len(result) == 1
    assert result[0].unite == "tonnes"


def test_search_recoltes_by_quality(
    service,
    culture,
):
    """La recherche doit fonctionner sur la qualité."""

    recolte_1 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
        qualite="Excellente",
    )

    recolte_2 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-06-20",
        quantite=300.0,
        unite="kg",
        qualite="Moyenne",
    )

    service.create_recolte(
        recolte_1
    )

    service.create_recolte(
        recolte_2
    )

    result = service.search_recoltes(
        "Excellente"
    )

    assert len(result) == 1
    assert result[0].qualite == "Excellente"


def test_search_recoltes_by_description(
    service,
    culture,
):
    """La recherche doit fonctionner sur la description."""

    recolte_1 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
        description="Récolte principale",
    )

    recolte_2 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-06-20",
        quantite=300.0,
        unite="kg",
        description="Récolte secondaire",
    )

    service.create_recolte(
        recolte_1
    )

    service.create_recolte(
        recolte_2
    )

    result = service.search_recoltes(
        "principale"
    )

    assert len(result) == 1
    assert result[0].description == "Récolte principale"


def test_search_recoltes_case_insensitive(
    service,
    culture,
):
    """La recherche doit être insensible à la casse."""

    recolte = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="KG",
        qualite="Excellente",
    )

    service.create_recolte(
        recolte
    )

    result = service.search_recoltes(
        "excellente"
    )

    assert len(result) == 1


def test_search_recoltes_empty_search(
    service,
    culture,
):
    """Une recherche vide doit retourner toutes les récoltes."""

    recolte_1 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
    )

    recolte_2 = Recolte(
        culture_id=culture.id,
        date_recolte="2026-06-10",
        quantite=300.0,
        unite="kg",
    )

    service.create_recolte(
        recolte_1
    )

    service.create_recolte(
        recolte_2
    )

    result = service.search_recoltes(
        ""
    )

    assert len(result) == 2


def test_search_recoltes_whitespace_search(
    service,
    culture,
):
    """Une recherche composée d'espaces doit retourner toutes les récoltes."""

    recolte = Recolte(
        culture_id=culture.id,
        date_recolte="2026-05-10",
        quantite=500.0,
        unite="kg",
    )

    service.create_recolte(
        recolte
    )

    result = service.search_recoltes(
        "   "
    )

    assert len(result) == 1


def test_search_recoltes_invalid_type(
    service,
):
    """Le terme de recherche doit être une chaîne."""

    with pytest.raises(
        ValueError,
        match="terme de recherche doit être une chaîne",
    ):
        service.search_recoltes(
            123
        )

