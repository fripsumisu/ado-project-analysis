import datetime
import os.path
from git import Repo
from typing import Any

from src import ado_test_src_file_analyser


def get_repo_stats(ado_repo_summary: dict):

    temp_path = "temp/" + ado_repo_summary['name']

    if os.path.exists(temp_path):
        repo = Repo(temp_path)
    else:
        repo = Repo.clone_from(ado_repo_summary['cloneUrl'], temp_path)

    repo_head = repo.head
    last_commit_author = repo_head.commit.author.email
    last_commit_timestamp = datetime.datetime.fromtimestamp(repo_head.commit.authored_date)
    print(f"Temp repo stats: \nlast commit made by = {last_commit_author} on {last_commit_timestamp}\nBranches:")
    ado_repo_summary['lastCommitBy'] = last_commit_author
    ado_repo_summary['lastCommitTimeStamp'] = str(last_commit_timestamp)
    ado_repo_summary['branchAnalysed'] = repo_head.name

    branches = add_list_of_branches(repo)
    ado_repo_summary['branches'] = branches

    log_output = repo.git.log("--pretty=format:", "--name-only", "--diff-filter=A")
    list_of_files = log_output.splitlines()
    num_files = len(list_of_files)
    print(f"Number files in repo history: {num_files}")
    ado_repo_summary['numberOfFiles'] = num_files
    ado_repo_summary['possibleTestFiles'] = get_possible_test_classes(temp_path=temp_path, list_of_files=list_of_files)

    return ado_repo_summary


def add_list_of_branches(repo: Repo) -> list[Any]:
    remote_refs = repo.remote().refs
    branches = []
    for ref in remote_refs:
        print("    " + ref.name)
        branches.append(ref.name)
    return branches

def get_possible_test_classes(temp_path: str, list_of_files: list[Any]):
    possible_test_files = []
    for filepath in list_of_files:
        if 'test' in filepath and (str(filepath).endswith(".py") or str(filepath).endswith(".java")):
            candidate_test_path = f"{temp_path}/{filepath}"
            if os.path.isfile(candidate_test_path):
                possible_test_files.append(ado_test_src_file_analyser.parse_possible_test_file(filepath=candidate_test_path))
    return possible_test_files