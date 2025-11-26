import requests
import pytest
class TestApiCrud:
    url="http://127.0.0.1:5000/api/"

    @pytest.fixture(scope="function",autouse=True)
    def set_up(self):
        
    def test_create_account(self):
        
        account_data={
            "name": "james",
            "surname": "jakis",
            "pesel": "12312312312"
        }

        response=request.post(url+"accounts",json=account_data)