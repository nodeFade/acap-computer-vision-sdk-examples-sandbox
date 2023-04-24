import requests
import sys
import os

# password=$1
# username=$2
# url_base=$3

password = sys.argv[1]
username = sys.argv[2]
url_base = sys.argv[3]

class Authentication:
    def __init__(self, username, password, url_base):
        self.username = username
        self.password = password
        self.url_base = url_base
        
# def get_auth_token(self):
        # your authentication code here
        # returns the auth token
#         return "your_auth_token_here"
    
# def get_token(username, password, url_base):
def get_auth_token(self):
    # Define the authentication endpoint URL
    auth_url = f"{url_base}/api/auth/token"

    # Define the request headers
    headers = {
        "Content-Type": "application/json"
    }

    # Define the request body
    data = {
        "username": username,
        "password": password
    }

    # Send the POST request to the authentication endpoint
    response = requests.post(auth_url, headers=headers, json=data)

    # If the request was successful, return the token
    if response.status_code == 200:
        token = response.json()["token"]
        return token

    # If the request failed, raise an exception
    else:
        raise Exception(f"Failed to authenticate user: {response.status_code} {response.reason}")
    
