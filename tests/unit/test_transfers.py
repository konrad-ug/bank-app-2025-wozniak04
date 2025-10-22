from src.account import PersonalAccount
from src.company_account import Company_Account
class Test_transfers:
    def test_incoming_transfer_normal(self):
        account1 = PersonalAccount("Miki","wu","04291203458","PROM_abcd")
        account2 = PersonalAccount("davey","santa","04091267191","PROM_csa")
        

        account1.balance=1000
        account2.balance=1000
        account1.incoming_transfer(1500)
        account2.incoming_transfer(-500)

        assert account1.balance == 2500
        assert account2.balance == 1000

    def test_outgoing_trasfer_normal(self):
        account1 = PersonalAccount("Miki","wu","04291203458","PROM_abcd")
        account2 = PersonalAccount("davey","santa","04091267191","PROM_csa")
        account3 = PersonalAccount("davey3","santa3","04291203448")

        account1.balance=1000
        account2.balance=1000
        account3.balance=1000

        account1.out_going_transfer(500)
        account2.out_going_transfer(-100)
        account3.out_going_transfer(1001)

        assert account1.balance==500
        assert account2.balance==1000
        assert account3.balance==1000
    
    def test_incoming_transfer_company(self):
        account1 = Company_Account("wieśbud","1234567890")
        account2 = Company_Account("amazon","0987654321")
        

        account1.balance=1000
        account2.balance=1000
        account1.incoming_transfer(1500)
        account2.incoming_transfer(-500)

        assert account1.balance == 2500
        assert account2.balance == 1000

        
    def test_outgoing_trasfer_normal(self):
        account1 = Company_Account("wieśbud","123")
        account2 = Company_Account("cos","2")
        account3 = Company_Account("a","12")

        account1.balance=1000
        account2.balance=1000
        account3.balance=1000

        account1.out_going_transfer(500)
        account2.out_going_transfer(-100)
        account3.out_going_transfer(1001)

        assert account1.balance==500
        assert account2.balance==1000
        assert account3.balance==1000

    def test_express_transfers(self):
        company1=Company_Account("wieśbud","1")
        company1.balance=1000
        company2=Company_Account("wieśbud2","2")
        company2.balance=1000
        company3=Company_Account("wieśbud3","3")
        company3.balance=1000

        company1.express_transfer(100)
        company2.express_transfer(1000)
        company3.express_transfer(1001)
        
        assert company1.balance == 895
        assert company2.balance == -5
        assert company3.balance == 1000

        account1 = PersonalAccount("Miki","wu","04291203458","PROM_abcd")
        account2 = PersonalAccount("davey","santa","04091267191","PROM_csa")
        account3 = PersonalAccount("davey","santa","04091267191","PROM_csa")
        account1.balance=1000
        account2.balance=1000
        account3.balance=1000

        account1.express_transfer(100)
        account2.express_transfer(1000)
        account3.express_transfer(1001)

        assert account1.balance == 899
        assert account2.balance == -1
        assert account3.balance == 1000

        