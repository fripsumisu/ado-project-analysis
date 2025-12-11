import csv
import json


def read_json_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' does not contain valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def write_csv_summary(json_summary):
    # Get list of repos
    repo_list = json_summary["projectRepos"]
    # Define the headers
    headers = ["Repo_Name", "Repo_Size", "URL", "Mainline_Branch", "Latest_Commit_By", "Latest_Commit_Date",
               "Last_Mainline_Commit",
               "Number_Of_Branches", "Branch_Analysed", "Lines_of_Code", "Num_Files", "Num_Unreadable_Files", "Num_Test_Files", "Num_Tests",
               "Num_Dud_Tests"]

    # Create and write to the CSV file
    with open(report_filename_csv, mode="w", newline="") as f:
        writer = csv.writer(f)
        # Write the header row
        writer.writerow(headers)
        for repo in repo_list:
            writer.writerow(get_repo_row(repo_obj=repo))


def get_repo_row(repo_obj):

    if repo_obj["size"] > 0:
        num_tests = 0
        num_dud_tests = 0
        test_file_list = repo_obj["possibleTestFiles"]
        for test_file in test_file_list:
            num_tests = num_tests + test_file["possibleTests"]
            num_dud_tests = num_dud_tests + test_file["possibleDudTests"]

        row = [
            repo_obj["name"],
            repo_obj["size"],
            repo_obj["cloneUrl"],
            repo_obj["defaultBranch"],
            repo_obj["lastCommitBy"],
            repo_obj["lastCommitTimeStamp"],
            repo_obj["lastCommitToMainline"],
            repo_obj["remoteBranches"],
            repo_obj["branchAnalysed"],
            repo_obj["linesOfCode"],
            repo_obj["numberOfFiles"],
            repo_obj["unreadableFiles"],
            len(repo_obj["possibleTestFiles"]),
            num_tests,
            num_dud_tests
        ]
    else:
        row = [
            repo_obj["name"],
            repo_obj["size"],
            repo_obj["cloneUrl"]
        ]
    return row


# Assume this file name in the local directory
report_summary_json = "project-summary.json"
report_filename_csv = "project-summary.csv"

project_json = read_json_file(file_path=report_summary_json)
write_csv_summary(project_json)
