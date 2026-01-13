import pytest
from src.personal_account import Personal_Account


@pytest.fixture
def personal_account():
    account = Personal_Account("Miki", "wu", "04291203458", "PROM_abcd")
    return account


class TestAccount:
    @pytest.mark.parametrize("transfers,loan_amount,expected_result,expected_balance", [
        # Test case: last three transfers positive
        (
            [("incoming", 100), ("incoming", 200), ("incoming", 300)],
            500,
            True,
            1000 + 100 + 200 + 300 + 500  
        ),
        # Test case: sum of last five greater than loan amount
        (
            [("incoming", 10), ("incoming", 10), ("incoming", 5), ("incoming", 3), ("incoming", 2)],
            20,
            True,
            1000 + 10 + 10 + 5 + 3 + 2 + 20  
        ),
        # Test case: last three not all positive (contains outgoing)
        (
            [("incoming", 10), ("outgoing", 5), ("incoming", 10)],
            200,
            False,
            1000 + 10 - 5 + 10  # 1015
        ),
        # Test case: sum of last five not enough for loan
        (
            [("incoming", 5), ("incoming", 5), ("incoming", 2), ("outgoing", 1), ("incoming", 2)],
            20,
            False,
            1000 + 5 + 5 + 2 - 1 + 2  
        ),
        # Test case: not enough transactions (less than 3)
        (
            [("incoming", 100), ("incoming", 200)],
            300,
            False,
            1000 + 100 + 200  
        ),
        # Test case: last three not all positive with mixed transfers
        (
            [("incoming", 100),("outgoing", 50),("incoming",30),("incoming",20),("outgoing",10)],
            80,
            True,
            1000 + 100 - 50 + 30 + 20 - 10 + 80
        )
    ])
    def test_submit_for_loan(self,personal_account, transfers, loan_amount, expected_result, expected_balance):
        """Parametrized test for submit_for_loan in personal account functionality"""
        
        personal_account.balance = 1000

        
        for transfer_type, amount in transfers:
            if transfer_type == "incoming":
                personal_account.incoming_transfer(amount)
            elif transfer_type == "outgoing":
                personal_account.out_going_transfer(amount)

        result = personal_account.submit_for_loan(loan_amount)

        assert result is expected_result
        assert personal_account.balance == expected_balance
