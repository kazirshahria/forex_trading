import requests

class StoneX:

    def __init__(self, username, password, app_key):
        # Credentials
        self.username = username
        self.password = password
        self.app_key = app_key
        # Base url to send request
        self.base_url = "https://ciapi.cityindex.com"
        # Session
        self.session = None
        self.session = self.login()

    def send_request(self, method: str, template: str, version: str=None, json: dict=None, headers: dict=None) -> dict:
        if version:
            url = f"{self.base_url}/{version}/{template}"
        else:
            url = f"{self.base_url}/{template}"

        r = requests.request(
            method=method,
            url=url,
            json = json,
            headers = headers
        )

        if r.status_code == 200:
            return r.json()
        else:
            return None
        
    def login(self) -> str:
        if self.session == None:
            r = self.send_request(
                method="POST",
                template="Session",
                version="v2",
                json={"UserName": self.username, "Password": self.password, "AppKey": self.app_key},
            )
            if r.get("statusCode") == 0:
                print("Successfully logged into StoneX")
                self.session = r.get("session")
                return self.session
        else:
            print("StoneX session is still active")
    
    def logout(self) -> str:
        if self.session:
            r = self.send_request(
                method="POST",
                template=f"TradingAPI/session/deleteSession?UserName={self.username}&Session={self.session}",
            )
            if r.get("LoggedOut") == True:
                self.session = None
                print("Logged out of StoneX")
        else:
            print("Please log into StoneX")
    