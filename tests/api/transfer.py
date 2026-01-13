import requests
import pytest

class TestApiTransfer:
    url = "http://127.0.0.1:5000/api/"
    TEST_PESEL = "11111111111"
    NON_EXISTENT_PESEL = "00000000000"
    INITIAL_BALANCE = 1000
    TRANSFER_AMOUNT = 500

    @pytest.fixture(scope="function", autouse=True)
    def set_up_teardown(self):
         
        yield
        
        requests.delete(f"{self.url}accounts/{self.TEST_PESEL}")

    @pytest.fixture(scope="function")
    def create_account_with_balance(self):
       
        account_data = {
            "name": "Transfer",
            "surname": "Test",
            "pesel": self.TEST_PESEL
        }
        
        requests.post(f"{self.url}accounts", json=account_data)
        
       
        deposit_data = {
            "amount": self.INITIAL_BALANCE,
            "type": "incoming"
        }
        requests.post(f"{self.url}accounts/{self.TEST_PESEL}/transfer", json=deposit_data)
        
        
        response = requests.get(f"{self.url}accounts/{self.TEST_PESEL}")
        assert response.json()["balance"] == self.INITIAL_BALANCE
        
        return self.TEST_PESEL

    
    def test_transfer_account_not_found(self):
        
        transfer_data = {"amount": 100, "type": "incoming"}
        response = requests.post(
            f"{self.url}accounts/{self.NON_EXISTENT_PESEL}/transfer", 
            json=transfer_data
        )
        assert response.status_code == 404
        

    
    def test_transfer_unknown_type(self, create_account_with_balance):
        
        pesel = create_account_with_balance
        transfer_data = {"amount": 100, "type": "unknown_type"}
        response = requests.post(f"{self.url}accounts/{pesel}/transfer", json=transfer_data)
        
        assert response.status_code == 400
        

   
    def test_transfer_incoming_success(self, create_account_with_balance):
        
        pesel = create_account_with_balance
        transfer_data = {"amount": self.TRANSFER_AMOUNT, "type": "incoming"}
        
        response = requests.post(f"{self.url}accounts/{pesel}/transfer", json=transfer_data)
        
        assert response.status_code == 200
        
        
        
        response_get = requests.get(f"{self.url}accounts/{pesel}")
        expected_balance = self.INITIAL_BALANCE + self.TRANSFER_AMOUNT
        assert response_get.json()["balance"] == expected_balance

   
    def test_transfer_outgoing_success(self, create_account_with_balance):
        
        pesel = create_account_with_balance 
        transfer_data = {"amount": 300, "type": "outgoing"}
        
        response = requests.post(f"{self.url}accounts/{pesel}/transfer", json=transfer_data)
        
        assert response.status_code == 200
        
        
        response_get = requests.get(f"{self.url}accounts/{pesel}")
        expected_balance = self.INITIAL_BALANCE - 300
        assert response_get.json()["balance"] == expected_balance

    
    def test_transfer_express_success(self, create_account_with_balance):
        
        pesel = create_account_with_balance 
        transfer_data = {"amount": 100, "type": "express"}
        
        response = requests.post(f"{self.url}accounts/{pesel}/transfer", json=transfer_data)
        
        assert response.status_code == 200
        
        
        response_get = requests.get(f"{self.url}accounts/{pesel}")
        
        expected_balance = self.INITIAL_BALANCE - 101
        assert response_get.json()["balance"] == expected_balance


    
    def test_transfer_outgoing_insufficient_funds(self, create_account_with_balance):
        
        pesel = create_account_with_balance 
        transfer_data = {"amount": 1500, "type": "outgoing"} 
        
        response = requests.post(f"{self.url}accounts/{pesel}/transfer", json=transfer_data)
        
        assert response.status_code == 422
        assert "Niewystarczające środki" in response.json()["message"]
        
            
        response_get = requests.get(f"{self.url}accounts/{pesel}")
        assert response_get.json()["balance"] == self.INITIAL_BALANCE