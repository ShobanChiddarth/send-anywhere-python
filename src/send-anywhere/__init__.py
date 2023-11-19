import requests
import json

class Send_Anywhere_Error(Exception):
    """Custom exception for Send Anywhere API errors."""
    pass

class Device:
    def __init__(self, api_key: str) -> None:
        """\
Initialize a Send Anywhere Device object.

Parameters:
- api_key (str): The API key required for authentication.

Raises:
- Send_Anywhere_Error: If there's an error in the API response.
"""

        profile_name: str="send-anywhere-python"
        self.headers = {
            "User-Agent": "send-anywhere-python",
            "X-Api-Key": api_key,
        }
        self.session = requests.Session()
        response = self.session.get("https://send-anywhere.com/web/v1/device", headers=self.headers)
        response_dict = response.json()

        if (not response.status_code==200) or ("error" in response_dict):
            raise Send_Anywhere_Error(response_dict['error'])
        else:
            self.device_key = response_dict['device_key']
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
        response = requests.get("https://send-anywhere.com/web/v1/key", headers=self.headers, cookies=self.cookies, body=json.dumps(body))
        if (not response.status_code==200) or ("error" in response.json()):
            raise Send_Anywhere_Error(response.json['error'])
        

        weblink = response.json()['weblink']
        files_to_post = []
        for filepath in abs_paths:
            files_to_post.append(open(filepath, 'rb'))
        requests.post(weblink, files=files_to_post)
        for fh in files_to_post:
            fh.close()

        return response['key']
    
    def recieve_files(self, key: str) -> bytes:
        """\
Receive files using the Send Anywhere API.

Parameters:
- key (str): The 6-digit key for receiving files.

Returns:
- bytes: The content of the received file.

Raises:
- Send_Anywhere_Error: If there's an error in the API response.
"""

        response = requests.get(f"https://send-anywhere.com/web/v1/key/{key}", headers=self.headers, cookies=self.cookies)
        if (not response.status_code==200) or ("error" in response.json()):
            raise Send_Anywhere_Error(response.json['error'])
        file_data = requests.get(response.json()['weblink']).content
        return file_data
