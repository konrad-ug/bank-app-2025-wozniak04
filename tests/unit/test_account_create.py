from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe","0402901056")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert len(account.pesel) == 11 or account.pesel=="invalid"
        
    def test_prom_codes(self):
        account_to_get_prom = Account("Miki","wu","04291203458","PROM_abcd")
        account_not_to_get_prom_1 = Account("davey","santa","04091267191","PROM_csa")
        account_not_to_get_prom_2 = Account("davey2","santa2","04291203458","PRO_2sa")
        account_not_to_get_prom_3 = Account("davey3","santa3","042912034581","PROM_2sa")
        account_not_to_get_prom_4 = Account("davey3","santa3","04291203448")
        account_not_to_get_prom_5 = Account("davey3","santa3","042912034581","PROM_")
        assert account_to_get_prom.balance == 50
        assert account_not_to_get_prom_1.balance == 0
        assert account_not_to_get_prom_2.balance == 0
        assert account_not_to_get_prom_3.pesel == "invalid"
        assert account_not_to_get_prom_3.balance == 0
        assert account_not_to_get_prom_4.balance == 0
        assert account_not_to_get_prom_5.balance == 0
