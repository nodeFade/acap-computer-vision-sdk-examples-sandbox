import requests

def authenticate(url_base, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(url_base, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False
