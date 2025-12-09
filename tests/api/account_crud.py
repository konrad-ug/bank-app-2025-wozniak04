import requests
import pytest

class TestApiCrud:
    url = "http://127.0.0.1:5000/api/"
    
    # Dane testowe do wielokrotnego użytku
    TEST_PESEL = "12312312312"
    TEST_NAME = "james"
    TEST_SURNAME = "jakis"
    NON_EXISTENT_PESEL = "99999999999"

    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
       
        
        yield
        requests.delete(f"{self.url}accounts/{self.TEST_PESEL}")


    @pytest.fixture(scope="function")
    def create_test_account(self):
       
        account_data = {
            "name": self.TEST_NAME,
            "surname": self.TEST_SURNAME,
            "pesel": self.TEST_PESEL
        }
        # Wymuszamy utworzenie konta przed testami, które go potrzebują
        response = requests.post(f"{self.url}accounts", json=account_data)
        assert response.status_code == 201
        return account_data

    def test_create_account_by_pesel_that_already_exists(self,create_test_account):
        account_data = {
            "name": self.TEST_NAME,
            "surname": self.TEST_SURNAME,
            "pesel": self.TEST_PESEL
        }
        
        response = requests.post(f"{self.url}accounts", json=account_data)
        assert response.status_code == 409
    
    #Test który wyśle zapytanie GET o wyszukanie konta z peselem
    def test_get_account_by_pesel_success(self, create_test_account):
        
        pesel_to_search = self.TEST_PESEL
        response = requests.get(f"{self.url}accounts/{pesel_to_search}")

        assert response.status_code == 200
        data = response.json()
        assert data["pesel"] == pesel_to_search
        assert data["name"] == self.TEST_NAME
        assert data["surname"] == self.TEST_SURNAME
        # Sprawdzamy, czy pole 'balance' istnieje i ma oczekiwaną wartość początkową (0)
        assert "balance" in data and data["balance"] == 0

    # Test, który sprawdzi czy zwracamy 404 gdy konta o podanym peselu nie ma w rejestrze ---
    def test_get_account_by_pesel_not_found(self):
        """
        Testuje przypadek, gdy konto o podanym PESELu nie istnieje (oczekiwany 404).
        """
        pesel_to_search = self.NON_EXISTENT_PESEL
        response = requests.get(f"{self.url}accounts/{pesel_to_search}")

        assert response.status_code == 404
        assert response.json()["message"] == "account not found"

    # Test na update konta (PATCH)
    def test_update_account_success(self, create_test_account):
     
        pesel_to_update = self.TEST_PESEL
        new_name = "jacek"
        new_surname = "nowak"
        update_data = {
            "first_name": new_name,
            "surname": new_surname
        }
        
        # 1. Wysyłamy zapytanie PATCH
        response_patch = requests.patch(f"{self.url}accounts/{pesel_to_update}", json=update_data)
        assert response_patch.status_code == 200
        assert response_patch.json()["message"] == "Account updated"

        # 2. Weryfikujemy zmianę za pomocą zapytania GET
        response_get = requests.get(f"{self.url}accounts/{pesel_to_update}")
        data = response_get.json()
        assert response_get.status_code == 200
        assert data["name"] == new_name
        assert data["surname"] == new_surname
        
        assert data["balance"] == 0

    def test_update_account_not_found(self):
        
        update_data = {"first_name": "New Name"}
        response = requests.patch(f"{self.url}accounts/{self.NON_EXISTENT_PESEL}", json=update_data)
        assert response.status_code == 404
        assert response.json()["message"] == "did not found account with that pesel"

    # Test na delete konta 
    def test_delete_account_success(self, create_test_account):
        
        
        
        pesel_to_delete = self.TEST_PESEL

        # 1. Usuwamy konto
        response_delete = requests.delete(f"{self.url}accounts/{pesel_to_delete}")
        assert response_delete.status_code == 200
        assert response_delete.json()["message"] == "Account deleted"

        # 2. Weryfikujemy usunięcie próbując pobrać konto (oczekiwane 404)
        response_get = requests.get(f"{self.url}accounts/{pesel_to_delete}")
        assert response_get.status_code == 404
        assert response_get.json()["message"] == "account not found"
        
    def test_delete_account_not_found(self):
        
        #Testuje próbę usunięcia konta, które nie istnieje (oczekiwany 404).
        
        response = requests.delete(f"{self.url}accounts/{self.NON_EXISTENT_PESEL}")
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"