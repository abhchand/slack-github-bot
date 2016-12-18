from datetime import datetime

class PullRequest:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def number(self):
        return self.raw_data["number"]

    def title(self):
        return self.raw_data["title"]

    def author(self):
        return self.raw_data["user"]["login"]

    def assignees(self):
        return map(lambda x: x["login"], self.raw_data["assignees"])

    def url(self):
        return self.raw_data["html_url"]

    def age(self):
        now = datetime.utcnow()
        created_at = datetime.strptime(
            self.raw_data["created_at"],
            "%Y-%m-%dT%H:%M:%SZ")

        return (now - created_at).days
