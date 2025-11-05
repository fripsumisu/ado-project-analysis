# Azure DevOps Project Analysis
A simple command line app built around _requests_ calls to MS Azure Devops projects to get a summary of repositories and then using [GitPython](https://github.com/gitpython-developers/GitPython) to examine repo health.

Currently _WIP_

## Usage
The module [ado_project_reporter](src/ado_project_reporter.py) is a simple command line utility to be used for generating a report in JSON format summarising a project, along with it's constituent Git repos, managed in Microsoft's Azure DevOps CI/CD platform.
The script will use the ADO APIs to collate and summary of the project and associated code repositories before cloning each of these to local _temp_ directory and using the _GitPython_ library to collate some figures on numbers of branches, files, possible test files, and attempt to identify the numbers of associated test files.
**N.B.** this utility does still require ADO authentication via the personal [PAT](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops) token method of _basic authentication_.

```terminaloutput
$ python -m ado_project_reporter
usage: Azure DevOps Project Analyser [-h] [-p PROXY] [-pu PROXYUSER] [-pp PROXYPSWD] [-pj PROJECT] [-o ORG] [-tk TOKEN]

A client script for querying an Azure Projects, collecting repo meta-data and compiling a JSON report of findings

options:
  -h, --help            show this help message and exit
  -p PROXY, --proxy PROXY
                        Optional, the URL of any proxy that may need to be used when calling out to ADO (default: None)
  -pu PROXYUSER, --proxyuser PROXYUSER
                        The username to be used with the specified proxy (default: None)
  -pp PROXYPSWD, --proxypswd PROXYPSWD
                        The user's password to be used with the specified proxy (default: None)
  -pj PROJECT, --project PROJECT
                        The name of the ADO project to be analysed (default: None)
  -o ORG, --org ORG     The name of the ADO organisation to be queried (default: None)
  -tk TOKEN, --token TOKEN
                        The name of the ADO PAT token to be used for authentication (default: None)
```

Invoking the module without a corporate proxy in the way, simply run the following:
```shell
python -m ado_project_reporter -pj <my-project-name> -o <my-ado-org> -tk <my-pat-token>
```
### Working behind a proxy server
For those behind a corporate proxy, be sure to provide the details of your company's proxy server along with any ID and password needed to authenticate with that proxy. 
```shell
python -m ado_project_reporter -p <my-co-proxy-url> -pu <proxy-username> -pp <user-password> -pj <my-project-name> -o <my-ado-org> -tk <my-pat-token>
```