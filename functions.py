import requests

def get_token(username, password, url_base):
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
