import getopt
import os
import yaml
import re

class OptionsParser:
    HELP_TEXT = """
    Usage:

        main.py -c <config_file> [-d] [-v]

    -c, --config        Path to config file (sample: )
    -d, --dry-run       Performa a dry run, but don't post to Slack
    -v, --Verbose       Print verbose output

    For
    For more information see: github.com/abhchand/slack-github-bot
    """

    SLACK_URL_FORMAT = re.compile("^https:\/\/hooks.slack.com\/services\/[a-zA-Z0-9]{9}\/[a-zA-Z0-9]{9}\/[a-zA-Z0-9]{24}$")
    GITHUB_ACCESS_TOKEN_FORMAT = re.compile("^[a-f0-9]{40}")

    def __init__(self, argv):
        self.__set_defaults()

        self.__parse_options(argv)
        self.__read_config_file()
        self.__validate()

        self.__set_options()

        print "Config options:", self.options

    def __set_defaults(self):
        self.config_file = ''
        self.dry_run = False
        self.verbose = False

    def __set_options(self):
        self.options = self.config_file_data.copy()

        username_mapping = {}
        for entry in self.config_file_data["usernames"]:
            username_mapping[entry["github"]] = entry["slack"]
        self.options["username_mapping"] = username_mapping

        self.options.update({
            "dry_run": self.dry_run,
            "verbose": self.verbose})

        self.options["github"].update(
            { "access_token": os.environ["GITHUB_ACCESS_TOKEN"]})

    def __parse_options(self, argv):
        try:
            opts, args = getopt.getopt(
                argv,"hc:dv",
                ["config=","dry-run","verbose"])
        except getopt.GetoptError:
            print self.HELP_TEXT
            os.sys.exit(1)

        if len(opts) == 0:
            print self.HELP_TEXT
            os.sys.exit()

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print self.HELP_TEXT
                os.sys.exit()
            elif opt in ("-c", "--config"):
                self.config_file = os.path.expanduser(arg)
            elif opt in ("-d", "--dry-run"):
                self.dry_run = True
            elif opt in ("-v", "--verbose"):
                self.verbose = True

    def __read_config_file(self):
        # Check if the file exists
        if os.path.exists(self.config_file) == False:
            print "Filepath", self.config_file, "is not valid!"
            exit(1)

        # Read it
        with open(self.config_file, "r") as stream:
            try:
                self.config_file_data = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                exit(1)

    def __validate(self):
        self.__validate_slack_url()
        self.__validate_github_repo()
        self.__validate_github_access_token()
        self.__validate_usernames()

    def __validate_slack_url(self):
        if ("slack" not in self.config_file_data or
                "webhook_url" not in self.config_file_data["slack"]):
            print "Missing Slack Webhook URL"
            exit(1)

        if not self.SLACK_URL_FORMAT.match(self.config_file_data["slack"]["webhook_url"]):
            print "Invalid format for Slack Webhook URL"
            exit(1)

    def __validate_github_repo(self):
        pattern = re.compile("^.*$")

        if "github" not in self.config_file_data:
            print "Missing Github repository information"
            exit(1)

        if ("repo_owner" not in self.config_file_data["github"] or
                not pattern.match(self.config_file_data["github"]["repo_owner"])):
            print "Missing Github repository owner"
            exit(1)

        if ("repo_name" not in self.config_file_data["github"] or
                not pattern.match(self.config_file_data["github"]["repo_name"])):
            print "Missing Github repository name"
            exit(1)

    def __validate_github_access_token(self):
        try:
            if not self.GITHUB_ACCESS_TOKEN_FORMAT.match(os.environ["GITHUB_ACCESS_TOKEN"]):
                print "Invalid format for GITHUB_ACCESS_TOKEN"
                exit(1)
        except KeyError:
            print "Excpecting enviornment variable GITHUB_ACCESS_TOKEN"
            exit(1)

    def __validate_usernames(self):
        # A mapping of github <> slack usernames must be specified
        for user in self.config_file_data["usernames"]:
            for key in ["github", "slack"]:
                if key not in user:
                    print "`", key, "` username missing for at least one user"
                    exit(1)

        # List of github usernames must be unique
        names = map(lambda x: x["github"], self.config_file_data["usernames"])
        if len(names) != len(set(names)):
            print "Duplicate github username found"
            exit(1)
