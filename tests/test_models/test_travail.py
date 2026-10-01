from core.models.travail import Travail


# ============================================================
# TEST CRÉATION
# ============================================================

def test_create_travail():
    """
    Vérifie qu'un travail agricole peut être créé.
    """

    travail = Travail(
        parcelle_id=1,
        culture_id=2,
        type_travail="Préparation du sol",
        date_travail="2026-08-25",
        cout=150000,
        description="Préparation avant semis",
    )

    assert travail.parcelle_id == 1
    assert travail.culture_id == 2
    assert travail.type_travail == "Préparation du sol"
    assert travail.date_travail == "2026-08-25"
    assert travail.cout == 150000
    assert travail.description == "Préparation avant semis"


# ============================================================
# TEST VALEURS PAR DÉFAUT
# ============================================================

def test_travail_default_values():
    """
    Vérifie les valeurs par défaut du modèle.
    """

    travail = Travail(
        parcelle_id=1,
        type_travail="Désherbage",
        date_travail="2026-09-20",
    )

    assert travail.culture_id is None
    assert travail.cout == 0.0
    assert travail.description is None
    assert travail.id is None


# ============================================================
# TEST IDENTIFIANT
# ============================================================

def test_travail_with_id():
    """
    Vérifie qu'un travail peut recevoir un identifiant.
    """

    travail = Travail(
        id=10,
        parcelle_id=1,
        type_travail="Irrigation",
        date_travail="2026-09-21",
    )

    assert travail.id == 10


# ============================================================
# TEST PARCELLE INVALIDE
# ============================================================

def test_travail_invalid_parcelle_id():
    """
    Vérifie que l'identifiant de parcelle doit être positif.
    """

    try:
        Travail(
            parcelle_id=0,
            type_travail="Désherbage",
            date_travail="2026-09-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'identifiant de la parcelle doit être "
            "strictement positif."
        )


# ============================================================
# TEST CULTURE INVALIDE
# ============================================================

def test_travail_invalid_culture_id():
    """
    Vérifie que l'identifiant de culture doit être positif.
    """

    try:
        Travail(
            parcelle_id=1,
            culture_id=0,
            type_travail="Désherbage",
            date_travail="2026-09-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'identifiant de la culture doit être "
            "strictement positif."
        )


# ============================================================
# TEST TYPE CULTURE INVALIDE
# ============================================================

def test_travail_invalid_culture_type():
    """
    Vérifie que culture_id doit être un entier ou None.
    """

    try:
        Travail(
            parcelle_id=1,
            culture_id="2",
            type_travail="Désherbage",
            date_travail="2026-09-20",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "L'identifiant de la culture doit être "
            "un entier ou None."
        )


# ============================================================
# TEST TYPE DE TRAVAIL VIDE
# ============================================================

def test_travail_empty_type():
    """
    Vérifie que le type de travail ne peut pas être vide.
    """

    try:
        Travail(
            parcelle_id=1,
            type_travail="",
            date_travail="2026-09-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le type de travail ne peut pas être vide."
        )


# ============================================================
# TEST TYPE TRAVAIL INVALIDE
# ============================================================

def test_travail_invalid_type():
    """
    Vérifie que le type de travail doit être une chaîne.
    """

    try:
        Travail(
            parcelle_id=1,
            type_travail=123,
            date_travail="2026-09-20",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le type de travail doit être une chaîne "
            "de caractères."
        )


# ============================================================
# TEST DATE VIDE
# ============================================================

def test_travail_empty_date():
    """
    Vérifie que la date ne peut pas être vide.
    """

    try:
        Travail(
            parcelle_id=1,
            type_travail="Désherbage",
            date_travail="",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La date du travail ne peut pas être vide."
        )


# ============================================================
# TEST COÛT NÉGATIF
# ============================================================

def test_travail_negative_cost():
    """
    Vérifie qu'un coût négatif est refusé.
    """

    try:
        Travail(
            parcelle_id=1,
            type_travail="Désherbage",
            date_travail="2026-09-20",
            cout=-5000,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le coût du travail ne peut pas être négatif."
        )


# ============================================================
# TEST TYPE COÛT
# ============================================================

def test_travail_invalid_cost_type():
    """
    Vérifie que le coût doit être numérique.
    """

    try:
        Travail(
            parcelle_id=1,
            type_travail="Désherbage",
            date_travail="2026-09-20",
            cout="5000",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le coût du travail doit être un nombre."
        )