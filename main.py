import os
import re
from ruamel.yaml import YAML
from github import Github
import src.chess_functions as cf

# Initialize GitHub
token = os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("GITHUB_REPOSITORY")
issue_number = int(os.environ.get("ISSUE_NUMBER", 0))

g = Github(token)
repo = g.get_repo(repo_name)
issue = repo.get_issue(number=issue_number)
issue_title = issue.title.strip()
issue_author = issue.user.login

# Load settings
yaml = YAML()
with open("data/settings.yaml", "r") as f:
    settings = yaml.load(f)

# Route commands
if issue_title.lower() == "chess: start new game":
    cf.start_new_game(repo, issue, settings)
elif issue_title.lower().startswith("chess:"):
    move = issue_title.split(":")[-1].strip()
    cf.play_move(repo, issue, move, issue_author, settings)
else:
    issue.create_comment("Command not recognized. Please use one of the available move links.")
    issue.edit(state="closed")