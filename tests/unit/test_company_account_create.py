import pytest
from src.company_account import Company_Account

class TestCompanyAccount:
    
    def test_company_creation_success(self, mocker):

        mock_vat = mocker.patch('src.company_account.Company_Account._is_vatstatus_active')
        mock_vat.return_value = True


        company = Company_Account("wieśbud", "1234567890")
        
        assert company.company_name == "wieśbud"
        assert company.nip == "1234567890"
        mock_vat.assert_called_once()

    def test_company_creation_fails_when_vat_inactive(self, mocker):

        mock_vat = mocker.patch('src.company_account.Company_Account._is_vatstatus_active')
        mock_vat.return_value = False


        with pytest.raises(ValueError, match="Company not registered!!"):
            Company_Account("Nieaktywna Firma", "0987654321")
        
        mock_vat.assert_called_once()