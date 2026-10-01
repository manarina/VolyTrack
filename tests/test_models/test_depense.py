from core.models.depense import Depense


# ============================================================
# TEST CRÉATION
# ============================================================

def test_create_depense():
    """
    Vérifie qu'une dépense peut être créée.
    """

    depense = Depense(
        parcelle_id=1,
        culture_id=2,
        categorie="Semences",
        montant=120000,
        date_depense="2026-09-01",
        description="Achat de semences",
    )

    assert depense.parcelle_id == 1
    assert depense.culture_id == 2
    assert depense.categorie == "Semences"
    assert depense.montant == 120000
    assert depense.date_depense == "2026-09-01"
    assert depense.description == "Achat de semences"


# ============================================================
# TEST VALEURS PAR DÉFAUT
# ============================================================

def test_depense_default_values():
    """
    Vérifie les valeurs par défaut.
    """

    depense = Depense(
        categorie="Engrais",
        montant=80000,
        date_depense="2026-09-15",
    )

    assert depense.parcelle_id is None
    assert depense.culture_id is None
    assert depense.description is None
    assert depense.id is None


# ============================================================
# TEST IDENTIFIANT
# ============================================================

def test_depense_with_id():
    """
    Vérifie qu'une dépense peut recevoir un identifiant.
    """

    depense = Depense(
        id=10,
        categorie="Matériel",
        montant=50000,
        date_depense="2026-09-20",
    )

    assert depense.id == 10


# ============================================================
# TEST PARCELLE INVALIDE
# ============================================================

def test_depense_invalid_parcelle_id():
    """
    Vérifie que l'identifiant de parcelle doit être positif.
    """

    try:
        Depense(
            parcelle_id=0,
            categorie="Semences",
            montant=10000,
            date_depense="2026-09-01",
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

def test_depense_invalid_culture_id():
    """
    Vérifie que l'identifiant de culture doit être positif.
    """

    try:
        Depense(
            culture_id=0,
            categorie="Semences",
            montant=10000,
            date_depense="2026-09-01",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'identifiant de la culture doit être "
            "strictement positif."
        )


# ============================================================
# TEST CATÉGORIE VIDE
# ============================================================

def test_depense_empty_category():
    """
    Vérifie que la catégorie ne peut pas être vide.
    """

    try:
        Depense(
            categorie="",
            montant=10000,
            date_depense="2026-09-01",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La catégorie ne peut pas être vide."
        )


# ============================================================
# TEST TYPE CATÉGORIE
# ============================================================

def test_depense_invalid_category_type():
    """
    Vérifie que la catégorie doit être une chaîne.
    """

    try:
        Depense(
            categorie=123,
            montant=10000,
            date_depense="2026-09-01",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La catégorie doit être une chaîne "
            "de caractères."
        )


# ============================================================
# TEST MONTANT NÉGATIF
# ============================================================

def test_depense_negative_amount():
    """
    Vérifie qu'un montant négatif est refusé.
    """

    try:
        Depense(
            categorie="Semences",
            montant=-10000,
            date_depense="2026-09-01",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le montant ne peut pas être négatif."
        )


# ============================================================
# TEST TYPE MONTANT
# ============================================================

def test_depense_invalid_amount_type():
    """
    Vérifie que le montant doit être numérique.
    """

    try:
        Depense(
            categorie="Semences",
            montant="10000",
            date_depense="2026-09-01",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le montant doit être un nombre."
        )


# ============================================================
# TEST DATE VIDE
# ============================================================

def test_depense_empty_date():
    """
    Vérifie que la date ne peut pas être vide.
    """

    try:
        Depense(
            categorie="Semences",
            montant=10000,
            date_depense="",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La date de dépense ne peut pas être vide."
        )


# ============================================================
# TEST TYPE DATE
# ============================================================

def test_depense_invalid_date_type():
    """
    Vérifie que la date doit être une chaîne.
    """

    try:
        Depense(
            categorie="Semences",
            montant=10000,
            date_depense=20260901,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La date de dépense doit être une chaîne "
            "de caractères."
        )