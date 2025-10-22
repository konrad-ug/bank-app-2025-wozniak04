from src.account import Account

class Company_Account(Account):
    def __init__(self,company_name,nip):
        super().__init__()
        self.company_name=company_name
        if len(nip)!=10:
            self.nip="invalid"
        else:
            self.nip=nip
    def _get_express_cost(self):
        return 5