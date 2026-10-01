from core.models.parcelle import Parcelle


# ============================================================
# TEST CRÉATION
# ============================================================

def test_create_parcelle():
    """
    Vérifie qu'une parcelle peut être créée.
    """

    parcelle = Parcelle(
        nom="Parcelle Nord",
        superficie=1.5,
        unite_superficie="ha",
        localisation="Zone Nord",
        description="Parcelle principale",
    )

    assert parcelle.nom == "Parcelle Nord"
    assert parcelle.superficie == 1.5
    assert parcelle.unite_superficie == "ha"
    assert parcelle.localisation == "Zone Nord"
    assert parcelle.description == "Parcelle principale"


# ============================================================
# TEST VALEURS PAR DÉFAUT
# ============================================================

def test_parcelle_default_values():
    """
    Vérifie les valeurs par défaut du modèle.
    """

    parcelle = Parcelle(
        nom="Parcelle Sud",
        superficie=0.8,
    )

    assert parcelle.unite_superficie == "ha"
    assert parcelle.localisation is None
    assert parcelle.description is None
    assert parcelle.id is None


# ============================================================
# TEST IDENTIFIANT
# ============================================================

def test_parcelle_with_id():
    """
    Vérifie qu'une parcelle peut recevoir un identifiant.
    """

    parcelle = Parcelle(
        id=10,
        nom="Parcelle Test",
        superficie=2.0,
    )

    assert parcelle.id == 10


# ============================================================
# TEST NOM VIDE
# ============================================================

def test_parcelle_empty_name_raises_error():
    """
    Vérifie qu'une parcelle ne peut pas avoir
    un nom vide.
    """

    try:
        Parcelle(
            nom="",
            superficie=1.0,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le nom de la parcelle ne peut pas être vide."
        )


# ============================================================
# TEST SUPERFICIE NÉGATIVE
# ============================================================

def test_parcelle_negative_area_raises_error():
    """
    Vérifie qu'une superficie négative est refusée.
    """

    try:
        Parcelle(
            nom="Parcelle Test",
            superficie=-1.0,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La superficie doit être strictement positive."
        )


# ============================================================
# TEST SUPERFICIE NULLE
# ============================================================

def test_parcelle_zero_area_raises_error():
    """
    Vérifie qu'une superficie nulle est refusée.
    """

    try:
        Parcelle(
            nom="Parcelle Test",
            superficie=0,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La superficie doit être strictement positive."
        )


# ============================================================
# TEST TYPE SUPERFICIE
# ============================================================

def test_parcelle_invalid_area_type():
    """
    Vérifie qu'une superficie non numérique est refusée.
    """

    try:
        Parcelle(
            nom="Parcelle Test",
            superficie="1.5",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La superficie doit être un nombre."
        )


# ============================================================
# TEST NOM NON VALIDE
# ============================================================

def test_parcelle_invalid_name_type():
    """
    Vérifie que le nom doit être une chaîne.
    """

    try:
        Parcelle(
            nom=123,
            superficie=1.0,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le nom de la parcelle doit être une chaîne de caractères."
        )


# ============================================================
# TEST UNITÉ VIDE
# ============================================================

def test_parcelle_empty_unit():
    """
    Vérifie que l'unité de superficie ne peut pas
    être vide.
    """

    try:
        Parcelle(
            nom="Parcelle Test",
            superficie=1.0,
            unite_superficie="",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'unité de superficie ne peut pas être vide."
        )