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
    
    def _is_amount_valid_for_loan(self, amount):
        if amount*2<=self.balance:
            return True
        return False
    def _has_transfer_for_zus(self):
        for transfer in self.history:
            if transfer==-1775:
                return True
        return False

    def submit_for_loan(self, amount):
        if self._is_amount_valid_for_loan(amount) and self._has_transfer_for_zus():
            return True
        return False