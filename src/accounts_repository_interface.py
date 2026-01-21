from abc import ABC,abstractmethod

class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self,accounts:list):
        pass
    @abstractmethod
    def load_all(self):
        pass