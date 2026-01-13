import pytest
import requests
import time


BASE_URL = "http://localhost:5000/api"

class TestApiPerformance:

    def test_create_and_delete_account_speed(self):
        
        for i in range(100):
            pesel="12312312312"
            payload = {
                "name": "Jan",
                "surname": "Performance",
                "pesel": pesel
            }
            
            response = requests.post(f"{BASE_URL}/accounts", json=payload, timeout=0.5)
            assert response.status_code == 201
            
            del_response = requests.delete(f"{BASE_URL}/accounts/{pesel}", timeout=0.5)
            assert del_response.status_code == 200

    def test_multiple_transfers_speed_and_balance(self):
      
        test_pesel = "99999999999"
        requests.delete(f"{BASE_URL}/accounts/{test_pesel}")
        
        
        payload = {"name": "Test", "surname": "Szybki", "pesel": test_pesel}
        requests.post(f"{BASE_URL}/accounts", json=payload)

        transfer_amount = 50
        expected_balance = 0

        
        for i in range(100):
            
            res = requests.post(
                f"{BASE_URL}/accounts/{test_pesel}/transfer",
                json={"amount": transfer_amount, "type": "incoming"},
                timeout=0.5
            )
            
            
            assert res.status_code == 200
            
            expected_balance += transfer_amount

        
        final_res = requests.get(f"{BASE_URL}/accounts/{test_pesel}")
        assert final_res.status_code == 200
        assert final_res.json()["balance"] == expected_balance

    # def test_batch_create_then_batch_delete_1000(self):
        
    #     pesels = [str(20000000000 + i) for i in range(1000)]
        
        
    #     for p in pesels:
    #         res = requests.post(f"{BASE_URL}/accounts", 
    #                             json={"name": "X", "surname": "Y", "pesel": p},
    #                             timeout=0.5)
    #         assert res.status_code == 201

        
    #     for p in pesels:
    #         res = requests.delete(f"{BASE_URL}/accounts/{p}", timeout=0.5)
    #         assert res.status_code == 200