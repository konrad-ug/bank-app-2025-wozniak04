import pytest
from src.company_account import Company_Account
from src.personal_account import Personal_Account
from smtp.smtp import SMTPClient
from datetime import date

class TestSendHistoryEmail:

    @pytest.fixture(autouse=True)
    def mock_vat_api(self, mocker):
        
        return mocker.patch('src.company_account.Company_Account._is_vatstatus_active', return_value=True)

    def test_send_history_company_account_success(self, mocker):
        
        mock_smtp = mocker.patch('src.account.SMTPClient.send', return_value=True)
        
        
        company = Company_Account("Januszex", "1234567890")
        company.history = [1000, -500]
        email = "test@firma.pl"
        
        
        result = company.send_history_via_email(email)
        assert result is True
        
        today = date.today().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_body = f"Company Account history: [1000, -500]"
        
        mock_smtp.assert_called_once()
        assert mock_smtp.call_args[0][0] == expected_subject
        assert mock_smtp.call_args[0][1] == expected_body
        assert mock_smtp.call_args[0][2] == email

    def test_send_history_personal_account_failure(self, mocker):
        
        mock_smtp = mocker.patch('src.account.SMTPClient.send', return_value=False)
        
        
        personal = Personal_Account("Jan", "Kowalski","123321123") 
        personal.history = [200, -50]
        email = "jan@kowalski.pl"
        
        
        result = personal.send_history_via_email(email)
        assert result==False
        
        today = date.today().strftime("%Y-%m-%d")
        expected_body = f"Personal Account history: [200, -50]"
        expected_subject=f"Account Transfer History {today}"
        
        assert mock_smtp.call_args[0][0] == expected_subject
        assert mock_smtp.call_args[0][1] == expected_body
        assert mock_smtp.call_args[0][2] == email
        