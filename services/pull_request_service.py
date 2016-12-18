import numpy
from config.definitions import Definitions

from jinja2 import Template
from models.pull_request import PullRequest

class PullRequestService:
    def __init__(self, github_handler, slack_handler, username_mapping):
        self.github_handler = github_handler
        self.slack_handler = slack_handler
        self.username_mapping = username_mapping

        self.pulls_path = (
            "/repos/" +
            self.github_handler.repo_owner + "/" +
            self.github_handler.repo_name + "/pulls")

    def run(self):
        grouping = self.__find_all().__group_by_github_user()
        known_users, unknown_users = self.__map_to_slack_usernames(grouping)

        message = self.__compose_message(known_users, unknown_users)
        self.slack_handler.post_message(message)

    def __find_all(self):
        response = self.github_handler.request(self.pulls_path)
        self.pull_requests = self.__parse_pull_requests(response)

        return self

    def __group_by_github_user(self):
        results = {}

        for pull_request in self.pull_requests:
            author = [pull_request.author()]
            assignees = pull_request.assignees()

            users = numpy.unique(numpy.concatenate([author, assignees]))

            for github_user in users:
                if github_user not in results:
                    results[github_user] = []
                results[github_user].append(pull_request)

        return results

    def __map_to_slack_usernames(self, grouping):
        known_users = {}
        unknown_users = {}

        for github_username, data in grouping.items():
            if github_username in self.username_mapping:
                slack_username = self.username_mapping[github_username]
                if slack_username not in known_users:
                    known_users[slack_username] = []
                known_users[slack_username] = known_users[slack_username] + data
            else:
                unknown_users[github_username] = data

        return known_users, unknown_users

    def __parse_pull_requests(self, response):
        pull_requests = []

        for pull_request_data in response.json():
            pull_requests.append(PullRequest(pull_request_data))

        return pull_requests

    def __compose_message(self, known_users, unknown_users):
        path = Definitions.ROOT_DIR + "/templates/pull_request.txt"
        template = Template(open(path).read())

        return template.render(
            known_users=known_users,
            unknown_users=unknown_users)
