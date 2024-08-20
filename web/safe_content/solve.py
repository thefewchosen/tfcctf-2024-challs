import requests
import base64
import urllib.parse

# Read and encode the zip file
with open('test2.zip', 'rb') as file:
    zip_content = file.read()
    zip_content_base64 = base64.b64encode(zip_content).decode('utf-8')
    url_encoded_content = urllib.parse.quote(zip_content_base64)

# Define the base URL and parameters
base_url = "http://localhost:7000/"
params = {'url': f'data://localhost/,test'}

# Define cookies and headers
cookies = {"BEEFHOOK": "DrhU0KXNBe9GZPbzCXDOFHLftqtxOJeL1dGsU6IQjhQMtqnzctSGwZr91xDKhLACN6w2ERFMdTn8gqub"}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i"
}

# Send the GET request
response = requests.get(base_url, headers=headers, cookies=cookies, params=params)

# Print the response
print(response.text)
