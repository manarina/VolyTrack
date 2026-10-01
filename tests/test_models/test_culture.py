from core.models.culture import Culture


# ============================================================
# TEST CRÉATION
# ============================================================

def test_create_culture():
    """
    Vérifie qu'une culture peut être créée.
    """

    culture = Culture(
        parcelle_id=1,
        nom="Riz",
        variete="Variété locale",
        date_semis="2026-09-01",
        date_prevue_recolte="2027-01-15",
        statut="En croissance",
        description="Culture de démonstration",
    )

    assert culture.parcelle_id == 1
    assert culture.nom == "Riz"
    assert culture.variete == "Variété locale"
    assert culture.date_semis == "2026-09-01"
    assert culture.date_prevue_recolte == "2027-01-15"
    assert culture.statut == "En croissance"
    assert culture.description == "Culture de démonstration"


# ============================================================
# TEST VALEURS PAR DÉFAUT
# ============================================================

def test_culture_default_values():
    """
    Vérifie les valeurs par défaut.
    """

    culture = Culture(
        parcelle_id=1,
        nom="Tomate",
    )

    assert culture.variete is None
    assert culture.date_semis is None
    assert culture.date_prevue_recolte is None
    assert culture.statut == "Planifiée"
    assert culture.description is None
    assert culture.id is None


# ============================================================
# TEST IDENTIFIANT
# ============================================================

def test_culture_with_id():
    """
    Vérifie qu'une culture peut recevoir un identifiant.
    """

    culture = Culture(
        id=10,
        parcelle_id=1,
        nom="Riz",
    )

    assert culture.id == 10


# ============================================================
# TEST PARCELLE INVALIDE
# ============================================================

def test_culture_invalid_parcelle_id():
    """
    Vérifie que l'identifiant de parcelle doit être positif.
    """

    try:
        Culture(
            parcelle_id=0,
            nom="Riz",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'identifiant de la parcelle doit être "
            "strictement positif."
        )


# ============================================================
# TEST NOM VIDE
# ============================================================

def test_culture_empty_name():
    """
    Vérifie qu'une culture ne peut pas avoir
    un nom vide.
    """

    try:
        Culture(
            parcelle_id=1,
            nom="",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le nom de la culture ne peut pas être vide."
        )


# ============================================================
# TEST TYPE NOM
# ============================================================

def test_culture_invalid_name_type():
    """
    Vérifie que le nom doit être une chaîne.
    """

    try:
        Culture(
            parcelle_id=1,
            nom=123,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le nom de la culture doit être une chaîne "
            "de caractères."
        )


# ============================================================
# TEST STATUT VIDE
# ============================================================

def test_culture_empty_status():
    """
    Vérifie que le statut ne peut pas être vide.
    """

    try:
        Culture(
            parcelle_id=1,
            nom="Riz",
            statut="",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le statut ne peut pas être vide."
        )


# ============================================================
# TEST TYPE DATE
# ============================================================

def test_culture_invalid_date_type():
    """
    Vérifie que les dates sont des chaînes ou None.
    """

    try:
        Culture(
            parcelle_id=1,
            nom="Riz",
            date_semis=20260901,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La date de semis doit être une chaîne ou None."
        )


# ============================================================
# TEST TYPE PARCELLE
# ============================================================

def test_culture_invalid_parcelle_type():
    """
    Vérifie que parcelle_id doit être un entier.
    """

    try:
        Culture(
            parcelle_id="1",
            nom="Riz",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "L'identifiant de la parcelle doit être un entier."
        )