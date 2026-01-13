from flask import Flask,request,jsonify
from src.account_register import AccountRegister
from src.personal_account import Personal_Account

app = Flask(__name__)

registry = AccountRegister()
@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    if registry.search_account_by_pesel(data["pesel"]) is not None:
        return jsonify({"message": "Account with that pesel already exists"}), 409
    
    account = Personal_Account(data["name"], data["surname"], data["pesel"])
    registry.register_personal_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200
    

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count=registry.number_of_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account=registry.search_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message" : "account not found"}), 404

    return jsonify({"name": account.first_name, "surname":account.last_name, "pesel":pesel, "balance":account.balance}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account=registry.search_account_by_pesel(pesel)

    if account is None:
        return jsonify({"message": "did not found account with that pesel"}), 404

    if "first_name" in data:
        account.first_name=data["first_name"]

    if "surname" in data:
        account.last_name=data["surname"]

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account=registry.search_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404
    all_accounts=registry.get_all_accounts()

    all_accounts=[a for a in all_accounts if a.pesel != pesel]
    registry.accounts=all_accounts
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer_funds(pesel):
    data = request.get_json()
    amount = data["amount"]
    transfer_type = data["type"]

    account = registry.search_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404

    success = False

    match transfer_type:
        case "incoming":
            
            success = account.incoming_transfer(amount)
        
        case "outgoing":
            
            success = account.out_going_transfer(amount)
        
        case "express":
            
            success = account.express_transfer(amount)
            
        case _: 
            return jsonify({
                "message": f"Nieznany typ przelewu: {transfer_type}. Obsługiwane typy: incoming, outgoing, express."
            }), 400 

   
    if success is None:
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    else:
       
        if transfer_type == "outgoing" or transfer_type == "express":
             return jsonify({"message": "Transakcja nieudana. Niewystarczające środki lub błąd wewnętrzny."}), 422
       
        return jsonify({"message": "Transakcja nieudana. Błąd wewnętrzny."}), 500
    