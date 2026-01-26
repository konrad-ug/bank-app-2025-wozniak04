from .accounts_repository_interface import AccountsRepository
from pymongo import MongoClient
import os
class MongoAccountsRepository(AccountsRepository):
    def __init__(self,mongo_url=None,db_name=None,collection_name=None,collection=None):
        if collection is not None:
            self._collection=collection
            return
        mongo_url=mongo_url or os.getenv("MONGO_URL","mongodb://localhost:27017") # pragma: no cover
        db_name=db_name or os.getenv("MONGO_DB","bank_app") # pragma: no cover
        collection_name=collection_name or os.getenv("MONGO_COLLECTION","accounts") # pragma: no cover
        client=MongoClient(mongo_url) # pragma: no cover
        db=client[db_name] # pragma: no cover
        self._collection=db[collection_name] # pragma: no cover


    def save_all(self,accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
            {"pesel": account.pesel},
            {"$set": account.to_dict()},
            upsert=True,
            )
    def load_all(self):
        all_accounts = self._collection.find({})
        
        accounts = []
        for account in all_accounts:
            accounts.append(account)
            
        return accounts