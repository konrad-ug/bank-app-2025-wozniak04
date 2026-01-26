import pytest
from src.personal_account import Personal_Account
from src.mongoAccountsRepository import MongoAccountsRepository

class TestMongoAccountsRegistry:
    account1=Personal_Account("katarzyna","wurst","12312312312")
    account2=Personal_Account("katarzyna2","wurst2","12312312321")

    @pytest.fixture(autouse=True)
    def transfer_to_account1(self):
        self.account1.incoming_transfer(1000)
    def test_save_and_load(self,mocker):
        mock_collection=mocker.Mock()
        mock_collection.find.return_value=[
            self.account1.to_dict(),
            self.account2.to_dict()
        ]
        mongo_repo=MongoAccountsRepository(collection=mock_collection)
        mongo_repo.save_all([self.account1,self.account2])
        assert mock_collection.update_one.call_count == 2
        accounts=mongo_repo.load_all()
        assert len(accounts)==2
        assert accounts[0]["pesel"] == self.account1.pesel
        assert accounts[0]["name"] == self.account1.first_name
        assert accounts[0]["balance"] == 1000

        assert accounts[1]["pesel"] == self.account2.pesel
        assert accounts[1]["surname"] == self.account2.last_name
        assert accounts[1]["balance"] == 0