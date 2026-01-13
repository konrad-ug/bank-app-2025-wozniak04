import pytest
from src.personal_account import Personal_Account 


@pytest.fixture
def valid_account():
    """Fixture for a valid personal account"""
    return Personal_Account("John", "Doe", "0402901056")


@pytest.fixture
def prom_account_valid():
    """Fixture for account with valid promotional code"""
    return Personal_Account("Miki", "wu", "04291203458", "PROM_abcd")


@pytest.fixture
def prom_account_invalid_code():
    """Fixture for account with invalid promotional code format"""
    return Personal_Account("davey", "santa", "04091267191", "PROM_csa")


@pytest.fixture
def prom_account_invalid_prefix():
    """Fixture for account with invalid PROM prefix"""
    return Personal_Account("davey2", "santa2", "04291203458", "PRO_2sa")


@pytest.fixture
def prom_account_invalid_pesel():
    """Fixture for account with invalid PESEL (too long)"""
    return Personal_Account("davey3", "santa3", "042912034581", "PROM_2sa")


@pytest.fixture
def account_no_prom():
    """Fixture for account without promotional code"""
    return Personal_Account("davey3", "santa3", "04291203448")


@pytest.fixture
def account_empty_prom():
    """Fixture for account with empty promotional code"""
    return Personal_Account("davey3", "santa3", "00830100011", "PROM_")


class TestAccount:
    def test_account_creation(self, valid_account):
        """Test basic account creation with valid data"""
        assert valid_account.first_name == "John"
        assert valid_account.last_name == "Doe"
        assert len(valid_account.pesel) == 11 or valid_account.pesel == "invalid"

    @pytest.mark.parametrize("account_fixture,expected_balance,expected_pesel", [
        ("prom_account_valid", 50, "04291203458"),
        ("prom_account_invalid_code", 0, "04091267191"),
        ("prom_account_invalid_prefix", 0, "04291203458"),
        ("prom_account_invalid_pesel", 0, "invalid"),
        ("account_no_prom", 0, "04291203448"),
        ("account_empty_prom", 0, "00830100011"),
    ])
    def test_prom_codes(self, request, account_fixture, expected_balance, expected_pesel):
        """Parametrized test for promotional code validation"""
        account = request.getfixturevalue(account_fixture)
        assert account.balance == expected_balance
        assert account.pesel == expected_pesel
