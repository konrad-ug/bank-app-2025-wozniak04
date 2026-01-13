from src.personal_account import Personal_Account

class AccountRegister:
    def __init__(self):
        self.accounts = []

    def register_personal_account(self,account):
        self.accounts.append(account)
        return account
    
    def search_account_by_pesel(self, pesel):
        for account in self.accounts:
            if isinstance(account, Personal_Account) and account.pesel == pesel:
                return account
        return None
    def get_all_accounts(self):
        return self.accounts
    def number_of_accounts(self):
        return len(self.accounts)
