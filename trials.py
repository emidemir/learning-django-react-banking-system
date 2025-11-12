import requests
import json

BASE_URL = "http://127.0.0.1:8000/"


# ----- TOKEN AUTHCATION -----
auth_data = {
    "username": "test_client_1",
    "email": "tc1@g.com",
    "password": "123456789"
}
auth_response = requests.post(f"{BASE_URL}/auth/login/", data=auth_data)
token = auth_response.json()['Token']

# ----- FETCH -----
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Bearer {token}"
}
response = requests.get(url=f"{BASE_URL}/profiles/", headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.status_code)