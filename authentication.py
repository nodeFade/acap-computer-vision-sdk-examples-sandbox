# import requests
# auth_token=$1
# url_base=$2
# def authenticate(url_base, auth_token):
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     response = requests.get(url_base, headers=headers)
#     if response.status_code == 200:
#         return True
#     else:
#         return False

import os

class Authentication:
    def __init__(self, username, password, url_base):
        self.username = username
        self.password = password
        self.url_base = url_base

    def get_auth_token(self):
        # your authentication code here
        # returns the auth token
        return "your_auth_token_here"

# read the secrets from environment variables
username = os.environ.get("CAM_USERNAME")
password = os.environ.get("CAM_PASSWORD")
url_base = os.environ.get("URL_BASE")

# create an Authentication object
auth = Authentication(username, password, url_base)

# get the auth token and print it
auth_token = auth.get_auth_token()
print("Auth token:", auth_token)
