"""\
Send Anywhere API implemented in python

This module provides a Python interface for interacting with the Send Anywhere
file transfer API. It includes a `Device` class that allows authentication,
file sending, and file receiving using the Send Anywhere API.

Classes:
- Send_Anywhere_Error: Custom exception for Send Anywhere API errors.
- Device: Represents Send Anywhere device and allows file transfer.

Usage:

1. Import the module:

   ```python
   import send_anywhere
   ```

2. Create a Device instance with your API key:

    ```python
    device = Device(api_key="YOUR_API_KEY")
    ```

3. Use the Device instance to send or receive files:

    ```python
# to send
try:
    paths_list = ["/path/to/file1.txt", "/path/to/file2.jpg"]
    key = device.send_files(abs_paths=paths_list)
    print("File sent successfully. Key:", key)
except Send_Anywhere_Error as e:
    print("Error:", str(e))

# to receive
try:
    file_data = device.receive_files(code="123456")
    with open("received_file.txt", "wb") as f:
        f.write(file_data)
    print("File received successfully.")
except Send_Anywhere_Error as e:
    print("Error:", str(e))

Note: Replace "YOUR_API_KEY" with your actual Send Anywhere API key.
"""
import json
import requests


class Send_Anywhere_Error(Exception):
    """Custom exception for Send Anywhere API errors."""
    pass


class Device:
    """\
Represents a Send Anywhere device and provides methods for file transfer.

Attributes:
- api_key (str): The API key required for authentication.
- profile_name (str): The name of the client device profile.

Methods:
- __init__: Initializes a Send Anywhere Device object.
- send_files: Sends files using the Send Anywhere API.
- receive_files: Receives files using the Send Anywhere API.
"""
    def __init__(self, api_key: str) -> None:
        """\
Initialize a Send Anywhere Device object.

Parameters:
- api_key (str): The API key required for authentication.

Raises:
- Send_Anywhere_Error: If there's an error in the API response.
"""

        profile_name = "send-anywhere-python"
        self.headers = {
            "User-Agent": "send-anywhere-python",
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        response = self.session.get("https://send-anywhere.com/web/v1/device",
                                    headers=self.headers,
                                    params={"profile_name": profile_name})


        if (not response.status_code == 200) or ("error" in response):
            raise Send_Anywhere_Error(response.text)
        else:
            self.device_key = response.json()['device_key']

        self.cookies = self.session.cookies

    def send_files(self, abs_paths: list) -> str:
        """\
Send files using the Send Anywhere API.

Parameters:
- abs_paths (list): List of absolute paths to the files to be sent.

Returns:
- str: The generated key for file transfer.

Raises:
- ValueError: If the list of paths is empty.
- Send_Anywhere_Error: If there's an error in the API response.
"""

        if not abs_paths:
            raise ValueError("list of paths is empty")
        body = {
            "file": abs_paths
        }
        response = requests.get("https://send-anywhere.com/web/v1/key",
                                headers=self.headers, cookies=self.cookies,
                                body=json.dumps(body),
                                timeout = 600)
        if (not response.status_code == 200) or ("error" in response.json()):
            raise Send_Anywhere_Error(response.json['error'])

        weblink = response.json()['weblink']
        files_to_post = []
        for filepath in abs_paths:
            files_to_post.append(open(filepath, 'rb'))
        requests.post(weblink, files=files_to_post, timeout=600)
        for fh in files_to_post:
            fh.close()

        return response['key']

    def receive_files(self, key: str) -> bytes:
        """\
Receive files using the Send Anywhere API.

Parameters:
- key (str): The 6-digit key for receiving files.

Returns:
- bytes: The content of the received file.

Raises:
- Send_Anywhere_Error: If there's an error in the API response.
"""

        response = requests.get(f"https://send-anywhere.com/web/v1/key/{key}",
                                headers=self.headers,
                                cookies=self.cookies,
                                timeout=600)
        if (not response.status_code == 200) or ("error" in response.json()):
            raise Send_Anywhere_Error(response.json['error'])
        file_data = requests.get(response.json()['weblink'], timeout=600).content
        return file_data
