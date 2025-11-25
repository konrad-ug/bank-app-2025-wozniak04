import pytest
from src.company_account import Company_Account 

@pytest.fixture
def company_account():
    
    account = Company_Account("Januszex Sp. z o.o.", "1234567890")
    return account

class TestCompanyAccount:
    
    @pytest.mark.parametrize("balance, history, loan_amount, expected_result", [
        # Case 1: Ideal scenario
        # Sufficient balance (1000 >= 2 * 500) AND ZUS transfer (-1775) exists
        (1000, [-100, -1775, 2000], 500, True),

        # Case 2: No ZUS transfer
        # Sufficient balance, but -1775 missing from history
        (1000, [-100, -200, 2000], 500, False),

        # Case 3: Loan amount too high
        # ZUS exists, but loan (501) * 2 = 1002, which is > balance (1000)
        (1000, [-1775], 501, False),

        # Case 4: Loan amount exactly at the limit
        # 500 * 2 = 1000 (equals balance), ZUS is present
        (1000, [-1775], 500, True),

        # Case 5: Empty history (no ZUS)
        (5000, [], 100, False),

        # Case 6: Different negative amount (not ZUS)
        (2000, [-1774, -1776], 500, False)
    ])
    def test_submit_for_loan(self, company_account, balance, history, loan_amount, expected_result):
        """
        Tests company loan logic:
        1. Loan amount * 2 <= balance
        2. History must contain a transfer of -1775 (ZUS / Social Security)
        """
        
        
        company_account.balance = balance
        
        
        company_account.history = history

        
        result = company_account.submit_for_loan(loan_amount)

        
        assert result is expected_result