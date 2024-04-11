import os
import json
import requests
import argparse
import getpass
from datetime import datetime


class Dataiku:
    def __init__(self, host):
        self.host = host
        self.cookies = ''

    def login(self, login, password):
        s = requests.Session()
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': self.host,
            'Referer': "{}/login/?redirectTo=~2F".format(self.host),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = {
            'login': login,
            'password': password,
        }

        s.post(
            self.host + '/dip/api/login',
             headers=headers, 
             data=data
        ) #getting dss_identity_token_ and dss_access_token_ cookies
        
        s.get(
            self.host + '/dip/api/get-configuration'
        ) #getting dss_xsrf_token_ cookies

        self.cookies = s.cookies.get_dict()

        return True

    def run(self, projectKey, targetDataset):
        #check dss_xsrf_token and set value for XSRF token in header
        for cookie in self.cookies:
            if 'xsrf' in cookie:
                xsrf_value = self.cookies[cookie]

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': self.host,
            'Referer': "{}/projects/{}/flow/".format(
                self.host, 
                projectKey
            ),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-XSRF-TOKEN' : xsrf_value,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = {
            'data': '{\
                "type":"NON_RECURSIVE_FORCED_BUILD",\
                "refreshHiveMetastore":true,\
                "projectKey":"'+projectKey+'",\
                "outputs":\
                    [\
                        {\
                            "targetDataset":"'+targetDataset+'",\
                            "targetDatasetProjectKey":"'+projectKey+'",\
                            "type":"DATASET",\
                            "targetPartition":null\
                        }\
                    ]\
            }'
        }
        response = requests.post(
            self.host + '/dip/api/flow/jobs/start/', 
            cookies=self.cookies, 
            headers=headers, 
            data=data
        )

        if response.text:
            return response.text
        else:
            return False

def main(raw_args = None):
    ##ARGUMENTS
    parser=argparse.ArgumentParser()
    parser.add_argument('-host', '--host', help='Dataiku host with http:// or https:// and final slash')
    parser.add_argument('-user', '--user', help='Dataiku user')
    parser.add_argument('-password', '--password', help='Dataiku password')
    parser.add_argument('-project', '--project', help='Dataiku project')
    parser.add_argument('-dataset', '--dataset', help='Dataset to build')
    args = parser.parse_args(raw_args)
    host = args.host
    user = args.user
    password = args.password
    project = args.project
    dataset = args.dataset



    # If password wasn't provided, prompt the user to enter it securely without echoing
    if host is None:
        host = input('Please enter your Dataiku host (with protocol http or https and final slash): ')

    if user is None:
        user = input('Please enter your Dataiku username: ')

    if password is None:
        # Si no se pasó por la línea de comandos, intenta obtenerlo de la variable de entorno
        password = os.getenv('DATAIKU_PASSWORD', None)
        
    if password is None:
        password = getpass.getpass(prompt='Please enter your Dataiku password: ')

    ##CONFIG
    if host \
    and user \
    and password:

        ##DATAIKU REQUEST
        di = Dataiku(host)
        di.login(user, password)
        print(
            di.run(
                project,
                dataset
            )
        )

if __name__ == "__main__":
    main()