import json
from http.client import HTTPException

import requests
from requests import RequestException
from requests.utils import DEFAULT_CA_BUNDLE_PATH

import ado_repo_analyser


def build_proxies(proxy_user: str,
                  proxy_pswd: str,
                  proxy_endpoint: str):
    return {
        'http': f'http://{proxy_user}:{proxy_pswd}@{proxy_endpoint}',
        'https': f'http://{proxy_user}:{proxy_pswd}@{proxy_endpoint}',
    }

def get_repo_details(ado_repo_id: str, project_repos_url: str, headers: dict, **proxies):

    try:
        ado_response = requests.get(url=f"{project_repos_url}/{ado_repo_id}/?api-version=7.1",
                                headers=headers,
                                proxies=proxies)

    except RequestException as req_err:
        print(f"ERROR - unable to connect to Azure DevOps repo API: \n{req_err}")
    except HTTPException as http_err:
        print(f"ERROR - http error connecting with ADO endpoint: \n{http_err}")
    else:
        raw_ado_response = json.loads(ado_response.text)
        cur_repo = {
            'repoId': ado_repo_id,
            'name': raw_ado_response['name'],
            'size': raw_ado_response['size'],
            'cloneUrl': raw_ado_response['remoteUrl']
        }
        if cur_repo['size'] > 0:
            cur_repo['defaultBranch'] = raw_ado_response['defaultBranch']
            repo_summary = ado_repo_analyser.get_repo_stats(ado_repo_summary=cur_repo)
            return repo_summary
        else:
            return cur_repo


def get_project_details(org_name: str, proj_name: str, token: str, **proxies):
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic ' + token
    }
    project_repos_url = get_project_repos_url(org_name, proj_name)
    print("DEBUG - Default CA Bundle Path:  " + DEFAULT_CA_BUNDLE_PATH)
    if proxies is None:
        response = requests.get(url=f"{project_repos_url}?api-version=7.1",
                                headers=headers)
    else:
        response = requests.get(url=f"{project_repos_url}?api-version=7.1",
                                headers=headers,
                                proxies=proxies)

    if response.status_code == 200:
        response_body = json.loads(response.text)
        num_repos = response_body["count"]
        print(f"{num_repos} repositories found in project {org_name}")
        first_repo = response_body["value"][0]["project"]
        project_summary = {
            "projectName": first_repo["name"],
            "description": first_repo["description"],
            "projectUrl": first_repo["url"],
            "lastUpdated": first_repo["lastUpdateTime"]
        }
        project_repos = []
        for obj in response_body["value"]:
            cur_repo = get_repo_details(ado_repo_id=obj["id"],
                                        project_repos_url=project_repos_url,
                                        headers=headers,
                                        proxies=proxies)
            print("Parsed repo " + cur_repo["name"])
            project_repos.append(cur_repo)

        project_summary["projectRepos"] = project_repos
        report_file_path = f"temp/{proj_name}.json"
        print(f"Writing project report summary to {report_file_path}")
        with open(f'temp/{proj_name}.json', 'w') as ps:
            json.dump(project_summary, ps)


def get_project_repos_url(org_name: str, proj_name: str) -> str:
    project_repos_url = f"https://dev.azure.com/{org_name}/{proj_name}/_apis/git/repositories"
    return project_repos_url
