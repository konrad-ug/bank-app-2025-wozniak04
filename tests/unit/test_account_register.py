import pytest
from src.account_register import AccountRegister

@pytest.fixture
def register():
    return AccountRegister()

class TestAccountRegister:

    @pytest.mark.parametrize("users_to_add, pesel_to_search, expected_result_exists", [
        
        ([], "99999999999", False),

        
        ([("Jan", "Kowalski", "12345678901")], "12345678901", True),

        
        ([("Jan", "Kowalski", "12345678901")], "99999999999", False),

        
        (
            [
                ("Anna", "Nowak", "11111111111"), 
                ("Piotr", "Zyla", "22222222222"), 
                ("Miki", "Wu", "33333333333")
            ], 
            "22222222222", 
            True
        ),
    ])
    def test_search_account_by_pesel(self, register, users_to_add, pesel_to_search, expected_result_exists):
        """
        Testuje wyszukiwanie po PESELu.
        Parametry:
        - users_to_add: lista krotek (imie, nazwisko, pesel) do dodania PRZED testem
        - pesel_to_search: pesel, którego szukamy
        - expected_result_exists: czy spodziewamy się znaleźć konto (True/False)
        """
        
        # 1. ARRANGE (Przygotowanie) - Wypełniamy rejestr danymi z parametru
        for first_name, last_name, pesel in users_to_add:
            register.register_personal_account(first_name, last_name, pesel)

        # 2. ACT (Działanie)
        found_account = register.search_account_by_pesel(pesel_to_search)

        # 3. ASSERT (Sprawdzenie)
        if expected_result_exists:
            assert found_account is not None
            assert found_account.pesel == pesel_to_search
        else:
            assert found_account is None

    
    @pytest.mark.parametrize("users_to_add, expected_count", [
        ([], 0),                                       
        ([("Jan", "K", "123")], 1),                    
        ([("Jan", "K", "1"), ("Anna", "N", "2")], 2),  
    ])
    def test_number_of_accounts(self, register, users_to_add, expected_count):
        """Sprawdza czy licznik kont działa poprawnie"""
        
        
        for data in users_to_add:
            register.register_personal_account(*data)
            
        assert register.number_of_accounts() == expected_count
    @pytest.mark.parametrize("users_to_add, expected_accounts_data", [
        ([], []),                                       
        ([("Jan", "K", "12312332112")], [("Jan", "K", "12312332112")]),                    
        (
            [("Jan", "K", "22222222222"), ("Anna", "N", "21111111111")],  
            [("Jan", "K", "22222222222"), ("Anna", "N", "21111111111")]
        ),
        ])
    def test_get_all_accounts(self, register, users_to_add, expected_accounts_data):
        """
        Checks if the get_all_accounts method returns the correct list of registered account objects.
        NOTE: We check the data (PESELs/Names) rather than comparing the object references.
        """
        
        # ARRANGE - Register accounts
        for data in users_to_add:
            register.register_personal_account(*data)
        
        # ACT
        actual_accounts = register.get_all_accounts()
        
        # ASSERT 1: Check if the number of accounts is correct
        assert len(actual_accounts) == len(expected_accounts_data)

        # ASSERT 2: Extract key data (PESEL) and compare it against the expected data
        actual_pesels = [account.pesel for account in actual_accounts]
        expected_pesels = [data[2] for data in expected_accounts_data] # Index 2 is PESEL

        # The core assertion: check if the list of actual PESELs matches the expected PESELs
        assert actual_pesels == expected_pesels
        
  