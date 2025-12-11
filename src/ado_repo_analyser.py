import datetime
import os.path

from git import Repo
from typing import Any

import ado_test_src_file_analyser


def get_repo_stats(ado_repo_summary: dict):

    temp_path = "/temp/" + ado_repo_summary['name']

    if os.path.exists(temp_path):
        repo = Repo(temp_path)
    else:
        repo = Repo.clone_from(ado_repo_summary['cloneUrl'], temp_path)

    repo.remotes.origin.fetch()
    # Get all remote branches and their latest commit date
    branches = repo.git.for_each_ref("--sort=-committerdate", "--format='%(refname:short)'").split("\n")
    print(branches)
    latest_branch_name = branches[0]
    print(f"Latest branch by commit date: {latest_branch_name}")
    checkout_branch(latest_branch_name, repo)
    last_commit_author = repo.active_branch.commit.author.email
    last_commit_timestamp = datetime.datetime.fromtimestamp(repo.active_branch.commit.authored_date)
    print(f"Temp repo stats: \nlast commit made by = {last_commit_author} on {last_commit_timestamp}\nBranches:")

    ado_repo_summary['lastCommitToMainline'] = str(get_last_commit_date(repo=repo, branch=ado_repo_summary['defaultBranch']))
    ado_repo_summary['lastCommitBy'] = last_commit_author
    ado_repo_summary['lastCommitTimeStamp'] = str(last_commit_timestamp)
    ado_repo_summary['branchAnalysed'] = repo.active_branch.name
    ado_repo_summary['remoteBranches'] = len(branches)

    log_output = repo.git.log("--pretty=format:", "--name-only", "--diff-filter=A")
    list_of_files = log_output.splitlines()
    num_files = len(list_of_files)
    lines_of_code = 0
    unreadable_files = 0
    for file in list_of_files:
        absolute_path = temp_path + '/' + str(file)
        if os.path.isfile(absolute_path):
            try:
                lines = count_lines_in_file(file_path=absolute_path)
            except UnicodeDecodeError:
                unreadable_files = unreadable_files + 1
                print(f"Invalid char encoding in file {file}: " + str(UnicodeDecodeError.reason))
            lines_of_code = lines_of_code + lines

    print(f"Number files in repo history: {num_files}")
    ado_repo_summary['numberOfFiles'] = num_files
    ado_repo_summary['linesOfCode'] = lines_of_code
    ado_repo_summary['possibleTestFiles'] = get_possible_test_classes(temp_path=temp_path, list_of_files=list_of_files)
    ado_repo_summary['unreadableFiles'] = unreadable_files

    return ado_repo_summary


def checkout_branch(branch_name: str, repo: Repo):
    cleaned_branch_name = branch_name.removeprefix("'origin/").rstrip("'")
    print(f"Checking out branch {cleaned_branch_name} for analysis")
    if cleaned_branch_name in repo.active_branch.name:
        repo.git.checkout(cleaned_branch_name)
    else:
        repo.git.checkout('-b', cleaned_branch_name)


def add_list_of_branches(repo: Repo) -> list[Any]:
    remote_refs = repo.remote().refs
    branches = []
    for ref in remote_refs:
        print("    " + ref.name)
        branches.append(ref.name)
    return branches

def count_lines_in_file(file_path: str):
    """
    Counts the number of lines in a given file.

    Args:
        file_path (str): The path to the file to parse.

    Returns:
        Number of lines in the file.
    """
    with open(file_path, 'r', encoding="utf-8") as fp:
        count = 0
        for count, line in enumerate(fp):
            pass
    return count

def get_possible_test_classes(temp_path: str, list_of_files: list[Any]):
    possible_test_files = []
    for filepath in list_of_files:
        if 'test' in filepath and (str(filepath).endswith(".py") or str(filepath).endswith(".java")):
            candidate_test_path = f"{temp_path}/{filepath}"
            if os.path.isfile(candidate_test_path):
                possible_test_files.append(ado_test_src_file_analyser.parse_possible_test_file(filepath=candidate_test_path))
    return possible_test_files

def get_last_commit_date(repo: Repo, branch: str):
    """
    Return (sha, iso_datetime) for the last commit on origin/<branch>.
    """
    # Resolve commit from remote-tracking branch
    commit = repo.commit(f"{branch}")
    iso_commit_date = commit.committed_date
    return datetime.datetime.fromtimestamp(iso_commit_date)