#!/usr/bin/python

import sys
import os

from options_parser import OptionsParser

from services.github import Github
from services.slack import Slack

from services.pull_request_service import PullRequestService

if __name__ == "__main__":
    options = OptionsParser(sys.argv[1:]).options

    github_handler = Github(options["github"])
    slack_handler = Slack(options["slack"])

    service = PullRequestService(
        github_handler,
        slack_handler,
        options["username_mapping"])
    service.run()
