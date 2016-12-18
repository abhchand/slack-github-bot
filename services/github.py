import requests

class Github(object):
    HOSTNAME = "https://api.github.com"

    def __init__(self, options):
        self.repo_owner = options["repo_owner"]
        self.repo_name = options["repo_owner"]
        self.access_token = options["access_token"]

    def request(self, path):
        payload = { "access_token": self.access_token }

        try:
            return requests.get(
                self.HOSTNAME + path,
                params=payload,
                timeout=10)
        except requests.exceptions.RequestException as error:
            print error
            exit (1)

        if response.status_code in range(200, 299):
            return response
        elif response.status_code in range(400, 599):
            print "Error in making Github request: " + response.url
            print "Response: " + response.text
            exit(1)
