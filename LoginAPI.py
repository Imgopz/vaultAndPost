import requests

class LoginAPI:
    def __init__(self, username, password, api_url, logger=None):
        self.username = username
        self.password = password
        self.api_url = api_url
        self.logger = logger

    def login(self):
        try:
            response = requests.post(self.api_url + "/login", data={"username": self.username, "password": self.password})
            response.raise_for_status()
            if self.logger:
                self.logger.info("Successfully logged in.")
            return response.json()
        except Exception as e:
            if self.logger:
                self.logger.error("Failed to log in.")

    def fetch_data(self):
        try:
            response = self.session.get(self.api_url + "/data")
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            self.logger.error("Data fetch failed: %s", error)
            return None
        else:
            self.logger.info("Data fetch successful")
            return response.json()


