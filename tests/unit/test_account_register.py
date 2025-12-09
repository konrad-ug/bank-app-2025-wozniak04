import pytest
from src.account_register import AccountRegister
from src.personal_account import PersonalAccount 

@pytest.fixture
def register():
    return AccountRegister()

class TestAccountRegister:

    @pytest.mark.parametrize("users_to_add, pesel_to_search, expected_result_exists", [
        
        # Test 1: Pusty rejestr
        ([], "99999999999", False),

        # Test 2: Konto znalezione
        ([("Jan", "Kowalski", "12345678901")], "12345678901", True),

        # Test 3: Konto nieznalezione
        ([("Jan", "Kowalski", "12345678901")], "99999999999", False),

        # Test 4: Wiele kont, szukamy środkowego
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
      
        
       
        for first_name, last_name, pesel in users_to_add:
            
            account = PersonalAccount(first_name, last_name, pesel)
            register.register_personal_account(account)

        
        found_account = register.search_account_by_pesel(pesel_to_search)

        
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
        
        
        for first_name, last_name, pesel in users_to_add:
            
            account = PersonalAccount(first_name, last_name, pesel)
            register.register_personal_account(account)
            
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
        """
        
        # ARRANGE - Register accounts
        for first_name, last_name, pesel in users_to_add:
            
            account = PersonalAccount(first_name, last_name, pesel)
            register.register_personal_account(account)
        
        
        actual_accounts = register.get_all_accounts()
        
        
        assert len(actual_accounts) == len(expected_accounts_data)

        
        actual_pesels = [account.pesel for account in actual_accounts]
        expected_pesels = [data[2] for data in expected_accounts_data] 

        
        assert actual_pesels == expected_pesels