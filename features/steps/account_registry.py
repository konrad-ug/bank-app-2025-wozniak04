from behave import *
import requests

URL = "http://127.0.0.1:5000"


@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {"name": name, "surname": last_name, "pesel": pesel}
    r = requests.post(f"{URL}/api/accounts", json=json_body)
    assert r.status_code == 201

@step('Account registry is empty')
def clear_registry(context):
    r = requests.get(f"{URL}/api/accounts")
    if r.status_code == 200:
        for acc in r.json():
            requests.delete(f"{URL}/api/accounts/{acc['pesel']}")

@step('Number of accounts in registry equals: "{count}"')
def check_count(context, count):
    r = requests.get(f"{URL}/api/accounts/count")
    assert r.status_code == 200
    assert int(r.json()["count"]) == int(count)

@step('Account with pesel "{pesel}" exists in registry')
def check_exists(context, pesel):
    r = requests.get(f"{URL}/api/accounts/{pesel}")
    assert r.status_code == 200

@step('Account with pesel "{pesel}" does not exist in registry')
def check_not_exists(context, pesel):
    r = requests.get(f"{URL}/api/accounts/{pesel}")
    assert r.status_code == 404

@when('I delete account with pesel: "{pesel}"')
def delete_acc(context, pesel):
    r = requests.delete(f"{URL}/api/accounts/{pesel}")
    assert r.status_code == 200

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_acc(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    json_body = { f"{field}": f"{value}" }
    response = requests.patch(URL + f"/api/accounts/{pesel}", json = json_body)
    assert response.status_code == 200

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def check_field(context, pesel, field, value):
    r = requests.get(f"{URL}/api/accounts/{pesel}")
    assert r.status_code == 200
    data = r.json()
    if field not in ["name", "surname","balance"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    assert str(data[field]) == str(value)
