# Slack Github Bot

A slackbot that posts Github information to your Slack channel

![Slack Github Bot](https://cloud.githubusercontent.com/assets/13787645/21373169/9a93211c-c6d1-11e6-89f0-1f2d4d3b1c46.png)

# Quick Start

This project requires Python 2.7.8.

Clone and install dependencies:

```
git clone git@github.com:abhchand/slack-github-bot.git
pip install -r requirements.txt
```

The slackbot can be run or scheduled with the following command -

```
GITHUB_ACCESS_TOKEN=1bb9702b8b172e19ca863117a2b3e1e30bf9f865 ./main.py -c ./config.yml
```

Where `GITHUB_ACCESS_TOKEN` is the access token for your github repository (provided as `ENV` variable for security reasons) and `config.yml` is a configuration file of options with the format -

``` yml
# Slack webhook URL from your slack admin configuration
slack:
  webhook_url: https://hooks.slack.com/services/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

# URL components of your github project
# e.g. github.com/:repo_owner:/:repo_name:
github:
  repo_owner: my-project-owner
  repo_name: my-project-name

# Mapping of github usernames to slack usernames
usernames:
  - github: abhchand
    slack: abhishek
  - github: evilCorpPR
    slack: angela
  - github: DenverCoder9
    slack: randall

```
