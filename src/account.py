class Account:
    def __init__(self, first_name, last_name,pesel,prom_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance=0

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


