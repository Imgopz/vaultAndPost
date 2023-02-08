import requests

class APIHandler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth = None
        
    def login(self, username, password, endpoint='/login'):
        url = self.base_url + endpoint
        try:
            response = self.session.post(url, data={'username': username, 'password': password})
            response.raise_for_status()
            self.auth = response.json()
        except requests.exceptions.HTTPError as error:
            raise Exception(f"HTTP error occured during login: {error}")
        except requests.exceptions.RequestException as error:
            raise Exception(f"Request error occured during login: {error}")
        return True
    
    def logout(self, endpoint='/logout'):
        url = self.base_url + endpoint
        try:
            response = self.session.post(url)
            response.raise_for_status()
            self.auth = None
        except requests.exceptions.HTTPError as error:
            raise Exception(f"HTTP error occured during logout: {error}")
        except requests.exceptions.RequestException as error:
            raise Exception(f"Request error occured during logout: {error}")
        return True
    
    def fetch_data(self, endpoint, page_param='page', page_size=100):
        all_data = []
        page = 1
        while True:
            url = self.base_url + endpoint + f"?{page_param}={page}&page_size={page_size}"
            try:
                response = self.session.get(url, headers=self.auth)
                response.raise_for_status()
                data = response.json()
                all_data.extend(data)
                if len(data) < page_size:
                    break
                page += 1
            except requests.exceptions.HTTPError as error:
                raise Exception(f"HTTP error occured during fetch_data: {error}")
            except requests.exceptions.RequestException as error:
                raise Exception(f"Request error occured during fetch_data: {error}")
        return all_data


import requests
import logging

class LoginAPI:
    def __init__(self, username, password, api_url, logger=None):
        self.username = username
        self.password = password
        self.api_url = api_url
        self.logger = logger or logging.getLogger(__name__)
        self.session = requests.Session()

    def login(self):
        try:
            response = self.session.post(
                self.api_url + "/login",
                data={"username": self.username, "password": self.password}
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            self.logger.error("Login failed: %s", error)
            return False
        else:
            self.logger.info("Login successful")
            return True

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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api = LoginAPI("user", "password", "https://api.example.com", logger)


if api.login():
    data = api.fetch_data()
    if data:
        print(data)
