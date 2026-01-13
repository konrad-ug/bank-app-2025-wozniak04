from src.account import Account
import requests
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv() 

class Company_Account(Account):
    def __init__(self,company_name,nip):
        super().__init__()
        self.company_name=company_name
        if len(nip)!=10:
            self.nip="invalid"
        else:
            if not self._is_vatstatus_active(nip):
                raise ValueError("Company not registered!!")
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

    def _is_vatstatus_active(self, nip):
        base_url = os.getenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl/api/search/nip/')
        today = date.today().strftime("%Y-%m-%d")
        url = f"{base_url}{nip}?date={today}"
        
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            print(f"Log: Response from MF for NIP {nip}: {data}")
            
            if "result" in data and data["result"].get("subject"):
                status = data["result"]["subject"].get("statusVat")
                return status == "Czynny"
            
            return False
        except Exception as e:
            print(f"Log: API Error: {e}")
            return False
        
    def submit_for_loan(self, amount):
        if self._is_amount_valid_for_loan(amount) and self._has_transfer_for_zus():
            return True
        return False