from abc import abstractmethod
from smtp.smtp import SMTPClient
from datetime import date
class Account:
    def __init__(self):
        self.balance=0
        self.history=[]

    def incoming_transfer(self,price):
        if price<0:
            return "price can't be negative"

        self.balance+=price
        self.history.append(price)

    def out_going_transfer(self,price):
        if price<0:
            return "transfer can't be negative"

        if self.balance-price<0:
            return "you don't have money for the transfer"
       
        self.balance-=price
        self.history.append(-price)

    def express_transfer(self,price):
        if price<0:
            return "transfer can't be negative"
        if self.balance-price<0:
            return "you don't have money for the transfer"
        self.balance-=(price+self._get_express_cost())
        self.history.append(-price) 
        self.history.append(-self._get_express_cost())

    def send_history_via_email(self,email):
        today = date.today().strftime("%Y-%m-%d")
        class_type = self.__class__.__name__
        display_name = class_type.replace('_', ' ')
        
        return SMTPClient.send(f"Account Transfer History {today}",f"{display_name} history: {self.history}",email)


    @abstractmethod
    def _get_express_cost(self): # pragma: no cover
        pass


