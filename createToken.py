import requests
import sys
import os

# password = sys.argv[1]
# username = sys.argv[2]
# url_base = sys.argv[3]

class Authentication:
    def __init__(self, password, username, url_base):
        self.password = password
        self.username = username
        self.url_base = url_base
        
# def get_token(username, password, url_base):
# This makes the authentication process more secure 
# because you don't have to store your username and password in your code 
# or send them over the network for each request.
    def get_auth_token(self):
        # Define the authentication endpoint URL
        auth_url = f"{self.url_base}/api/auth/token"

        # Define the request headers
        headers = {
            "Content-Type": "application/json"
        }

        # Define the request body
        data = {
            "username": self.username,
            "password": self.password
        }

        # Send the POST request to the authentication endpoint
        response = requests.post(auth_url, headers=headers, json=data)

        # If the request was successful, return the token
        if response.status_code == 200:
            token = response.json()["token"]
            print(f"Token created: {token}")
            return token

        # If the request failed, raise an exception
        else:
            raise Exception(f"Failed to authenticate user: {response.status_code} {response.reason}")
     

    # def login(self):
    #     # Define the authentication endpoint URL
    #     auth_url = f"{self.url_base}/api/auth/token"

    #     # Define the request headers
    #     headers = {
    #         "Content-Type": "application/json"
    #     }

    #     # Define the request body
    #     data = {
    #         "username": self.username,
    #         "password": self.password
    #     }

    #     # Send the POST request to the authentication endpoint
    #     response = requests.post(auth_url, headers=headers, json=data)

    #     # If the request was successful, return the token
    #     if response.status_code == 200:
    #         token = response.json()["token"]
    #         return token

    #     # If the request failed, raise an exception
    #     else:
    #         raise Exception(f"Failed to authenticate user: {response.status_code} {response.reason}")
        
    # def logout(self):
    #     # Define the logout endpoint URL
    #     logout_url = f"{self.url_base}/api/auth/logout"

    #     # Define the request headers
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {self.token}"
    #     }

    #     # Send the POST request to the logout endpoint
    #     response = requests.post(logout_url, headers=headers)

    #     # If the request was successful, print a success message
    #     if response.status_code == 200:
    #         print("User logged out successfully.")

    #     # If the request failed, raise an exception
    #     else:
    #         raise Exception(f"Failed to log out user: {response.status_code} {response.reason}")
