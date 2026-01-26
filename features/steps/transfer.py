from behave import *
import requests

URL = "http://127.0.0.1:5000"



@when('I perform "{transfer_type}" transfer with amount: "{amount}" for account with pesel: "{pesel}"')
@given('I perform "{transfer_type}" transfer with amount: "{amount}" for account with pesel: "{pesel}"')
def perform_transfer(context, transfer_type, amount, pesel):
    payload = {
        "amount": int(amount),
        "type": transfer_type
    }
    context.response = requests.post(f"{URL}/api/accounts/{pesel}/transfer", json=payload)

@then("The transfer is successful")
def check_transfer_success(context):
    assert context.response.status_code == 200

@then('The transfer fails with status "{status_code}"')
def check_transfer_fail(context, status_code):
    assert context.response.status_code == int(status_code)

