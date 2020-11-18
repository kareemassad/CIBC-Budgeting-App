from plaid import Client
import requests
from plaid.errors import APIError, ItemError

# Available environments are 'sandbox', 'development', and 'production'.
client = Client(client_id="***", secret="***", environment="development")

response = client.Transactions.get(access_token, start_date="", end_date="")
transactions = response["transactions"]

# the transactions in the response are paginated, so make multiple calls while increasing the offset to
# retrieve all transactions
while len(transactions) < response["total_transactions"]:
    response = client.Transactions.get(
        access_token,
        start_date="2016-07-12",
        end_date="2017-01-09",
        offset=len(transactions),
    )
    transactions.extend(response["transactions"])
