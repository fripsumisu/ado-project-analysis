import base64
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import ado_project_analyser as apa

parser = ArgumentParser(prog="Azure DevOps Project Analyser",
                        description="A client script for querying an Azure Projects, collecting repo meta-data and compiling a JSON report of findings",
                        formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument("-p", "--proxy",
                    help="Optional, the URL of any proxy that may need to be used when calling out to ADO")
parser.add_argument("-pu", "--proxyuser",
                    help="The username to be used with the specified proxy")
parser.add_argument("-pp", "--proxypswd",
                    help="The user's password to be used with the specified proxy")
parser.add_argument("-pj", "--project",
                    help="The name of the ADO project to be analysed")
parser.add_argument("-o", "--org",
                    help="The name of the ADO organisation to be queried")
parser.add_argument("-tk", "--token",
                    help="The name of the ADO PAT token to be used for authentication")
args = parser.parse_args()

# Cmd line script starts.......
if args.project is None or args.org is None or args.token is None:
    parser.print_help()
    print(sys.stderr.write(f"ERROR: the script is missing mandatory command line arguments!\n"))
else:
    pat = args.token
    encoded_token = str(base64.b64encode(bytes(':' + pat, 'ascii')), 'ascii')

    proxy_arg = args.proxy
    if proxy_arg is not None:
        proxies = apa.build_proxies(proxy_user=args.proxyuser,
                                    proxy_pswd=args.proxypswd,
                                    proxy_endpoint=proxy_arg)
        apa.get_project_details(org_name=args.org, proj_name=args.project, token=encoded_token, proxies=proxies)
    else:
        apa.get_project_details(org_name=args.org, proj_name=args.project, token=encoded_token)