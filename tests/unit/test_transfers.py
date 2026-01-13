import pytest
from src.personal_account import PersonalAccount
from src.company_account import Company_Account


@pytest.fixture
def personal_account_1():
    """Fixture for first personal account"""
    account = PersonalAccount("Miki", "wu", "04291203458", "PROM_abcd")
    account.balance = 1000
    return account


@pytest.fixture
def personal_account_2():
    """Fixture for second personal account"""
    account = PersonalAccount("davey", "santa", "04091267191", "PROM_csa")
    account.balance = 1000
    return account


@pytest.fixture
def personal_account_3():
    """Fixture for third personal account"""
    account = PersonalAccount("davey3", "santa3", "04291203448")
    account.balance = 1000
    return account


@pytest.fixture
def company_account_1(mocker):
    """Fixture for first company account"""
    mocker.patch('src.company_account.Company_Account._is_vatstatus_active', return_value=True)
    account = Company_Account("wieśbud", "1234567890")
    account.balance = 1000
    return account


@pytest.fixture
def company_account_2(mocker):
    """Fixture for second company account"""
    mocker.patch('src.company_account.Company_Account._is_vatstatus_active', return_value=True)
    account = Company_Account("amazon", "0987654321")
    account.balance = 1000
    return account


@pytest.fixture
def company_accounts_for_express(mocker):
    """Fixture for multiple company accounts for express transfer testing"""
    mocker.patch('src.company_account.Company_Account._is_vatstatus_active', return_value=True)
    companies = [
        Company_Account("wieśbud", "1"),
        Company_Account("wieśbud2", "2"),
        Company_Account("wieśbud3", "3"),
        Company_Account("wieśbud4", "4"),
    ]
    for company in companies:
        company.balance = 1000
    return companies


@pytest.fixture
def personal_accounts_for_express():
    """Fixture for multiple personal accounts for express transfer testing"""
    accounts = [
        PersonalAccount("Miki", "wu", "04291203458", "PROM_abcd"),
        PersonalAccount("davey", "santa", "04091267191", "PROM_csa"),
        PersonalAccount("davey", "santa", "04091267191", "PROM_csa"),
    ]
    for account in accounts:
        account.balance = 1000
    return accounts


class Test_transfers:
    @pytest.mark.parametrize("transfer_amount,expected_balance_1,expected_balance_2", [
        (1500, 2500, 1000),  # Normal positive transfer
        (-500, 1000, 1000),  # Negative transfer (should be rejected)
    ])
    def test_incoming_transfer_personal(self, personal_account_1, personal_account_2, 
                                       transfer_amount, expected_balance_1, expected_balance_2):
        """Parametrized test for personal incoming transfers"""
        personal_account_1.incoming_transfer(transfer_amount)
        personal_account_2.incoming_transfer(-500)

        assert personal_account_1.balance == expected_balance_1
        assert personal_account_2.balance == expected_balance_2

    @pytest.mark.parametrize("transfer_amount,expected_balance", [
        (500, 500),      # Normal transfer
        (-100, 1000),    # Negative transfer (should be rejected)
        (1001, 1000),    # Transfer exceeding balance
    ])
    def test_outgoing_transfer_personal(self, personal_account_1, personal_account_2, 
                                       personal_account_3, transfer_amount, expected_balance):
        """Parametrized test for personal outgoing transfers"""
        if personal_account_1.balance >= transfer_amount >= 0:
            personal_account_1.out_going_transfer(transfer_amount)
            assert personal_account_1.balance == expected_balance
        else:
            personal_account_1.out_going_transfer(transfer_amount)
            assert personal_account_1.balance == 1000

    def test_outgoing_transfer_personal_all_cases(self, personal_account_1, 
                                                  personal_account_2, personal_account_3):
        """Test all outgoing transfer cases for personal accounts"""
        personal_account_1.out_going_transfer(500)
        personal_account_2.out_going_transfer(-100)
        personal_account_3.out_going_transfer(1001)

        assert personal_account_1.balance == 500
        assert personal_account_2.balance == 1000
        assert personal_account_3.balance == 1000

    @pytest.mark.parametrize("transfer_amount,expected_balance_1,expected_balance_2", [
        (1500, 2500, 1000),  # Normal positive transfer
        (-500, 1000, 1000),  # Negative transfer (should be rejected)
    ])
    def test_incoming_transfer_company(self, company_account_1, company_account_2,
                                      transfer_amount, expected_balance_1, expected_balance_2):
        """Parametrized test for company incoming transfers"""
        company_account_1.incoming_transfer(transfer_amount)
        company_account_2.incoming_transfer(-500)

        assert company_account_1.balance == expected_balance_1
        assert company_account_2.balance == expected_balance_2

    def test_outgoing_transfer_company_all_cases(self):
        """Test all outgoing transfer cases for company accounts"""
        company_1 = Company_Account("wieśbud", "123")
        company_2 = Company_Account("cos", "2")
        company_3 = Company_Account("a", "12")

        company_1.balance = 1000
        company_2.balance = 1000
        company_3.balance = 1000

        company_1.out_going_transfer(500)
        company_2.out_going_transfer(-100)
        company_3.out_going_transfer(1001)

        assert company_1.balance == 500
        assert company_2.balance == 1000
        assert company_3.balance == 1000

    def test_express_transfers_company(self, company_accounts_for_express):
        """Test express transfers for company accounts"""
        company_accounts_for_express[0].express_transfer(100)
        company_accounts_for_express[1].express_transfer(1000)
        company_accounts_for_express[2].express_transfer(1001)
        company_accounts_for_express[3].express_transfer(-100)
        
        assert company_accounts_for_express[0].balance == 895
        assert company_accounts_for_express[1].balance == -5
        assert company_accounts_for_express[2].balance == 1000
        assert company_accounts_for_express[3].balance == 1000

    def test_express_transfers_personal(self, personal_accounts_for_express):
        """Test express transfers for personal accounts"""
        personal_accounts_for_express[0].express_transfer(100)
        personal_accounts_for_express[1].express_transfer(1000)
        personal_accounts_for_express[2].express_transfer(1001)

        assert personal_accounts_for_express[0].balance == 899
        assert personal_accounts_for_express[1].balance == -1
        assert personal_accounts_for_express[2].balance == 1000

    def test_transfer_history(self, personal_account_1):
        """Test transfer history tracking"""
        personal_account_1.incoming_transfer(500)
        personal_account_1.out_going_transfer(200)
        personal_account_1.express_transfer(100)

        assert personal_account_1.history == [500, -200, -100, -1]