from core.models.recolte import Recolte


# ============================================================
# TEST CRÉATION
# ============================================================

def test_create_recolte():
    """
    Vérifie qu'une récolte peut être créée.
    """

    recolte = Recolte(
        culture_id=1,
        date_recolte="2027-01-20",
        quantite=2500,
        unite="kg",
        qualite="Bonne",
        description="Récolte principale de riz",
    )

    assert recolte.culture_id == 1
    assert recolte.date_recolte == "2027-01-20"
    assert recolte.quantite == 2500
    assert recolte.unite == "kg"
    assert recolte.qualite == "Bonne"
    assert recolte.description == (
        "Récolte principale de riz"
    )


# ============================================================
# TEST VALEURS PAR DÉFAUT
# ============================================================

def test_recolte_default_values():
    """
    Vérifie les valeurs par défaut.
    """

    recolte = Recolte(
        culture_id=1,
        date_recolte="2027-01-20",
        quantite=500,
        unite="kg",
    )

    assert recolte.qualite is None
    assert recolte.description is None
    assert recolte.id is None


# ============================================================
# TEST IDENTIFIANT
# ============================================================

def test_recolte_with_id():
    """
    Vérifie qu'une récolte peut recevoir un identifiant.
    """

    recolte = Recolte(
        id=10,
        culture_id=2,
        date_recolte="2027-02-15",
        quantite=800,
        unite="kg",
    )

    assert recolte.id == 10


# ============================================================
# TEST CULTURE INVALIDE
# ============================================================

def test_recolte_invalid_culture_id():
    """
    Vérifie que l'identifiant de culture doit être positif.
    """

    try:
        Recolte(
            culture_id=0,
            date_recolte="2027-01-20",
            quantite=500,
            unite="kg",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'identifiant de la culture doit être "
            "strictement positif."
        )


# ============================================================
# TEST TYPE CULTURE
# ============================================================

def test_recolte_invalid_culture_type():
    """
    Vérifie que l'identifiant de culture doit être un entier.
    """

    try:
        Recolte(
            culture_id="1",
            date_recolte="2027-01-20",
            quantite=500,
            unite="kg",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "L'identifiant de la culture doit être un entier."
        )


# ============================================================
# TEST DATE VIDE
# ============================================================

def test_recolte_empty_date():
    """
    Vérifie que la date ne peut pas être vide.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="",
            quantite=500,
            unite="kg",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La date de récolte ne peut pas être vide."
        )


# ============================================================
# TEST TYPE DATE
# ============================================================

def test_recolte_invalid_date_type():
    """
    Vérifie que la date doit être une chaîne.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte=20270120,
            quantite=500,
            unite="kg",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La date de récolte doit être une chaîne "
            "de caractères."
        )


# ============================================================
# TEST QUANTITÉ NULLE
# ============================================================

def test_recolte_zero_quantity():
    """
    Vérifie qu'une quantité nulle est refusée.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="2027-01-20",
            quantite=0,
            unite="kg",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La quantité récoltée doit être "
            "strictement positive."
        )


# ============================================================
# TEST QUANTITÉ NÉGATIVE
# ============================================================

def test_recolte_negative_quantity():
    """
    Vérifie qu'une quantité négative est refusée.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="2027-01-20",
            quantite=-100,
            unite="kg",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La quantité récoltée doit être "
            "strictement positive."
        )


# ============================================================
# TEST TYPE QUANTITÉ
# ============================================================

def test_recolte_invalid_quantity_type():
    """
    Vérifie que la quantité doit être numérique.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="2027-01-20",
            quantite="500",
            unite="kg",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La quantité récoltée doit être un nombre."
        )


# ============================================================
# TEST UNITÉ VIDE
# ============================================================

def test_recolte_empty_unit():
    """
    Vérifie que l'unité ne peut pas être vide.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="2027-01-20",
            quantite=500,
            unite="",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'unité ne peut pas être vide."
        )


# ============================================================
# TEST TYPE UNITÉ
# ============================================================

def test_recolte_invalid_unit_type():
    """
    Vérifie que l'unité doit être une chaîne.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="2027-01-20",
            quantite=500,
            unite=123,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "L'unité doit être une chaîne de caractères."
        )


# ============================================================
# TEST TYPE QUALITÉ
# ============================================================

def test_recolte_invalid_quality_type():
    """
    Vérifie que la qualité doit être une chaîne ou None.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="2027-01-20",
            quantite=500,
            unite="kg",
            qualite=123,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La qualité doit être une chaîne ou None."
        )


# ============================================================
# TEST TYPE DESCRIPTION
# ============================================================

def test_recolte_invalid_description_type():
    """
    Vérifie que la description doit être une chaîne ou None.
    """

    try:
        Recolte(
            culture_id=1,
            date_recolte="2027-01-20",
            quantite=500,
            unite="kg",
            description=123,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La description doit être une chaîne ou None."
        )


# ============================================================
# TEST TYPE ID
# ============================================================

def test_recolte_invalid_id_type():
    """
    Vérifie que l'identifiant doit être un entier ou None.
    """

    try:
        Recolte(
            id="1",
            culture_id=1,
            date_recolte="2027-01-20",
            quantite=500,
            unite="kg",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "L'identifiant doit être un entier ou None."
        )