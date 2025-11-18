import pytest
from src.company_account import Company_Account


@pytest.fixture
def company_valid():
    """Fixture for valid company account"""
    return Company_Account("wieśbud", "1234567890")


@pytest.fixture
def company_invalid_nip():
    """Fixture for company with invalid NIP length"""
    return Company_Account("amazon", "12342123211232131")


class TestCompanyAccount:
    @pytest.mark.parametrize("company_name,nip,expected_company_name,expected_nip", [
        ("wieśbud", "1234567890", "wieśbud", "1234567890"),
        ("amazon", "12342123211232131", "amazon", "invalid"),
    ])
    def test_company_account_creation(self, company_name, nip, 
                                      expected_company_name, expected_nip):
        """Parametrized test for company account creation"""
        company = Company_Account(company_name, nip)
        assert company.company_name == expected_company_name
        assert company.nip == expected_nip