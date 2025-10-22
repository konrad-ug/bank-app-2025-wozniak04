from src.company_account import Company_Account

class TestCompanyAccount:
    def creating_accout(self):
        company1=Company_Account("wieśbud","1234567890")
        company2=Company_Account("amazon","12342123211232131")


        assert company1.company_name == "wieśbud"
        assert company1.nip == "1234567890"

        assert company2.company_name == "amazon"
        assert company2.nip == "invalid"