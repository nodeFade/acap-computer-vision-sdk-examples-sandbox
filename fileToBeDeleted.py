import requests
import sys
from createToken import Authentication

password = sys.argv[1]
username = sys.argv[2]
url_base = sys.argv[3]

token = Authentication.get_auth_token(password, username, url_base)
url = "{url_base}/camera/index.html#/system/users"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # The request was successful
    print(response.json())
else:
    # The request failed
    print(f"Request failed with status code {response.status_code}")
