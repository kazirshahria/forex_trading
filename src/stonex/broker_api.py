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
        self.session, self.user_headers = self._create_session()
        # Account information
        self.additional_information = self._account_information()
        self.client_account_id = self.additional_information.get("tradingAccounts")[0].get("clientAccountId")
        # Market information
        self.market_tags = self.get_market_tags()

    def _send_api_request(self, method: str, version: str=None, template: str=None, json: dict=None, params: dict=None, headers: dict=None) -> dict:
        if version:
            url = f"{self.base_url}/{version}/{template}"
        else:
            url = f"{self.base_url}/{template}"

        r = requests.request(
            method=method,
            url=url,
            json = json,
            params=params,
            headers = headers
        )

        if r.status_code == 200:
            return r.json()
        else:
            return None
        
    def _create_session(self) -> str:
        if self.session == None:
            r = self._send_api_request(
                method="POST",
                template="Session",
                version="v2",
                json={"UserName": self.username, "Password": self.password, "AppKey": self.app_key},
            )
            if r.get("statusCode") == 0:
                print("Successfully logged into StoneX")
                self.session = r.get("session")
                self.user_headers = {"UserName": self.username, "Session": self.session}
                return self.session, self.user_headers
        else:
            print("StoneX session is still active")
    
    def _disconnect_session(self) -> str:
        if self.session:
            r = self._send_api_request(
                method="POST",
                template=f"TradingAPI/session/deleteSession?UserName={self.username}&Session={self.session}",
            )
            if r.get("LoggedOut") == True:
                self.session = None
                print("Logged out of StoneX")
        else:
            print("Please log into StoneX")

    def _account_information(self) -> dict:
        r = self._send_api_request(
            method="GET",
            version="v2",
            template="userAccount/ClientAndTradingAccount",
            headers=self.user_headers
        )
        if r == None:
            print("Cannot access additional account information")
        return r

    def get_market_tags(self) -> dict:
        r = self._send_api_request(
            method="GET",
            version="v2",
            template=f"market/tagLookup",
            params={"clientAccountId": self.client_account_id},
            headers=self.user_headers
        )
        if r == None:
            print("Market tags cannot be retrived")
        return r

    