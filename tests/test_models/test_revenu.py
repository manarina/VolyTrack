from core.models.revenu import Revenu


# ============================================================
# TEST CRÉATION
# ============================================================

def test_create_revenu():
    """
    Vérifie qu'un revenu peut être créé.
    """

    revenu = Revenu(
        parcelle_id=1,
        culture_id=2,
        produit="Riz",
        quantite=2500,
        prix_unitaire=1500,
        montant=3750000,
        date_revenu="2027-01-20",
        description="Vente de riz",
    )

    assert revenu.parcelle_id == 1
    assert revenu.culture_id == 2
    assert revenu.produit == "Riz"
    assert revenu.quantite == 2500
    assert revenu.prix_unitaire == 1500
    assert revenu.montant == 3750000
    assert revenu.date_revenu == "2027-01-20"
    assert revenu.description == "Vente de riz"


# ============================================================
# TEST VALEURS PAR DÉFAUT
# ============================================================

def test_revenu_default_values():
    """
    Vérifie les valeurs par défaut.
    """

    revenu = Revenu(
        produit="Tomate",
        quantite=800,
        prix_unitaire=2000,
        montant=1600000,
        date_revenu="2026-12-15",
    )

    assert revenu.parcelle_id is None
    assert revenu.culture_id is None
    assert revenu.description is None
    assert revenu.id is None


# ============================================================
# TEST IDENTIFIANT
# ============================================================

def test_revenu_with_id():
    """
    Vérifie qu'un revenu peut recevoir un identifiant.
    """

    revenu = Revenu(
        id=10,
        produit="Riz",
        quantite=100,
        prix_unitaire=1500,
        montant=150000,
        date_revenu="2027-01-20",
    )

    assert revenu.id == 10


# ============================================================
# TEST PARCELLE INVALIDE
# ============================================================

def test_revenu_invalid_parcelle_id():
    """
    Vérifie que l'identifiant de parcelle doit être positif.
    """

    try:
        Revenu(
            parcelle_id=0,
            produit="Riz",
            quantite=100,
            prix_unitaire=1500,
            montant=150000,
            date_revenu="2027-01-20",
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

def test_revenu_invalid_culture_id():
    """
    Vérifie que l'identifiant de culture doit être positif.
    """

    try:
        Revenu(
            culture_id=0,
            produit="Riz",
            quantite=100,
            prix_unitaire=1500,
            montant=150000,
            date_revenu="2027-01-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "L'identifiant de la culture doit être "
            "strictement positif."
        )


# ============================================================
# TEST PRODUIT VIDE
# ============================================================

def test_revenu_empty_product():
    """
    Vérifie que le produit ne peut pas être vide.
    """

    try:
        Revenu(
            produit="",
            quantite=100,
            prix_unitaire=1500,
            montant=150000,
            date_revenu="2027-01-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le produit ne peut pas être vide."
        )


# ============================================================
# TEST TYPE PRODUIT
# ============================================================

def test_revenu_invalid_product_type():
    """
    Vérifie que le produit doit être une chaîne.
    """

    try:
        Revenu(
            produit=123,
            quantite=100,
            prix_unitaire=1500,
            montant=150000,
            date_revenu="2027-01-20",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le produit doit être une chaîne de caractères."
        )


# ============================================================
# TEST QUANTITÉ NULLE
# ============================================================

def test_revenu_zero_quantity():
    """
    Vérifie qu'une quantité nulle est refusée.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=0,
            prix_unitaire=1500,
            montant=0,
            date_revenu="2027-01-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La quantité doit être strictement positive."
        )


# ============================================================
# TEST QUANTITÉ NÉGATIVE
# ============================================================

def test_revenu_negative_quantity():
    """
    Vérifie qu'une quantité négative est refusée.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=-100,
            prix_unitaire=1500,
            montant=150000,
            date_revenu="2027-01-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La quantité doit être strictement positive."
        )


# ============================================================
# TEST TYPE QUANTITÉ
# ============================================================

def test_revenu_invalid_quantity_type():
    """
    Vérifie que la quantité doit être numérique.
    """

    try:
        Revenu(
            produit="Riz",
            quantite="100",
            prix_unitaire=1500,
            montant=150000,
            date_revenu="2027-01-20",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La quantité doit être un nombre."
        )


# ============================================================
# TEST PRIX UNITAIRE NÉGATIF
# ============================================================

def test_revenu_negative_unit_price():
    """
    Vérifie qu'un prix unitaire négatif est refusé.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=100,
            prix_unitaire=-1500,
            montant=150000,
            date_revenu="2027-01-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le prix unitaire ne peut pas être négatif."
        )


# ============================================================
# TEST TYPE PRIX UNITAIRE
# ============================================================

def test_revenu_invalid_unit_price_type():
    """
    Vérifie que le prix unitaire doit être numérique.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=100,
            prix_unitaire="1500",
            montant=150000,
            date_revenu="2027-01-20",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le prix unitaire doit être un nombre."
        )


# ============================================================
# TEST MONTANT NÉGATIF
# ============================================================

def test_revenu_negative_amount():
    """
    Vérifie qu'un montant négatif est refusé.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=100,
            prix_unitaire=1500,
            montant=-150000,
            date_revenu="2027-01-20",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Le montant ne peut pas être négatif."
        )


# ============================================================
# TEST TYPE MONTANT
# ============================================================

def test_revenu_invalid_amount_type():
    """
    Vérifie que le montant doit être numérique.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=100,
            prix_unitaire=1500,
            montant="150000",
            date_revenu="2027-01-20",
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "Le montant doit être un nombre."
        )


# ============================================================
# TEST DATE VIDE
# ============================================================

def test_revenu_empty_date():
    """
    Vérifie que la date ne peut pas être vide.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=100,
            prix_unitaire=1500,
            montant=150000,
            date_revenu="",
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "La date du revenu ne peut pas être vide."
        )


# ============================================================
# TEST TYPE DATE
# ============================================================

def test_revenu_invalid_date_type():
    """
    Vérifie que la date doit être une chaîne.
    """

    try:
        Revenu(
            produit="Riz",
            quantite=100,
            prix_unitaire=1500,
            montant=150000,
            date_revenu=20270120,
        )

        assert False

    except TypeError as exc:
        assert str(exc) == (
            "La date du revenu doit être une chaîne "
            "de caractères."
        )