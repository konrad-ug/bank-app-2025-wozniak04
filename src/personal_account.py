from src.account import Account
class Personal_Account(Account):

    def __init__(self, first_name, last_name,pesel,prom_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name

        if self.is_pesel_valid(pesel):
            self.pesel=pesel
        else:
            self.pesel="invalid"
        
        
        if self.valid_prom_code(prom_code):  
            self.balance+=50

    def is_pesel_valid(self,pesel):
         return len(pesel) == 11

    def valid_prom_code(self,prom_code):
        if self.pesel == "invalid":
            return False
        if prom_code is None:
            return False
        if "PROM_" in prom_code and self.get_birth_year_from_pesel(self.pesel)>1960 and len(prom_code)>5:
            return True
        return False
        
        
    def get_birth_year_from_pesel(self,pesel):
        year=""
        year_from_pesel=pesel[0:2]
        month_with_centaury=pesel[2:4]
        if int(month_with_centaury)>12:
            if int(month_with_centaury)>32:
                year="18"+year_from_pesel
            else:
                year="20"+year_from_pesel
        else:
            year="19"+year_from_pesel
        return int(year)
    def _get_express_cost(self):
        return 1

    def _check_last_three_transfers(self):
        
        if len(self.history) >= 3:
            last_three = self.history[-3:]
            return all(x > 0 for x in last_three)
        return False

    def _check_last_five_transfers_sum(self, amount):
        
        if len(self.history) >= 5:
            last_five_sum = sum(self.history[-5:])
            return last_five_sum > amount
        return False

    def submit_for_loan(self, amount):
      
        if self._check_last_three_transfers():
            self.balance += amount
            return True

        if self._check_last_five_transfers_sum(amount):
            self.balance += amount
            return True

        return False
    def to_dict(self):
        return {
            "name":self.first_name,
            "surname":self.last_name,
            "pesel":self.pesel,
            "balance":self.balance,
            "history":self.history
        }
        