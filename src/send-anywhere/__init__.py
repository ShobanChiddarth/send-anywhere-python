import requests
import json

class Send_Anywhere_Error(Exception):
    pass

class Device:
    def __init__(self, api_key: str, profile_name: str="send-anywhere-python") -> None:
        self.headers = {
            "User-Agent": "send-anywhere-python",
            "X-Api-Key": api_key,
        }
        self.session = requests.Session()
        response = self.session.get("https://send-anywhere.com/web/v1/device", headers=self.headers)
        response_dict = response.json()

        if "error" in self.response_dict:
            raise Send_Anywhere_Error(response_dict['error'])
        else:
            self.device_key = response_dict['device_key']
        self.cookies = self.session.cookies
    
    def send_files(self, abs_paths: list) -> str:
        if not abs_paths:
            raise ValueError("list of paths is empty")
        body = {
            "file": abs_paths
        }
        response = requests.get("https://send-anywhere.com/web/v1/key", headers=self.headers, cookies=self.cookies, body=json.dumps(body)).json()

        weblink = response['weblink']
        files_to_post = []
        for filepath in abs_paths:
            files_to_post.append(open(filepath, 'rb'))
        requests.post(response['weblink'], files=files_to_post)

        return response['key']
    
    def recieve_files(self, code: str) -> bytes:
        response = requests.get(f"https://send-anywhere.com/web/v1/key/{code}", headers=self.headers, cookies=self.cookies).json()
        file_data = requests.get(response['weblink']).content
        return file_data




d = Device("sample")
