import requests

class JsonPlaceHolder:
    def __init__(self, logstash_url):
        self.logstash_url = logstash_url
        self.session = requests.Session()
        self.request_count = 0

    def post(self, data):
        self.request_count += 1
        response = self.session.post(self.logstash_url, json=data)
        if self.request_count >= 20:
            self.session.close()
            self.session = requests.Session()
            self.request_count = 0
        return response

json_placeholder = JsonPlaceHolder("https://jsonplaceholder.typicode.com/posts")

# Example usage
data = {"message": "Example log message"}
for i in range(100):
    response = json_placeholder.post(data)
    print(f"Sent request {i + 1}. Response status code: {response.status_code}")
