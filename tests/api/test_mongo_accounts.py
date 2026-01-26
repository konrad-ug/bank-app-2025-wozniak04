import requests
import pytest

class TestApiPersistence:
    url = "http://127.0.0.1:5000/api/"
    
    TEST_PESEL = "12312312312"
    TEST_NAME = "james"
    TEST_SURNAME = "jakis"

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
        response = requests.post(f"{self.url}accounts", json=account_data)
        assert response.status_code == 201
        return account_data

    def test_save_accounts_success(self, create_test_account):
        response = requests.post(f"{self.url}accounts/save")
        
        assert response.status_code == 200
        assert response.json()["message"] == "sukces"

    def test_load_accounts_success(self, create_test_account):
        requests.post(f"{self.url}accounts/save")

        response = requests.post(f"{self.url}accounts/load")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "sukces"
        
        konta = data["konta"]
        znalezione_konto = next((acc for acc in konta if acc["pesel"] == self.TEST_PESEL), None)
        
        assert znalezione_konto is not None
        assert znalezione_konto["pesel"] == self.TEST_PESEL
        assert znalezione_konto["name"] == self.TEST_NAME
        assert znalezione_konto["balance"] == 0

